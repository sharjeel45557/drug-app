#!/usr/bin/env python3
"""Generate PharmaPulse brand images for the web app.

Outputs (all into docs/):
  - apple-touch-icon.png (180), icon-192.png, icon-512.png  — favicon / PWA / home-screen
  - og-image.png (1200x630)                                 — social link preview card

Run:  python3 pipeline/make_icon.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

SS = 4  # supersample for smooth edges
A = (30, 58, 138)    # #1E3A8A deep blue
B = (37, 99, 235)    # #2563EB brand blue
WHITE = (255, 255, 255)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(w, h, c0, c1):
    img = Image.new("RGB", (w, h), c0)
    px = img.load()
    denom = max(1, (w - 1) + (h - 1))
    for y in range(h):
        for x in range(w):
            px[x, y] = lerp(c0, c1, (x + y) / denom)
    return img


def pulse(draw, pts, lw, color, shadow=None):
    if shadow:
        sp = [(x + 6 * SS, y + 8 * SS) for x, y in pts]
        draw.line(sp, fill=shadow, width=lw, joint="curve")
        for x, y in sp:
            r = lw / 2
            draw.ellipse([x - r, y - r, x + r, y + r], fill=shadow)
    draw.line(pts, fill=color, width=lw, joint="curve")
    for x, y in pts:
        r = lw / 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


# ---------- square icon ----------
S = 1024 * SS
img = gradient(S, S, A, B)
d = ImageDraw.Draw(img, "RGBA")
path24 = [(3, 12), (7, 12), (9, 5), (13, 19), (15, 10), (16.5, 14), (21, 14)]
sx = sy = (760 / 18) * SS
ox = (132 - 3 * (760 / 18)) * SS
cy = 512 * SS
pts = [(ox + px * sx, cy + (py - 12) * sy) for px, py in path24]
pulse(d, pts, int(46 * SS), WHITE, shadow=(10, 20, 60, 90))
icon = img.resize((1024, 1024), Image.LANCZOS).convert("RGB")

for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
    icon.resize((size, size), Image.LANCZOS).save(os.path.join(DOCS, name))
    print("wrote", name)

# ---------- social preview (1200x630) ----------
W, H = 1200 * SS, 630 * SS
card = gradient(W, H, A, B)
dc = ImageDraw.Draw(card, "RGBA")
# pulse motif along the lower third
p2 = [(60, 360), (260, 360), (330, 235), (450, 470), (560, 150), (650, 410), (720, 360), (1140, 360)]
p2 = [(x * SS, y * SS) for x, y in p2]
pulse(dc, p2, int(16 * SS), (255, 255, 255, 60))
margin = 74 * SS
max_w = W - 2 * margin


def fit_font(text, start_px):
    size = start_px
    while size > 10:
        f = ImageFont.truetype(FONT, size)
        if dc.textlength(text, font=f) <= max_w:
            return f
        size -= 2 * SS
    return ImageFont.truetype(FONT, size)


title = "PharmaPulse"
subtitle = "Weekly pharma & drug-industry intelligence"
title_font = fit_font(title, 132 * SS)
sub_font = fit_font(subtitle, 50 * SS)
dc.text((margin, 150 * SS), title, font=title_font, fill=WHITE)
dc.text((margin + 4 * SS, 320 * SS), subtitle, font=sub_font, fill=(226, 232, 240))
card.resize((1200, 630), Image.LANCZOS).convert("RGB").save(os.path.join(DOCS, "og-image.png"))
print("wrote og-image.png")
