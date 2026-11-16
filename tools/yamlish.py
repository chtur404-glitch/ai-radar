"""迷你 YAML 子集解析器（只用標準函式庫，不依賴 PyYAML）。

支援：
    key: value                  純量（字串／整數／浮點／true/false/null）
    key: "字串"                 引號字串（可用 \\" 轉義）
    key: [a, b, c]              內聯陣列
    key:                        兩層縮排 map
      child: value
    key:                        區塊陣列（純量或 map）
      - item
      - name: value
        other: value
整行以 # 開頭視為註解。多行字串、錨點、>3 層巢狀不支援。
"""

import re

INT = re.compile(r"^-?\d+$")
FLOAT = re.compile(r"^-?\d+\.\d+$")


class YamlError(Exception):
    pass


def _split_inline(s):
    parts, buf, quote, depth = [], [], "", 0
    for ch in s:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch in "[{":
            depth += 1
            buf.append(ch)
        elif ch in "]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if "".join(buf).strip():
        parts.append("".join(buf))
    return [p.strip() for p in parts]


def scalar(s):
    s = s.strip()
    if s == "":
        return None
    if s[0] in "\"'":
        q = s[0]
        if len(s) >= 2 and s.endswith(q):
            inner = s[1:-1]
            return inner.replace('\\"', '"').replace("\\\\", "\\") if q == '"' else inner
        return s[1:]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [scalar(x) for x in _split_inline(inner)]
    low = s.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~"):
        return None
    if INT.match(s):
        return int(s)
    if FLOAT.match(s):
        return float(s)
    return s


def _lines(text):
    out = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        out.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    return out


def _parse_block(lines, i, indent):
    if i >= len(lines):
        return {}, i
    if lines[i][1].startswith("- "):
        items = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
            rest = lines[i][1][2:].strip()
            i += 1
            block = []
            while i < len(lines) and lines[i][0] > indent:
                block.append(lines[i])
                i += 1
            if ":" in rest and not rest.startswith(("http", "\"")):
                sub = [(indent + 2, rest)] + block
                val, _ = _parse_block(sub, 0, indent + 2)
                items.append(val)
            elif block:
                raise YamlError("列表項混用純量與縮排內容：%r" % rest)
            else:
                items.append(scalar(rest))
        return items, i
    data = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
        line = lines[i][1]
        i += 1
        key, sep, rest = line.partition(":")
        if not sep:
            raise YamlError("這行不是 key: value → %r" % line)
        key = key.strip()
        rest = rest.strip()
        if rest:
            data[key] = scalar(rest)
        else:
            block = []
            while i < len(lines) and lines[i][0] > indent:
                block.append(lines[i])
                i += 1
            if not block:
                data[key] = None
            else:
                data[key], _ = _parse_block(block, 0, block[0][0])
    return data, i


def loads(text):
    """把 YAML 子集字串解析成 dict。"""
    lines = _lines(text)
    if not lines:
        return {}
    data, _ = _parse_block(lines, 0, lines[0][0])
    if not isinstance(data, dict):
        raise YamlError("最外層必須是 key: value 形式")
    return data


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return loads(fh.read())
