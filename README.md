# THE WORLD IN A DAY — Tuesday 17 November 2026 in one image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Sazharr911/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Sazharr911/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the make.fun bounty [Sum up 17 November's world news in one image](https://make.fun/bounty/news-image-20261117).

One image, drawn entirely in code: a broadsheet front page for
**TUESDAY 17 NOVEMBER 2026**, with the day's lead story, the Asia summit,
seven further stories in labelled panels, and a news ticker along the
bottom. Every fact is reproduced exactly as supplied in the competition
brief — no numbers, names or outcomes added.

## The day's stories, as drawn

- **Lead — Ukraine strikes the Kerch Bridge to Crimea.** A road span
  collapsed into the sea; Russia vows to rebuild and strikes Kyiv bridges
  in reply. *Source note: the day's lead story, per the competition brief;
  drawn as the large bridge panel under the masthead.*
- **Trump in Asia.** APEC summit in Shenzhen: Trump, Xi and Putin hold
  trilateral talks on nuclear risks and Ukraine; in Manila, Trump also
  signed a trade statement with Thailand. *Source note: second story, per
  the brief; drawn as three leaders at a summit table with US, Chinese and
  Russian flags.*
- **Tankers hit mines in Hormuz.** Two tankers hit naval mines in the
  Strait of Hormuz; a third US carrier arrives. *Source note: brief item 1;
  panel glyph: tanker, naval mine, burst.*
- **Nvidia's first earnings after Huang.** Nvidia reports its first
  earnings since Jensen Huang's exit; the US tightens AI chip export
  curbs. *Source note: brief item 2; panel glyph: microchip and rising
  chart.*
- **Europe's Rwanda return hub.** Five European nations unveil a joint
  Rwanda return hub for rejected asylum seekers. *Source note: brief
  item 3; panel glyph: aircraft and return arrow.*
- **Japan scrambles jets at Russia.** Japan scrambles fighter jets after
  Russian aircraft violate its airspace. *Source note: brief item 4; panel
  glyph: fighter jet over the rising sun.*
- **Vulcan failure: 40 satellites lost.** A ULA Vulcan rocket fails in
  flight, destroying 40 Amazon Leo satellites. *Source note: brief item 5;
  panel glyph: rocket, burst, falling satellites.*
- **West to Israel: open Gaza aid.** The UK, Australia, Canada and Italy
  urge Israel to open Gaza crossings for aid. *Source note: brief item 6;
  panel glyph: aid truck with red cross.*
- **UN: 1,390 Sudan civilians killed.** A UN report counts at least 1,390
  civilians killed in Sudan in the first half of 2026. *Source note: brief
  item 7; panel glyph: memorial candle.*
- **Ticker.** JPMorgan blames a software bug for a bank outage · US
  measles cases highest since 1991 · Yemen's government retreats before a
  Houthi advance. *Source note: the brief's three ticker items, run along
  the foot of the page.*

## How to run

```sh
python3 main.py
```

Writes `/output/entry.png` (override with the `MAKEFUN_OUT` environment
variable). `main.py` is a **stdlib-only copier**: the competition's
server runtime has no Pillow and no system fonts, so `main.py` does no
drawing — it copies the pre-rendered `entry.png` committed next to it to
the output path and exits 0. It needs nothing beyond Python 3's standard
library.

The image itself is generated at build time by `draw.py`:

```sh
python3 draw.py
```

`draw.py` is the drawing program (Pillow/PIL + the DejaVu fonts in
`/usr/share/fonts/truetype/dejavu/`, run locally only — never on the
server) and writes `entry.png` in this repo. The drawing is fully
deterministic — fixed geometry, no randomness, no clock, no network —
so repeated runs produce a byte-identical PNG.

The committed `entry.png` is that output: 1024 × 1024 px PNG, 95,801
bytes, sha256
`6e311451a87e1f3307eafccb871a27b422eecf8a3b851f71c56053d918cdccb9`.
