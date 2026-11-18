#!/usr/bin/env python3
"""
THE WORLD IN A DAY -- build-time drawing program.

This is the program that DRAWS the broadsheet front page summing up the
world news of Tuesday 17 November 2026. It runs at build time only, on a
machine that has Pillow (PIL) and the DejaVu fonts installed, and writes
the finished PNG to entry.png next to this file.

The drawing is fully deterministic: fixed geometry only, no randomness,
no clocks, no external data -- two runs produce a byte-identical PNG.

The server never runs this file. The competition's program/v1 runtime is
stdlib-only (no Pillow, no system fonts), so the submitted main.py is a
small stdlib copier that ships the pre-rendered entry.png to the output
path. Regenerate entry.png by running this file after any drawing change:

    python3 draw.py

Requires: Python 3.13, Pillow (PIL). Everything else is stdlib.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

W = H = 1024
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
F_SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 243, 231)
INK = (17, 19, 23)
RED = (156, 24, 24)
DARK_BLUE = (24, 52, 92)
SEA = (38, 96, 140)
SKY = (196, 220, 236)
GREY = (70, 74, 80)
WHITE = (255, 255, 255)
ORANGE = (232, 119, 34)
YELLOW = (245, 197, 49)
GREEN = (34, 110, 62)

MARGIN = 28
CW = W - 2 * MARGIN  # content width = 968


# --------------------------------------------------------------------------
# Text helpers
# --------------------------------------------------------------------------

def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_w, start):
    """Largest size <= start at which text fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that each fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def line_h(f):
    return int(f.size * 1.22)


def text_c(draw, cx, y, text, f, fill=INK):
    """Draw text horizontally centred on cx, top edge at y."""
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


def text_l(draw, x, y, text, f, fill=INK):
    draw.text((x, y), text, font=f, fill=fill)


def panel(draw, box, width=3):
    draw.rectangle(box, outline=INK, width=width)


# --------------------------------------------------------------------------
# Small illustration glyphs. Each draws inside box (x0, y0, x1, y1).
# --------------------------------------------------------------------------

def glyph_tanker_mine(d, box):
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    # sea waves
    for i in range(3):
        wy = y1 - 8 - i * 7
        d.line([(x0 + 4, wy), (x0 + 26, wy)], fill=SEA, width=3)
        d.line([(x0 + 58, wy), (x0 + 80, wy)], fill=SEA, width=3)
    # tanker hull + superstructure
    d.polygon([(x0 + 6, cy + 2), (x0 + 62, cy + 2), (x0 + 54, cy + 14),
               (x0 + 14, cy + 14)], fill=INK)
    d.rectangle([x0 + 14, cy - 10, x0 + 30, cy + 2], fill=INK)
    d.rectangle([x0 + 40, cy - 6, x0 + 58, cy + 2], fill=GREY)
    # naval mine: spiked circle
    mx, my, r = x1 - 22, cy + 2, 11
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1),
                   (-1, 1), (1, 1)]:
        d.line([(mx, my), (mx + dx * (r + 6), my + dy * (r + 6))],
               fill=INK, width=3)
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=RED)
    # burst between ship and mine
    bx, by = x0 + 74, cy - 8
    d.polygon([(bx, by - 10), (bx + 3, by - 3), (bx + 10, by - 4),
               (bx + 5, by + 1), (bx + 8, by + 8), (bx, by + 4),
               (bx - 8, by + 8), (bx - 5, by + 1), (bx - 10, by - 4),
               (bx - 3, by - 3)], fill=ORANGE)


def glyph_chip(d, box):
    x0, y0, x1, y1 = box
    # microchip
    cx0, cy0, cx1, cy1 = x0 + 8, y0 + 4, x0 + 48, y1 - 4
    d.rectangle([cx0, cy0, cx1, cy1], outline=INK, width=4)
    d.rectangle([cx0 + 11, cy0 + 11, cx1 - 11, cy1 - 11], outline=INK, width=3)
    for i in range(3):
        px = cx0 + 8 + i * 12
        d.line([(px, cy0 - 5), (px, cy0)], fill=INK, width=3)
        d.line([(px, cy1), (px, cy1 + 5)], fill=INK, width=3)
        py = cy0 + 8 + i * 10
        d.line([(cx0 - 5, py), (cx0, py)], fill=INK, width=3)
        d.line([(cx1, py), (cx1 + 5, py)], fill=INK, width=3)
    # rising earnings chart
    pts = [(x0 + 62, y1 - 10), (x0 + 76, y1 - 20), (x0 + 88, y1 - 16),
           (x0 + 104, y0 + 8)]
    d.line(pts, fill=GREEN, width=4)
    d.polygon([(x0 + 104, y0 + 8), (x0 + 94, y0 + 10), (x0 + 102, y0 + 18)],
              fill=GREEN)
    d.line([(x0 + 60, y1 - 6), (x1 - 4, y1 - 6)], fill=GREY, width=2)


def glyph_plane_return(d, box):
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    # aeroplane silhouette (side view, pointing right)
    d.polygon([(x0 + 10, cy), (x0 + 52, cy - 4), (x0 + 70, cy - 16),
               (x0 + 76, cy - 15), (x0 + 70, cy - 2), (x0 + 78, cy),
               (x0 + 70, cy + 3), (x0 + 74, cy + 14), (x0 + 68, cy + 14),
               (x0 + 54, cy + 4), (x0 + 16, cy + 5)], fill=DARK_BLUE)
    # return (U-turn) arrow beneath
    ax0, ay0, ax1, ay1 = x0 + 52, cy + 12, x1 - 8, y1 - 2
    d.arc([ax0, ay0 - 8, ax1, ay1 + 8], start=300, end=140, fill=RED, width=4)
    d.polygon([(ax0 + 2, ay0 + 2), (ax0 + 14, ay0 - 2), (ax0 + 12, ay0 + 12)],
              fill=RED)


def glyph_jet(d, box):
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    # rising sun disc (Japan)
    d.ellipse([x0 + 58, cy - 20, x0 + 98, cy + 20], fill=RED)
    # fighter jet silhouette crossing it
    d.polygon([(x0 + 6, cy + 12), (x0 + 34, cy - 2), (x0 + 62, cy - 14),
               (x0 + 88, cy - 16), (x0 + 66, cy - 4), (x0 + 84, cy + 2),
               (x0 + 52, cy + 4), (x0 + 62, cy + 14), (x0 + 44, cy + 12),
               (x0 + 26, cy + 16)], fill=INK)
    # contrails
    d.line([(x0 + 4, cy + 18), (x0 + 30, cy + 12)], fill=GREY, width=3)
    d.line([(x0 + 4, cy + 24), (x0 + 28, cy + 18)], fill=GREY, width=3)


def glyph_rocket(d, box):
    x0, y0, x1, y1 = box
    # rocket body, tilted, nose up-right
    d.polygon([(x0 + 26, y1 - 6), (x0 + 34, y1 - 26), (x0 + 52, y0 + 16),
               (x0 + 62, y0 + 10), (x0 + 66, y0 + 20), (x0 + 48, y1 - 12),
               (x0 + 38, y1 - 4)], fill=GREY)
    d.ellipse([x0 + 52, y0 + 12, x0 + 64, y0 + 24], fill=DARK_BLUE)
    # flame
    d.polygon([(x0 + 28, y1 - 8), (x0 + 18, y1 + 2), (x0 + 36, y1 - 2)],
              fill=ORANGE)
    # explosion burst at the nose
    bx, by = x0 + 74, y0 + 12
    d.polygon([(bx, by - 12), (bx + 4, by - 4), (bx + 13, by - 6),
               (bx + 6, by + 0), (bx + 11, by + 9), (bx + 2, by + 5),
               (bx - 3, by + 12), (bx - 5, by + 3), (bx - 13, by + 5),
               (bx - 7, by - 2), (bx - 12, by - 9), (bx - 3, by - 5)],
              fill=RED)
    # falling satellites (small squares with panels)
    for sx, sy in [(x0 + 88, y0 + 30), (x0 + 70, y1 - 16), (x0 + 96, y1 - 8)]:
        d.rectangle([sx, sy, sx + 8, sy + 8], fill=INK)
        d.line([(sx - 5, sy + 4), (sx, sy + 4)], fill=INK, width=2)
        d.line([(sx + 8, sy + 4), (sx + 13, sy + 4)], fill=INK, width=2)


def glyph_aid_truck(d, box):
    x0, y0, x1, y1 = box
    by = y1 - 12  # ground line
    # cargo box with red cross
    d.rectangle([x0 + 6, y0 + 4, x0 + 58, by - 8], outline=INK, width=4)
    cx, cy = x0 + 32, (y0 + 4 + by - 8) // 2
    d.rectangle([cx - 4, cy - 11, cx + 4, cy + 11], fill=RED)
    d.rectangle([cx - 11, cy - 4, cx + 11, cy + 4], fill=RED)
    # cab
    d.polygon([(x0 + 62, by - 8), (x0 + 62, y0 + 16), (x0 + 76, y0 + 16),
               (x0 + 88, by - 8)], fill=DARK_BLUE)
    # wheels
    for wx in (x0 + 22, x0 + 74):
        d.ellipse([wx - 8, by - 10, wx + 8, by + 6], fill=INK)
    d.line([(x0 + 2, by + 6), (x1 - 2, by + 6)], fill=GREY, width=3)


def glyph_candle(d, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    # flame
    d.ellipse([cx - 7, y0 + 2, cx + 7, y0 + 24], fill=ORANGE)
    d.ellipse([cx - 3, y0 + 10, cx + 3, y0 + 24], fill=YELLOW)
    # candle body
    d.rectangle([cx - 13, y0 + 28, cx + 13, y1 - 8], fill=WHITE)
    d.rectangle([cx - 13, y0 + 28, cx + 13, y1 - 8], outline=INK, width=3)
    d.line([(cx - 20, y1 - 4), (cx + 20, y1 - 4)], fill=INK, width=3)


GLYPHS = [glyph_tanker_mine, glyph_chip, glyph_plane_return, glyph_jet,
          glyph_rocket, glyph_aid_truck, glyph_candle]

LABELS = [
    "TANKERS HIT MINES IN HORMUZ",
    "NVIDIA'S FIRST EARNINGS AFTER HUANG",
    "EUROPE'S RWANDA RETURN HUB",
    "JAPAN SCRAMBLES JETS AT RUSSIA",
    "VULCAN FAILURE: 40 SATELLITES LOST",
    "WEST TO ISRAEL: OPEN GAZA AID",
    "UN: 1,390 SUDAN CIVILIANS KILLED",
]


# --------------------------------------------------------------------------
# Big illustrations
# --------------------------------------------------------------------------

def draw_bridge(d, box):
    """Lead art: bridge over the sea, one span collapsed into the water."""
    x0, y0, x1, y1 = box
    sea_y = y0 + int((y1 - y0) * 0.58)
    # sky and sea
    d.rectangle([x0, y0, x1, sea_y], fill=SKY)
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # clouds
    for cx, cy, s in [(x0 + 90, y0 + 22, 1), (x0 + 300, y0 + 14, 0), (x1 - 120, y0 + 20, 1)]:
        d.ellipse([cx - 34 - s * 8, cy - 10, cx + 34 + s * 8, cy + 12], fill=WHITE)
    deck_y = y0 + int((y1 - y0) * 0.52)
    tower_top = y0 + 4
    # towers
    for tx in (x0 + 120, x0 + 330):
        d.line([(tx, tower_top), (tx, deck_y + 26)], fill=INK, width=9)
    # suspension cables
    d.line([(x0 + 120, tower_top), (x0 + 330, tower_top)], fill=INK, width=3)
    d.line([(x0 + 4, deck_y), (x0 + 120, tower_top)], fill=INK, width=3)
    for tx in (x0 + 120, x0 + 330):
        for off in (40, 80, 120, 160):
            if tx + off < x0 + 470:
                d.line([(tx + off, tower_top + off // 6), (tx + off, deck_y)],
                       fill=INK, width=2)
    # intact deck (left)
    d.line([(x0 + 2, deck_y), (x0 + 478, deck_y)], fill=INK, width=11)
    # burst at the break
    bx, by = x0 + 492, deck_y - 4
    d.polygon([(bx, by - 22), (bx + 6, by - 7), (bx + 22, by - 10),
               (bx + 10, by + 1), (bx + 18, by + 14), (bx + 3, by + 8),
               (bx - 4, by + 20), (bx - 8, by + 5), (bx - 22, by + 9),
               (bx - 12, by - 3), (bx - 20, by - 15), (bx - 5, by - 8)],
              fill=ORANGE)
    # collapsed span: tilted down into the sea
    d.line([(x0 + 486, deck_y + 2), (x0 + 640, y1 - 26)], fill=INK, width=11)
    d.line([(x0 + 560, deck_y + 26), (x0 + 668, y1 - 40)], fill=GREY, width=7)
    # sunken segment in the water
    d.line([(x0 + 660, y1 - 18), (x0 + 790, y1 - 34)], fill=INK, width=9)
    # right-hand stub of deck, broken end
    d.line([(x0 + 838, deck_y), (x1 - 2, deck_y)], fill=INK, width=11)
    d.polygon([(x0 + 838, deck_y - 6), (x0 + 822, deck_y), (x0 + 838, deck_y + 6)],
              fill=INK)
    # splashes and foam
    for sx, sy in [(x0 + 636, y1 - 30), (x0 + 700, y1 - 16), (x0 + 600, y1 - 12)]:
        d.arc([sx - 20, sy - 12, sx + 20, sy + 12], start=180, end=360,
              fill=WHITE, width=4)
    for wx in range(x0 + 30, x1 - 30, 64):
        d.arc([wx, y1 - 14, wx + 30, y1 - 2], start=180, end=360,
              fill=WHITE, width=3)


def draw_summit(d, box):
    """Second-story art: three leaders at a summit table, flags behind."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    centres = [cx - 118, cx, cx + 118]
    flag_y0, flag_y1 = y0 + 2, y0 + 44
    # flags: USA, China, Russia
    for i, fx in enumerate(centres):
        fw = 62
        fx0, fx1 = fx - fw // 2, fx + fw // 2
        d.line([(fx, flag_y0), (fx, y1 - 46)], fill=GREY, width=3)
        if i == 0:  # USA: stripes + blue canton
            d.rectangle([fx0, flag_y0, fx1, flag_y1], fill=WHITE, outline=INK)
            for s in range(0, 42, 12):
                d.rectangle([fx0, flag_y0 + s, fx1, flag_y0 + s + 6], fill=RED)
            d.rectangle([fx0, flag_y0, fx0 + 26, flag_y0 + 20], fill=DARK_BLUE)
        elif i == 1:  # China: red field, yellow stars
            d.rectangle([fx0, flag_y0, fx1, flag_y1], fill=RED, outline=INK)
            d.ellipse([fx0 + 6, flag_y0 + 6, fx0 + 16, flag_y0 + 16], fill=YELLOW)
            for sx, sy in [(20, 4), (24, 12), (20, 20)]:
                d.ellipse([fx0 + sx, flag_y0 + sy, fx0 + sx + 5,
                           flag_y0 + sy + 5], fill=YELLOW)
        else:  # Russia: white / blue / red
            third = (flag_y1 - flag_y0) // 3
            d.rectangle([fx0, flag_y0, fx1, flag_y0 + third], fill=WHITE,
                        outline=INK)
            d.rectangle([fx0, flag_y0 + third, fx1, flag_y0 + 2 * third],
                        fill=DARK_BLUE)
            d.rectangle([fx0, flag_y0 + 2 * third, fx1, flag_y1], fill=RED)
    # leaders: head + shoulders behind the table
    head_y = y0 + 56
    for fx in centres:
        d.ellipse([fx - 17, head_y, fx + 17, head_y + 34], fill=INK)
        d.pieslice([fx - 37, head_y + 24, fx + 37, head_y + 88], start=180,
                   end=360, fill=INK)
    # table
    table_y = y0 + 104
    d.polygon([(x0 + 16, table_y), (x1 - 16, table_y), (x1 - 34, y1 - 4),
               (x0 + 34, y1 - 4)], fill=(96, 66, 38))
    d.line([(x0 + 16, table_y), (x1 - 16, table_y)], fill=INK, width=4)


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # page frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([17, 17, W - 18, H - 18], outline=INK, width=1)

    cx = W // 2

    # ---- masthead ------------------------------------------------------
    f_title = fit_font(d, "THE WORLD IN A DAY", F_SERIF_BOLD, 760, 62)
    text_c(d, cx, 26, "THE WORLD IN A DAY", f_title)
    d.line([(MARGIN, 100), (W - MARGIN, 100)], fill=INK, width=4)
    d.line([(MARGIN, 106), (W - MARGIN, 106)], fill=INK, width=1)

    f_date = fit_font(d, "TUESDAY 17 NOVEMBER 2026", F_SANS_BOLD, CW - 8, 88)
    text_c(d, cx, 116, "TUESDAY 17 NOVEMBER 2026", f_date, fill=RED)
    d.line([(MARGIN, 196), (W - MARGIN, 196)], fill=INK, width=3)

    # ---- lead story ----------------------------------------------------
    lead = (MARGIN, 208, W - MARGIN, 512)
    panel(d, lead)
    lx0, ly0, lx1, ly1 = lead
    f_head = font(F_SANS_BOLD, 43)
    lines = wrap(d, "UKRAINE STRIKES KERCH BRIDGE TO CRIMEA", f_head, CW - 32)
    y = ly0 + 12
    for ln in lines:
        text_c(d, cx, y, ln, f_head)
        y += line_h(f_head)
    f_deck = font(F_SANS, 20)
    deck = ("A road span collapses into the sea. Russia vows to rebuild "
            "the bridge -- and strikes Kyiv bridges in reply.")
    y += 2
    for ln in wrap(d, deck, f_deck, CW - 48):
        text_c(d, cx, y, ln, f_deck)
        y += line_h(f_deck)
    draw_bridge(d, (lx0 + 14, ly1 - 126, lx1 - 14, ly1 - 14))

    # ---- second story --------------------------------------------------
    sec = (MARGIN, 522, W - MARGIN, 694)
    panel(d, sec)
    sx0, sy0, sx1, sy1 = sec
    f_kick = font(F_SANS_BOLD, 16)
    text_l(d, sx0 + 16, sy0 + 12, "APEC SUMMIT · SHENZHEN", f_kick, fill=RED)
    f_head2 = font(F_SANS_BOLD, 31)
    y = sy0 + 38
    for ln in wrap(d, "TRUMP, XI AND PUTIN HOLD TRILATERAL TALKS",
                   f_head2, 520):
        text_l(d, sx0 + 16, y, ln, f_head2)
        y += line_h(f_head2)
    f_deck2 = font(F_SANS, 18)
    deck2 = ("Nuclear risks and Ukraine top the agenda. In Manila, Trump "
             "also signs a trade statement with Thailand.")
    for ln in wrap(d, deck2, f_deck2, 520):
        text_l(d, sx0 + 16, y, ln, f_deck2)
        y += line_h(f_deck2)
    draw_summit(d, (sx0 + 560, sy0 + 14, sx1 - 14, sy1 - 14))

    # ---- seven small panels --------------------------------------------
    grid_y0, grid_y1 = 704, 944
    row_h = (grid_y1 - grid_y0 - 8) // 2
    f_label = font(F_SANS_BOLD, 17)
    cells = []
    for r in range(2):
        n = 4 if r == 0 else 3
        cw = CW // n
        for c in range(n):
            x0 = MARGIN + c * cw
            x1 = x0 + cw - (8 if c < n - 1 else 0)
            y0 = grid_y0 + r * (row_h + 8)
            cells.append((x0, y0, x1, y0 + row_h))
    for (x0, y0, x1, y1), glyph, label in zip(cells, GLYPHS, LABELS):
        panel(d, (x0, y0, x1, y1), width=2)
        glyph(d, (x0 + (x1 - x0 - 110) // 2, y0 + 6,
                  x0 + (x1 - x0 + 110) // 2, y0 + 50))
        ly = y0 + 56
        for ln in wrap(d, label, f_label, (x1 - x0) - 16):
            text_c(d, (x0 + x1) // 2, ly, ln, f_label)
            ly += int(f_label.size * 1.15)

    # ---- bottom ticker ---------------------------------------------------
    tick = (MARGIN, 954, W - MARGIN, 1006)
    d.rectangle(tick, fill=INK)
    f_tick = font(F_SANS_BOLD, 16)
    text_c(d, cx, 962,
           "JPMORGAN BLAMES SOFTWARE BUG FOR BANK OUTAGE  •  "
           "US MEASLES CASES HIGHEST SINCE 1991", f_tick, fill=WHITE)
    text_c(d, cx, 984, "YEMEN GOVERNMENT RETREATS BEFORE HOUTHI ADVANCE",
           f_tick, fill=YELLOW)

    return img


def main():
    img = build()
    img.save(OUT_PATH, format="PNG")
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
