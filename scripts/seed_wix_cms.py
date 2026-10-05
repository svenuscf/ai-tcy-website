#!/usr/bin/env python3
"""Seed the Wix staging CMS from the reviewed static site snapshot.

The script is intentionally idempotent: existing rows are matched by the
stable ``recordKey`` field and updated instead of duplicated.
"""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
COLLECTION_ID = "WebsiteContent"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def build_audio_map(node: object, result: dict[str, str]) -> None:
    if isinstance(node, dict):
        local_url = node.get("local_url")
        remote_url = node.get("url")
        if isinstance(local_url, str) and isinstance(remote_url, str) and local_url.startswith("/media/audio/"):
            result[local_url] = remote_url
        for value in node.values():
            build_audio_map(value, result)
    elif isinstance(node, list):
        for value in node:
            build_audio_map(value, result)


AUDIO_URLS: dict[str, str] = {}
build_audio_map(json.loads((ROOT / "inventory" / "media-manifest.json").read_text(encoding="utf-8")), AUDIO_URLS)


@dataclass
class Element:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["Element | str"] = field(default_factory=list)

    def has_class(self, name: str) -> bool:
        return name in self.attrs.get("class", "").split()

    def descendants(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.descendants()

    def first(self, *, tag: str | None = None, cls: str | None = None, attr: tuple[str, str] | None = None):
        for node in self.descendants():
            if tag and node.tag != tag:
                continue
            if cls and not node.has_class(cls):
                continue
            if attr and node.attrs.get(attr[0]) != attr[1]:
                continue
            return node
        return None

    def all(self, *, tag: str | None = None, cls: str | None = None):
        result = []
        for node in self.descendants():
            if tag and node.tag != tag:
                continue
            if cls and not node.has_class(cls):
                continue
            result.append(node)
        return result

    @property
    def text(self) -> str:
        return "".join(c if isinstance(c, str) else c.text for c in self.children)


class Parser(__import__("html.parser", fromlist=["HTMLParser"]).HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Element(tag, {key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def serialize(node: Element | str) -> str:
    if isinstance(node, str):
        return html.escape(node, quote=False)
    attrs = "".join(
        f' {html.escape(key, quote=True)}="{html.escape(value, quote=True)}"'
        for key, value in node.attrs.items()
    )
    if node.tag in VOID:
        return f"<{node.tag}{attrs}>"
    return f"<{node.tag}{attrs}>" + "".join(serialize(c) for c in node.children) + f"</{node.tag}>"


def inner(node: Element | None) -> str:
    return "" if node is None else "".join(serialize(c) for c in node.children)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u200b", " ").replace("\xa0", " ")).strip()


def parse(path: Path) -> Element:
    parser = Parser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.root


def find_direct(node: Element, *, tag: str | None = None, cls: str | None = None):
    for child in node.children:
        if not isinstance(child, Element):
            continue
        if tag and child.tag != tag:
            continue
        if cls and not child.has_class(cls):
            continue
        return child
    return None


def media_fields(work_body: Element) -> dict[str, object]:
    result: dict[str, object] = {}
    tracks: list[dict[str, str]] = []
    for recording in work_body.all(cls="recording"):
        audio = recording.first(tag="audio")
        if not audio:
            continue
        audio_url = audio.attrs.get("src", "")
        label = recording.first(cls="recording-label")
        strong = label.first(tag="strong") if label else None
        credit_spans = [
            span for span in (label.all(tag="span") if label else [])
            if span.attrs.get("aria-hidden") != "true"
        ]
        tracks.append({
            "url": AUDIO_URLS.get(audio_url, audio_url),
            "title": clean_text(strong.text if strong else audio.attrs.get("aria-label", "")),
            "credit": clean_text(credit_spans[-1].text) if credit_spans else "",
        })
    if tracks:
        # Preserve the familiar single-track CMS fields while retaining complete
        # Wix playlists in a structured field for the frontend.
        result["audioUrl"] = tracks[0]["url"]
        result["audioTitle"] = tracks[0]["title"]
        result["audioCredit"] = tracks[0]["credit"]
        result["audioTracks"] = {"tracks": tracks}
    iframe = work_body.first(tag="iframe")
    if iframe:
        result["videoEmbedUrl"] = iframe.attrs.get("src", "")
        performance = work_body.first(cls="performance")
        watch = performance.first(tag="a") if performance else None
        if watch:
            result["videoWatchUrl"] = watch.attrs.get("href", "")
    image = work_body.first(tag="img", cls="publication-cover")
    if image:
        result["imageUrl"] = image.attrs.get("src", "")
        result["imageAlt"] = image.attrs.get("alt", "")
    return {key: value for key, value in result.items() if value not in ("", None)}


def work_records(page_key: str, language: str, path: Path) -> list[dict[str, object]]:
    root = parse(path)
    rail = root.first(cls="work-rail")
    nav_titles: dict[str, str] = {}
    if rail:
        for link in rail.all(tag="a"):
            href = link.attrs.get("href", "")
            if href.startswith("#work-"):
                nav_titles[href[1:]] = clean_text(link.text.lstrip("0123456789 "))
    records = []
    articles = root.all(tag="article", cls="work")
    for position, article in enumerate(articles, 1):
        entry_key = article.attrs.get("id", f"work-{position}")
        order = (len(articles) - position + 1) * 10
        body = article.first(cls="work-body")
        content_parts: list[str] = []
        if body:
            for child in body.children:
                if isinstance(child, Element) and (
                    child.has_class("recording")
                    or child.has_class("performance")
                    or child.has_class("publication-cover")
                ):
                    continue
                content_parts.append(serialize(child))
        title = nav_titles.get(entry_key, clean_text(body.text if body else entry_key)[:120])
        record = {
            "recordKey": f"{page_key}:{language}:{entry_key}",
            "pageKey": page_key,
            "language": language,
            "entryKey": entry_key,
            "sortOrder": order,
            "title": title,
            "body": "".join(content_parts),
            "published": True,
        }
        if body:
            record.update(media_fields(body))
        records.append(record)
    return records


def paper_records(language: str, path: Path) -> list[dict[str, object]]:
    root = parse(path)
    records = []
    articles = root.all(tag="article", cls="paper")
    for position, article in enumerate(articles, 1):
        entry_key = article.attrs.get("id", f"paper-{position}")
        order = (len(articles) - position + 1) * 10
        source = article.first(cls="source")
        details = source.first(tag="details", cls="abstract") if source else None
        abstract = details.first(cls="abstract-body") if details else None
        body_children = []
        if source:
            for child in source.children:
                if child is details:
                    continue
                body_children.append(serialize(child))
        title_text = clean_text(source.text if source else entry_key)
        year = int(article.attrs.get("data-year", "0") or 0)
        records.append({
            "recordKey": f"academic:{language}:{entry_key}",
            "pageKey": "academic",
            "language": language,
            "entryKey": entry_key,
            "sortOrder": order,
            "title": title_text[:300],
            "body": "".join(body_children),
            "abstract": inner(abstract),
            "year": year,
            "published": True,
        })
    return records


def profile_record(language: str, path: Path, portrait_url: str) -> dict[str, object]:
    root = parse(path)
    biography = root.first(cls="biography")
    prose = biography.first(cls="prose") if biography else None
    source = find_direct(prose, cls="source") if prose else None
    return {
        "recordKey": f"home:{language}:profile",
        "pageKey": "home",
        "language": language,
        "entryKey": "profile",
        "sortOrder": 10,
        "title": "關於謝俊仁" if language == "zh" else "About TSE Chun-Yan",
        "body": inner(source),
        "imageUrl": portrait_url,
        "imageAlt": "謝俊仁" if language == "zh" else "TSE Chun-Yan",
        "published": True,
    }


def api(token: str, site_id: str, method: str, path: str, payload=None, raw: bytes | None = None, content_type="application/json"):
    url = path if path.startswith("https://") else f"https://www.wixapis.com{path}"
    headers = {"Authorization": f"Bearer {token}", "wix-site-id": site_id}
    data = raw
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if data is not None:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            value = response.read()
            return json.loads(value) if value else {}
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        raise RuntimeError(f"Wix API {method} {path} failed ({error.code}): {detail[:1000]}") from error


def upload_portrait(token: str, site_id: str, path: Path) -> str:
    generated = api(token, site_id, "POST", "/site-media/v1/files/generate-upload-url", {
        "mimeType": "image/jpeg",
        "fileName": "tse-chun-yan-portrait-2023.jpg",
    })
    upload_url = generated.get("uploadUrl") or generated.get("upload_url")
    if not upload_url:
        raise RuntimeError(f"Wix did not return an upload URL: {generated}")
    uploaded = api(token, site_id, "PUT", upload_url, raw=path.read_bytes(), content_type="image/jpeg")
    file_data = uploaded.get("file", uploaded)
    media_url = file_data.get("url", "")
    if not media_url:
        file_id = file_data.get("id")
        if file_id:
            for _ in range(8):
                time.sleep(1)
                checked = api(token, site_id, "GET", f"/site-media/v1/files/get-file-by-id?fileId={urllib.parse.quote(file_id)}")
                file_data = checked.get("file", checked)
                media_url = file_data.get("url", "")
                if media_url:
                    break
    if not media_url:
        raise RuntimeError(f"Uploaded portrait has no Wix media URL: {uploaded}")
    return media_url


def ensure_collection(token: str, site_id: str) -> None:
    existing = api(token, site_id, "GET", f"/wix-data/v2/collections/{COLLECTION_ID}")
    if existing.get("collection") or existing.get("dataCollection"):
        return


def collection_exists(token: str, site_id: str) -> bool:
    try:
        api(token, site_id, "GET", f"/wix-data/v2/collections/{COLLECTION_ID}")
        return True
    except RuntimeError as error:
        if "(404)" in str(error):
            return False
        raise


def create_collection(token: str, site_id: str) -> None:
    fields = [
        ("recordKey", "Stable Record Key", "TEXT", True),
        ("pageKey", "Page", "TEXT", True),
        ("language", "Language", "TEXT", True),
        ("entryKey", "Entry Key", "TEXT", True),
        ("sortOrder", "Display Order", "NUMBER", True),
        ("title", "Contents Title", "TEXT", True),
        ("body", "Main Content", "RICH_TEXT", False),
        ("abstract", "Abstract", "RICH_TEXT", False),
        ("year", "Publication Year", "NUMBER", False),
        ("published", "Visible on Website", "BOOLEAN", True),
        ("audioUrl", "Audio URL", "URL", False),
        ("audioTitle", "Audio Title", "TEXT", False),
        ("audioCredit", "Performer / Credit", "TEXT", False),
        ("audioTracks", "Audio Tracks (agent-managed)", "OBJECT", False),
        ("videoEmbedUrl", "Video Embed URL", "URL", False),
        ("videoWatchUrl", "Video Page URL", "URL", False),
        ("imageUrl", "Image", "IMAGE", False),
        ("imageAlt", "Image Description", "TEXT", False),
        ("editorNote", "Editor Note", "TEXT", False),
    ]
    api(token, site_id, "POST", "/wix-data/v2/collections", {
        "collection": {
            "id": COLLECTION_ID,
            "displayName": "Website Content",
            "fields": [
                {"key": key, "displayName": label, "type": kind, "required": required}
                for key, label, kind, required in fields
            ],
            "permissions": {"insert": "ADMIN", "update": "ADMIN", "remove": "ADMIN", "read": "ANYONE"},
        }
    })


def query_all(token: str, site_id: str) -> list[dict]:
    items: list[dict] = []
    offset = 0
    while True:
        response = api(token, site_id, "POST", "/wix-data/v2/items/query", {
            "dataCollectionId": COLLECTION_ID,
            "query": {"paging": {"limit": 100, "offset": offset}},
        })
        batch = response.get("dataItems", [])
        items.extend(batch)
        if len(batch) < 100:
            return items
        offset += len(batch)


def upsert_records(token: str, site_id: str, records: list[dict[str, object]]) -> None:
    existing = {item.get("data", {}).get("recordKey"): item for item in query_all(token, site_id)}
    inserts = [record for record in records if record["recordKey"] not in existing]
    updates = []
    for record in records:
        old = existing.get(record["recordKey"])
        if old:
            updates.append({"id": old.get("id") or old.get("data", {}).get("_id"), "data": record})
    for start in range(0, len(inserts), 20):
        api(token, site_id, "POST", "/wix-data/v2/bulk/items/insert", {
            "dataCollectionId": COLLECTION_ID,
            "dataItems": [{"data": record} for record in inserts[start:start + 20]],
            "returnEntity": True,
        })
    for start in range(0, len(updates), 20):
        api(token, site_id, "POST", "/wix-data/v2/bulk/items/update", {
            "dataCollectionId": COLLECTION_ID,
            "dataItems": updates[start:start + 20],
            "returnEntity": True,
        })


def build_records(portrait_url: str) -> list[dict[str, object]]:
    records = [
        profile_record("zh", SITE / "index.html", portrait_url),
        profile_record("en", SITE / "en" / "index.html", portrait_url),
    ]
    for language, prefix in (("zh", SITE), ("en", SITE / "en")):
        for page_key in ("compositions", "reconstruction", "cds-and-books"):
            records.extend(work_records(page_key, language, prefix / page_key / "index.html"))
        records.extend(paper_records(language, prefix / "academic" / "index.html"))
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--token-env", default="TCY_WIX_TOKEN")
    parser.add_argument("--portrait-url")
    args = parser.parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        parser.error(f"missing token environment variable {args.token_env}")

    portrait_url = args.portrait_url
    if not portrait_url:
        portrait = SITE / "media" / "images" / "7a7959_48926c570bcc4867943edef403304cee~mv2.jpg"
        portrait_url = upload_portrait(token, args.site_id, portrait)

    if not collection_exists(token, args.site_id):
        create_collection(token, args.site_id)
    records = build_records(portrait_url)
    upsert_records(token, args.site_id, records)
    stored = query_all(token, args.site_id)
    stored_keys = {item.get("data", {}).get("recordKey") for item in stored}
    missing = [record["recordKey"] for record in records if record["recordKey"] not in stored_keys]
    if missing:
        raise RuntimeError(f"CMS verification failed; missing {len(missing)} rows: {missing[:5]}")
    output = {
        "collectionId": COLLECTION_ID,
        "recordCount": len(records),
        "storedCount": len(stored),
        "portraitUrl": portrait_url,
        "pages": sorted({str(record["pageKey"]) for record in records}),
        "languages": ["zh", "en"],
    }
    (ROOT / "inventory" / "wix-cms-seed.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
