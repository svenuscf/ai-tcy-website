# Cloudflare R2 媒體儲存與遷移記錄

最後更新：2026 年 10 月 5 日

## 已建立的資源

- Bucket：`tsechunyan-media`
- Region hint：Asia-Pacific (APAC)
- Storage class：Standard
- 臨時公開測試網址：<https://pub-730971bf7ce14078bf615c3bd0c516a9.r2.dev>

`r2.dev` 網址只供測試，Cloudflare 會限制流量，亦沒有正式 custom domain 的完整快取及控制功能。正式遷移時建議使用 `media.tsechunyan.com`，並保留 `www.tsechunyan.com` 及現有 QR code 目標不變。

## Pilot 驗證

以下三個測試物件已上載並可公開讀取：

- `r2-pilot-upload/audio/compositions/pilot-guiyuan-cao.mp3`
- `r2-pilot-upload/documents/scores/pilot-dongting-qiusi.pdf`
- `r2-pilot-upload/images/portraits/tse-chun-yan-current.jpg`

驗證結果：

- MP3：`audio/mpeg`，2,481,969 bytes
- PDF：`application/pdf`，315,362 bytes
- JPEG：`image/jpeg`，7,569 bytes
- 三者均支援 byte ranges；MP3 的 `Range: bytes=0-1023` 測試回傳 `206 Partial Content`，適合 HTML audio 串流及跳播。

測試期間建立的 bucket-scoped Object Read & Write API token 已在測試後撤銷。repository 及本機沒有保存有效的 Cloudflare secret。

## 建議的正式物件路徑

```text
audio/compositions/<stable-key>/<track-number>-<slug>.mp3
documents/scores/<stable-key>/<slug>.pdf
images/portraits/<slug>.jpg
images/covers/<stable-key>/<slug>.jpg
```

路徑應使用長期穩定的英文 slug 或 CMS stable key。不要把顯示次序、年份或容易改動的標題作為唯一識別。

## 正式遷移程序

1. 從 Wix media manifest 和 CMS 匯出完整媒體 URL 清單，分開圖片、錄音及 PDF；YouTube、Bilibili 影片只保留外部連結。
2. 下載每個原檔，記錄來源 URL、檔案大小、MIME type 及 SHA-256 checksum。
3. 建立只限 `tsechunyan-media` bucket 的短期 Object Read & Write token，放在被 Git 忽略的本機 `.env.r2.local`，不可貼進 MD、CMS 或 commit。
4. 按上述穩定路徑批量上載，逐檔比對大小及 checksum。
5. 為 bucket 連接 `media.tsechunyan.com`；此步需要先把 `tsechunyan.com` DNS 加入 Cloudflare，並完整保留 Wix 所需的 A、CNAME、TXT、MX 及驗證記錄。
6. 先在 staging 將 CMS 媒體 URL 指向 R2，檢查中英文頁面、圖片、PDF、所有單曲及多曲 playlist。
7. 驗證 desktop、mobile、跨瀏覽器、HTTP range、cache header、404 和下載行為。
8. 正式站切換後至少平行保留 Wix 原媒體一段觀察期；確認存取記錄及頁面沒有遺漏，才考慮降低或取消 Wix plan。
9. 完成後立即撤銷短期寫入 token。日常公開讀取不需要把 API secret 放在前端。

## 成本與容量判斷

目前 pilot 遠低於 Cloudflare R2 免費額度。正式評估應以完整 inventory 的總 bytes、每月新增量、請求數及熱門錄音播放量為準。R2 的公開 egress 不收費，但儲存量和 Class A／B 操作超出免費額度後會計費；正式遷移前再次查看 Cloudflare 當時的價格及 account usage。

## 現時限制

- Wix 正式網站尚未改用 R2，現有網站及 CMS 沒有因本次 pilot 被修改。
- `r2.dev` 仍是公開測試入口；未連接 production custom domain。
- 下一次需要寫入時要另建短期、bucket-scoped token，完成後撤銷。
- 取消 Wix 前必須確認 Wix plan 是否仍承擔 domain、Headless hosting、CMS 或其他正式站功能；R2 只解決媒體 object storage，不會自動取代 CMS 和 hosting。
