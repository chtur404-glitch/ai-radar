"""極簡模板引擎（只用標準函式庫）。

支援語法：
    {{ path.to.value }}     變數（預設 HTML escape，加 |raw 可輸出原始 HTML）
    {% for x in items %}…{% endfor %}      迴圈，附 loop.index / loop.first / loop.last
    {% if expr %}…{% else %}…{% endif %}   條件（支援 not、真值判斷）
    {% include "name.html" %}?            不支援，請用 build.py 組合
註解：{# … #}
"""

import html
import re

TOKEN = re.compile(r"\{\{\s*(.*?)\s*\}\}|\{%\s*(.*?)\s*%\}|\{#.*?#\}", re.S)
FOR = re.compile(r"^for\s+(\w+)\s+in\s+([\w.]+)$")
IF = re.compile(r"^if\s+(not\s+)?([\w.]+)$")


class TemplateError(Exception):
    pass


def _tokenize(text):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            out.append(("text", text[pos:m.start()]))
        if m.group(1) is not None:
            out.append(("var", m.group(1)))
        elif m.group(2) is not None:
            out.append(("tag", m.group(2)))
        pos = m.end()
    if pos < len(text):
        out.append(("text", text[pos:]))
    return out


def _parse(tokens, i=0, stop=()):
    nodes = []
    while i < len(tokens):
        kind, val = tokens[i]
        if kind != "tag":
            nodes.append((kind, val))
            i += 1
            continue
        head = val.split()[0] if val.split() else ""
        if head in stop:
            return nodes, i
        if head == "for":
            m = FOR.match(val)
            if not m:
                raise TemplateError("bad for tag: {%% %s %%}" % val)
            body, i = _parse(tokens, i + 1, ("endfor",))
            nodes.append(("for", m.group(1), m.group(2), body))
            i += 1
        elif head == "if":
            m = IF.match(val)
            if not m:
                raise TemplateError("bad if tag: {%% %s %%}" % val)
            body, i = _parse(tokens, i + 1, ("else", "endif"))
            alt = []
            if tokens[i][1].split()[0] == "else":
                alt, i = _parse(tokens, i + 1, ("endif",))
            nodes.append(("if", bool(m.group(1)), m.group(2), body, alt))
            i += 1
        elif head == "include":
            m = re.match(r'^include\s+"([\w./\-]+)"$', val)
            if not m:
                raise TemplateError('bad include tag: {%% %s %%}' % val)
            nodes.append(("include", m.group(1)))
            i += 1
        else:
            raise TemplateError("unexpected tag: {%% %s %%}" % val)
    if stop:
        raise TemplateError("missing {%% %s %%}" % stop[0])
    return nodes, i


def _lookup(stack, path):
    parts = path.split(".")
    for scope in reversed(stack):
        if parts[0] in scope:
            cur = scope[parts[0]]
            for p in parts[1:]:
                if isinstance(cur, dict):
                    cur = cur.get(p, "")
                else:
                    cur = getattr(cur, p, "")
            return cur
    return ""


def _render(nodes, stack):
    out = []
    for node in nodes:
        if node[0] == "text":
            out.append(node[1])
        elif node[0] == "var":
            expr = node[1]
            raw = expr.endswith("|raw")
            if raw:
                expr = expr[:-4].strip()
            val = _lookup(stack, expr)
            if val is None:
                val = ""
            out.append(str(val) if raw else html.escape(str(val), quote=True))
        elif node[0] == "for":
            _, var, path, body = node
            items = _lookup(stack, path) or []
            n = len(items)
            for idx, item in enumerate(items):
                loop = {"index": idx + 1, "first": idx == 0, "last": idx == n - 1}
                stack.append({var: item, "loop": loop})
                out.append(_render(body, stack))
                stack.pop()
        elif node[0] == "include":
            lib = _lookup(stack, "__templates__") or {}
            src = lib.get(node[1])
            if src is None:
                raise TemplateError("include 找不到模板：%s" % node[1])
            key = "\x00inc:" + node[1]
            if key not in _cache:
                _cache[key], _ = _parse(_tokenize(src))
            out.append(_render(_cache[key], stack))
        elif node[0] == "if":
            _, negate, path, body, alt = node
            truthy = bool(_lookup(stack, path))
            if negate:
                truthy = not truthy
            out.append(_render(body if truthy else alt, stack))
    return "".join(out)


_cache = {}


def render(text, context):
    """把模板字串套用 context（dict）後回傳 HTML 字串。"""
    nodes, _ = _parse(_tokenize(text))
    return _render(nodes, [context])
