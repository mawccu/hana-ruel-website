"""Rebuild img/*.jpg from source-photos/ (the original Unsplash downloads, 1400px wide).

Each product photo is centre-cropped to the painting's real width:height ratio,
resized so its long side is at most L pixels, and saved as a progressive JPEG (quality 82).

Usage (from the hana-ruel-website folder):  python tools/crop_photos.py
Requires Pillow:  pip install pillow
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-photos"
OUT = ROOT / "img"

# (output name, source file, width/height ratio, max long side in px)
JOBS = [
    ("harbour-early",  "p1531489956451-20957fab52f2", 90 / 90,   1300),
    ("low-tide",       "p1552312097-8ef75595e2a2",    80 / 60,   1200),
    ("blue-hour",      "p1618331833071-ce81bd50d300", 60 / 80,   1200),
    ("weather-report", "p1541512416146-3cf58d6b27cc", 75 / 100,  1200),
    ("salt",           "p1681235014294-588fea095706", 70 / 70,   1100),
    ("cascais",        "p1533208087231-c3618eab623c", 90 / 60,   1200),
    ("fog-study",      "p1583591900414-7031eb309cb6", 30 / 40,    900),
    ("yellow-room",    "p1787181876151-824ed8be7b1d", 40 / 60,   1000),
    ("studio",         "p1785423613154-a3f078420790", 1400 / 933, 1400),
    ("loupe",          "p1541512416146-3cf58d6b27cc", 1.0,        1400),  # same painting as weather-report, square crop
]

OUT.mkdir(exist_ok=True)
for name, src, ratio, long_side in JOBS:
    im = Image.open(SRC / f"{src}.jpg").convert("RGB")
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
    else:
        nh = int(w / ratio)
        box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
    im = im.crop(box)
    im.thumbnail((long_side, long_side), Image.LANCZOS)
    im.save(OUT / f"{name}.jpg", quality=82, optimize=True, progressive=True)
    print(name, im.size)
