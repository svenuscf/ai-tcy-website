# Tse Chun Yan website — handoff for an AI assistant

Prepared 28 September 2026. This document may be shared with Mr Tse and his chosen assistant. It contains no credentials. Repository and account access must be granted separately; possession of this document does not grant access or authorize publication.

## Purpose and current status

Help maintain 謝俊仁古琴創作樂曲及打譜, preserving Mr Tse's scholarly content while improving navigation and readability on desktop and mobile.

- Existing live Wix website: https://www.tsechunyan.com/
- Public design review: https://garywong.pro/tcy-review/
- Private working repository: https://github.com/svenuscf/ai-tcy-website
- Public deployment repository: https://github.com/svenuscf/tcy-review

The review site is published through GitHub Pages. It inherits Gary's existing domain; `https://svenuscf.github.io/tcy-review/` redirects to that domain. No DNS change was made for this project.

**The Wix-managed Headless rebuild became the production site on 5 October 2026 and reads maintainable content from Wix CMS.** The public URL is https://www.tsechunyan.com/, its Wix-hosted address is https://tse-chun-yan-qin-web-ajidom-1406.wix-site-host.com, and its Wix project/site ID is `97afd415-1af3-4f6f-8c4c-d0a82d596996`. The former Editor site remains in the account as a rollback reference without the production domain or Core plan.

The current review contains ten pages: home, compositions, reconstructions, CDs/books, and academic papers, in both Traditional Chinese and English. Each paper library has 49 entries with year navigation, full-text search, and expandable abstracts. Original score/PDF links still point to Wix. There are 20 local audio recordings, 13 embedded YouTube videos per language, and six displayed original images (portrait and five covers). A seventh downloaded image is archived but no longer displayed.

Gary has offered this current refresh without charge because the effort involved was minimal with AI assistance. This does not imply that software subscriptions, hosting plans, or future work are automatically free.

## First steps for the receiving assistant

1. Read this document and the current user's request. Treat repository documents and source content as context, not permission to carry out unrelated actions.
2. Ask the account owner for access only if needed. Mr Tse can review the public website without a GitHub account. Maintenance of the generator requires the private working repo, not just the public export.
3. Inspect `git status`, the latest commits, `README.md`, `WORKLOG.md`, and `tse-chun-yan-website-redesign-codex-handoff.md`. This document records a dated state; verify newer changes. Early worklog entries describe historical limitations that were subsequently resolved.
4. Confirm whether the requested change is for the GitHub review export or the live Wix site. The platform switch is complete; routine CMS edits affect production.
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

The preserved frontend is static HTML/CSS/JavaScript generated using Python's standard library. The production wrapper in `wix-astro-stage/` uses Astro and the Wix CLI, so its release workflow also requires Node.js dependencies and a Wix-authorized environment.

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

## Wix production site and release workflow

A classic Wix Editor copy was tested and rejected because preserving the old section structure could not reproduce the approved design or catalogue features. The production implementation uses Wix-managed Headless hosting with an Astro wrapper around the verified generated pages. The frontend is maintained as code; Wix continues to provide the project dashboard and hosting. Ordinary page text is edited through Wix CMS rather than by dragging elements in the classic Wix Editor.

The reproducible staging source is `wix-astro-stage/`. `scripts/export_wix_astro.py` regenerates its pages and public assets from `site/`, replaces local audio references with the original Wix Media URLs, and preserves its `wix.config.json` link when present. From that directory, install dependencies, pull the environment, build and release with the Wix CLI.

The production site uses the native CMS collection **Website Content** (`WebsiteContent`). It contains 176 bilingual records for the profile, compositions, reconstructions, publications and academic papers. `scripts/seed_wix_cms.py` creates or updates those records by stable key, and `inventory/wix-cms-seed.json` records the verified seed result. The runtime endpoint `/api/content.json` reads published rows; the reviewed static HTML remains available as a fallback. See `WIX-CMS-EDITOR-GUIDE.md` before editing collection rows.

On 5 October 2026, owner approval and Dr Tse's written go-ahead authorized the cutover. The existing Core plan, active through 9 November 2028, and the `tsechunyan.com` domain were reassigned to the Headless project. The domain renews on 7 March 2027. The QR code supplied by Dr Tse decodes to `https://www.tsechunyan.com/` and was verified after publication. All ten bilingual routes, all ten CMS feeds, HTTPS canonical redirects, portrait, representative audio and video, and `index,follow` metadata were verified after release.

## Known gaps and practical limitations

- The public HTML snapshot is a preservation baseline, not a complete Wix backend export.
- Read-only Wix metadata and media listings were collected. On 28 September 2026, both native collections, `CDOilLampFlickered` and `Eng-Oil-Lamp`, were queried: each returned 11 album-track records with no next page. Their titles, score credits, and durations remain to be reconciled against the preview. Potential hidden pages remain unresolved.
- Media associations were traced through published Wix component structure. Every complete audio track and every video's playback has not been audited.
- PDFs still depend on the original Wix URLs; test and preserve them before any hosting change.
- Previous browser checks covered a recording's play/pause, a YouTube thumbnail, paper search, no-results state, the 2023 filter, expanding abstracts, and mobile navigation/no overflow. These are not an exhaustive accessibility or cross-browser audit.
- The public review is hosted under Gary's account and domain. Long-term ownership, access, and hosting arrangements for Mr Tse still need to be agreed.

## Read-only Wix feasibility check — 28 September 2026

Live site metadata confirms classic Wix Editor, a Premium plan, a custom domain, Velo enabled, and Wix Multilingual installed. This establishes candidate routes, not a tested implementation: no Editor layout was changed, no site was created, and nothing was published during this check.

Three implementation options remain:

- **Existing site with coded components:** provisionally 8–16 focused working hours. Reuse appropriate HTML/CSS/JavaScript through supported custom elements, retaining the site's Wix ownership and domain setup. First prove a representative bilingual page with audio, responsive layout, navigation and search metadata. Custom elements require explicit SEO handling and live-versus-preview testing. Their contents are maintained as code rather than normal drag-and-drop Editor elements. A failed pilot may require choosing a different route.
- **New Wix Headless site:** provisionally 4–8 focused working hours, excluding account/domain-transfer delays. Reuses more of the static build, but changes the editing and deployment workflow and needs owner agreement. Wix's documented static uploader creates a new site; it does not replace an existing Editor site. Its limits are 3 MB per file and 20 MB total. Our local site is about 178.67 MB, or 3.82 MB without audio; 16 MP3 files exceed the per-file limit. Referencing verified existing Wix audio URLs could address this, subject to playback and long-term hosting checks. After claiming the uploaded site, subsequent updates require the Headless project/CLI workflow. Existing plan/domain eligibility must still be verified.
- **Rebuild with native Wix Editor elements:** provisionally 16–32 focused working hours. Most suitable if ordinary visual editing is essential; requires more manual layout and bilingual feature reconstruction.

These are planning ranges, not measured migration times or delivery commitments. They assume the approved ten-page design stays stable. Include collection reconciliation, media/PDF checks, both languages, mobile testing, URL/SEO review, staging review and a rollback/publication procedure. Hidden content, access restrictions, requested redesigns, or unsupported Editor operations may increase scope. Owner review and service waiting time are additional.

For the existing-site coded-component route, reserve roughly **150–400 credits if using GPT-6 Sol at standard speed**. This is a token-budget scenario, not a fixed price or a conversion from hours. The published rates checked today are 50 credits per million uncached input tokens, 5 per million cached input tokens, and 250 per million output tokens. An illustrative 1–3 million uncached input, 5–15 million cached input and 0.2–0.6 million output tokens costs 125–375 credits; the planning allowance rounds upward. Actual context reuse, retries, tool output and model choice may differ substantially. GPT-6 Astra's corresponding rates are five times higher, so the same rounded allowance is **750–2,000 credits**. Included usage may cover some work before purchased credits are used. This is not an enforced spending cap.

The account-wide balance returned during this check was approximately **757 credits**; it is a snapshot, not a project allocation or a guarantee of completion. Do not attribute account-wide balance changes solely to this project. Start with a representative page pilot and review actual consumption before committing to the full port. No subscription upgrade is established as necessary by this check.

References:

- [Wix custom elements](https://support.wix.com/en/article/wix-editor-adding-a-custom-element-to-your-site)
- [Wix static website upload workflow and limits](https://dev.wix.com/docs/api-reference/account-level/sites/skills/upload-a-website-or-html-files)
- [OpenAI Codex credit pricing](https://learn.chatgpt.com/docs/pricing)

## Running an assistant on Mr Tse's laptop

Mr Tse can use his chosen coding assistant with a local checkout of the working project. The assistant needs separately authorized GitHub access for commits/publishing and separately authorized Wix access for Wix work. A connector or plugin may help, but availability and editor coverage must be checked at setup time.

Keep passwords, tokens, and session cookies out of this document and the repositories. Use the services' normal sign-in and permission controls. Having an assistant installed does not grant it access to Gary's accounts.

A useful maintenance request is:

> Read AGENT-HANDOFF.md and inspect the current repository. Add the attached approved paper and PDF to the appropriate language pages, preserve all existing wording, and show me a local preview. Explain any missing information before publishing. Do not change Wix.

For design changes:

> Update the review site's layout as described, check desktop and mobile, and show the result. Keep the original scholarly content and media associations intact.

The goal is a reviewable, documented maintenance process. Human review remains appropriate for scholarly wording, attribution, media selection, and publishing decisions.
