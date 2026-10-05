# Editing the live website in Wix CMS

The live website reads regularly updated content from the **Website Content** CMS collection. Wix CMS works like a content table: each row is one Chinese or English entry, and each column controls part of that entry. The site's layout, typography, navigation and responsive behaviour remain in the codebase.

- Live website: https://www.tsechunyan.com/
- Wix-hosted project address: https://tse-chun-yan-qin-web-ajidom-1406.wix-site-host.com
- Website Content collection: https://manage.wix.com/dashboard/97afd415-1af3-4f6f-8c4c-d0a82d596996/wix-cms/data/WebsiteContent?referralInfo=sidebar
- CMS collection name: **Website Content** (`WebsiteContent`)

CMS changes affect the public website after Wix saves them. Review each change on the live website immediately; use **Visible on Website** to hide an unfinished item.

## Basic editing procedure

1. Sign in to Wix and open the **Website Content** link above.
2. Select **Filter** and choose the required **Page** and **Language**. Filtering first reduces the chance of editing the wrong language or section.
3. Use **Search** to find the title, or locate the row in the filtered list.
4. Edit the relevant cell. Open the row if Wix provides a larger editing form for rich text, images or media fields.
5. Wait for Wix to finish saving. Most table edits autosave, but do not close the page while a saving indicator is visible.
6. Open or refresh the live website and check both desktop and mobile layouts. For bilingual material, also check the other language page.

The page identifiers used in the collection are:

- `home`
- `compositions`
- `reconstruction`
- `cds-and-books`
- `academic`

The language identifiers are `zh` for Chinese and `en` for English.

## Fields intended for ordinary editing

- **Contents Title**: the label shown in the page's contents list.
- **Display Order**: the item's sorting priority. Every content section uses newest-first ordering, so a new item receives a number higher than the current maximum. Avoid duplicate values.
- **Main Content**: formatted text, links and score-download links.
- **Abstract**: the expandable abstract on the academic papers page.
- **Publication Year**: the year used to group academic papers.
- **Visible on Website**: turn this off to hide an item without deleting it.
- **Audio URL**, **Audio Title**, **Performer / Credit**: recording details.
- **Audio Tracks (agent-managed)**: ordered multi-track playlist data. Leave this
  structured field to the maintaining agent; it is used when one work contains
  more than one audio player.
- **Video Embed URL**, **Video Page URL**: embedded video and its fallback link.
- **Image** and **Image Description**: portrait or publication cover and accessible description.
- **Editor Note**: an internal note; it is not displayed on the website.

## Fields to leave unchanged during routine editing

- **Stable Record Key**
- **Page**
- **Language**
- **Entry Key**

These four fields connect a CMS row to the correct bilingual page. Changing them can move an entry to another page, create a duplicate, or prevent it from appearing. Each Chinese and English entry is a separate record; editing one does not automatically translate or update the other.

## Example: edit the biography

1. Filter **Page** to `home` and **Language** to `zh`.
2. Open the record whose **Stable Record Key** is `home:zh:profile`.
3. Edit **Main Content** and allow Wix to save.
4. Refresh the Chinese live homepage.
5. Repeat with `home:en:profile` if the English biography also needs to change.

Rich-text formatting and links should be edited inside the expanded field editor when available.

## Example: replace the portrait

1. Filter **Page** to `home`.
2. Open `home:zh:profile` and replace the **Image** with the new portrait.
3. Set **Image Description** to a short description such as `謝俊仁`.
4. Open `home:en:profile`, select the same image, and set the description to `TSE Chun-Yan`.
5. Refresh the Chinese and English live homepages.

Updating both profile records keeps the portrait consistent when visitors switch languages.

## Example: edit an existing composition

1. Filter **Page** to `compositions` and **Language** to `zh`.
2. Search for the title, for example `短松岡`.
3. Change **Contents Title** if the contents-list label needs to change.
4. Change **Main Content** for the description, formatted text or score links.
5. Update **Audio URL**, **Audio Title** and **Performer / Credit** for a recording.
6. Update **Video Embed URL** and **Video Page URL** for a video.
7. Refresh the Chinese compositions page on the live site and test every changed link or player.
8. Repeat on the corresponding `en` record when needed.

For YouTube, **Video Embed URL** should normally use the embed form, such as `https://www.youtube.com/embed/VIDEO_ID`. **Video Page URL** can use the ordinary public watch-page URL.

## Example: change the contents order

1. Filter to one **Page** and one **Language**.
2. For a new item, find the current highest **Display Order** on that page and add `10`. For example, if the newest existing composition is `150`, set the new one to `160`. Because all content sections sort in descending order, it will appear first automatically.
3. To place an item between orders `140` and `130`, use a value such as `135`.
4. The same newest-first rule applies to compositions, reconstructions, CDs and books, and academic papers.
5. Refresh the live page and confirm that both the contents list and the article order changed.
6. Repeat the same ordering value in the other language if the two versions should match.

Avoid duplicate order numbers because their relative order may be unpredictable.

## Example: hide and restore an entry

1. Find the record using **Page**, **Language** and **Search**.
2. Turn off **Visible on Website**.
3. Refresh the live page and confirm that the item and its contents-list link are gone.
4. Turn the field on again to restore the item.

This is safer than deleting a row and preserves all text and media information.

## Example: edit an academic paper

1. Filter **Page** to `academic` and select the language.
2. Search for the paper title.
3. Edit **Main Content** for the citation, title and links.
4. Edit **Abstract** for the expandable abstract text.
5. Change **Publication Year** if the paper belongs under another year heading.
6. Refresh the live academic page and test its abstract and links.
7. Repeat for the other language record if required.

## Example: edit a CD or book

1. Filter **Page** to `cds-and-books` and select the language.
2. Search for the publication title.
3. Edit **Contents Title** and **Main Content**.
4. Replace **Image** for the cover and update **Image Description**.
5. Refresh the live page and check the image crop, text and links.

## Adding a new item

Adding a new composition, reconstruction, publication or paper is more technical than editing an existing row. It requires a unique **Stable Record Key**, the correct **Entry Key**, ordering, formatted content, media checks and usually a matching record in the other language.

The recommended procedure is to give the material to the maintaining AI agent, for example:

> Add this as a new Chinese and English composition after “短松岡”. Use the attached score, audio recording and YouTube link. Leave the English description marked for review if the translation is uncertain.

The agent can create the paired CMS records and verify links, ordering, desktop and mobile presentation. Dr Tse can comfortably use CMS for routine text edits, portrait and cover replacements, ordering, and hiding or restoring existing entries. Visual-design changes should continue through the code workflow.

CMS edits appear after refreshing the live page. The site retains the reviewed static content as a fallback if Wix CMS is temporarily unavailable.
