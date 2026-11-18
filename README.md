# THE WORLD IN A DAY — Tuesday 17 November 2026 in one image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Sazharr911/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Sazharr911/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the make.fun bounty [Sum up 17 November's world news in one image](https://make.fun/bounty/news-image-20261117).

One image, drawn entirely in code: a broadsheet front page for
**TUESDAY 17 NOVEMBER 2026** carrying **43 stories from 6 continents** —
14 numbered, illustrated panels, a world map with numbered pins showing
where each panel story happened, and a 29-item "ALSO ON TUESDAY
17 NOVEMBER" list. Stories were researched from the day's reporting
(Level Headlines' Daily Brief, Asas Press's World News Digest and story
pages, and BBC/Reuters/AP-style feeds); contested claims are attributed
on the page ("Ukraine says", "Russia: says it downed…"). The full
research notes are in `STORIES.md`.

## The day's stories, as drawn

**Top row**

1. **Europe · Ukraine war** — Ukraine says a Crimean (Kerch) Bridge road
   span fell into the sea; a second strike in two days.
2. **Middle East · Iran war** — Iran sends drones at a US radar site in
   Bahrain; all downed, US jets strike Qeshm; Iran says tankers hit
   mines in Hormuz.
3. **Asia · Diplomacy** — Trump holds his first Quad summit, in Manila;
   critical-minerals deals; Putin reaches Shenzhen.

**Panels 4–13**

4. **Africa · Health** — Ebola cases in DR Congo top 11,000 (WHO);
   about 5,400 deaths.
5. **Global · Climate** — COP31 in Antalya divided over a fossil-fuel
   phase-out draft.
6. **Americas · Health** — US, Mexico and Bolivia lose measles-free
   status (PAHO); the US counts 5,400+ cases in 2026.
7. **Americas · Business** — Nvidia's quarterly sales double to
   $115.8bn; the Dow fell 849 points earlier.
8. **Middle East · Gaza** — Gaza truce at risk of collapse, the UN is
   told; 1.4m face acute hunger; winter aid held up.
9. **Asia · Politics** — Mongolia's president says he will resign;
   denies a $25m railway claim.
10. **Europe · Politics** — Serbia's student-led list takes 140 of 250
    seats as the new parliament is sworn in.
11. **Asia · Labour** — Bangladesh police tear-gas garment workers
    demanding Tk 30,000 a month; dozens of factories shut.
12. **Asia · Air crash** — Russian An-12 crashes near Kemerovo, Siberia;
    all 19 aboard killed.
13. **Africa · Justice** — Mozambique puts opposition leader Venâncio
    Mondlane on trial on 5 charges.

**Strip**

14. **Global · Space** — Voyager 1 reaches one light-day from Earth,
    the first spacecraft to do so.

**Also on Tuesday (15–43)** — Kyiv's Dnipro bridges hit · Russia's
record 1,441 drones claim · UN: Ukraine civilian deaths top all of
2025 · Prague train collision, 46 injured · France strike: 146,000
march (CGT: 500,000) · Tusk survives no-confidence vote · Deutsche Bank
falls on data leak · Moldova shuts airspace · Sözcü TV seized · Kahana
elected Knesset speaker 66–52 · West Bank settler killing · Yemen
government retreat · Araghchi in Oman · Japan protests Russian airspace
intrusion · ~4m Syrians returned · Jordan and Iraq block Telegram ·
Cyclone Akvan · Uttarakhand bus crash, 8 dead · China–Canada tariff
cuts · Macron in Malaysia · Thailand to scrap US tariffs · IMF lifts
South Korea to 3.9% · WFP aids 30,000 in Kenya · Norway 3–2 Denmark
(Haaland twice) · India 2–1 Pakistan, SAFF final · Togo 3–0 Algeria ·
Pope Leo XIV ends South America tour · Australia eases backpacker visa
curbs · Apple services outage.

## How to run

```sh
python3 main.py
```

Writes `/output/entry.png` (override with the `MAKEFUN_OUT` environment
variable). `main.py` is a **stdlib-only copier**: the competition's
server runtime has no Pillow and no system fonts, so `main.py` does no
drawing — it verifies the committed `entry.png` (integrity, 1024×1024
dimensions, the 1 MiB competition cap), copies it to the output path,
verifies the copy byte-for-byte, and exits 0. It needs nothing beyond
Python 3's standard library.

The image itself is generated at build time by `draw.py`:

```sh
python3 draw.py
```

`draw.py` is the drawing program (Pillow/PIL + the DejaVu fonts in
`/usr/share/fonts/truetype/dejavu/`, run locally only — never on the
server) and writes `entry.png` in this repo. The drawing is fully
deterministic — fixed geometry, no randomness, no clock, no network —
so repeated runs produce a byte-identical PNG.

The committed `entry.png` is that output: 1024 × 1024 px PNG, 225,554
bytes, sha256
`3e069795f1fb087e6edc5614864f21fde1365d3cd2eb220ddadaf005a6ac89d3`.
