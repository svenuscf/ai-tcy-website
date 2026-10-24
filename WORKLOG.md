# Redesign work log

## 2026-10-24 — Future media uploads target the new site

The owner reports that another agent fixed the missing Media Library migration.
This documentation update does not independently audit that migration. Updated
AGENTS.md, FINAL-WORKFLOW-HANDOFF.md and WIX-CMS-EDITOR-GUIDE.md to require future
image, audio and PDF uploads to the production Headless site's Media Library
(`97afd415-1af3-4f6f-8c4c-d0a82d596996`), never the old Editor site's library.
Use the returned URLs / media IDs in the relevant bilingual CMS records and verify
live rendering, playback or downloads. The R2 pilot is not the routine upload target.

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

## 2026-09-28 — Public review published

Owner authorized publishing the current build for Mr Tse's review. GitHub Free
cannot publish Pages directly from the private working repo, so created separate
public `svenuscf/tcy-review` containing only website files, README, robots.txt and
.nojekyll. Initial public commit e8b9a1c. No private inventory or working history
was copied. Export script adjusts project paths and validates all local targets.

Pages deployment 36375858322 completed successfully. Live HTTPS URL:
https://garywong.pro/tcy-review/. GitHub automatically inherited the account's
existing custom domain; no DNS or domain settings changed. All ten live pages
and CSS/JS return successfully; homepage browser rendering confirmed. Working repository stays private; Wix remains unchanged.

## 2026-09-28 — Owner-approved credit update

Updated both homepages to copyright 2026 and added an AI management and maintenance
credit for 2026 following the 2022 redesign. Retained the original Lee Chee-Keung
and Wong Chun-Fung acknowledgments, including the historical 2022 design date.
Frozen source snapshots remain unchanged. Validation explicitly permits only the
two copyright-year substitutions; the new management sentence is separate from
source text. This supersedes verbatim preservation for the copyright year only.

## 2026-09-28 — Shareable agent handoff

Prepared AGENT-HANDOFF.md for Gary to share with Mr Tse or another assistant.
Includes portable build/export instructions, approved design and content decisions,
access/ownership boundaries, remaining migration gaps, and a practical maintenance
workflow. Corrected outdated README statements about public hosting and copyright
preservation. No website content or hosting changes in this documentation update.

## 2026-10-04 — Full Wix Headless staging rebuild

Replaced the first classic-Editor styling exercise with a new Wix-managed Headless
staging project whose frontend is generated directly from the approved GitHub design.
This preserves the complete ten-page Chinese/English information architecture,
catalogue rails, paper search, year filtering, expandable abstracts, responsive
navigation, portrait, cover art, video embeds, PDF links and 2026 credits.

The first static-uploader proof reproduced the homepage but exposed a Wix routing
limitation for nested folders. Added reproducible static and Astro exporters, wrapped
the verified pages in a minimal Wix-linked Astro project, changed the Wix build to
server output, and released the corrected site at:

https://tse-chun-yan-qin-web-ajidom-1406.wix-site-host.com

The project dashboard/site ID is `97afd415-1af3-4f6f-8c4c-d0a82d596996`. Audio is
served from the existing Wix Media URLs rather than duplicated in the frontend
bundle; four representative sources were verified on the released compositions
page. Browser checks confirmed the Chinese homepage, English homepage, academic
route, a two-result Chinese search for `康熙`, and abstract expansion. The production
domain and existing live Wix site were not changed.

## 2026-10-05 — Production cutover

Dr Tse gave written approval to publish the redesign on the pre-existing domain and
supplied the book QR code for verification. The QR decodes to
`https://www.tsechunyan.com/`. Reassigned the existing Wix Core plan from the former
Editor site to the Wix-managed Headless project; Wix also reassigned the domain to
that project. No additional plan was purchased. The Core plan remains active through
9 November 2028, and the separately billed domain renews on 7 March 2027. The former
Editor site remains in the Wix account without the domain or Core plan as rollback
reference.

Removed preview-only labels, enabled `index,follow` for production, and released the
final build. Verified the QR destination, HTTPS and canonical www redirects, all ten
Chinese/English routes, all ten CMS feeds and their 176 records, the portrait, a
representative Wix-hosted audio file, and a representative YouTube embed. The live
site is now https://www.tsechunyan.com/.

## 2026-10-05 — Final maintenance handoff

Unpublished the separate GitHub Pages review and set its source to `None`; the
public review repository remains as a historical export. Added
`FINAL-WORKFLOW-HANDOFF.md` as the current Traditional Chinese handoff covering
Wix CMS editing, source structure, build and release, rollback, repositories,
permissions and long-term maintenance. Copyright now displays `2022–current year`
automatically, while the 2026 redesign statement remains a fixed historical fact.

## 2026-10-05 — Multi-track CMS migration fix

Fixed a production-only porting defect on the composition
`Confucius 63/Confucius: 63 Revisited`. The preserved static page contained all
three original Wix tracks, but the first CMS schema supported only one audio URL,
so CMS hydration replaced the complete playlist with track 1. Added the structured
`audioTracks` object field, migrated only the two affected Chinese and English CMS
records, and taught the frontend to render every ordered track while retaining the
legacy single-track fields. A regression assertion now confirms three tracks in
both languages. Verified three live players per language and HTTP 206 responses
from all three Wix Media sources.
