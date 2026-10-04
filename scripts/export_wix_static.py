#!/usr/bin/env python3
"""Create a Wix static-upload bundle without duplicating Wix-hosted audio."""

from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
TARGET = ROOT / "wix-static-stage"
ARCHIVE = ROOT / "wix-static-stage.zip"
MANIFEST = ROOT / "inventory" / "media-manifest.json"

ROUTES = {
    "/compositions/": "/compositions.html",
    "/reconstruction/": "/reconstruction.html",
    "/cds-and-books/": "/cds-and-books.html",
    "/academic/": "/academic.html",
    "/en/compositions/": "/en-compositions.html",
    "/en/reconstruction/": "/en-reconstruction.html",
    "/en/cds-and-books/": "/en-cds-and-books.html",
    "/en/academic/": "/en-academic.html",
    "/en/": "/en.html",
}

FLAT_FILES = {
    "compositions/index.html": "compositions.html",
    "reconstruction/index.html": "reconstruction.html",
    "cds-and-books/index.html": "cds-and-books.html",
    "academic/index.html": "academic.html",
    "en/index.html": "en.html",
    "en/compositions/index.html": "en-compositions.html",
    "en/reconstruction/index.html": "en-reconstruction.html",
    "en/cds-and-books/index.html": "en-cds-and-books.html",
    "en/academic/index.html": "en-academic.html",
}


def audio_map(node: object, result: dict[str, str]) -> None:
    if isinstance(node, dict):
        local_url = node.get("local_url")
        remote_url = node.get("url")
        if (
            isinstance(local_url, str)
            and local_url.startswith("/media/audio/")
            and isinstance(remote_url, str)
            and remote_url.startswith("https://")
        ):
            result[local_url] = remote_url
        for value in node.values():
            audio_map(value, result)
    elif isinstance(node, list):
        for value in node:
            audio_map(value, result)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    replacements: dict[str, str] = {}
    audio_map(manifest, replacements)

    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET, ignore=shutil.ignore_patterns("audio"))

    replaced = 0
    for html_path in TARGET.rglob("*.html"):
        source = html_path.read_text(encoding="utf-8")
        updated = source
        for local_url, remote_url in replacements.items():
            updated = updated.replace(local_url, remote_url)
        for route, flat_route in ROUTES.items():
            updated = updated.replace(f'href="{route}', f'href="{flat_route}')
        replaced += sum(source.count(local) for local in replacements)
        html_path.write_text(updated, encoding="utf-8")

    for nested, flat in FLAT_FILES.items():
        source_path = TARGET / nested
        destination = TARGET / flat
        destination.write_bytes(source_path.read_bytes())
    shutil.rmtree(TARGET / "en")
    for directory in ("compositions", "reconstruction", "cds-and-books", "academic"):
        shutil.rmtree(TARGET / directory)

    unresolved = []
    for html_path in TARGET.rglob("*.html"):
        if "/media/audio/" in html_path.read_text(encoding="utf-8"):
            unresolved.append(str(html_path.relative_to(TARGET)))
    if unresolved:
        print(f"Unresolved audio references: {unresolved}", file=sys.stderr)
        return 1

    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(TARGET.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(TARGET))

    print(f"Wrote {ARCHIVE} ({ARCHIVE.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"Replaced {replaced} local audio references with Wix-hosted URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
