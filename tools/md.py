"""極簡 Markdown 渲染器（只用標準函式庫）。

支援：## 標題、段落、**粗體**、*斜體*、`行內程式`、~~刪除~~、[連結](url)、
![圖](url)、- / 1. 清單（可兩層縮排）、> 引用（含 > [!NOTE] 標註框）、
``` 程式碼區塊、| 表格 |、--- 分隔線、<開頭的行直接當原始 HTML。
"""

import html as _html
import re

LIST_RE = re.compile(r"^([-*+]|\d+[.)])\s+")
HEAD_RE = re.compile(r"^(#{1,4})\s+(.*)$")
HR_RE = re.compile(r"^(-{3,}|\*{3,})$")
SEP_RE = re.compile(r"^\|?[\s:\-|]+\|?$")
CALLOUT = {"NOTE": "note", "TIP": "tip", "WARN": "warn", "IMPORTANT": "warn"}


def esc(s):
    return _html.escape(s, quote=False)


def inline(text):
    """行內語法。先 escape HTML，再放回標記產生的 HTML。"""
    out = esc(text)
    out = re.sub(r"`([^`]+)`", lambda m: "<code>%s</code>" % m.group(1), out)
    out = re.sub(
        r"!\[([^\]]*)\]\(([^)\s]+)\)",
        lambda m: '<img src="%s" alt="%s" loading="lazy">' % (_attr(m.group(2)), _attr(m.group(1))),
        out,
    )
    out = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (_attr(m.group(2)), m.group(1)),
        out,
    )
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", out)
    return out


def _attr(s):
    return _html.escape(s, quote=True)


def _list_items(lines, i, base_indent):
    """收集清單項目，回傳 (items, next_i)。items = [(indent, ordered, text)]"""
    items = []
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped:
            if i + 1 < len(lines) and LIST_RE.match(lines[i + 1].strip()) and (
                len(lines[i + 1]) - len(lines[i + 1].lstrip(" "))
            ) >= base_indent:
                i += 1
                continue
            break
        indent = len(raw) - len(raw.lstrip(" "))
        m = LIST_RE.match(stripped)
        if m and indent <= base_indent and items and indent == base_indent:
            # 同縮排但清單類型改變（有序 ↔ 無序）→ 視為新的清單
            if m.group(1)[0].isdigit() != items[0][1]:
                break
        if m and indent <= base_indent + 2:
            items.append((indent, m.group(1)[0].isdigit(), stripped[m.end():]))
            i += 1
        elif items and indent > base_indent:
            items[-1] = (items[-1][0], items[-1][1], items[-1][2] + " " + stripped)
            i += 1
        else:
            break
    return items, i


def _build_list(items, pos=0, indent=None):
    if indent is None:
        indent = items[0][0]
    ordered = items[pos][1]
    out = ["<ol>" if ordered else "<ul>"]
    while pos < len(items):
        ind, is_ord, text = items[pos]
        if ind < indent:
            break
        if ind > indent:
            sub, pos = _build_list(items, pos, ind)
            out[-1] = out[-1][:-5] + sub + "</li>" if out[-1].endswith("</li>") else out[-1]
            continue
        out.append("<li>%s</li>" % inline(text))
        pos += 1
    out.append("</ol>" if ordered else "</ul>")
    html = "".join(out)
    return html.replace("</li><ol>", "<ol>").replace("</ol></li>", "</ol>"), pos


def _table(lines, i):
    header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
    i += 2
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        i += 1
    out = ['<div class="table-wrap"><table><thead><tr>']
    out += ["<th>%s</th>" % inline(c) for c in header]
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out), i


def _quote(buf):
    kind, title = None, None
    if buf and re.match(r"^\[!\w+\]", buf[0]):
        m = re.match(r"^\[!(\w+)\]\s*(.*)$", buf[0])
        kind = CALLOUT.get(m.group(1).upper(), "note")
        title = m.group(2).strip()
        buf = buf[1:]
    body = _blocks(buf)
    if kind:
        head = '<p class="callout-title">%s</p>' % inline(title) if title else ""
        return '<aside class="callout callout-%s">%s%s</aside>' % (kind, head, body)
    return "<blockquote>%s</blockquote>" % body


def _blocks(lines):
    out = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append(
                '<pre class="code-block"%s><code>%s</code></pre>'
                % (' data-lang="%s"' % _attr(lang) if lang else "", esc("\n".join(code)))
            )
            continue
        if HR_RE.match(s):
            out.append("<hr>")
            i += 1
            continue
        if s.startswith("<"):
            buf = []
            while i < len(lines) and lines[i].strip() and not LIST_RE.match(lines[i].strip()):
                buf.append(lines[i].strip())
                i += 1
            out.append("".join(buf))
            continue
        m = HEAD_RE.match(s)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (min(level + 1, 4), inline(m.group(2)), min(level + 1, 4)))
            i += 1
            continue
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(_quote(buf))
            continue
        if "|" in s and i + 1 < len(lines) and SEP_RE.match(lines[i + 1].strip()) and "-" in lines[i + 1]:
            html, i = _table(lines, i)
            out.append(html)
            continue
        if LIST_RE.match(s):
            items, i = _list_items(lines, i, len(lines[i]) - len(lines[i].lstrip(" ")))
            html, _ = _build_list(items)
            out.append(html)
            continue
        buf = [s]
        i += 1
        while i < len(lines) and lines[i].strip():
            nxt = lines[i].strip()
            if HEAD_RE.match(nxt) or LIST_RE.match(nxt) or nxt.startswith((">", "```", "|", "<")) or HR_RE.match(nxt):
                break
            buf.append(nxt)
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(buf)))
    return "".join(out)


def render(text):
    return _blocks(text.replace("\r\n", "\n").split("\n"))


def strip_markdown(text):
    """給計算字數／摘要用：移除標記後回傳純文字。"""
    t = re.sub(r"```.*?```", " ", text, flags=re.S)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[#>*`|_~-]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()
