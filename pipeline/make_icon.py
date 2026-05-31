#!/usr/bin/env python3
"""Generate the PharmaPulse app icon at all required sizes.

App Store icons must be opaque (no alpha) and square with no rounded corners —
the system applies the mask. We render once at high resolution and downscale.

Run:  python3 pipeline/make_icon.py
"""
from PIL import Image, ImageDraw
import os

SS = 4  # supersample factor for smooth edges
S = 1024 * SS

A = (30, 58, 138)    # #1E3A8A  deep pharma blue (top-left)
B = (37, 99, 235)    # #2563EB  brand blue (bottom-right)
WHITE = (255, 255, 255)

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diagonal_gradient(size, c0, c1):
    img = Image.new("RGB", (size, size), c0)
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = lerp(c0, c1, t)
    return img

# --- background ---
img = diagonal_gradient(S, A, B)
draw = ImageDraw.Draw(img, "RGBA")

# brand ECG/pulse path (24-unit space) -> screen space
path24 = [(3, 12), (7, 12), (9, 5), (13, 19), (15, 10), (16.5, 14), (21, 14)]
sx = sy = (760 / 18) * SS
ox = (132 - 3 * (760 / 18)) * SS
cy = 512 * SS
pts = [(ox + px * sx, cy + (py - 12) * sy) for px, py in path24]

lw = int(46 * SS)

# soft shadow for depth
shadow = [(x + 6 * SS, y + 8 * SS) for x, y in pts]
draw.line(shadow, fill=(10, 20, 60, 90), width=lw, joint="curve")
for x, y in shadow:
    r = lw / 2
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(10, 20, 60, 90))

# main white pulse line with rounded caps/joins
draw.line(pts, fill=WHITE, width=lw, joint="curve")
for x, y in pts:
    r = lw / 2
    draw.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)

# small accent dot at the final upbeat (subtle brand touch)
ex, ey = pts[-1]
r = 30 * SS
draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=WHITE)

# downscale (antialias)
icon = img.resize((1024, 1024), Image.LANCZOS).convert("RGB")  # convert => no alpha

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) native app icon (single 1024, opaque)
appicon = os.path.join(root, "PharmaPulse", "Assets.xcassets", "AppIcon.appiconset", "AppIcon-1024.png")
icon.save(appicon)
print("wrote", appicon)

# 2) web / PWA icons
for name, size in [("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)]:
    p = os.path.join(root, "docs", name)
    icon.resize((size, size), Image.LANCZOS).save(p)
    print("wrote", p)
