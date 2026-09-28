# Redesign work log

## 2026-09-28 — private GitHub repository

User approved creating `svenuscf/ai-tcy-website` as private and uploading the
handoff, snapshots, inventory, and rebuild code. Created the repository and
verified the Private badge on GitHub. Mr Tse's review access is deferred until
requested. No preview deployment or Wix switch is part of this approval.

## 2026-09-28 — connected backend inventory

- GitHub authentication verified as `svenuscf`; installed-repository search and owner listing returned no accessible repositories. No repository was created.
- Wix connection verified against `aac32e79-b06c-4e40-bf49-8cb31b2ebc69`, 謝俊仁古琴創作樂曲及打譜, at the expected public domain. Wix Editor, Premium, Velo enabled, zh/HK, Asia/Hong_Kong confirmed.
- CMS schema listing succeeded: eight collections total, including two native collections `CDOilLampFlickered` and `Eng-Oil-Lamp`. Saved the full response locally. Collection records have not yet been exported.
- Media Manager root and all four returned subfolders were listed: root 4 files, MP3 20, Papers 13, Scores 31, Photos 18; 86 file descriptors total. Every response reports no next page, and all four subfolders have no further subfolders. Raw API responses are saved under `inventory/wix-*-response.json`.
- This covers the active folder tree returned by the API, not external embeds, trash, or a declaration of media ownership/reuse rights. No media binary files were downloaded or uploaded.
- The discovered headless sitemap API explicitly excludes classic Editor static pages; it was not used as a substitute for a full Editor page inventory. Hidden pages and Editor text export remain unresolved.
- All Wix calls were read-only. Next: export the two native content collections, reconcile media descriptors with public-page links, and resolve the source of academic text blocks.

## 2026-09-28 — public source baseline

Read `tse-chun-yan-website-redesign-codex-handoff.md`. First priority is read-only inventory and an auditable content baseline, followed by the academic-library MVP.

Completed locally:
- Saved the ten known Chinese and English public pages under `inventory/raw/`.
- Retrieved robots.txt, both language sitemap indexes, and their page sitemaps. These were inaccessible during the earlier handoff research.
- Created `scripts/build_inventory.py` and generated `inventory/content-baseline.json` with source URLs, language, raw SHA-256 hashes, ordered rich-text blocks, Wix element IDs, decoded text fragments, text hashes, and DOM reference attributes.
- Extracted 250 rich-text blocks across ten pages. These are source components, not counts of papers or works.
- Both academic pages contain 50 rich-text components, requiring classification and reconciliation before building the paper library.

Limits:
- Public HTML is an auditable starting snapshot, not an authoritative backend export or a completed migration audit.
- No Wix connector is available in this session. Hidden pages, CMS collections, Editor structure, Media Manager, media ownership, and permissions remain unverified.
- Text nodes are decoded without trimming or normalization; paragraph layout and line breaks must be checked against preserved HTML and the rendered website.
- DOM reference extraction does not cover every runtime player or embedded JSON asset. Link availability, performer/score identity, and download restrictions require further checks.
- No images have been selected for the redesign.
- No Git repository, deployment, or external write was performed.

Next actions:
1. Reconcile sitemap URLs and rendered public content with the snapshots; identify media references and restrictions.
2. Obtain read-only Wix backend access or an administrator-provided export for the missing backend inventory.
3. Map each academic bibliography and full abstract to its source component; flag ambiguous splits rather than rewriting text.
4. Build the local paper-library MVP with year grouping, search, and expandable full abstracts, then verify source-to-view text and links.
5. Resolve the concrete repository and preview destination before requesting approval for external publishing.

## 2026-09-28 — Bilingual design preview and original media

Built ten static pages, preserving 250 source text components verbatim and all
rich-text anchor targets (local route rewrites retain original target metadata).
Added publication-year browsing, text search, expandable abstracts and mobile navigation.
Removed the header 琴 badge at the owner's request.

Following authorization to download Wix media, captured the public published
component data for all ten pages. Mapped players through the component hierarchy
to original text blocks. Downloaded 20 distinct audio recordings and seven original
images (portrait, qin detail, five covers); embedded 13 original YouTube videos.
Per-language instances share the same local files. No Wix modification occurred.

Validation: generated HTML passes checks for all 250 exact text blocks, original
rich-text link targets, local route/asset existence and no nested anchors. JavaScript
syntax passes. Browser checks: first recording starts and pauses; first YouTube
thumbnail renders; Messiaen search returns one paper, no-match search shows empty
state, 2023 filter returns six, expand abstracts works. Mobile DOM at 390px has no
horizontal overflow and navigation expands. Desktop homepage visually checked.
YouTube playback for every video and every full audio track has not been audited.
Native CMS records and potential hidden pages remain pending for migration completeness.

## 2026-09-28 — Simplify homepage opening

Removed the oversized qin close-up from both language homepages after owner feedback.
Reduced the hero spacing and gave the title full width. The portrait and publication
covers remain. Original downloaded image is retained in the media archive. Rebuilt
all pages; the 250-block text/link and local-asset checks pass.
