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

LAYOUT (round 3): the page is built for legibility at thumbnail size.
One dominant lead with a big bridge illustration, one second story, and
five panels with large headlines (28-32 px) and at most two short
summary lines each. Nothing on the page is set below 16 px.
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


def block_c(draw, cx, y, text, f, max_w, lh=None, fill=INK):
    """Wrap text and draw it centred, one line under another.

    Returns the y just past the last line.
    """
    if lh is None:
        lh = line_h(f)
    for ln in wrap(draw, text, f, max_w):
        text_c(draw, cx, y, ln, f, fill=fill)
        y += lh
    return y


def block_l(draw, x, y, text, f, max_w, lh=None, fill=INK):
    """Wrap text and draw it left-aligned. Returns the y past the end."""
    if lh is None:
        lh = line_h(f)
    for ln in wrap(draw, text, f, max_w):
        text_l(draw, x, y, ln, f, fill=fill)
        y += lh
    return y


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
    for cx, cy, s in [(x0 + 90, y0 + 16, 1), (x0 + 300, y0 + 10, 0),
                      (x1 - 120, y0 + 14, 1)]:
        d.ellipse([cx - 34 - s * 8, cy - 10, cx + 34 + s * 8, cy + 12],
                  fill=WHITE)
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
    for sx, sy in [(x0 + 636, y1 - 30), (x0 + 700, y1 - 16),
                   (x0 + 600, y1 - 12)]:
        d.arc([sx - 20, sy - 12, sx + 20, sy + 12], start=180, end=360,
              fill=WHITE, width=4)
    for wx in range(x0 + 30, x1 - 30, 64):
        d.arc([wx, y1 - 14, wx + 30, y1 - 2], start=180, end=360,
              fill=WHITE, width=3)


def draw_summit(d, box):
    """Second-story art: three leaders at a summit table, flags behind."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    centres = [cx - 108, cx, cx + 108]
    flag_y0, flag_y1 = y0 + 2, y0 + 40
    # flags: USA, China, Russia
    for i, fx in enumerate(centres):
        fw = 58
        fx0, fx1 = fx - fw // 2, fx + fw // 2
        d.line([(fx, flag_y0), (fx, y1 - 42)], fill=GREY, width=3)
        if i == 0:  # USA: stripes + blue canton
            d.rectangle([fx0, flag_y0, fx1, flag_y1], fill=WHITE, outline=INK)
            for s in range(0, 38, 11):
                d.rectangle([fx0, flag_y0 + s, fx1, flag_y0 + s + 5], fill=RED)
            d.rectangle([fx0, flag_y0, fx0 + 24, flag_y0 + 18], fill=DARK_BLUE)
        elif i == 1:  # China: red field, yellow stars
            d.rectangle([fx0, flag_y0, fx1, flag_y1], fill=RED, outline=INK)
            d.ellipse([fx0 + 6, flag_y0 + 5, fx0 + 15, flag_y0 + 14],
                      fill=YELLOW)
            for sx, sy in [(19, 3), (23, 10), (19, 17)]:
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
    head_y = y0 + 50
    for fx in centres:
        d.ellipse([fx - 16, head_y, fx + 16, head_y + 32], fill=INK)
        d.pieslice([fx - 35, head_y + 22, fx + 35, head_y + 82], start=180,
                   end=360, fill=INK)
    # table
    table_y = y0 + 96
    d.polygon([(x0 + 14, table_y), (x1 - 14, table_y), (x1 - 30, y1 - 4),
               (x0 + 30, y1 - 4)], fill=(96, 66, 38))
    d.line([(x0 + 14, table_y), (x1 - 14, table_y)], fill=INK, width=4)


# --------------------------------------------------------------------------
# Page content
# --------------------------------------------------------------------------

LEAD_HEADLINE = "UKRAINE STRIKES KERCH BRIDGE TO CRIMEA"
LEAD_DECK = ("A road span collapses into the sea. Russia vows to rebuild "
             "the bridge -- and strikes Kyiv bridges in reply.")

SECOND_KICKER = "APEC SUMMIT · SHENZHEN"
SECOND_HEADLINE = "TRUMP, XI AND PUTIN HOLD TRILATERAL TALKS"
SECOND_DECK = ("Nuclear risks and Ukraine top the agenda. In Manila, "
               "Trump also signs a trade statement with Thailand.")

# Five panels: (headline, summary). The narrow top row takes the
# headlines whose two-line splits fit its width; the wide bottom row
# takes the two longest. Regional spread: Hormuz and Gaza (Middle
# East), Japan/Russia (Asia-Pacific), Europe, space.
PANELS_TOP = [
    ("TANKERS HIT MINES IN HORMUZ",
     "Two tankers hit mines in the strait; a third US carrier "
     "arrives."),
    ("JAPAN SCRAMBLES JETS AT RUSSIA",
     "Jets scramble after Russian aircraft violate its airspace."),
    ("WEST TO ISRAEL: OPEN GAZA AID",
     "UK, Australia, Canada and Italy urge Israel to open "
     "crossings."),
]
PANELS_BOTTOM = [
    ("EUROPE'S RWANDA RETURN HUB",
     "Five nations unveil a joint hub for rejected asylum seekers."),
    ("VULCAN FAILURE: 40 SATELLITES LOST",
     "A ULA Vulcan rocket fails in flight, destroying 40 Amazon "
     "Leo satellites."),
]

TICKER_1 = ("JPMORGAN BLAMES SOFTWARE BUG FOR BANK OUTAGE  •  "
            "US MEASLES HIGHEST SINCE 1991")
TICKER_2 = "UN: 1,390 SUDAN CIVILIANS KILLED"


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------

def story_panel(d, box, headline, summary, head_size, sum_size):
    """One news panel: big centred headline, up to two summary lines."""
    x0, y0, x1, y1 = box
    panel(d, box, width=2)
    cx = (x0 + x1) // 2
    inner_w = (x1 - x0) - 16
    f_head = font(F_SANS_BOLD, head_size)
    y = y0 + 11
    y = block_c(d, cx, y, headline, f_head, inner_w,
                lh=int(head_size * 1.13))
    y += 5
    f_sum = font(F_SANS, sum_size)
    block_c(d, cx, y, summary, f_sum, inner_w, lh=int(sum_size * 1.22))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # page frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([17, 17, W - 18, H - 18], outline=INK, width=1)

    cx = W // 2

    # ---- masthead ------------------------------------------------------
    f_title = fit_font(d, "THE WORLD IN A DAY", F_SERIF_BOLD, 760, 62)
    text_c(d, cx, 24, "THE WORLD IN A DAY", f_title)
    d.line([(MARGIN, 98), (W - MARGIN, 98)], fill=INK, width=4)
    d.line([(MARGIN, 104), (W - MARGIN, 104)], fill=INK, width=1)

    f_date = fit_font(d, "TUESDAY 17 NOVEMBER 2026", F_SANS_BOLD, CW - 8, 88)
    text_c(d, cx, 112, "TUESDAY 17 NOVEMBER 2026", f_date, fill=RED)
    d.line([(MARGIN, 196), (W - MARGIN, 196)], fill=INK, width=3)

    # ---- lead story ----------------------------------------------------
    lead = (MARGIN, 208, W - MARGIN, 500)
    panel(d, lead)
    lx0, ly0, lx1, ly1 = lead
    f_head = font(F_SANS_BOLD, 50)
    y = block_c(d, cx, ly0 + 14, LEAD_HEADLINE, f_head, CW - 48, lh=60)
    f_deck = font(F_SANS, 21)
    y = block_c(d, cx, y + 6, LEAD_DECK, f_deck, CW - 68, lh=26)
    draw_bridge(d, (lx0 + 14, y + 8, lx1 - 14, ly1 - 12))

    # ---- second story --------------------------------------------------
    sec = (MARGIN, 510, W - MARGIN, 672)
    panel(d, sec)
    sx0, sy0, sx1, sy1 = sec
    f_kick = font(F_SANS_BOLD, 17)
    text_l(d, sx0 + 16, sy0 + 12, SECOND_KICKER, f_kick, fill=RED)
    f_head2 = font(F_SANS_BOLD, 32)
    y = block_l(d, sx0 + 16, sy0 + 38, SECOND_HEADLINE, f_head2, 590, lh=38)
    f_deck2 = font(F_SANS, 18)
    block_l(d, sx0 + 16, y + 2, SECOND_DECK, f_deck2, 590, lh=22)
    draw_summit(d, (sx0 + 634, sy0 + 14, sx1 - 14, sy1 - 14))

    # ---- five panels: three over two ------------------------------------
    top_y0, top_y1 = 682, 808
    bot_y0, bot_y1 = 818, 946
    n = len(PANELS_TOP)
    pw = (CW - (n - 1) * 8) // n
    for i, (headline, summary) in enumerate(PANELS_TOP):
        x0 = MARGIN + i * (pw + 8)
        x1 = x0 + pw if i < n - 1 else W - MARGIN
        story_panel(d, (x0, top_y0, x1, top_y1), headline, summary, 28, 17)
    n = len(PANELS_BOTTOM)
    pw = (CW - (n - 1) * 8) // n
    for i, (headline, summary) in enumerate(PANELS_BOTTOM):
        x0 = MARGIN + i * (pw + 8)
        x1 = x0 + pw if i < n - 1 else W - MARGIN
        story_panel(d, (x0, bot_y0, x1, bot_y1), headline, summary, 32, 17)

    # ---- bottom ticker ---------------------------------------------------
    tick = (MARGIN, 956, W - MARGIN, 1000)
    d.rectangle(tick, fill=INK)
    f_tick1 = fit_font(d, TICKER_1, F_SANS_BOLD, CW - 16, 19)
    text_c(d, cx, 959, TICKER_1, f_tick1, fill=WHITE)
    f_tick2 = font(F_SANS_BOLD, 21)
    text_c(d, cx, 979, TICKER_2, f_tick2, fill=YELLOW)

    return img


def main():
    img = build()
    img.save(OUT_PATH, format="PNG")
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
