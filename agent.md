# AGENTS.md — AI Radar 專案規範

本檔案是這個專案唯一的規範來源。任何人（或 AI Agent）在這個專案新增、修改內容或程式碼前，
都必須先讀完本檔並遵守。**新增文章只需要動 `content/` 底下的檔案，不需要改任何程式碼或 HTML。**

---

## 1. 專案目的

AI Radar 是一個繁體中文（台灣用語）的 AI 工具與技術介紹網站。

- 題材範圍：AI 工具、模型、技術、應用與有趣的新發展（圖像、影片、語音、音樂、程式開發、
  AI Agent、遊戲、世界模型，以及其他有趣的 AI 應用）。
- 內容來源：官方部落格、論文、GitHub、YouTube／Bilibili／Instagram、Reddit、官方文件等。
- **唯一最重要的目標：讓讀者產生興趣。** 讀完應該覺得「這東西真有意思，我想去玩玩看」。
- 明確不是：完整教學、工具資料庫、評測排行榜、新聞快訊。

判斷標準：如果一篇文章寫完像產品說明書或維基條目，就是寫壞了。

## 2. 技術與檔案結構

技術棧刻意保持極簡：**純靜態 HTML/CSS/JS ＋ Python 標準函式庫建置腳本**。
沒有 npm、沒有框架、沒有執行期依賴（唯一的外部請求是 Google Fonts，失敗時退回系統字型）。

```
aI_radar/
├─ README.md              操作說明（建置、預覽、部署）
├─ AGENTS.md              本規範（唯一規範來源）
├─ docs/
│  ├─ project-spec.md     完整規範（本檔的長版）
│  └─ writing-spec.md     文章格式、語氣、事實紀律
├─ content/               【唯一需要人工編輯的地方】
│  ├─ config.yml          站名、標語、分類定義（六個分類與各自的強調色）
│  └─ articles/*.md       文章，一檔一篇
├─ templates/             頁面骨架：base / index / article / category ＋ _card_*.html 卡片樣板
├─ static/                css（base, components, pages）、js/main.js、favicon.svg
├─ tools/                 build.py、covers.py、md.py、template.py、yamlish.py、check_links.py
└─ site/                  【產物，不要手改】每次建置整批重建
   ├─ index.html
   ├─ articles/<slug>.html
   ├─ categories/<id>.html
   └─ assets/{css,js,covers,favicon.svg}
```

**來源 vs 產物的鐵則**

- 要改內容 → `content/`。要改版面 → `templates/`。要改樣式 → `static/`。
- `site/` 底下的一切都是 `python tools/build.py` 的產物，**任何改動都會被下一次建置覆蓋**。
- 不要把備份檔、實驗檔、暫存檔留在專案裡。這裡沒有版本控制，唯一的還原方式是重新建置。

## 3. 建置、驗證與預覽

```bash
python tools/build.py             # content/ + templates/ + static/ → site/
python -m http.server -d site     # 本機預覽（http://localhost:8000）
python tools/check_links.py       # 檢查每篇文章的 tool.url 與 sources 是否還活著
```

- 建置必須是幂等的：同樣的來源跑兩次得到完全一樣的輸出（封面圖由 slug 決定，不含隨機成分）。
- frontmatter 有問題（缺 title／summary、category 不存在、date 格式錯、motif 或 palette 不在清單內、
  沒有 sources、tool.url 不是 http）必須報錯並以非 0 結束，**不可靜默產生壞掉的頁面**。
- 長度類問題（標題過長、摘要過長、正文過短）只警告，不中斷建置。
- 交付前必須實際打開產物確認，不能只看程式碼。`site/index.html` 直接雙擊就要能瀏覽
  （所有連結為相對路徑，不依賴 fetch、不依賴伺服器）。

## 4. 視覺設計規範

### 4.1 氣質

深色、精密、克制的科技感，像儀器面板而不是電競周邊。**不堆裝飾**：每個動畫、每條漸層都要有理由，
寧可少。優先照顧閱讀體驗與視覺一致性。

### 4.2 色彩（定義在 `static/css/base.css` 的 `:root`）

| 變數 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#06070a` | 頁面底色 |
| `--surface` / `--surface-2` | `#10131a` / `#161a23` | 卡片面板／hover |
| `--line` / `--line-strong` | `rgba(255,255,255,.08)` / `.16` | 一般／強調邊框 |
| `--text` / `--text-dim` / `--text-mute` | `#e8ecf4` / `#a2abbb` / `#6f7889` | 主／次／標籤文字 |
| `--accent` / `--accent-2` | `#4fe3c1`（薄荷青）/ `#7d8bff`（靛藍） | 主／次強調色 |

分類各有強調色（定義在 `content/config.yml`），只用於該分類的標籤、線條與封面：
agent `#7d8bff`｜coding `#7ee787`｜image `#ffb35c`｜video `#c58bff`｜audio `#4fe3c1`｜fun `#ff7ac6`。
卡片與面板用 `style="--c: …"` 把分類色注入區域變數，CSS 以 `var(--c, var(--accent))` 取用。

深色是唯一主題，不做淺色模式。內文與背景對比維持 WCAG AA 以上。

### 4.3 字體與排版

```css
--font-sans: "Inter", "Noto Sans TC", system-ui, -apple-system, "Segoe UI", "PingFang TC", "Microsoft JhengHei", sans-serif;
--font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
```

- 英文、數字、kicker 標籤、日期、來源網域一律用 `--font-mono`。這是最重要的「科技感」來源。
- 內文 `1.0625rem`／行高 `1.85`；文章正文最大寬 `720px`（約 38–42 字／行）。
- 標題：`h1 clamp(2.2rem, 5vw, 3.6rem)`、`h2 clamp(1.5rem, 3vw, 2rem)`、`h3 1.2rem`，字距 -.02em 起跳。

### 4.4 元件與間距

- 容器最大寬 `1180px`，左右留白 `clamp(20px, 5vw, 40px)`。
- 圓角：卡片 `14px`、面板／圖片 `12px`、標籤與按鈕 `999px`。
- 間距只用 `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96` 這組數列。
- 卡片：`--surface` 底、`--line` 邊框，hover 上浮 `4px`、邊框轉為分類強調色並帶柔和光暈。
- 封面圖一律 `aspect-ratio: 16/10`，由 `tools/covers.py` 產生 SVG，不依賴外部圖片。

### 4.5 動態

- 一律使用 `cubic-bezier(.22,.61,.36,1)`，時長 `180–420ms`。
- 進場：`IntersectionObserver` 加 `.is-visible`，同容器每張卡片錯開 60ms，只播一次。
- 首頁主視覺是純 CSS 雷達（conic-gradient 掃描＋同心圓＋光點脈動），不使用外部圖片或影片。
- **必須**尊重 `@media (prefers-reduced-motion: reduce)`：關閉所有位移與循環動畫。

### 4.6 響應式

斷點 `1024 / 768 / 560`。網格用 `auto-fill, minmax()` 或明確斷點，不可出現橫向捲動。
手機版導覽收成漢堡選單（純 CSS ＋ 少量 JS，不用外部函式庫）。
驗證橫向捲動要看 `document.documentElement.scrollWidth === clientWidth`，不要只看截圖。

## 5. 頁面結構

全站只有三種頁面。共用置頂導覽（品牌＋首頁／精選／最新發現／分類）與頁尾
（品牌、一句話說明、分類清單與篇數、來源聲明、年份）。

1. **首頁 `index.html`**：主視覺（雷達＋標語＋CTA＋統計）→ 精選內容（`rank` 最小者為大卡，
   其餘為橫式小卡）→ 最新發現（日期新到舊，最多 9 篇）→ 主題分類（六個磁磚，附篇數與最新日期）→ 頁尾。
2. **文章頁 `articles/<slug>.html`**：麵包屑 → 分類標籤 → 標題 → 摘要 → 日期／閱讀時間 →
   標籤 → 大封面 → 重點速覽 → 正文（Markdown）→ 延伸潛力 → 原始來源 → 同分類其他文章 → 頁尾。
   右側欄（桌機 sticky）放工具資訊卡與「數據以官方頁面為準」的提醒。
3. **分類頁 `categories/<id>.html`**：分類名稱／說明／篇數 → 卡片網格 → 其他分類磁磚 → 頁尾。
   該分類沒有文章時顯示「雷達還在掃描中」空狀態，不可留白或顯示錯誤。

## 6. 文章內容格式

文章是 Markdown 檔，放在 `content/articles/<slug>.md`。檔案開頭是 frontmatter（`---` 包住，
mini-YAML：純量、`[a, b]` 內聯陣列、`- ` 區塊陣列、兩層縮排 map），後面是 Markdown 正文。
**完整欄位定義、語氣範例與自我檢查清單見 `docs/writing-spec.md`，寫作前必須先讀。**

```yaml
---
title: "標題（20–34 字，具體物件＋好奇心缺口，不要標題殺）"
slug: nano-banana-pro
summary: "40–70 字，說明這是什麼 ＋ 為什麼有趣"
category: image                  # 必須是 config.yml 裡的分類 id
tags: [圖像生成, 文字渲染]
date: 2026-11-16
updated: 2026-11-20              # 可省略
featured: true                   # 可省略
rank: 1                          # featured 時的排序，1 為首頁最大卡
reading_time: 5                  # 可省略，預設依字數估算
cover:
  motif: image                   # image / video / audio / agent / coding / fun
  palette: amber                  # amber / violet / cyan / indigo / lime / magenta
tool:
  name: "Nano Banana Pro"
  maker: "Google DeepMind"
  url: "https://blog.google/innovation-and-ai/products/nano-banana-pro/"
  type: "圖像生成與編輯模型"
  open_source: false             # true / false / unknown
  cost: "Gemini API 或訂閱方案計費"
sources:
  - label: "Google 官方部落格（2025-11-20）"
    url: "https://blog.google/innovation-and-ai/products/nano-banana-pro/"
highlights:
  - "3–4 條，每條 15–35 字，放具體數字或反直覺的事實"
extend:
  - "3 條延伸潛力，每條 20–40 字，屬推測者標「（推測）」"
---
```

| 欄位 | 必填 | 規則 |
| --- | --- | --- |
| `title` | ✔ | 20–34 字。有具體物件、能引起好奇，但不耍曖昧 |
| `summary` | ✔ | 40–70 字，一句話說清它是什麼＋為何有趣 |
| `category` | ✔ | 只能是 `config.yml` 既有分類 id |
| `tags` | ✔ | 2–4 個，中文為主，不要泛用詞（「AI」「工具」這種不要） |
| `date` | ✔ | `YYYY-MM-DD` |
| `cover.motif` / `palette` | ✔ | 決定自動生成的封面圖形狀與配色 |
| `tool.*` | ✔ | 工具資訊卡內容，至少要 name 與 url |
| `sources` | ✔ | 至少 3 條，其中至少 1 條一手來源（官方部落格／論文／官方文件／GitHub） |
| `highlights` | ✔ | 3–4 條，讀者只看這裡也能抓到重點 |
| `extend` | ✔ | 3 條延伸潛力，可合理外推但要標明是推測 |

正文規範：

- 長度 **450–700 字**（中文字計，建置時會檢查）。繁體中文（台灣用語），工具與模型名稱保留英文原文。
- 建議段落順序：一句話說它是什麼 → 它到底能做什麼 → 為什麼值得注意（放數字）→
  實際可以怎麼用 → 還沒被驗證的地方（誠實說限制）。
- 開頭第一段直接給最有趣的事實，不要鋪陳、不要「近年來 AI 快速發展」這種開場。
- 可用 `##` 小標、清單、粗體、引用區塊 `>`、標註框 `> [!TIP] 標題`、小表格、行內程式碼。
  **不要用 emoji。** 不要在正文重複 frontmatter 已有的標題或摘要。
- 篇幅不必求全：寧可只講兩件有趣的事，也不要為了塞滿欄位而稀釋重點。

**事實紀律（最重要）**

1. 每個數字、日期、名稱、功能都必須來自實際查證過的來源，並對應 `sources` 中的一條。
2. 標明數字是誰說的：官方自稱、論文自報、第三方評測，三者不可混用。沒有第三方複現的要寫明。
3. `sources` 的 URL 必須真的存在（用 `python tools/check_links.py` 驗）。
4. 查不到的事就不要寫。**絕對不可編造數字、日期、功能、價格或連結。**
5. 保留原始出處與體驗入口（`tool.url`），讓讀者能自己去看。

## 7. 新增一篇文章的 SOP

1. 在 `content/articles/` 新增 `<slug>.md`，依第 6 節與 `docs/writing-spec.md` 填寫。
2. 跑 `python tools/build.py`，確認零錯誤（警告也要看）。
3. 需要時跑 `python tools/check_links.py` 確認來源連結有效。
4. 打開 `site/index.html`、新文章頁與分類頁確認：卡片出現、封面生成、排序正確、
   375px 寬沒有橫向捲動。
5. 要精選就加 `featured: true` 與 `rank`。首頁、分類頁、相關文章會自動更新，**不需要改任何程式碼**。

## 8. 新增一個分類

在 `content/config.yml` 的 `categories` 加一筆（`id`／`name`／`desc`／`accent`／`motif`／`palette`），
分類頁會自動產生；記得為它寫至少一篇文章，否則那頁會是空狀態。

## 9. 命名與放置

- 文章：`content/articles/<slug>.md`，slug 全小寫、`-` 分隔、只用英數字（例：`zonos3-mini.md`）。
- 封面：由 `tools/covers.py` 依 `slug + motif + palette` 產生 `site/assets/covers/<slug>.svg`，
  不需要手動放圖。文章內要插圖時用 Markdown 圖片語法連到外部來源並標註出處。
- 模板：`templates/` 下 `base.html`（骨架）、`index.html`／`article.html`／`category.html`（頁面）、
  `_card_*.html`（卡片樣板）。卡片樣板以 `card` 為迴圈變數，一律寫成
  `{% for card in … %}{% include "_card_grid.html" %}{% endfor %}`。
- CSS／JS 放 `static/`，不要寫進模板或行內（除少量 `--c` 分類色注入）。
- 不留 `*.bak`、`*_old.py`、`test_*.py` 之類的檔案。

## 10. Agent 修改時的必守規則

- **先讀 `content/config.yml`、`docs/writing-spec.md` 與既有文章的真實格式再動手**，不要憑這份文件想像。
- 改 `tools/` 或 `templates/` 後，一定要重新建置並實際打開產物確認，不能只看程式碼。
- 一次改一個關注點（版面、樣式、內容分開改），不要順手重構無關的部分。
- 不引入任何新的執行期依賴（npm 套件、CDN 的 JS 函式庫、Python 第三方套件）；字型之外不連外網。
- 不刪除既有的來源標註、不為了版面好看而刪掉事實性內容、不編造數字。
- 大範圍改動前先把現況寫成說明（改了什麼、為什麼、影響哪些頁面），改完再對照驗證。

## 11. 已知限制

- 沒有搜尋、RSS、標籤頁、留言、會員：目前刻意不做（見第 1 節）。
- 字型依賴 Google Fonts；離線時退化為系統字型，版面不受影響。
- 封面圖是程式生成的抽象視覺，不宣稱代表工具本身。要放真實截圖時，放 `static/` 並在文章內以
  Markdown 引用，同時標註出處。
- 原始需求提到的 IG Reel 與 Bilibili 影片尚未收錄：建置環境無法取得其內容，
  需由使用者提供摘要或截圖後再寫。
