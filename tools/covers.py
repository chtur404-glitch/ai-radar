"""封面圖產生器：依文章 slug + 分類 motif + palette 產生確定性的 SVG 封面。

不依賴任何外部圖片或套件。同一個 (slug, motif, palette) 永遠產生同樣的圖，
因此建置是幂等的。輸出尺寸 1200x750（16:10），與卡片、文章頁主視覺一致。
"""

import hashlib
import math
import os

W, H = 1200, 750

PALETTES = {
    "amber": ("#ffb35c", "#ff8a3d"),
    "violet": ("#c58bff", "#8b5cf6"),
    "cyan": ("#4fe3c1", "#22d3ee"),
    "indigo": ("#7d8bff", "#5b6cff"),
    "lime": ("#7ee787", "#39d353"),
    "magenta": ("#ff7ac6", "#f2569f"),
}

MOTIF_LABEL = {
    "image": "IMAGE / DESIGN",
    "video": "VIDEO GEN",
    "audio": "AUDIO / VOICE",
    "agent": "AI AGENT",
    "coding": "DEV TOOLS",
    "fun": "WORLD MODEL",
}


class Rng:
    """由字串種子決定的極簡 LCG，保證跨平台一致。"""

    def __init__(self, seed):
        self.s = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12], 16) | 1

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return (self.s >> 33) / float(1 << 31)

    def rng(self, lo, hi):
        return lo + (hi - lo) * self.next()


def _defs(c1, c2, uid):
    return f"""  <defs>
    <linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}" stop-opacity=".95"/>
      <stop offset="100%" stop-color="{c2}" stop-opacity=".55"/>
    </linearGradient>
    <radialGradient id="glow{uid}" cx="78%" cy="18%" r="72%">
      <stop offset="0%" stop-color="{c1}" stop-opacity=".38"/>
      <stop offset="60%" stop-color="{c1}" stop-opacity=".06"/>
      <stop offset="100%" stop-color="{c1}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid{uid}" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0v48" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="1"/>
    </pattern>
    <linearGradient id="fade{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#06070a" stop-opacity="0"/>
      <stop offset="100%" stop-color="#06070a" stop-opacity=".92"/>
    </linearGradient>
  </defs>"""


def _art_image(r, c1, c2):
    out = []
    cols, rows = 5, 3
    gap, pad = 14, 90
    bw = (W - pad * 2 - gap * (cols - 1)) / cols
    bh = (H - 200 - gap * (rows - 1)) / rows
    for row in range(rows):
        for col in range(cols):
            x = pad + col * (bw + gap)
            y = 120 + row * (bh + gap)
            hot = r.next() > 0.72
            op = 0.30 if hot else r.rng(0.05, 0.16)
            fill = "url(#g%s)" % r.uid if hot else c1
            out.append(
                '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" opacity="%.2f"/>'
                % (x, y, bw, bh, fill, 1.0 if hot else op)
            )
    out.append(
        '<rect x="%.1f" y="120" width="%.1f" height="%.1f" rx="10" fill="none" stroke="%s" stroke-opacity=".5"/>'
        % (pad + 2 * (bw + gap), bw, bh, c1)
    )
    return "".join(out)


def _art_video(r, c1, c2):
    out = ['<line x1="0" y1="375" x2="%d" y2="375" stroke="%s" stroke-opacity=".25"/>' % (W, c1)]
    n = 7
    fw, gap, pad = 118, 18, 90
    for k in range(n):
        x = pad + k * (fw + gap)
        hot = k == 3
        op = 0.85 if hot else 0.10
        out.append(
            '<rect x="%.1f" y="215" width="%d" height="%d" rx="12" fill="%s" opacity="%.2f" stroke="%s" stroke-opacity="%.2f"/>'
            % (x, fw, 132, c1, op, c1, 0.5 if hot else 0.18)
        )
        out.append(
            '<circle cx="%.1f" cy="281" r="%d" fill="none" stroke="%s" stroke-opacity="%.2f"/>'
            % (x + fw / 2, 9, c1, 0.7 if hot else 0.25)
        )
    for k in range(4):
        y = 430 + k * 26
        out.append(
            '<rect x="%d" y="%d" width="%.0f" height="4" rx="2" fill="%s" opacity="%.2f"/>'
            % (90 + k * 14, y, W - 300 - k * 90 * r.rng(0.6, 1.4), c1, 0.42 - k * 0.08)
        )
    return "".join(out)


def _art_audio(r, c1, c2):
    out = ['<line x1="90" y1="375" x2="%d" y2="375" stroke="%s" stroke-opacity=".22"/>' % (W - 90, c1)]
    n = 56
    bw = 9
    pad = 90
    step = (W - pad * 2) / n
    for k in range(n):
        env = 1.0 - abs(k / (n - 1) - 0.42) * 1.5
        amp = max(10, min(210, r.rng(24, 210) * env))
        x = pad + k * step
        hot = 0.30 < k / n < 0.72 and r.next() > 0.55
        out.append(
            '<rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="4.5" fill="%s" opacity="%.2f"/>'
            % (x, 375 - amp / 2, bw, amp, c1, 0.85 if hot else 0.26)
        )
        out.append(
            '<rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="4.5" fill="%s" opacity="%.2f"/>'
            % (x, 375 + amp * 0.10, bw, amp * 0.34, c2, 0.5 if hot else 0.14)
        )
    return "".join(out)


def _art_agent(r, c1, c2):
    pts = [(180, 250), (400, 180), (620, 300), (860, 200), (1010, 360), (330, 470), (700, 520), (930, 560)]
    out = []
    for i in range(len(pts) - 2):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 2]
        out.append(
            '<path d="M%d %d C %d %d, %d %d, %d %d" fill="none" stroke="%s" stroke-opacity=".34" stroke-width="1.6"/>'
            % (x1, y1, (x1 + x2) / 2, y1 - 40, (x1 + x2) / 2, y2 + 40, x2, y2, c1)
        )
    for i, (x, y) in enumerate(pts):
        hot = i == 2
        rr = 34 if hot else r.rng(14, 24)
        out.append(
            '<circle cx="%d" cy="%d" r="%.0f" fill="%s" opacity="%.2f" stroke="%s" stroke-opacity="%.2f"/>'
            % (x, y, rr, c1, 0.75 if hot else 0.10, c1, 0.8 if hot else 0.35)
        )
        if hot:
            out.append(
                '<circle cx="%d" cy="%d" r="%.0f" fill="none" stroke="%s" stroke-opacity=".45"/>' % (x, y, rr + 26, c2)
            )
    return "".join(out)


def _art_coding(r, c1, c2):
    out = []
    rows = 9
    for k in range(rows):
        y = 150 + k * 48
        width = r.rng(220, 760) * (1.0 - abs(k - 4) / 14.0)
        hot = r.next() > 0.78
        out.append(
            '<rect x="%d" y="%d" width="%.0f" height="12" rx="6" fill="%s" opacity="%.2f"/>'
            % (140 + r.rng(0, 120), y, max(90, width), c1, 0.7 if hot else 0.16)
        )
        out.append('<circle cx="108" cy="%d" r="4" fill="%s" opacity="%.2f"/>' % (y + 6, c2, 0.55 if hot else 0.2))
    out.append('<rect x="860" y="486" width="18" height="30" rx="3" fill="%s" opacity=".8"/>' % c1)
    out.append(
        '<path d="M700 92 l-58 58 58 58" fill="none" stroke="%s" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/>' % c2
    )
    out.append(
        '<path d="M840 92 l58 58 -58 58" fill="none" stroke="%s" stroke-opacity=".5" stroke-width="10" stroke-linecap="round"/>' % c2
    )
    return "".join(out)


def _art_fun(r, c1, c2):
    out = []
    cx, cy = 640, 400
    for k in range(1, 6):
        out.append(
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity="%.2f"/>'
            % (cx, cy, 70 * k, c1, 0.34 - k * 0.045)
        )
    for _ in range(26):
        ang = r.rng(0, 6.283)
        rad = r.rng(80, 400)
        x = cx + rad * math.cos(ang)
        y = cy + rad * math.sin(ang) * 0.62
        out.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r.rng(2, 7), c1, r.rng(0.2, 0.8)))
    out.append('<circle cx="%d" cy="%d" r="46" fill="url(#g%s)" opacity=".9"/>' % (cx, cy, r.uid))
    out.append('<ellipse cx="%d" cy="%d" rx="330" ry="205" fill="none" stroke="%s" stroke-opacity=".3" transform="rotate(-14 %d %d)"/>' % (cx, cy, c2, cx, cy))
    return "".join(out)


ART = {
    "image": _art_image,
    "video": _art_video,
    "audio": _art_audio,
    "agent": _art_agent,
    "coding": _art_coding,
    "fun": _art_fun,
}


class _Rng(Rng):
    uid = ""


def build_svg(slug, motif, palette):
    motif = motif if motif in ART else "image"
    c1, c2 = PALETTES.get(palette, PALETTES["cyan"])
    r = _Rng(slug)
    r.uid = hashlib.sha1(slug.encode("utf-8")).hexdigest()[:6]
    art = ART[motif](r, c1, c2)
    label = MOTIF_LABEL.get(motif, "AI RADAR")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="AI Radar 封面圖">
{_defs(c1, c2, r.uid)}
  <rect width="{W}" height="{H}" fill="#0b0d13"/>
  <rect width="{W}" height="{H}" fill="url(#grid{r.uid})"/>
  <rect width="{W}" height="{H}" fill="url(#glow{r.uid})"/>
{art}
  <rect width="{W}" height="{H}" fill="url(#fade{r.uid})" opacity=".55"/>
  <g font-family="JetBrains Mono, ui-monospace, Consolas, monospace" font-size="20" letter-spacing="4">
    <text x="90" y="672" fill="{c1}" opacity=".92">{label}</text>
    <text x="{W - 90}" y="672" fill="#ffffff" opacity=".34" text-anchor="end">AI RADAR</text>
  </g>
  <rect x="90" y="694" width="150" height="3" rx="1.5" fill="{c1}" opacity=".8"/>
</svg>
"""


def write_cover(out_dir, slug, motif, palette):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "%s.svg" % slug)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_svg(slug, motif, palette))
    return path
