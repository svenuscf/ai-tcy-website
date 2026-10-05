# 謝俊仁網站：最終工作流程與交接記錄

最後更新：2026 年 10 月 5 日

本文件是目前網站的主要交接文件，供網站擁有人、黃振豐、謝俊仁老師及日後接手的 AI agent 使用。文件不含密碼、API key、session cookie 或其他登入資料；GitHub 和 Wix 權限必須由帳戶擁有人另行授予。

## 1. 目前狀態

- 正式網站：<https://www.tsechunyan.com/>
- QR code 目標：`https://www.tsechunyan.com/`
- Wix 託管網址：<https://tse-chun-yan-qin-web-ajidom-1406.wix-site-host.com>
- Wix project/site ID：`97afd415-1af3-4f6f-8c4c-d0a82d596996`
- Wix app ID：`9599e984-94a2-4b11-b6af-70b0a39d21b2`
- 私人原始碼 repository：<https://github.com/svenuscf/ai-tcy-website>
- 舊公開預覽 repository：<https://github.com/svenuscf/tcy-review>

Wix Headless 新版已於 2026 年 10 月 5 日成為正式網站。原有 `tsechunyan.com` 網址保持不變，因此書籍中的 QR code 無須更換。

GitHub Pages 預覽已停止：`https://garywong.pro/tcy-review/` 現在回傳 404，Pages source 已設為 `None`，不會因 push 而自動重建。`tcy-review` repository 暫時保留作歷史記錄，不再是網站發布來源。

原 Wix Editor 網站仍留在 Wix 帳戶內作回復參考，但已沒有正式 domain 和 Core plan。現有 Core plan 及 domain 已連接到上述 Wix Headless project。文件記錄的 plan 到期日為 2028 年 11 月 9 日，domain 續期日為 2027 年 3 月 7 日；處理續期前應在 Wix Billing 再確認。

## 2. 維護模式

網站現在分成兩個維護層次：

1. **Wix CMS 管理內容**：傳記、創作、打譜、唱片與書籍、論文、摘要、圖片、錄音和影片連結。
2. **私人 GitHub repository 管理設計及程式**：版面、字體、顏色、導覽、搜尋、排序、響應式設計、CMS 讀取方式和 Wix 發布設定。

一般文字修訂由謝老師直接在 Wix CMS 完成。新增中英文項目、結構調整、版面修改、媒體整合及發布工作，交由獲授權的 AI agent 處理。這套分工可以減少每次更新的人工成本，也讓黃振豐不必長期擔任日常網站管理員。

AI agent 不應自行改寫學術內容、翻譯缺少的英文稿、改動署名或發布未經核准的材料。人仍需審核學術文字、圖片、錄音、版權和最終發布結果。

## 3. Wix CMS 日常編輯

- Collection：**Website Content**
- Collection ID：`WebsiteContent`
- 直接連結：<https://manage.wix.com/dashboard/97afd415-1af3-4f6f-8c4c-d0a82d596996/wix-cms/data/WebsiteContent?referralInfo=sidebar>
- 詳細圖文以外的操作說明：[`WIX-CMS-EDITOR-GUIDE.md`](WIX-CMS-EDITOR-GUIDE.md)

日常編輯步驟：

1. 在 CMS 先按 `Page` 和 `Language` 篩選。
2. 搜尋標題或 Stable Record Key。
3. 修改 `Main Content`、`Contents Title`、`Abstract`、圖片或媒體欄位。
4. 等待 Wix 儲存完成。
5. 重新載入正式網站，檢查中文和英文頁面。

不要在一般編輯中修改：

- `Stable Record Key`
- `Page`
- `Language`
- `Entry Key`

所有內容頁面按 `Display Order` 由大至小排列。新增項目時，找出該頁及語言的最高數值，再加 10；例如最高是 `150`，新項目使用 `160`，便會自動顯示在最前。無須將所有舊項目逐一加 1。中英文配對項目通常使用相同排序值。

未完成項目應先關閉 `Visible on Website`，不要刪除。新增作品、論文或出版物時，建議由 agent 建立中英文配對記錄、檢查 stable key、排序、PDF、圖片、錄音和影片。

## 4. 程式結構及資料來源

- `scripts/build_site.py`：從保留的 Wix 原始內容產生十個中英文頁面；版面模板和核准文字調整在此維護。
- `scripts/check_site.py`：驗證十頁、250 個原始文字元件、連結、資產、媒體及核准的文字差異。
- `site/assets/style.css`：全站視覺與響應式設計。
- `site/assets/app.js`：選單、搜尋、年份篩選、摘要、CMS hydration 及自動年份。
- `site/`：產生後的靜態頁面和保留媒體。
- `scripts/export_wix_astro.py`：把已驗證的 `site/` 包裝成 Wix Astro project。
- `wix-astro-stage/`：Wix Headless 正式部署來源。
- `scripts/seed_wix_cms.py`：以 stable key 建立或更新 CMS 記錄，不應產生重複項目。
- `scripts/migrate_multi_track_audio.py`：只為含多條錄音的作品建立及更新
  `audioTracks` CMS 欄位，避免 playlist 被簡化成單一播放器。
- `inventory/content-baseline.json`：原始文字、連結和 hash 基準。
- `inventory/media-manifest.json`：圖片、錄音、影片及來源對應。
- `WORKLOG.md`：歷史操作與決定。

不要只修改 `site/**/index.html` 或 `wix-astro-stage/src/pages/*.astro`；這些是產生檔，下次 build 會被覆寫。應修改 generator、CSS、JavaScript 或 CMS，再重新產生。

CMS API endpoint 為 `/api/content.json`。正式頁面優先顯示 Wix CMS 已發布的記錄；如 CMS 暫時無法讀取，頁面會使用已審核的靜態內容作 fallback。

多條錄音的作品使用 `Audio Tracks (agent-managed)` 結構化欄位。普通的
`Audio URL`、`Audio Title` 和 `Performer / Credit` 仍保留作單曲目編輯。
2026 年 10 月 5 日已修復《孔子63》/《孔子．回首63》配樂在 CMS
migration 後只剩第 1 條錄音的問題；中英文頁面現均顯示第 1、2、3 條。

## 5. 本機建置及檢查

在私人 repository 根目錄執行：

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check site/assets/app.js
python3 -m http.server 4317 --bind 127.0.0.1 --directory site
```

在瀏覽器打開 `http://127.0.0.1:4317/`。修改相關功能後，至少檢查：

- 中文和英文；
- desktop 和 mobile；
- 導覽及語言切換；
- 新增或修改的文字、連結、PDF、圖片和媒體；
- 論文搜尋、年份篩選及摘要；
- 內容排序及目錄連結。

## 6. Wix 發布流程

只有在內容擁有人已核准修改時才發布。普通 CMS 修改通常不需要重新 build；程式、版面或靜態 fallback 修改才需要以下流程。

在 repository 根目錄：

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 scripts/export_wix_astro.py
```

然後：

```sh
cd wix-astro-stage
npm install
npm run build
npm run release
```

Wix CLI 必須由獲授權帳戶登入，環境連接資料不得提交到 Git。`npm run release` 會更新正式網站；完成後不能只相信 CLI 的成功訊息，必須直接檢查 `https://www.tsechunyan.com/`。

發布後應：

1. 檢查受影響的中英文頁面。
2. 確認首頁、mobile menu、圖片及代表性錄音仍可使用。
3. 如修改 CMS rendering，檢查 `/api/content.json` 回應及項目數量。
4. 將 source change commit 並 push 到私人 repository。
5. 不要重新開啟 GitHub Pages 預覽，除非擁有人另行要求。

## 7. 回復與故障處理

小型內容錯誤：在 CMS 修正，或暫時關閉 `Visible on Website`。

程式發布出錯：使用 Git 找出上一個已知正常 commit，從該版本重新 build 及 `npm run release`。不要刪除 CMS collection 或 frozen inventory。

Wix CMS 暫時失效：網站應顯示靜態 fallback；先確認正式頁仍可讀，再檢查 CMS 權限、collection ID 和 API endpoint。

重大故障才考慮把 domain/plan 重新連接到舊 Wix Editor site。這會涉及 Wix 帳戶、plan 和 domain 設定，操作前必須確認目前狀態並取得擁有人核准。

## 8. 已確認的設計決定

- 保留米白背景、深綠文字、低調紅色點綴和充足留白。
- 不恢復頁首「琴」圖示。
- 不恢復首頁大型古琴琴弦近照。
- 保留原有 sitemap：首頁、創作樂曲、打譜、唱片書籍及論文，各有繁中和英文版本。
- 保留原有圖片、封面、錄音、YouTube、演奏者資料和 PDF 連結。
- 新內容排列在最前。
- Wix CMS 用於內容；設計和結構由 code 管理。

目前鳴謝文字把 2022 視為網站新形式開始的年份，2026 則記錄重新設計及整理：

> 本網站繼2022年改版後，於2026年重新設計及整理，現由AI助理協助管理及維護。

英文：

> Following the 2022 redesign, this website was redesigned and reorganized in 2026 and is now managed and maintained with the assistance of an AI assistant.

版權年份以 JavaScript 自動顯示為 `© 2022–當前年份`；2027 年會自動變成 `© 2022–2027`。頁尾「官方網站 · 年份」亦會自動更新。2026 的改版記錄保持固定，不應隨年份更改。

## 9. Repository 與權限原則

`ai-tcy-website` 必須保持 private。它是設計、generator、inventory、操作說明和 Wix 發布程式的主要版本記錄。

`tcy-review` 是已停用的公開預覽 repository。它不含私人 working history，但其內容仍公開可見；除非另有決定，不需刪除，也不要重新啟用 Pages。

不要把 Wix token、GitHub token、密碼、cookie、`.env.local` 或個人 session 放進任何 MD、commit 或 CMS 欄位。交給另一位 agent 時，只分享本文件不能取代正式權限授予。

## 10. 給下一個 agent 的起始指令

```text
先閱讀 FINAL-WORKFLOW-HANDOFF.md、WIX-CMS-EDITOR-GUIDE.md、README.md，
再檢查 git status 和最近 commits。正式網站由 Wix Headless 託管，內容主要來自
WebsiteContent CMS，私人 GitHub repository 保存設計和發布程式。保留原有學術文字、
媒體對應、中英文結構和最新內容優先排序。先完成修改及驗證，發布前確認授權；發布後
直接檢查 tsechunyan.com。不要重新啟用已停用的 GitHub Pages 預覽。
```

## 11. 建議的長期安排

謝老師可使用 Wix CMS 處理現有項目的文字、圖片及顯示狀態。大型更新交由能登入 Wix 並操作此 repository 的 agent。若香港地區的 agent 服務選擇有變，repository、CMS schema 和本文件仍可交給另一個工具；不要把維護能力綁定於單一 AI 供應商。

在 2028 年 Wix plan 續期前，重新評估繼續使用 Wix Headless，或把程式網站遷移到其他 hosting。無論選擇哪一個平台，先保留 domain、URL 路徑、QR code 目標、CMS 資料、PDF 和媒體連結。
