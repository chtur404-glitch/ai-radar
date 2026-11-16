#!/usr/bin/env python3
"""AI Radar 建置程式：content/ + templates/ + static/  →  site/

用法：python tools/build.py
只用 Python 標準函式庫。有問題會印出清楚的錯誤並以非 0 結束。
"""

import datetime
import os
import re
import shutil
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True  # 不在 tools/ 留下 __pycache__

import covers  # noqa: E402
import md  # noqa: E402
import template  # noqa: E402
import yamlish  # noqa: E402

CONTENT = os.path.join(ROOT, "content")
ARTICLES = os.path.join(CONTENT, "articles")
TEMPLATES = os.path.join(ROOT, "templates")
STATIC = os.path.join(ROOT, "static")
OUT = os.path.join(ROOT, "site")

MOTIFS = set(covers.ART)
PALETTES = set(covers.PALETTES)
ERRORS, WARNS = [], []
TPLS = {}


def host_of(url):
    return re.sub(r"^www\.", "", urlparse(url).netloc)


CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’._@/+&-]*")


def count_chars(text):
    """中文字數：中日韓字元各算 1，英數詞彙各算 1（避免英文縮寫被高估）。"""
    return len(CJK.findall(text)) + len(LATIN.findall(text))


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNS.append(msg)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def split_front(text, src):
    if not text.startswith("---"):
        err("%s：檔案開頭缺少 frontmatter（---）" % src)
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        err("%s：frontmatter 沒有結束的 ---" % src)
        return {}, text
    head = text[3:end]
    body = text[text.find("\n", end + 1) + 1:]
    try:
        data = yamlish.loads(head)
    except yamlish.YamlError as exc:
        err("%s：frontmatter 解析失敗 → %s" % (src, exc))
        return {}, body
    return data, body


def date_display(value):
    return "%d 年 %d 月 %d 日" % (value.year, value.month, value.day)


class Article:
    def __init__(self, path, fm, body, cats):
        src = os.path.basename(path)
        self.file = src
        self.slug = str(fm.get("slug") or os.path.splitext(src)[0])
        self.title = str(fm.get("title") or "").strip()
        self.summary = str(fm.get("summary") or "").strip()
        self.category = str(fm.get("category") or "").strip()
        self.tags = [str(t) for t in (fm.get("tags") or [])]
        self.body_md = body.strip()
        self.body_html = md.render(self.body_md)
        self.plain = md.strip_markdown(self.body_md)
        self.chars = count_chars(self.plain)
        self.raw = fm

        raw_date = fm.get("date")
        self.date = None
        if isinstance(raw_date, datetime.date):
            self.date = raw_date
        else:
            try:
                self.date = datetime.datetime.strptime(str(raw_date), "%Y-%m-%d").date()
            except ValueError:
                err("%s：date 必須是 YYYY-MM-DD，目前是 %r" % (src, raw_date))
        self.updated = None
        if fm.get("updated"):
            try:
                self.updated = datetime.datetime.strptime(str(fm["updated"]), "%Y-%m-%d").date()
            except ValueError:
                warn("%s：updated 格式不是 YYYY-MM-DD，已忽略" % src)

        self.reading_time = fm.get("reading_time") or max(1, round(self.chars / 450))
        self.featured = bool(fm.get("featured"))
        self.rank = fm.get("rank") or 99

        cover = fm.get("cover") or {}
        self.motif = str(cover.get("motif") or cats.get(self.category, {}).get("motif", "image"))
        self.palette = str(cover.get("palette") or cats.get(self.category, {}).get("palette", "cyan"))

        tool = fm.get("tool") or {}
        self.tool = {
            "name": str(tool.get("name") or "").strip(),
            "maker": str(tool.get("maker") or "").strip(),
            "url": str(tool.get("url") or "").strip(),
            "type": str(tool.get("type") or "").strip(),
            "cost": str(tool.get("cost") or "").strip(),
            "open_source": tool.get("open_source"),
        }
        self.sources = []
        for item in fm.get("sources") or []:
            if isinstance(item, dict) and item.get("url"):
                url = str(item["url"])
                self.sources.append({"label": str(item.get("label") or url), "url": url, "host": host_of(url)})
            else:
                warn("%s：sources 有一筆格式不對（需要 label/url）→ %r" % (src, item))
        self.highlights = [str(h) for h in (fm.get("highlights") or [])]
        self.extend = [str(x) for x in (fm.get("extend") or [])]
        self.validate(cats)

    def validate(self, cats):
        src = self.file
        if not self.title:
            err("%s：缺少 title" % src)
        elif not 6 <= len(self.title) <= 44:
            warn("%s：title 長度 %d 字，建議 20–34 字" % (src, len(self.title)))
        if not self.summary:
            err("%s：缺少 summary" % src)
        else:
            n = count_chars(self.summary)
            if n < 30:
                warn("%s：summary 只有 %d 字（中文字計），建議 40–70 字" % (src, n))
            elif n > 85:
                warn("%s：summary %d 字（中文字計），建議 40–70 字，考慮精簡" % (src, n))
        if self.category not in cats:
            err("%s：category %r 不在 content/config.yml 的分類清單中" % (src, self.category))
        if not self.tags:
            warn("%s：沒有 tags" % src)
        if self.date is None:
            pass
        if self.motif not in MOTIFS:
            err("%s：cover.motif %r 不合法（可用：%s）" % (src, self.motif, ", ".join(sorted(MOTIFS))))
        if self.palette not in PALETTES:
            err("%s：cover.palette %r 不合法（可用：%s）" % (src, self.palette, ", ".join(sorted(PALETTES))))
        if not self.tool["name"]:
            err("%s：缺少 tool.name" % src)
        if not self.tool["url"].startswith("http"):
            err("%s：tool.url 必須是 http(s) 連結" % src)
        if len(self.sources) < 1:
            err("%s：至少要有一個 sources 條目" % src)
        elif len(self.sources) < 3:
            warn("%s：sources 只有 %d 條，規範建議至少 3 條（含 1 條一手來源）" % (src, len(self.sources)))
        for item in self.sources:
            if not item["url"].startswith("http"):
                err("%s：sources 的 url 不合法 → %r" % (src, item["url"]))
        if len(self.highlights) < 3:
            warn("%s：highlights 只有 %d 條，建議 3–4 條" % (src, len(self.highlights)))
        if len(self.extend) < 1:
            err("%s：缺少 extend" % src)
        elif len(self.extend) < 3:
            warn("%s：extend 只有 %d 條，建議 3 條" % (src, len(self.extend)))
        if self.chars < 400:
            warn("%s：正文只有 %d 字（中文字計），規範建議 450–700 字" % (src, self.chars))
        elif self.chars > 800:
            warn("%s：正文 %d 字（中文字計），規範建議 450–700 字，考慮精簡" % (src, self.chars))

    @property
    def open_source_label(self):
        v = self.tool["open_source"]
        if v is True:
            return "開源"
        if v is False:
            return "非開源"
        return "未標明"

    @property
    def open_source_true(self):
        return self.tool["open_source"] is True


def load_articles(cats):
    out = []
    if not os.path.isdir(ARTICLES):
        err("找不到 content/articles/ 目錄")
        return out
    for name in sorted(os.listdir(ARTICLES)):
        if not name.endswith(".md") or name.startswith("_"):
            continue
        path = os.path.join(ARTICLES, name)
        fm, body = split_front(read(path), name)
        if not fm:
            continue
        out.append(Article(path, fm, body, cats))
    seen = {}
    for a in out:
        if a.slug in seen:
            err("slug 重複：%s 與 %s 都用了 %r" % (seen[a.slug].file, a.file, a.slug))
        seen[a.slug] = a
    out.sort(key=lambda a: (a.date or datetime.date(1970, 1, 1)), reverse=True)
    return out


def make_card(a, root, big=False):
    return {
        "url": root + "articles/%s.html" % a.slug,
        "title": a.title,
        "summary": a.summary,
        "cover": root + "assets/covers/%s.svg" % a.slug,
        "accent": a.accent,
        "category_name": a.category_name,
        "category_url": root + "categories/%s.html" % a.category,
        "motif": a.motif,
        "date": date_display(a.date) if a.date else "",
        "date_iso": a.date.isoformat() if a.date else "",
        "reading_time": a.reading_time,
        "tool_name": a.tool["name"],
        "open_source_label": a.open_source_label,
        "tags": [{"name": t} for t in a.tags],
        "big": big,
    }


def base_ctx(cfg, cats, root, page):
    return {
        "site": cfg["site"],
        "root": root,
        "page": page,
        "nav": [
            {"name": "首頁", "url": root + "index.html", "active": page["kind"] == "home"},
            {"name": "精選", "url": root + "index.html#featured", "active": False},
            {"name": "最新發現", "url": root + "index.html#latest", "active": False},
            {"name": "分類", "url": root + "index.html#categories", "active": False},
        ],
        "footer_categories": [
            {"name": c["name"], "url": root + "categories/%s.html" % c["id"], "count": c["count"]} for c in cats.values()
        ],
        "year": datetime.date.today().year,
    }


def render(tpl, ctx):
    ctx["__templates__"] = TPLS
    return template.render(tpl, ctx)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    cfg = yamlish.load(os.path.join(CONTENT, "config.yml"))
    site = cfg["site"]
    cats = {}
    for c in cfg["categories"]:
        cats[str(c["id"])] = {
            "id": str(c["id"]),
            "name": str(c["name"]),
            "desc": str(c.get("desc") or ""),
            "accent": str(c.get("accent") or "#4fe3c1"),
            "motif": str(c.get("motif") or "image"),
            "palette": str(c.get("palette") or "cyan"),
            "count": 0,
        }
    if not cats:
        err("content/config.yml 沒有定義任何分類")
        report()
        return 1

    arts = load_articles(cats)
    by_cat = {cid: [] for cid in cats}
    for a in arts:
        if a.category in cats:
            cats[a.category]["count"] += 1
            by_cat[a.category].append(a)
        a.category_name = cats.get(a.category, {}).get("name", a.category)
        a.accent = cats.get(a.category, {}).get("accent", "#4fe3c1")
        a.category_url = "categories/%s.html" % a.category

    tpls = {name: read(os.path.join(TEMPLATES, name)) for name in os.listdir(TEMPLATES) if name.endswith(".html")}
    TPLS.update(tpls)

    # ---- 輸出目錄
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(STATIC, os.path.join(OUT, "assets"))
    cover_dir = os.path.join(OUT, "assets", "covers")
    for a in arts:
        covers.write_cover(cover_dir, a.slug, a.motif, a.palette)

    featured = sorted([a for a in arts if a.featured], key=lambda a: (a.rank, a.date or datetime.date(1970, 1, 1)))
    if not featured:
        warn("沒有任何文章設 featured: true，首頁精選區會是空的")
    featured_slugs = {a.slug for a in featured}
    rest = [a for a in arts if a.slug not in featured_slugs]

    # ---- 首頁
    ctx = base_ctx(cfg, cats, "", {"kind": "home", "title": "%s — %s" % (site["name"], site["tagline"]),
                                   "desc": site["description"], "og_type": "website",
                                   "og_image": "assets/covers/%s.svg" % (arts[0].slug if arts else "none")})
    ctx.update({
        "stats": {"articles": len(arts), "categories": len([c for c in cats.values() if c["count"]]),
                  "latest": date_display(arts[0].date) if arts else "—"},
        "card": make_card(featured[0], "", True) if featured else None,
        "featured_main": make_card(featured[0], "", True) if featured else None,
        "featured_side": [make_card(a, "") for a in featured[1:4]],
        "latest": [make_card(a, "") for a in rest[:9]],
        "category_tiles": [
            dict(c, url="categories/%s.html" % c["id"], latest=date_display(by_cat[c["id"]][0].date) if by_cat[c["id"]] else "尚無文章")
            for c in cats.values()
        ],
        "featured_all": [make_card(a, "") for a in featured],
    })
    body = render(tpls["index.html"], ctx)
    ctx["content"] = body
    write(os.path.join(OUT, "index.html"), render(tpls["base.html"], ctx))

    # ---- 文章頁
    for a in arts:
        cards = [make_card(x, "../") for x in arts if x.category == a.category and x.slug != a.slug][:3]
        ctx = base_ctx(cfg, cats, "../", {"kind": "article", "title": "%s — %s" % (a.title, site["name"]),
                                          "desc": a.summary, "og_type": "article",
                                          "og_image": "../assets/covers/%s.svg" % a.slug})
        ctx["article"] = {
            "title": a.title, "summary": a.summary, "body": a.body_html,
            "cover": "../assets/covers/%s.svg" % a.slug,
            "date_iso": a.date.isoformat() if a.date else "",
            "date": date_display(a.date) if a.date else "",
            "updated": date_display(a.updated) if a.updated else "",
            "reading_time": a.reading_time,
            "tags": [{"name": t} for t in a.tags],
            "category_name": a.category_name,
            "category_url": "../categories/%s.html" % a.category,
            "accent": a.accent,
            "tool": dict(a.tool, open_source_label=a.open_source_label, is_open=a.open_source_true),
            "sources": a.sources,
            "highlights": [{"text": h} for h in a.highlights],
            "extend": [{"text": e} for e in a.extend],
            "plain_url": a.tool["url"],
        }
        ctx["related"] = cards
        ctx["related_title"] = "同分類的其他訊號"
        body = render(tpls["article.html"], ctx)
        ctx["content"] = body
        write(os.path.join(OUT, "articles", "%s.html" % a.slug), render(tpls["base.html"], ctx))

    # ---- 分類頁
    for cid, cat in cats.items():
        items = by_cat[cid]
        ctx = base_ctx(cfg, cats, "../", {"kind": "category", "title": "%s — %s" % (cat["name"], site["name"]),
                                          "desc": cat["desc"], "og_type": "website",
                                          "og_image": "../assets/covers/%s.svg" % items[0].slug if items else "../assets/favicon.svg"})
        ctx["category"] = dict(cat, url="../categories/%s.html" % cid)
        ctx["articles"] = [make_card(a, "../") for a in items]
        ctx["others"] = [dict(c, url="../categories/%s.html" % c["id"]) for k, c in cats.items() if k != cid]
        body = render(tpls["category.html"], ctx)
        ctx["content"] = body
        write(os.path.join(OUT, "categories", "%s.html" % cid), render(tpls["base.html"], ctx))

    print("建置完成 → %s" % OUT)
    print("  文章 %d 篇、分類 %d 個、封面 %d 張" % (len(arts), len(cats), len(arts)))
    for a in arts:
        print("  · %-22s %s  %d 字" % (a.slug, a.category, a.chars))
    report()
    return 1 if ERRORS else 0


def report():
    for w in WARNS:
        print("  ⚠ %s" % w)
    for e in ERRORS:
        print("  ✗ %s" % e, file=sys.stderr)
    if ERRORS:
        print("\n建置失敗：%d 個錯誤必須修正。" % len(ERRORS), file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
