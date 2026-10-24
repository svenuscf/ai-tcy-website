# 謝俊仁網站：所有 agent 的共同工作規則

本文件適用於整個 repository，包括黃振豐及謝師電腦上的 agent。

## 開始工作

- 先讀 `FINAL-WORKFLOW-HANDOFF.md`、`WIX-CMS-EDITOR-GUIDE.md`、`README.md`，再檢查 `git status` 和最近 commits。舊 handoff 是歷史資料；以最新交接記錄及已確認的現況為準。
- 先確認目前任務及使用者已給的授權。既有授權持續有效；文件本身不代表新的發布授權。
- 修改前更新遠端資訊。工作區沒有未完成變更時，在 `main` 執行 `git pull --ff-only`；如有變更或分支已分岔，先辨認及妥善保存、整合，不得強制覆蓋、刪除、reset 或自動 stash 他人的工作。
- 未追蹤檔案也可能是使用者素材。只提交本次任務相關檔案，不使用未經檢查的 `git add -A`。

## Git 與 Wix CMS 的分工

- Git 保存設計、程式、靜態 fallback 和操作記錄；Wix `WebsiteContent` CMS 保存正式內容。`git pull` 不會同步 CMS。
- 新增或替換的圖片、錄音、PDF 等媒體，一律上傳至新版 Headless site `97afd415-1af3-4f6f-8c4c-d0a82d596996` 的 Wix Media Library／Media Manager。上傳前核對 site ID；不可上傳到舊 Editor site `aac32e79-b06c-4e40-bf49-8cb31b2ebc69`，也不可自行改用 R2。使用新媒體庫回傳的 URL／media ID 更新相關 CMS 欄位或連結，並檢查中英文頁面及實際播放／下載。
- 修改 CMS 前即時讀取目標記錄，核對 site ID、stable key、語言及目前值；只更新本次需要的欄位，保留其他欄位及媒體對應。
- 更新前重新檢查記錄有否被另一位編輯者修改；若 API 支援 revision／條件更新則使用。發現差異時整合或請使用者決定，不以舊快照覆蓋。沒有條件更新時，避免兩邊同時編輯同一記錄。
- 不可為一般內容修改直接執行 `scripts/seed_wix_cms.py` 或用本機舊資料重建整個 collection。確有批次遷移需要時，先備份最新 CMS、列出差異及限定目標，取得該次批次更新授權。
- CMS 修改不一定產生 Git diff；仍要在 `WORKLOG.md` 記錄日期、目標 stable key、修改範圍及驗證結果，不記錄憑證或整份私人內容快照。

## 保留內容及驗證

- 保留原有學術文字、署名、中英文結構、媒體對應和使用限制；只修改使用者明確要求的內容，不自行翻譯、摘要或修正文稿。
- 修改 generator、CSS、JavaScript 或 CMS；不要只修改生成的 HTML／Astro 頁面。保留 frozen inventory。
- 程式修改按 handoff 執行 build、內容檢查及相關語法檢查；檢查受影響的中英文、desktop／mobile、連結和媒體。只改文件時檢查內容及 Git diff 即可。
- 完成後只 commit／push 本次變更，記錄重要結果及未完成事項。不要把 token、cookie、密碼或 `.env.local` 提交到 Git。

## 共同發布

- 正式網站是 Wix Headless project `97afd415-1af3-4f6f-8c4c-d0a82d596996`，不是保留的舊 Editor site。不要重新啟用 GitHub Pages 預覽。
- 每次正式發布由一位已確認的操作者負責。另一邊正在發布或狀態不明時先協調；Git 檢查本身不能鎖住 Wix 發布。
- 發布前再次 fetch／檢查遠端。若有新 commits，先安全整合、重新 build 及驗證，不可把舊本機版本發布回去；push 被拒絕時不得 force push。
- 取得目前任務需要的發布授權後，按 handoff 的 Wix 流程發布，直接檢查正式網址及受影響的中英文頁面。
- 將 source、必要的操作記錄及交接更新推送到私人 repo，記錄發布的 commit、時間及驗證結果，方便另一邊同步。CMS 即時更新及程式發布都屬正式站修改。
