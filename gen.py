#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image: THE DAY IN ONE MAP.

Original layout (not a front page): a stylised world map pins the
day's stories to where they happened, numbered 1-5, with the
headline cards underneath and a full-width GTA VI sales band
between map and cards. Every fact was checked against live news
reports of Friday 20 November 2026 before drawing.

Stories (all 20 Nov 2026):
  1. Trump delays any Iran decision to 2027 ("see what happens
     after Jan 1") - Reuters / Times of India.
  2. Cyclone Akvan makes landfall in Odisha today; 300,000 people
     evacuated to 9,341 shelters; winds 90-100 km/h, gusts 110 -
     ANI / The Hindu / IMD.
  3. Europe ready for talks with Russia on ending the Ukraine war
     - BBC.
  4. Hayabusa2's asteroid landing called off: all ion engines
     failed; JAXA retargets to asteroid 2015BM510 in fiscal 2028 -
     Space / JAXA.
  5. Haiti police kill 34 gang members in a capital raid -
     Al Jazeera.
  6. GTA VI tops $1.84bn (Sensor Tower ESTIMATE, not official):
     19.05m copies on day one, passing The Odyssey's $1.80bn;
     PS5 14.23m / $1.38bn, Xbox 4.82m / $464m; ~6m watched the
     launch livestreams - Mezha / GameSpot / USA Today.

Run: python3 gen.py   (writes entry.png next to this file)
Requires Pillow + DejaVu fonts on this build machine only; the
submitted program (main.ts) just copies the finished PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (14, 27, 51)        # banner + footer
NAVY2 = (20, 38, 66)
GOLD = (224, 178, 90)
OCEAN = (22, 52, 84)       # map sea
OCEAN_LT = (30, 66, 102)
LAND = (216, 201, 163)     # map land
LAND_EDGE = (178, 162, 122)
PAPER = (247, 243, 234)    # cards background
INK = (22, 22, 34)
SLATE = (84, 96, 120)
WHITE = (255, 255, 255)
PIN_RED = (192, 57, 43)
PIN_TEAL = (14, 124, 123)
PIN_BLUE = (31, 78, 121)
PIN_PURPLE = (108, 52, 131)
PIN_ORANGE = (185, 90, 27)

MAP_TOP, MAP_BOT = 132, 580
MAP_H = MAP_BOT - MAP_TOP
LAT_TOP, LAT_BOT = 83.0, -58.0


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)


def proj(lon, lat):
    """Equirectangular projection into the map rectangle."""
    x = (lon + 180.0) / 360.0 * W
    y = MAP_TOP + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return (x, y)


# ---------------------------------------------------------------- continents
# Simplified lon/lat outlines, drawn as a stylised atlas map.
NORTH_AMERICA = [
    (-168, 66), (-162, 70), (-152, 70), (-140, 70), (-130, 68),
    (-125, 60), (-124, 49), (-120, 42), (-114, 32), (-108, 25),
    (-105, 22), (-97, 26), (-93, 20), (-90, 21), (-87, 15),
    (-83, 9), (-79, 9), (-80, 12), (-83, 15), (-86, 16),
    (-88, 21), (-91, 19), (-95, 19), (-97, 26), (-93, 29),
    (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35),
    (-74, 40), (-70, 42), (-66, 44), (-60, 47), (-55, 52),
    (-59, 55), (-64, 58), (-68, 58), (-73, 62), (-78, 62),
    (-85, 66), (-92, 66), (-95, 69), (-105, 68), (-115, 68),
    (-125, 70), (-135, 69), (-145, 70), (-155, 71), (-165, 68),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
    (-25, 70), (-20, 74), (-25, 78), (-35, 80), (-45, 81),
    (-55, 80), (-60, 76), (-58, 70),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 7), (-75, 10), (-72, 12), (-64, 10),
    (-60, 8), (-54, 6), (-52, 5), (-50, 0), (-44, -3),
    (-38, -5), (-35, -8), (-37, -13), (-40, -20), (-41, -23),
    (-48, -27), (-53, -33), (-58, -35), (-62, -39), (-65, -41),
    (-66, -45), (-68, -50), (-70, -54), (-74, -53), (-73, -45),
    (-73, -37), (-72, -28), (-70, -20), (-75, -15), (-77, -12),
    (-80, -6), (-81, -1), (-80, 2),
]
EUROPE = [
    (-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 47), (-4, 49),
    (-1, 50), (2, 51), (4, 53), (7, 54), (8, 57), (10, 59),
    (12, 58), (18, 56), (21, 55), (24, 58), (27, 59), (30, 60),
    (30, 64), (28, 68), (25, 71), (22, 70), (18, 69), (15, 68),
    (12, 65), (10, 64), (6, 62), (5, 59), (7, 58), (10, 57),
    (8, 55), (5, 53), (0, 51), (-3, 50), (-5, 48), (-2, 47),
    (-5, 44), (-9, 43), (-10, 39), (-9, 37),
]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57),
      (0, 53), (1, 51), (-2, 50)]
ICELAND = [(-22, 64), (-18, 63), (-15, 64), (-14, 66),
           (-18, 66), (-22, 65)]
AFRICA = [
    (-6, 35), (-10, 31), (-15, 28), (-17, 21), (-17, 15),
    (-16, 12), (-13, 9), (-8, 5), (-4, 5), (6, 4), (9, 4),
    (12, 0), (13, -5), (12, -10), (13, -15), (12, -18),
    (14, -22), (16, -28), (18, -32), (20, -35), (25, -34),
    (28, -33), (32, -29), (35, -25), (36, -20), (40, -16),
    (40, -11), (42, -5), (46, -2), (51, 2), (51, 11),
    (48, 11), (44, 11), (42, 13), (40, 15), (39, 18),
    (37, 20), (35, 23), (34, 27), (32, 31), (30, 32),
    (25, 32), (20, 33), (15, 33), (11, 34), (10, 37),
    (5, 37), (-1, 35),
]
ASIA = [
    (28, 41), (30, 36), (33, 36), (36, 36), (39, 38),
    (42, 41), (44, 39), (48, 38), (50, 37), (50, 30),
    (52, 28), (54, 27), (56, 26), (58, 25), (61, 25),
    (63, 25), (66, 25), (68, 23), (70, 22), (72, 20),
    (73, 16), (75, 12), (77, 8), (78, 10), (80, 13),
    (82, 16), (85, 19), (88, 22), (91, 22), (92, 20),
    (94, 17), (96, 16), (98, 15), (100, 13), (101, 9),
    (103, 5), (104, 2), (103, 1), (104, 6), (105, 9),
    (107, 11), (109, 13), (109, 16), (108, 18), (106, 20),
    (108, 21), (110, 20), (112, 21), (114, 22), (116, 23),
    (118, 25), (120, 27), (120, 30), (122, 31), (121, 34),
    (120, 36), (122, 38), (124, 40), (126, 40), (128, 38),
    (130, 42), (132, 43), (134, 44), (136, 44), (138, 46),
    (140, 47), (141, 50), (142, 53), (141, 56), (141, 59),
    (140, 60), (143, 59), (146, 59), (150, 60), (156, 59),
    (158, 56), (160, 55), (162, 58), (162, 60), (166, 60),
    (170, 61), (173, 62), (178, 65), (178, 68), (175, 70),
    (170, 70), (165, 68), (160, 70), (155, 70), (150, 71),
    (145, 72), (140, 72), (135, 72), (130, 72), (125, 73),
    (120, 73), (115, 73), (110, 74), (105, 76), (100, 77),
    (95, 76), (90, 75), (85, 74), (80, 73), (75, 72),
    (70, 72), (65, 69), (60, 69), (55, 68), (50, 68),
    (45, 68), (40, 67), (35, 66), (32, 67), (30, 70),
    (28, 65), (28, 55), (28, 45),
]
AUSTRALIA = [
    (114, -22), (113, -26), (115, -32), (118, -35), (122, -34),
    (126, -32), (129, -32), (132, -32), (135, -35), (137, -35),
    (139, -37), (141, -38), (144, -38), (147, -39), (150, -37),
    (152, -34), (153, -31), (153, -27), (151, -24), (149, -20),
    (146, -19), (144, -15), (142, -11), (141, -13), (139, -15),
    (137, -12), (136, -15), (135, -15), (132, -12), (130, -13),
    (128, -14), (126, -14), (124, -16), (122, -17), (120, -19),
    (117, -20),
]
TASMANIA = [(145, -41), (148, -41), (148, -43), (146, -43), (145, -42)]
NEW_ZEALAND = [
    (167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
    (178, -37), (176, -40), (174, -41), (172, -43), (169, -44),
]
JAPAN = [
    (130, 31), (131, 32), (133, 34), (135, 34), (136, 35),
    (138, 35), (139, 35), (140, 36), (141, 38), (141, 40),
    (141, 42), (142, 43), (143, 43), (144, 44), (143, 42),
    (142, 41), (141, 39), (140, 37), (139, 36), (137, 35),
    (135, 34), (133, 33), (131, 32),
]
BORNEO = [
    (109, 1), (111, 3), (113, 5), (116, 6), (118, 2),
    (119, -1), (117, -3), (114, -4), (111, -3), (109, 0),
]
SUMATRA = [
    (95, 5), (98, 3), (100, 0), (102, -2), (104, -4),
    (106, -6), (104, -5), (101, -1), (98, 2),
]
NEW_GUINEA = [
    (131, -1), (134, -2), (137, -3), (140, -4), (143, -5),
    (146, -6), (149, -8), (150, -10), (147, -9), (144, -8),
    (141, -8), (138, -7), (136, -4), (133, -2),
]
MADAGASCAR = [
    (44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
    (45, -25), (43, -22), (43, -18),
]
CUBA = [
    (-85, 23), (-80, 23), (-77, 21), (-74, 20), (-77, 21),
    (-80, 22), (-84, 22),
]
HISPANIOLA = [
    (-74, 20), (-72, 19), (-71, 18), (-69, 18), (-72, 19),
    (-74, 19),
]
CONTINENTS = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, UK, ICELAND,
    AFRICA, ASIA, AUSTRALIA, TASMANIA, NEW_ZEALAND, JAPAN,
    BORNEO, SUMATRA, NEW_GUINEA, MADAGASCAR, CUBA, HISPANIOLA,
]

# ---------------------------------------------------------------- stories
# (number, pin lon, pin lat, colour, headline, sub-line)
STORIES = [
    (1, -77, 39, PIN_RED,
     "TRUMP: NO RUSH ON IRAN",
     "\u201cSee what happens after Jan 1\u201d \u2014 decision waits until 2027"),
    (2, 85.5, 20, PIN_TEAL,
     "AKVAN HITS ODISHA TODAY",
     "300,000 evacuated to 9,341 shelters; winds to 110 km/h"),
    (3, 9, 51, PIN_BLUE,
     "EUROPE READY TO TALK TO RUSSIA",
     "On ending the Ukraine war \u2014 BBC"),
    (4, 136.5, 37, PIN_PURPLE,
     "HAYABUSA2 LANDING CALLED OFF",
     "All ion engines failed; JAXA retargets to asteroid 2015BM510 in 2028"),
    (5, -72.3, 18.9, PIN_ORANGE,
     "HAITI POLICE KILL 34 GANG MEMBERS",
     "PORT-AU-PRINCE \u2014 Capital raid, Al Jazeera reports"),
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, fnt, fill):
    """Draw text with wide letter spacing (for small caps labels)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + 4


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- banner
    d.rectangle([0, 0, W, MAP_TOP], fill=NAVY)
    spaced(d, (512 - 175, 16), "THE WORLD IN ONE DAY", BOLD(26), GOLD)
    d.text((512, 52), "FRIDAY 20 NOVEMBER 2026", font=BOLD(54),
           fill=WHITE, anchor="ma")
    d.rectangle([0, MAP_TOP - 4, W, MAP_TOP], fill=GOLD)

    # ---------------------------------------------------------- map
    d.rectangle([0, MAP_TOP, W, MAP_BOT], fill=OCEAN)
    # graticule
    for lon in range(-150, 181, 30):
        x = (lon + 180) / 360 * W
        d.line([(x, MAP_TOP), (x, MAP_BOT)], fill=OCEAN_LT, width=1)
    for lat in range(-60, 91, 30):
        y = MAP_TOP + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
        d.line([(0, y), (W, y)], fill=OCEAN_LT, width=1)
    # continents
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # ocean labels
    oc = (126, 158, 190)
    spaced(d, proj(-158, -2), "PACIFIC OCEAN", BOLD(17), oc)
    spaced(d, proj(-38, 12), "ATLANTIC OCEAN", BOLD(17), oc)
    spaced(d, proj(72, -34), "INDIAN OCEAN", BOLD(17), oc)
    # pins (numbered, on top of the land)
    for num, lon, lat, colour, _h, _s in STORIES:
        x, y = proj(lon, lat)
        d.ellipse([x - 18, y - 15, x + 18, y + 21], fill=(10, 30, 52))
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=colour,
                  outline=WHITE, width=3)
        d.text((x, y - 1), str(num), font=BOLD(22), fill=WHITE,
               anchor="mm")
    d.rectangle([0, MAP_BOT - 4, W, MAP_BOT], fill=GOLD)

    # ---------------------------------------------------------- GTA band
    BAND_TOP, BAND_BOT = MAP_BOT, 736
    for yy in range(BAND_TOP, BAND_BOT):
        t = (yy - BAND_TOP) / (BAND_BOT - BAND_TOP)
        r = int(38 + (122 - 38) * t)
        g = int(16 + (28 - 16) * t)
        b = int(64 + (86 - 64) * t)
        d.line([(0, yy), (W, yy)], fill=(r, g, b))
    d.text((32, BAND_TOP + 12), "CULTURE  \u00b7  VICE CITY  \u00b7  DAY TWO",
           font=BOLD(19), fill=GOLD)
    d.text((32, BAND_TOP + 36), "GTA VI TOPS $1.84bn",
           font=BOLD(58), fill=WHITE)
    d.text((32, BAND_TOP + 102),
           "Sensor Tower estimate \u2014 19.05m copies on day one, passing The Odyssey\u2019s $1.80bn",
           font=REG(23), fill=(235, 225, 255))
    d.text((32, BAND_TOP + 128),
           "PS5 14.23m \u00b7 $1.38bn    |    Xbox 4.82m \u00b7 $464m    |    ~6m watched the launch streams",
           font=REG(20), fill=(205, 195, 235))

    # ---------------------------------------------------------- story cards
    d.rectangle([0, BAND_BOT, W, H], fill=PAPER)
    margin, gutter = 16, 12
    col_w = (W - 2 * margin - 2 * gutter) // 3
    row1_y, row_h = 744, 120
    row2_y = 872
    wide_w = (W - 2 * margin - gutter) // 2

    def card(x, y, w, h, num, colour, headline, sub):
        d.rectangle([x, y, x + w, y + h], fill=WHITE,
                    outline=(200, 192, 172), width=2)
        d.rectangle([x, y, x + w, y + 6], fill=colour)
        # number chip
        cx, cy = x + 26, y + 32
        d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=colour)
        d.text((cx, cy - 1), str(num), font=BOLD(20), fill=WHITE,
               anchor="mm")
        tx = x + 48
        head_lines = wrap(d, headline, BOLD(24), w - 60)
        hy = y + 12
        for line in head_lines[:2]:
            d.text((tx, hy), line, font=BOLD(24), fill=INK)
            hy += 28
        sub_lines = wrap(d, sub, REG(17), w - 24)
        sy = y + h - 6 - 20 * min(len(sub_lines), 2)
        for line in sub_lines[:2]:
            d.text((x + 12, sy), line, font=REG(17), fill=SLATE)
            sy += 20

    for i in range(3):
        num, _lo, _la, colour, head, sub = STORIES[i]
        card(margin + i * (col_w + gutter), row1_y, col_w, row_h,
             num, colour, head, sub)
    for j in range(2):
        num, _lo, _la, colour, head, sub = STORIES[3 + j]
        card(margin + j * (wide_w + gutter), row2_y, wide_w, row_h,
             num, colour, head, sub)

    # ---------------------------------------------------------- footer
    d.rectangle([0, 996, W, H], fill=NAVY)
    d.text((512, 1005),
           "Sources, 20 Nov 2026: Reuters \u00b7 Times of India \u00b7 ANI \u00b7 The Hindu \u00b7 IMD \u00b7 BBC \u00b7 Space / JAXA \u00b7 Al Jazeera",
           font=REG(15), fill=(200, 210, 225), anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
