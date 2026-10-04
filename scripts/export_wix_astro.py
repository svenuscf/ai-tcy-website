#!/usr/bin/env python3
"""Wrap the verified Wix static bundle in a minimal Astro project."""

from __future__ import annotations


import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
TARGET = ROOT / "wix-astro-stage"
MANIFEST = ROOT / "inventory" / "media-manifest.json"


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


def main() -> None:
    wix_config = None
    if (TARGET / "wix.config.json").exists():
        wix_config = (TARGET / "wix.config.json").read_text(encoding="utf-8")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    (TARGET / "src" / "pages").mkdir(parents=True)
    (TARGET / "public").mkdir()

    shutil.copytree(SOURCE / "assets", TARGET / "public" / "assets")
    shutil.copytree(SOURCE / "media" / "images", TARGET / "public" / "media" / "images")

    replacements: dict[str, str] = {}
    audio_map(json.loads(MANIFEST.read_text(encoding="utf-8")), replacements)
    route_files = {
        "index.html": "index.astro",
        "compositions/index.html": "compositions.astro",
        "reconstruction/index.html": "reconstruction.astro",
        "cds-and-books/index.html": "cds-and-books.astro",
        "academic/index.html": "academic.astro",
        "en/index.html": "en/index.astro",
        "en/compositions/index.html": "en/compositions.astro",
        "en/reconstruction/index.html": "en/reconstruction.astro",
        "en/cds-and-books/index.html": "en/cds-and-books.astro",
        "en/academic/index.html": "en/academic.astro",
    }
    for source_name, route_name in route_files.items():
        html_path = SOURCE / source_name
        source = html_path.read_text(encoding="utf-8")
        for local_url, remote_url in replacements.items():
            source = source.replace(local_url, remote_url)
        if source.lower().startswith("<!doctype html>"):
            source = source[len("<!doctype html>") :]
        destination = TARGET / "src" / "pages" / route_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source, encoding="utf-8")

    package = {
        "name": "tse-chun-yan-wix-stage",
        "private": True,
        "type": "module",
        "scripts": {
            "build": "wix build",
            "dev": "wix dev",
            "preview": "wix preview",
            "release": "wix release",
            "env": "wix env",
        },
        "dependencies": {
            "astro": "^5.14.1",
            "@wix/sdk": "^1.15.23",
            "@wix/essentials": "^0.1.23",
            "@wix/dashboard": "^1.3.43",
        },
        "devDependencies": {
            "@astrojs/react": "^4.3.0",
            "@types/react": "^18.3.1",
            "@types/react-dom": "^18.3.1",
            "@wix/cli": "^1.1.92",
            "@wix/astro": "^2.39.0",
            "@wix/astro-pages": "^2.0.4",
            "@wix/astro-wix-hosting-adapter": "^2.0.0",
            "react": "18.3.1",
            "react-dom": "18.3.1",
        },
    }
    (TARGET / "package.json").write_text(
        json.dumps(package, indent=2) + "\n", encoding="utf-8"
    )
    (TARGET / "astro.config.mjs").write_text(
        "import { defineConfig } from 'astro/config';\n"
        "import react from '@astrojs/react';\n"
        "import wix from '@wix/astro';\n"
        "import wixPages from '@wix/astro-pages';\n"
        "import wixHostingAdapter from '@wix/astro-wix-hosting-adapter';\n"
        "export default defineConfig({\n"
        "  output: 'server',\n"
        "  integrations: [react(), wix(), wixPages()],\n"
        "  adapter: wixHostingAdapter(),\n"
        "  image: { domains: ['static.wixstatic.com'] },\n"
        "});\n",
        encoding="utf-8",
    )
    if wix_config is not None:
        (TARGET / "wix.config.json").write_text(wix_config, encoding="utf-8")
    print(f"Wrote Astro wrapper at {TARGET}")


if __name__ == "__main__":
    main()
