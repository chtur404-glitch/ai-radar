# AI Radar 專案規範（完整版）

這份文件是專案的規範來源。`AGENTS.md` 是它的入口摘要；文章格式與語氣細節見 `docs/writing-spec.md`，
操作步驟見 `README.md`。**新增文章只需要動 `content/`，不需要改任何程式碼或 HTML。**

## 1. 專案目的

繁體中文（台灣用語）的 AI 工具與技術介紹網站。題材包含 AI 工具、模型、技術與應用
（圖像、影片、語音、音樂、程式開發、AI Agent、遊戲、世界模型…），
來源可為官方部落格、論文、GitHub、YouTube／Bilibili／Instagram、Reddit、官方文件。

- **唯一最重要的目標：讓讀者產生興趣**，讀完覺得「這東西真有意思，我想去玩玩看」。
- 明確不是：完整教學、工具資料庫、評測排行、新聞快訊。
- 判斷標準：寫完像產品說明書或維基條目，就是寫壞了。

## 2. 技術棧與檔案結構

純靜態 HTML/CSS/JS ＋ Python 標準函式庫建置腳本。沒有 npm、沒有框架、沒有執行期依賴
（唯一的外部請求是 Google Fonts，失敗時退回系統字型）。

```
aI_radar/
├─ README.md              操作說明（建置、預覽、部署）
├─ AGENTS.md              規範入口
├─ docs/
│  ├─ project-spec.md     本檔：完整規範
│  └─ writing-spec.md     文章格式、語氣、事實紀律
├─ content/               【唯一需要人工編輯的地方】
│  ├─ config.yml          站名、標語、六個分類定義
│  └─ articles/*.md       文章，一檔一篇
├─ templates/             頁面骨架：base / index / article / category + _card_*.html 樣板
├─ static/                css(base, components, pages)、js/main.js、favicon.svg
├─ tools/                 build.py、covers.py、md.py、template.py、yamlish.py、check_links.py
└─ site/                  【產物，不要手改】每次建置整批重建
   ├─ index.html
   ├─ articles/<slug>.html
   ├─ categories/<id>.html
   └─ assets/{css,js,covers,favicon.svg}
```

**來源 vs 產物**：改內容 → `content/`；改版面 → `templates/`；改樣式 → `static/`。
`site/` 的一切都是產物，任何手改都會被下一次建置覆蓋。專案內不留備份檔、實驗檔、暫存檔
（沒有版本控制，唯一還原方式是重新建置）。

## 3. 建置與驗證

```bash
python tools/build.py          # content + templates + static → site/
python -m http.server -d site  # 預覽
python tools/check_links.py    # 檢查文章內的 tool.url 與 sources 是否活著
```

- 建置必須幂等：同樣來源跑兩次得到完全相同的輸出（封面圖由 slug 決定，不含隨機成分）。
- frontmatter 有問題時（缺 title/summary、category 不存在、date 格式錯、motif/palette 不在清單內、
  沒有 sources、tool.url 不是 http）必須報錯並以非 0 結束，不可靜默產生壞頁面。
- 長度類問題（標題過長、摘要過長、正文過短）只警告，不中斷建置。
- 交付前必須實際打開產物確認，不能只看程式碼。`site/index.html` 直接雙擊就要能瀏覽
  （所有連結為相對路徑，不依賴 fetch，不依賴伺服器）。

## 4. 視覺設計規範

### 4.1 氣質
深色、精密、克制的科技感，像儀器面板而不是電競周邊。不堆裝飾：每個動畫、每條漸層都要有理由。
優先照顧閱讀體驗與視覺一致性。

### 4.2 色彩（`static/css/base.css` 的 `:root`）

| 變數 | 值 | 用途 |
| --- | --- | --- |
| `--bg` | `#06070a` | 頁面底色 |
| `--surface` / `--surface-2` | `#10131a` / `#161a23` | 卡片面板／hover |
| `--line` / `--line-strong` | `rgba(255,255,255,.08)` / `.16` | 邊框 |
| `--text` / `--text-dim` / `--text-mute` | `#e8ecf4` / `#a2abbb` / `#6f7889` | 主／次／標籤文字 |
| `--accent` / `--accent-2` | `#4fe3c1` / `#7d8bff` | 主／次強調色 |

分類各有強調色，定義在 `content/config.yml`，只用於該分類的標籤、線條與封面：
agent `#7d8bff`｜coding `#7ee787`｜image `#ffb35c`｜video `#c58bff`｜audio `#4fe3c1`｜fun `#ff7ac6`。
卡片與面板用 `style="--c: …"` 把分類色注入區域變數，CSS 以 `var(--c, var(--accent))` 取用。

深色是唯一主題，不做淺色模式。內文對比維持 WCAG AA 以上。

### 4.3 字體與排版
`--font-sans`：Inter → Noto Sans TC → 系統字型；`--font-mono`：JetBrains Mono → Consolas。
英文、數字、kicker 標籤、日期、來源網域一律用 mono，這是科技感的主要來源。
內文 `1.0625rem`／行高 `1.85`；正文最大寬 `720px`；標題 `clamp()` 隨視窗縮放、字距 -.02em 起跳。

### 4.4 元件與間距
容器最大寬 `1180px`，左右留白 `clamp(20px, 5vw, 40px)`。圓角：卡片 14px、面板 10–12px、膠囊 999px。
間距只用 4/8/12/16/24/32/48/64/96。卡片 hover 上浮 4px 並讓邊框轉為分類色（`color-mix`）。
封面圖固定 `aspect-ratio: 16/10`，由 `tools/covers.py` 產生 SVG，不依賴外部圖片。

### 4.5 動態
一律 `cubic-bezier(.22,.61,.36,1)`、180–420ms。進場用 `IntersectionObserver` 加 `.is-visible`，
同容器每張卡片錯開 60ms、只播一次。首頁主視覺是純 CSS 雷達（conic-gradient 掃描＋同心圓＋光點脈動）。
**必須**尊重 `prefers-reduced-motion: reduce`（關閉位移與循環動畫）。

### 4.6 響應式
斷點 1024 / 768 / 560。手機版導覽收成漢堡選單。任何寬度都不可出現橫向捲動
（用 `document.documentElement.scrollWidth === clientWidth` 驗證，勿只看截圖）。

## 5. 頁面結構

全站只有三種頁面，共用置頂導覽（品牌＋首頁／精選／最新發現／分類）與頁尾（品牌、分類清單、
來源聲明、年份）。

1. **首頁 `index.html`**：主視覺（雷達＋標語＋CTA＋統計）→ 精選內容（`rank` 最小者為大卡）→
   最新發現（日期新到舊，最多 9 篇）→ 主題分類（六個磁磚，附文章數與最新日期）→ 頁尾。
2. **文章頁 `articles/<slug>.html`**：麵包屑 → 分類標籤 → 標題 → 摘要 → 日期／閱讀時間 → 標籤 →
   大封面 → 重點速覽 → 正文（Markdown）→ 延伸潛力 → 原始來源 → 同分類其他文章 → 頁尾；
   右側欄（桌機 sticky）放工具資訊卡與「數據以官方頁面為準」的提醒。
3. **分類頁 `categories/<id>.html`**：分類名稱／說明／篇數 → 卡片網格 →
   其他分類磁磚 → 頁尾。沒有文章時顯示「雷達還在掃描中」空狀態，不可空白或報錯。

## 6. 內容格式

文章放 `content/articles/<slug>.md`：開頭是 frontmatter（`---` 包住，mini-YAML：
純量、`[a, b]` 內聯陣列、`- ` 區塊陣列、兩層縮排 map），後面是 Markdown 正文。
**欄位定義、正文規範、事實紀律與語氣範例見 `docs/writing-spec.md`，寫作前必須先讀。**

摘要：`title` 20–34 字、`summary` 40–70 字、正文 450–700 字（中文字計，建置時自動檢查並警告）。
`tool.*` 至少要 name 與 url；`sources` 至少 3 條且至少 1 條一手來源；`highlights` 3–4 條；
`extend` 3 條，屬推測的要標「（推測）」。

## 7. 新增文章 SOP

1. 在 `content/articles/` 新增 `<slug>.md`，依 `docs/writing-spec.md` 撰寫。
2. 跑 `python tools/build.py`，確認零錯誤。
3. 需要時跑 `python tools/check_links.py` 確認來源連結有效。
4. 打開 `site/index.html`、新的文章頁與分類頁確認：卡片出現、封面生成、排序正確、
   375px 寬沒有橫向捲動。
5. 要精選加 `featured: true` 與 `rank`。首頁、分類頁、相關文章會自動更新，**不需改程式碼**。

新增分類：在 `content/config.yml` 的 `categories` 加一筆（`id`／`name`／`desc`／`accent`／`motif`／`palette`），
分類頁會自動產生。

## 8. 命名與放置

- 文章：`content/articles/<slug>.md`，slug 全小寫、`-` 分隔、只用英數字。
- 封面：由 `tools/covers.py` 依 `slug + motif + palette` 產生 `site/assets/covers/<slug>.svg`，
  不需要手動放圖；文章內要插圖時用 Markdown 連到外部來源並標註出處。
- 模板：`templates/` 下 `base.html`（骨架）、`index.html`／`article.html`／`category.html`（頁面）、
  `_card_*.html`（卡片樣板）。卡片樣板以 `card` 為迴圈變數，迴圈一律寫
  `{% for card in … %}{% include "_card_grid.html" %}{% endfor %}`。
- CSS／JS 放 `static/`，不要寫進行內或模板（除少量 `--c` 分類色注入）。

## 9. Agent 修改時的必守規則

- 先讀 `content/config.yml`、`docs/writing-spec.md` 與既有文章的真實格式再動手，不要憑文件想像。
- 改動 `tools/` 或 `templates/` 後一定要重新建置並實際開啟產物確認。
- 一次只改一個關注點（版面／樣式／內容分開），不要順手重構無關部分。
- 不新增任何執行期依賴（npm、CDN JS 函式庫、Python 第三方套件）；字型之外不連外網。
- 不刪除來源標註、不為了版面刪掉事實性內容、不編造數字。
- 大範圍改動前先寫下「改了什麼、為什麼、影響哪些頁面」，改完對照驗證。

## 10. 已知限制與待辦

- 沒有搜尋、RSS、標籤頁、留言、會員：目前刻意不做（見第 1 節）。
- 字型依賴 Google Fonts；離線時外觀會退化為系統字型（版面不受影響）。
- 空分類頁已實作並驗證過，但上線時六個分類都各有文章。
- 專案原始需求提到的 IG Reel 與 Bilibili 影片尚未收錄：建置環境無法取得其內容
  （無瀏覽器後端、web_extract 後端僅支援搜尋、B 站 API 回 412），需由使用者提供摘要或截圖後再寫。
- 封面圖是程式生成的抽象視覺，不宣稱代表工具本身；如要放真實截圖，放在 `static/` 並在
  frontmatter 之外以 Markdown 圖片語法引用，同時標註出處。
