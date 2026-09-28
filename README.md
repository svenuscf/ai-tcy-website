# Tse Chun Yan website rebuild

Private design preview for 謝俊仁古琴創作樂曲及打譜. The live Wix site is unchanged.

## Preview locally

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m http.server 4317 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:4317/. Chinese and English each have a homepage,
compositions, reconstructions, CDs/books, and an academic paper library.
The library provides publication-year navigation, full-text search, and expandable abstracts.

## Source preservation and media

All 250 original rich-text components retain their exact decoded text. Interface
labels are separate. Original link targets are retained as provenance where local
page navigation replaces a Wix page URL. Scores continue to link to their original PDFs.

Seven original images and 20 audio tracks are stored in `site/media/`. Thirteen
original YouTube videos are embedded, with direct fallback links and original start
times. Audio/video associations come from published Wix component structure;
`inventory/media-manifest.json` records those associations and download URLs.
Videos require YouTube access; no video files are rehosted. Media has no new license.

- `tse-chun-yan-website-redesign-codex-handoff.md`: original project brief.
- `WORKLOG.md`: progress and remaining reconciliation work.
- `inventory/raw/`: frozen public HTML and published component data.
- `inventory/content-baseline.json`: exact text and source links.
- `inventory/preview-source-map.json`: source-to-preview traceability.
- `scripts/check_site.py`: verifies rendered text, source links, local paths, asset presence, and anchor nesting.

## Review boundary

Repository remains private; Mr Tse's access will be arranged later. No public
hosting, Wix edits, DNS change, or production switch has been performed. This is a
design review build. Hidden pages and the two native CMS collections still need
reconciliation before a production migration can be declared complete.

## Public review export

The owner authorized a separate public review on 2026-09-28. Public repo:
https://github.com/svenuscf/tcy-review. Live review URL:
https://garywong.pro/tcy-review/. GitHub Pages inherits the existing account
custom domain; the github.io project URL redirects there.

`python3 scripts/export_review.py /private/tmp/tcy-review-publish` exports only
website files and adjusts root-relative paths for the `/tcy-review` project URL.
It also checks that every local asset and page target exists. Publish the export
on the public repo's `main` branch; GitHub Pages serves its root. Never copy the
working repository's inventory, notes, or git history into the public repo.
