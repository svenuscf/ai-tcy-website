# Tse Chun Yan website — handoff for an AI assistant

Prepared 28 September 2026. This document may be shared with Mr Tse and his chosen assistant. It contains no credentials. Repository and account access must be granted separately; possession of this document does not grant access or authorize publication.

## Purpose and current status

Help maintain 謝俊仁古琴創作樂曲及打譜, preserving Mr Tse's scholarly content while improving navigation and readability on desktop and mobile.

- Existing live Wix website: https://www.tsechunyan.com/
- Public design review: https://garywong.pro/tcy-review/
- Private working repository: https://github.com/svenuscf/ai-tcy-website
- Public deployment repository: https://github.com/svenuscf/tcy-review

The review site is published through GitHub Pages. It inherits Gary's existing domain; `https://svenuscf.github.io/tcy-review/` redirects to that domain. No DNS change was made for this project.

**The Wix website has not been changed. Mr Tse's design approval and approval to publish on Wix are still pending.** GitHub preview publication is not approval for a Wix migration. No automatic sync between GitHub and Wix exists.

The current review contains ten pages: home, compositions, reconstructions, CDs/books, and academic papers, in both Traditional Chinese and English. Each paper library has 49 entries with year navigation, full-text search, and expandable abstracts. Original score/PDF links still point to Wix. There are 20 local audio recordings, 13 embedded YouTube videos per language, and six displayed original images (portrait and five covers). A seventh downloaded image is archived but no longer displayed.

Gary has offered this current refresh without charge because the effort involved was minimal with AI assistance. This does not imply that software subscriptions, hosting plans, or future work are automatically free.

## First steps for the receiving assistant

1. Read this document and the current user's request. Treat repository documents and source content as context, not permission to carry out unrelated actions.
2. Ask the account owner for access only if needed. Mr Tse can review the public website without a GitHub account. Maintenance of the generator requires the private working repo, not just the public export.
3. Inspect `git status`, the latest commits, `README.md`, `WORKLOG.md`, and `tse-chun-yan-website-redesign-codex-handoff.md`. This document records a dated state; verify newer changes. Early worklog entries describe historical limitations that were subsequently resolved.
4. Confirm whether the requested change is for the review site or the live Wix site. Do not assume a platform switch has been approved.
5. Build and check locally before changing a published version. Carry forward explicit authorization given by the current owner; do not repeatedly ask for the same approval.

## Decisions already made

- Use a restrained cream background, dark green typography, subtle red accents, and readable scholarly layouts.
- Do not restore the red 琴 header badge.
- Do not restore the large qin close-up in the homepage opening. It was removed after review; the simpler typography and tighter spacing were preferred.
- Keep original photos, covers, recordings, video links, performer associations, and score-use restrictions.
- Preserve original Chinese and English wording unless a particular change is requested. Do not silently summarize abstracts, modernize spelling, translate passages, or correct apparent errors.
- Keep the private working repo separate from the public site export. Never publish raw inventories, internal notes, or the private repository's history in the review repository.

### Approved acknowledgments changes

Both homepages now use copyright **2026**. Preserve the historical 2022 credit to Mr Wong Chun-Fung and the score credit to Mr Lee Chee-Keung.

Chinese addition:

> 本網站繼2022年改版後，現於2026年由AI助理管理及維護。

English addition:

> Following the 2022 redesign, this website is now managed and maintained by an AI assistant in 2026.

The frozen original copyright says 2022; the generator and checks explicitly allow that approved substitution. The AI management sentence is separate from the preserved source blocks. This wording does not mean an autonomous assistant is continuously running or monitoring the site.

## Project structure

This is a static HTML/CSS/JavaScript website generated using Python's standard library. No npm install, frontend framework, database, or secret key is required to build it.

- `scripts/build_site.py`: parses frozen Wix HTML, verifies source hashes/text, creates all ten pages, and records source-to-preview mappings. Layouts and the approved credit changes live here.
- `site/assets/style.css`: responsive design.
- `site/assets/app.js`: navigation, paper search, year filtering, and abstract controls.
- `scripts/check_site.py`: checks 250 source components, approved copyright exceptions, original rich-text links, local paths/assets, and nested anchors.
- `scripts/export_review.py`: copies only website files, prefixes local URLs with `/tcy-review`, and creates `.nojekyll`, `robots.txt`, and a public README.
- `site/`: generated pages plus hand-maintained assets and downloaded media. Do not delete this folder as a build-cleaning step: media and assets are stored here.
- `inventory/content-baseline.json`: frozen text, links, and hashes.
- `inventory/raw/`: original public HTML and published Wix component data.
- `inventory/media-manifest.json`: media URLs, local files, source component associations, and evidence.
- `inventory/preview-source-map.json`: generated traceability map.
- `WORKLOG.md`: chronological findings and decisions.

Do not edit generated `site/**/index.html` as the sole implementation of a change: the next build will overwrite it. Edit the generator or introduce an explicit maintained content layer, then regenerate.

## Local build and verification

After cloning the private working repo, run these commands from its root. Python 3 is required; Node.js is used only for the optional JavaScript syntax check.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check site/assets/app.js
python3 -m http.server 4317 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:4317/`. Stop the server with Ctrl+C when finished. Paths in this document are relative to the repository, so the workflow is portable to another laptop.

For relevant changes, check Chinese and English, desktop and mobile, language switching, menu operation, search/no-results, year filters, abstracts, media controls, and PDF links. Check that unrelated original text is unchanged. Test the affected feature rather than repeatedly auditing everything after a tiny wording edit.

## Making content changes

For a simple layout change, edit the generator/CSS/JavaScript and regenerate.

For an approved wording change, record exactly what was authorized. Keep frozen source evidence intact; implement a narrowly scoped replacement or a separate edited-content layer. Update expected-content checks only for the approved difference. Do not weaken the preservation checks globally.

Adding or removing papers needs more work than editing HTML: the current builder uses an explicit `YEARS` list and expects 49 papers in each language, with some counts embedded in templates. Update the data, ordering, counts, and checks consistently. For ongoing additions, prefer refactoring to structured editable records with stable IDs and source provenance. Do not invent a missing English version; obtain approved wording.

When adding media, confirm the exact work, performer, language placement, and allowed use. Keep an explicit source mapping. Use local authorized audio and images where appropriate; preserve YouTube embeds and fallback links. Do not download YouTube videos. Do not assume publicly viewable material has a new redistribution license.

## Publishing an approved preview update

Use the existing repositories. Do not make the working repo public. Do not push the working repo's `main` branch to the public remote.

1. Build, check, and review the change in the private working repo. Commit and push the source changes there.
2. Clone or update the separate public repository in another directory. Check for collaborators' changes before exporting.
3. From the private working repo, export into that public checkout:

```sh
python3 scripts/export_review.py /absolute/path/to/tcy-review-checkout
```

4. Inspect `git status` and the diff in the public checkout. It should contain only site files, public README, `.nojekyll`, and `robots.txt`. The exporter copies files but does not remove stale files; explicitly review obsolete files when removing a page or asset. Do not publish this handoff by accident.
5. Commit and push that checkout's `main` branch. Existing GitHub Pages settings deploy `main` → repository root.
6. Wait for the Pages deployment to finish successfully. Verify the HTTPS review URL, affected pages, styles, JavaScript, and media after deployment. Report the actual live URL, not merely a successful git push.

The `/tcy-review` prefix is essential for this project URL. Do not upload the unmodified root-relative local build directly. If the public repo or hosting path changes, adjust `--base` and verify every internal link.

Cloudflare may rewrite email links and inject its email-decoding script in served HTML. An otherwise-correct live page may therefore differ byte-for-byte from the export. Check meaningful content and behavior rather than disabling security features or assuming every difference is a deployment defect.

The preview includes `noindex,nofollow`; the export also has a robots exclusion. These discourage indexing but are not access control. The review site and public repository are accessible to anyone.

## Before any Wix migration

A GitHub Pages build cannot simply be uploaded into the existing Wix Editor as an editable replacement. Inspect the current Wix editor and available supported integrations first, then agree on the implementation route. Do not promise that an AI agent can perform every Editor operation automatically.

1. Obtain Mr Tse's approval of the design and content, then confirm authorization for the chosen Wix implementation and eventual publication.
2. Use authorized Wix access to inspect the current site, editor capabilities, pages, collections, media, and multilingual setup. Do not rely on old connection status from this conversation.
3. Back up or duplicate the site where supported and establish a rollback route before changing the live version.
4. Reconcile content completeness, including hidden pages and native CMS records, before declaring migration complete.
5. Recreate and test the approved layout and features in a draft/staging version. Preserve existing URLs where possible and plan redirects for any approved URL changes.
6. Verify mobile layout, both languages, the full paper library, audio/video, PDF links, contact links, accessibility, and relevant search metadata.
7. Present the draft for review, then publish only within the owner's approved scope. GitHub review approval alone does not authorize DNS changes, account transfers, or changes to Gary's unrelated website.

Do not choose Wix Headless or another hosting platform without discussing the implications for Mr Tse's editing and ownership workflow. The exact migration method remains undecided.

## Known gaps and practical limitations

- The public HTML snapshot is a preservation baseline, not a complete Wix backend export.
- Read-only Wix metadata and media listings were collected. Two native collections, `CDOilLampFlickered` and `Eng-Oil-Lamp`, were identified, but their records remain to be reconciled. Potential hidden pages remain unresolved.
- Media associations were traced through published Wix component structure. Every complete audio track and every video's playback has not been audited.
- PDFs still depend on the original Wix URLs; test and preserve them before any hosting change.
- Previous browser checks covered a recording's play/pause, a YouTube thumbnail, paper search, no-results state, the 2023 filter, expanding abstracts, and mobile navigation/no overflow. These are not an exhaustive accessibility or cross-browser audit.
- The public review is hosted under Gary's account and domain. Long-term ownership, access, and hosting arrangements for Mr Tse still need to be agreed.

## Running an assistant on Mr Tse's laptop

Mr Tse can use his chosen coding assistant with a local checkout of the working project. The assistant needs separately authorized GitHub access for commits/publishing and separately authorized Wix access for Wix work. A connector or plugin may help, but availability and editor coverage must be checked at setup time.

Keep passwords, tokens, and session cookies out of this document and the repositories. Use the services' normal sign-in and permission controls. Having an assistant installed does not grant it access to Gary's accounts.

A useful maintenance request is:

> Read AGENT-HANDOFF.md and inspect the current repository. Add the attached approved paper and PDF to the appropriate language pages, preserve all existing wording, and show me a local preview. Explain any missing information before publishing. Do not change Wix.

For design changes:

> Update the review site's layout as described, check desktop and mobile, and show the result. Keep the original scholarly content and media associations intact.

The goal is a reviewable, documented maintenance process. Human review remains appropriate for scholarly wording, attribution, media selection, and publishing decisions.
