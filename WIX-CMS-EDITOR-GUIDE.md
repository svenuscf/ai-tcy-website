# Editing the staged website in Wix CMS

The Wix staging site reads its regularly updated content from the **Website Content** CMS collection. Layout, typography, navigation and responsive behaviour remain protected in the codebase.

- Staging preview: https://tse-chun-yan-qin-web-ajidom-1406.wix-site-host.com
- Wix dashboard: https://manage.wix.com/dashboard/97afd415-1af3-4f6f-8c4c-d0a82d596996/database/collections
- CMS collection: **Website Content** (`WebsiteContent`)

Sign in to the Wix account, open **CMS**, and select **Website Content**. Use the **Page** and **Language** columns to filter the list before editing.

## Fields intended for ordinary editing

- **Contents Title**: the title shown in the page contents list.
- **Display Order**: the item's position on its page. Use whole numbers.
- **Main Content**: formatted text, links and score-download links.
- **Abstract**: the expandable abstract on the academic papers page.
- **Publication Year**: the year used to group academic papers.
- **Visible on Website**: turn this off to hide an item without deleting it.
- **Audio URL**, **Audio Title**, **Performer / Credit**: recording details.
- **Video Embed URL**, **Video Page URL**: embedded video and its fallback link.
- **Image** and **Image Description**: portrait or publication cover and accessible description.
- **Editor Note**: an internal note; it is not displayed on the website.

## Fields to leave unchanged during routine editing

- **Stable Record Key**
- **Page**
- **Language**
- **Entry Key**

These fields connect a CMS row to the correct bilingual page. Changing them can move an entry to another page or prevent it from appearing.

## Common changes

To change the portrait, filter to `Page = home`, open the relevant Chinese and English profile rows, replace **Image**, and save. Both records currently use the same portrait.

To reorder a contents list, filter to the page and language, change **Display Order**, and save. The contents list and the entries use the same order automatically.

To hide an entry temporarily, turn off **Visible on Website**. This is safer than deleting it.

For a new composition, reconstruction, publication or paper, duplicate a similar row and ask the maintaining agent to assign a new stable key and check both language versions. The agent should also verify formatting, media, desktop and mobile display before publication.

CMS edits appear after refreshing the staging page. The site retains the reviewed static content as a fallback if Wix CMS is temporarily unavailable.
