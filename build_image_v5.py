#!/usr/bin/env python3
"""v5 — news-image-20261122, CROP FIX of v4 (hero 2 Chapo heads cut off).
v4's illus() center-cropped vertically: hero 2's image area (358x94,
target ~3.81) on a 1920x1280 source gives nh=504, center y0=388, so the
crop window y=388..892 cut off the helmet tops (heads start ~y285).
Fix: illus() gains a y_bias param (0.0 top / 0.5 center / 1.0 bottom)
and the Chapo hero uses y_bias=0.3 -> y0=232, window y=232..736: all
three heads fully visible with margin, torsos + rifles shown, legs cut.
COP31 lead and Kyiv hero keep the default center crop. No story text,
number or fact changed — crop only. v4 text fixes (medium 4-9, hero
decks) intact.
Deterministic, Pillow only. Writes entry_v5.png (1024x1024, <1 MiB)."""
from PIL import Image, ImageDraw, ImageFont
import os
from collections import Counter

W, H = 1024, 1024
PAPER = (250, 244, 230)
CARD = (255, 251, 242)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (105, 100, 90)
LIGHT = (205, 198, 184)
NAVY = (18, 42, 78)
SHADOW = (232, 226, 214)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

BASE = os.path.dirname(os.path.abspath(__file__))
ILLUS_DIR = os.path.join(BASE, "assets", "illustrations")
ILLUS = {
    "chapo": "media-generation-hero-chapo-0-7e31fde0-40da-4252-996d-e834d5bb118a.webp",
    "cop31": "media-generation-hero-cop31-0-c3c64e70-ca2c-4249-9bf0-660e1739d586.webp",
    "kyiv": "media-generation-hero-kyiv-0-74c7c238-2db6-434f-97d8-c2a94514a4ec.webp",
    "map": "media-generation-worldmap-0-06de1b11-1735-4afe-a2b6-b70884c71fd8.webp",
}

def F(p, s):
    if os.path.exists(p):
        return ImageFont.truetype(p, s)
    return ImageFont.truetype(SERIF if "Serif" in p else SANS, s)

def wrap(dr, text, font, max_w):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if dr.textlength(t, font=font) <= max_w:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out

def wrapped(dr, x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(dr, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y, len(lines)

def illus(w, h, key, y_bias=0.5):
    """Crop+resize an illustration to w x h. y_bias controls the vertical
    crop window: 0.0 = top, 0.5 = center (default), 1.0 = bottom.
    Only used when the source is narrower than the target (vertical crop)."""
    im = Image.open(os.path.join(ILLUS_DIR, ILLUS[key])).convert("RGB")
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:
        nw = int(ih * target); x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target); y0 = int((ih - nh) * y_bias)
        y0 = max(0, min(y0, ih - nh))
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)

# ---- story data: 1 lead + 2 heroes + 6 medium + 22 briefs = 31 ----
LEAD = (1, "WORLD", "ANTALYA  •  CLIMATE",
        "COP31 collapses as EU rejects draft with no mention of fossil fuels",
        "The climate summit ended with no deal after the EU objected to a final text with no mention of fossil fuels. Talks ran two days into overtime — the longest COP ever, and the first to collapse without a deal since Copenhagen 2009.",
        "cop31")
HEROES = [
    (2, "THE AMERICAS", "GUASAVE  •  JUSTICE",
     "Mexico captures cartel boss 'El Chapo Isidro'; 11 killed",
     "Special forces seized Fausto Isidro Meza Flores in Sinaloa with US intelligence help. Seven gunmen and four soldiers died.",
     "chapo"),
    (3, "EUROPE", "KYIV  •  WAR",
     "Russian drone hits Kyiv apartment; 14 missing",
     "A drone partly destroyed a residential block near Kyiv. A Russian missile also hit Zelenskyy's hometown Kryvyi Rih.",
     "kyiv"),
]
MEDIUM = [
    (4, "THE AMERICAS", "NEW YORK  •  MARKETS",
     "US stocks fall into correction in AI sell-off"),
    (5, "WORLD", "MERCURY  •  SPACE",
     "BepiColombo enters orbit around Mercury"),
    (6, "MIDEAST", "BAHRAIN  •  CONFLICT",
     "Iran strikes Bahrain as US blockade hits 130 days"),
    (7, "EUROPE", "GULF OF FINLAND  •  WAR",
     "Russian cargo ship ablaze after suspected drone strike"),
    (8, "ASIA-PACIFIC", "BANTEN  •  DISASTER",
     "Factory fire in Indonesia: 3 dead, 36 missing"),
    (9, "THE AMERICAS", "WASHINGTON  •  TECH",
     "FBI investigates hack of its criminal database"),
]
BRIEFS = [
    ("ASIA-PACIFIC", "South Korea minister quits over AI exam cheating"),
    ("THE AMERICAS", "GTA 6 sells $3.8bn in a day, biggest launch ever"),
    ("THE AMERICAS", "Amazon nears $7.5bn deal for AI startup Decart"),
    ("THE AMERICAS", "Verstappen wins Las Vegas GP; Antonelli already champion"),
    ("EUROPE", "Denmark expels Russian attaché over alleged plot"),
    ("MIDEAST", "Eisenkot invites Netanyahu's Likud to coalition talks"),
    ("MIDEAST", "Israeli strikes continue in Gaza; aid vehicle hit"),
    ("AFRICA", "Boat capsizes in Nigeria; 24 mourners dead"),
    ("THE AMERICAS", "Man convicted of starting 2025 Palisades fire"),
    ("MIDEAST", "Houthis fire missiles at Saudi Arabia"),
    ("EUROPE", "UK and EU strike deals; Burnham eyes rejoining"),
    ("EUROPE", "Turkey takes control of last independent news channel"),
    ("EUROPE", "Princess Kate says she is in remission from cancer"),
    ("THE AMERICAS", "Immigration arrests on Seattle jet bridge draw outcry"),
    ("ASIA-PACIFIC", "Garment strikes and clashes in Bangladesh"),
    ("THE AMERICAS", "Argentina approves $50bn LNG export project"),
    ("ASIA-PACIFIC", "Saudi Arabia triples oil stored in Japan"),
    ("EUROPE", "Leeds stun Chelsea 4-1 at Stamford Bridge"),
    ("THE AMERICAS", "Bolsonaro in intensive care with bowel obstruction"),
    ("AFRICA", "ANC fights to keep South Africa's key cities"),
    ("EUROPE", "Alcaraz reaches ATP Finals final"),
    ("THE AMERICAS", "Venezuela signs military deal with US"),
]
assert len(BRIEFS) == 22, len(BRIEFS)
assert all(len(t) <= 56 for _, t in BRIEFS), [t for _, t in BRIEFS if len(t) > 56]
TOTAL = 1 + 2 + 6 + len(BRIEFS)
assert TOTAL == 31

REGIONS = ["EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "WORLD"]
REG_COLORS = {"EUROPE": (31, 95, 160), "THE AMERICAS": (46, 139, 87),
              "ASIA-PACIFIC": (178, 34, 34), "MIDEAST": (176, 124, 34),
              "AFRICA": (70, 70, 70), "WORLD": (110, 110, 110)}
all_stories = [LEAD] + HEROES + MEDIUM
counts = Counter([r for _, r, *_ in all_stories] + [r for r, _ in BRIEFS])
assert sum(counts.values()) == 31, counts

NUMBERS = [
    ("11", "killed as Mexico captures 'El Chapo Isidro'"),
    ("$3.8bn", "GTA 6 sales in a single day — biggest launch ever"),
    ("14", "missing after Russian drone hits Kyiv apartment"),
    ("-3.7%", "S&P 500 fall as the AI sell-off spreads"),
    ("36", "still missing after Indonesia factory fire"),
    ("$50bn", "Argentina approves LNG export project"),
]

def lonlat_to_frac(lon, lat):
    return ((lon + 180) / 360.0, (90 - lat) / 180.0)

# map pins: (story no, fx, fy) — Europe cluster nudged apart for legibility.
# No pin for #5 BepiColombo: it is a space mission, not a place on Earth.
PINS = [
    (2, *lonlat_to_frac(-108.5, 25.6)),   # Guasave, Mexico
    (1, 0.60, 0.30),                      # Antalya (nudged)
    (3, 0.60, 0.22),                      # Kyiv (nudged)
    (4, *lonlat_to_frac(-74.0, 40.7)),    # New York
    (6, *lonlat_to_frac(50.6, 26.2)),     # Bahrain
    (7, 0.55, 0.15),                      # Gulf of Finland (nudged)
    (8, *lonlat_to_frac(106.2, -6.2)),    # Banten, Indonesia
    (9, 0.26, 0.32),                      # Washington DC (nudged off New York)
]
DOTS = [
    lonlat_to_frac(126.9, 37.5),    # Seoul
    lonlat_to_frac(-115.1, 36.1),   # Las Vegas
    lonlat_to_frac(12.6, 55.7),     # Copenhagen
    lonlat_to_frac(34.5, 31.5),     # Gaza
    lonlat_to_frac(6.3, 4.9),       # Bayelsa, Nigeria
    lonlat_to_frac(-0.1, 51.5),     # London
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28
RX = 996

# ---- top small caps ----
d.text((MX, 10), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
d.text((RX, 12), "SUNDAY'S NEWS  •  ONE PAGE  •  31 STORIES", font=F(SANS_B, 11), fill=INK, anchor="ra")
d.line([(MX, 30), (RX, 30)], fill=INK, width=2)

# ---- huge serif date ----
d.text((MX, 36), "Sunday 22 November 2026", font=F(SERIF_B, 52), fill=INK)
d.text((MX, 96), "COP31 collapses  •  El Chapo Isidro captured  •  Kyiv apartment hit",
       font=F(SERIF_I, 15), fill=RED)
d.line([(MX, 120), (RX, 120)], fill=INK, width=1)

# ---- region bar (6 regions, widths proportional, sum 968) ----
bar_y, bar_h = 126, 22
widths = {"EUROPE": 250, "THE AMERICAS": 344, "ASIA-PACIFIC": 125,
          "MIDEAST": 125, "AFRICA": 62, "WORLD": 62}
assert sum(widths.values()) == 968
x = MX
for reg in REGIONS:
    w = widths[reg]
    d.rectangle([x, bar_y, x + w, bar_y + bar_h], fill=REG_COLORS[reg])
    d.text((x + w / 2, bar_y + bar_h / 2), f"{reg} {counts[reg]}",
           font=F(SANS_B, 10), fill=(255, 255, 255), anchor="mm")
    x += w

# ---- statistics CARDS: 6 rounded cards + small globe motif ----
# Band y=150..214 (64px). Globe (36px) at left, then 6 cards.
def globe(cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    d.ellipse([cx - r * 0.42, cy - r, cx + r * 0.42, cy + r], outline=color, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=1)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=color, width=1)

sy, sh = 150, 64
globe(MX + 18, sy + sh // 2, 17, NAVY)
card_x0 = MX + 44
card_gap = 6
card_w = (RX - card_x0 - card_gap * 5) // 6
for i, (big, cap) in enumerate(NUMBERS):
    cx = card_x0 + i * (card_w + card_gap)
    # soft shadow, then the card
    d.rounded_rectangle([cx + 2, sy + 3, cx + card_w + 2, sy + sh + 1], radius=10, fill=SHADOW)
    d.rounded_rectangle([cx, sy, cx + card_w, sy + sh], radius=10, fill=CARD, outline=LIGHT, width=1)
    d.text((cx + 10, sy + 7), big, font=F(SERIF_B, 20), fill=RED)
    wrapped(d, cx + 10, sy + 36, cap, F(SANS, 9), card_w - 20, 11, fill=(70, 66, 58), max_lines=2)
d.line([(MX, 218), (RX, 218)], fill=INK, width=1)

# ---- LEAD hero (COP31, left, dominant) ----
lx, ly, lw = MX, 222, 592
d.rectangle([lx, ly, lx + lw, ly + 380], outline=LIGHT, width=1)
img.paste(illus(lw - 2, 228, LEAD[5]), (lx + 1, ly + 1))
d.ellipse([lx + 14, ly + 14, lx + 40, ly + 40], fill=RED, outline=(255, 255, 255), width=2)
d.text((lx + 27, ly + 27), "1", font=F(SANS_B, 15), fill=(255, 255, 255), anchor="mm")
d.rectangle([lx, ly + 229, lx + lw, ly + 252], fill=INK)
d.text((lx + 12, ly + 234), LEAD[2], font=F(SANS_B, 11), fill=(255, 255, 255))
_, n = wrapped(d, lx + 12, ly + 262, LEAD[3], F(SERIF_B, 24), lw - 24, 28, max_lines=2)
wrapped(d, lx + 12, ly + 262 + n * 28 + 6, LEAD[4], F(SANS, 12), lw - 24, 16, fill=(50, 46, 40), max_lines=3)

# ---- two stacked secondary heroes (right) ----
def side_hero(x, y, w, num, kick, head, deck, key, y_bias=0.5):
    h = 186
    d.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1)
    img.paste(illus(w - 2, 94, key, y_bias), (x + 1, y + 1))
    d.ellipse([x + 10, y + 10, x + 32, y + 32], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 21, y + 21), str(num), font=F(SANS_B, 12), fill=(255, 255, 255), anchor="mm")
    d.rectangle([x, y + 95, x + w, y + 114], fill=INK)
    d.text((x + 10, y + 98), kick, font=F(SANS_B, 9), fill=(255, 255, 255))
    _, n = wrapped(d, x + 10, y + 120, head, F(SERIF_B, 15), w - 20, 17, max_lines=2)
    wrapped(d, x + 10, y + 120 + n * 17 + 3, deck, F(SANS, 10), w - 20, 12, fill=(50, 46, 40), max_lines=2)

rx, rw = 636, 360
side_hero(rx, 222, rw, HEROES[0][0], HEROES[0][2], HEROES[0][3], HEROES[0][4], HEROES[0][5], y_bias=0.3)
side_hero(rx, 416, rw, HEROES[1][0], HEROES[1][2], HEROES[1][3], HEROES[1][4], HEROES[1][5])

# ---- 6 medium cards, 2 rows x 3 ----
def medium(x, y, w, num, kick, head):
    h = 58
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LIGHT, width=1)
    d.text((x + 10, y + 7), str(num), font=F(SANS_B, 14), fill=RED)
    d.text((x + 32, y + 9), kick, font=F(SANS_B, 9), fill=RED)
    wrapped(d, x + 10, y + 22, head, F(SERIF_B, 13), w - 20, 14, max_lines=2)

hx = [MX, 355, 682]
my = [606, 670]
for row, y in enumerate(my):
    for col, (num, reg, kick, head) in enumerate(MEDIUM[row * 3:(row + 1) * 3]):
        medium(hx[col], y, 314, num, kick, head)

d.line([(MX, 732), (RX, 732)], fill=INK, width=1)

# ---- bottom: map left, briefs right ----
d.text((MX, 736), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
map_x, map_y, map_w, map_h = MX, 754, 330, 176
src = Image.open(os.path.join(ILLUS_DIR, ILLUS["map"])).convert("RGB")
mw, mh = src.size
fit_h = int(map_w * mh / mw)  # 330 * 1120/2240 = 165
fit = src.resize((map_w, fit_h), Image.LANCZOS)
off_y = map_y + (map_h - fit_h) // 2
img.paste(fit, (map_x, off_y))
md = ImageDraw.Draw(img)
def map_px(fx, fy):
    return (map_x + fx * map_w, off_y + fy * fit_h)
for fx, fy in DOTS:
    px, py = map_px(fx, fy)
    md.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(120, 115, 105))
for num, fx, fy in PINS:
    px, py = map_px(fx, fy)
    md.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=2)
    md.text((px, py), str(num), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=LIGHT, width=1)

# ---- briefs: 22, 2 columns ----
bx = 372
d.text((bx, 736), "ALSO ON SUNDAY 22 NOVEMBER  —  22 MORE STORIES", font=F(SANS_B, 12), fill=RED)
cols = [BRIEFS[:11], BRIEFS[11:]]
for ci, col in enumerate(cols):
    x = bx + ci * 318
    y = 754
    for i, (reg, b) in enumerate(col):
        n = 10 + ci * 11 + i
        d.text((x, y), f"{n}.", font=F(SANS_B, 10), fill=RED)
        _, lines = wrapped(d, x + 24, y, b, F(SANS_B, 10), 282, 12, max_lines=2)
        y += lines * 12 + 3

# ---- DATE CHECK box ----
dy = 936
d.rectangle([MX, dy, RX, dy + 34], outline=RED, width=2)
d.text((MX + 10, dy + 5), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
wrapped(d, MX + 92, dy + 5,
        "First reported Thursday 19 Nov, so NOT on this page as news: the Shenzhen summit  •  Crimean Bridge strikes  •  Anthropic IPO  •  GTA VI launch  •  Iran's first Gulf strikes  •  EU–Indonesia trade deal  •  Cyclone Aqwan  •  World Court Myanmar ruling.",
        F(SANS, 9), RX - MX - 102, 11, fill=INK, max_lines=2)

# ---- markets + footer ----
d.line([(MX, 980), (RX, 980)], fill=INK, width=2)
d.text((MX, 988), "MARKETS  •  S&P 500 6,910  -3.70%   •   FTSE 100 10,346  -1.02%   •   Nikkei  -5.06%   •   Brent $89.95  +0.57%   •   Gold $3,515  -4.62%   •   US 10-yr 4.92%",
       font=F(SANS_B, 11), fill=INK)
d.text((MX, 1006), "Every story here happened, or was first reported, on Sunday 22 November 2026. Disputed claims are attributed, not stated as fact. Sources: BBC, The Guardian, Reuters, AP, AFP, Al Jazeera, One Turn. Original drawings.",
       font=F(SANS, 9), fill=GREY)

img.save(os.path.join(BASE, "entry_v5.png"), "PNG", optimize=True)
print("saved v5 1024x1024")
