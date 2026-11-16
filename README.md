# AI Radar

把有趣的 AI 放到你的雷達上。一個純靜態的繁體中文 AI 工具與技術介紹網站：
每篇文章只講一件事，目標是讓讀者想自己去玩，而不是讀完一份規格書。

## 快速開始

```bash
python tools/build.py             # 建置：content/ + templates/ + static/ → site/
python -m http.server -d site     # 本機預覽 http://localhost:8000
python tools/check_links.py       # 檢查每篇文章的來源連結是否還活著
```

也可以直接雙擊 `site/index.html`，不需要伺服器。

## 目錄結構

| 路徑 | 角色 |
| --- | --- |
| `content/config.yml` | 站名、標語、分類定義（六個分類與各自的強調色） |
| `content/articles/*.md` | **文章本體，一檔一篇。新增內容只需要動這裡。** |
| `templates/*.html` | 頁面骨架（首頁、文章頁、分類頁與卡片樣板） |
| `static/css`, `static/js` | 手寫樣式與少量互動（零依賴） |
| `tools/*.py` | 建置程式：`build.py`、`covers.py`（產生 SVG 封面）、`md.py`、`template.py`、`yamlish.py`、`check_links.py` |
| `site/` | **建置產物，不要手改**，每次建置都會重建 |
| `docs/writing-spec.md` | 文章格式、語氣與事實紀律的完整規範 |

## 新增一篇文章

1. 在 `content/articles/` 新增 `my-tool.md`，依 `docs/writing-spec.md` 填 frontmatter 與正文。
2. `python tools/build.py`（封面圖會自動生成，不需要準備圖片）。
3. 打開 `site/index.html` 確認卡片出現、順序正確。

要精選就加 `featured: true` 與 `rank: 1`。首頁、分類頁、相關文章都會自動更新。
新增分類則在 `content/config.yml` 的 `categories` 加一筆（`id`／`name`／`desc`／`accent`／`motif`／`palette`）。

## 部署

`site/` 就是完整網站，把整個目錄丟到 Netlify、Cloudflare Pages，或用 `python -m http.server -d site`
在區網分享都可以。沒有後端、沒有資料庫、沒有常駐服務。

### GitHub Pages（推薦）

本專案附了 `.github/workflows/pages.yml`：**push 到 `main` 就會自動跑 `python tools/build.py` 並發佈 `site/`**，
所以新增文章只要 commit 一個 `.md`，線上網站會自己更新。

1. 建立 repo 並推上去：
   ```bash
   git init && git add -A && git commit -m "feat: AI Radar 網站與專案規範"
   git branch -M main
   git remote add origin https://github.com/<你的帳號>/ai-radar.git
   git push -u origin main
   ```
2. repo → **Settings → Pages → Source 選「GitHub Actions」**。
3. 回到 **Actions** 分頁看 workflow 跑完，網址會是 `https://<你的帳號>.github.io/ai-radar/`。

不想用 Actions 也可以改成傳統做法：把 `site/` 的內容推到 `gh-pages` 分支，
Pages 的 Source 選該分支的 `/`（根目錄）即可；`site/` 預設也會一起被 commit，方便直接檢視產物。

## 環境需求

Python 3.9+（只用標準函式庫，不需 pip install）。字型從 Google Fonts 載入，
連不上時自動退回系統字型，版面仍然正常。

建置程式已設定 `sys.dont_write_bytecode`，所以不會在 `tools/` 裡留下 `__pycache__`。
