#!/usr/bin/env python3
"""檢查每篇文章的 tool.url 與 sources 連結是否活著（HTTP 2xx/3xx）。

用法：python tools/check_links.py [slug ...]
只用標準函式庫；沒有網路時會全部標為 UNKNOWN 而不是失敗。
"""

import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True  # 不在 tools/ 留下 __pycache__

from build import ARTICLES, read, split_front  # noqa: E402

UA = "Mozilla/5.0 (compatible; AI-Radar-link-check/1.0)"


def status(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:  # 連線問題（DNS、TLS、逾時…）
        return type(exc).__name__


def main(argv):
    wanted = set(argv)
    for name in sorted(os.listdir(ARTICLES)):
        if not name.endswith(".md"):
            continue
        if wanted and os.path.splitext(name)[0] not in wanted:
            continue
        fm, _ = split_front(read(os.path.join(ARTICLES, name)), name)
        urls = []
        tool_url = (fm.get("tool") or {}).get("url")
        if tool_url:
            urls.append(("tool.url", str(tool_url)))
        for item in fm.get("sources") or []:
            if isinstance(item, dict) and item.get("url"):
                urls.append(("source", str(item["url"])))
        print("── %s" % name)
        for kind, url in urls:
            print("   %-9s %-4s %s" % (kind, status(url), url))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
