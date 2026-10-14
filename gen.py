"""Generate animated SVG assets for the Demcruise GitHub profile README.

Run:  python gen.py   (writes into ./assets)
Pure CSS animations -> render fine inside GitHub's <img> sandbox.
The header banner is a GIF rendered with Remotion (see ./banner).
"""
import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CJK = "'Hiragino Sans','Yu Gothic','Microsoft YaHei','Noto Sans CJK JP',sans-serif"
BG = "#0d1117"
PURPLE = "#a78bfa"
CYAN = "#22d3ee"
PINK = "#f472b6"
YELLOW = "#fde047"
TEXT = "#e6edf3"
MUTED = "#8b949e"

# --------------------------------------------------------- Osaragi sprite ----
# Pixel-art chibi inspired by Osaragi (Sakamoto Days) — original fan-art,
# same palette as the Remotion banner (banner/src/sprite.ts).
PAL = {
    "K": "#1a1420",  # outline
    "H": "#24202c",  # hair
    "h": "#3d3749",  # hair shine
    "V": "#e9e4f2",  # veil lace
    "v": "#8e86a3",  # veil shade over hair
    "S": "#fbefe3",  # skin
    "s": "#eccfbd",  # skin shade
    "P": "#f3a5a5",  # blush
    "e": "#8d8b98",  # iris ring
    "E": "#2b2a35",  # pupil
    "w": "#ffffff",  # highlight
    "D": "#2b2639",  # sheer dress
    "d": "#453f57",  # dress mesh light
    "x": "#151219",  # dress pattern lines
    "L": "#3a3448",  # tights
    "B": "#f6f7fb",  # bowl white
    "b": "#2f50a8",  # bowl blue
    "c": "#c9d2ea",  # bowl shade
    "N": "#f6e2a0",  # noodles
    "n": "#d9bf74",  # noodle shade
    "C": "#7a5236",  # chopsticks
    "R": "#b8434a",  # open mouth
    "O": "#fff4df",  # sticker outline
    "G": "#1f2a1f",  # nori
}


def mirror(half, width):
    """Pad each left-half row to width/2 and mirror it into a full row."""
    n = width // 2
    rows = []
    for h in half:
        left = h.rjust(n, ".")[-n:]
        rows.append(left + left[::-1])
    return rows


# big bust (36 x 32) — same art as the banner
BUST = mirror([
    "............KKKKKK",
    ".........KKKVvvHHH",
    ".......KKVvHHHHHHH",
    "......KVvHHHHHHHHH",
    ".....KVvHHhhHHHHHH",
    "....KVvHHHHHhhHHHH",
    "....KVHHHHHHHHHHHH",
    "...KVvHHHHHHHHHHHH",
    "...KVHHHHKKKKKKKKK",
    "..KVvHHHKSSSSSSSSS",
    "..KVHHHKSSeeeeSSSS",
    "..KVHHHKSeEEEEeSSS",
    "..KVHHHKSeEwEEeSSS",
    "..KVHHHKSeEEEEeSSS",
    "..KVHHHKSSeeeeSSSS",
    ".KVvHHHKsPPSSSSSSS",
    ".KVHHHHKSSSSSSSSSS",
    ".KVHHHHHKSSSSSSSSS",
    ".KVHHHHHHKsSSSSSSS",
    ".KVHHHHHHHKKKKKSSS",
    ".KVHHHHHHKDDDDDxDD",
    ".KVHHHHHKDDdDDDDxD",
    "KVvHHHHKDDdDxDDDDx",
    "KVHHHHKDdDDDDxDDDD",
    "KVHHHHKDDDxDDDDxDD",
    "KVHHHHKDDxDDDDDDxD",
    "KVHHHHKDDDDdDDDDDD",
    "KVHHHHKDDDDDDdDDDD",
    "KVHHHKDDDDDDDDDDDD",
    "KVHHHKDDDDDDDDDDDD",
    "KHHHHKDDDDDDDDDDDD",
    "KHHHHKDDDDDDDDDDDD",
], 36)

BUST_BOWL = (11, 22, [
    ".KKKKKKKKKKKK.",
    "KcNnNNnNNnNNcK",
    "KBBBBBBBBBBBBK",
    "KbbbbbBBbbbbbK",
    "KbbbbBBBBbbbbK",
    ".KbbbbBBbbbbK.",
    "..KBBBBBBBBK..",
    "...KKKKKKKK...",
])
BUST_LEFT_HAND = (24, 24, ["KSSK", "SSSK", "SSSK", "KKK."])
BUST_SMILE = (16, 16, ["K..K", ".KK."])
BUST_BLINK = [
    (9, 10, ["SSSSSS", "SSSSSS", "SKKKKS", "SSKKSS", "SSSSSS"]),
    (21, 10, ["SSSSSS", "SSSSSS", "SKKKKS", "SSKKSS", "SSSSSS"]),
]

# mini full-body walker (18 x 23) carrying a bowl
MINI_BODY = mirror([
    "....KKKKK",
    "..KKVvHHH",
    ".KVvHHHHH",
    ".KVHHhHHH",
    "KVvHHHHHH",
    "KVHHKKKKK",
    "KVHKSSSSS",
    "KVHKSeESS",
    "KVHKSEESS",
    "KVHKsPSSS",
    "KVHKSSSSS",
    "KVHHKSSSS",
    "KVHHHKKKK",
    "KVHHKDDDD",
    "KVHKDDxDD",
    "KVHKDDDxD",
    "KVHKDDDDD",
    "KHHKDDdDD",
    ".KKKDDDDD",
    "...KDDDDD",
    "...KKKKKK",
], 18)
MINI_BOWL = (5, 14,["KKKKKKKK", "KNnNNnNK", "SbBbbBbS", ".KbBBbK.", "..KKKK.."])
MINI_MOUTH = (8, 10, ["KK"])
MINI_LEGS_A = [
    "......KLK..KLK....",
    "......KLK..KLK....",
    ".....KxxK..KxxK...",
]
MINI_LEGS_B = [
    "......KLK..KLK....",
    ".....KLK....KLK...",
    "....KxxK....KxxK..",
]
MINI_BLINK = [(5, 7, ["SS", "KK"]), (11, 7, ["SS", "KK"])]


def pixels(rows, px, gx=0, gy=0, color=None):
    """Rows of palette chars -> run-length merged <rect>s. gx/gy offset in grid cells."""
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            fill = color or PAL[c]
            out.append(
                f'<rect x="{(gx + x) * px:g}" y="{(gy + y) * px:g}" width="{run * px:g}" height="{px:g}" fill="{fill}"/>'
            )
            x += run
    return "".join(out)


def layer(spec, px):
    gx, gy, rows = spec
    return pixels(rows, px, gx, gy)


def sticker(rows, px):
    """Cream silhouette offset around the sprite so dark pixels read on dark backgrounds."""
    return "".join(
        pixels(rows, px, dx, dy, PAL["O"]) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
    )


def line(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def chopstick_hand(hx, hy, tx, ty, px):
    sticks = line(hx + 1, hy, tx, ty) + line(hx + 2, hy, tx + 1, ty)
    s = "".join(
        f'<rect x="{x * px:g}" y="{y * px:g}" width="{px:g}" height="{px:g}" fill="{PAL["C"]}"/>' for x, y in sticks
    )
    return s + pixels(["KSSK", "SSSS", "KSSK", ".KK."], px, hx, hy)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name, len(svg), "bytes")


# ---------------------------------------------------------------- terminal ---
def terminal():
    W = 860
    lines = [
        ("$", "whoami", CYAN),
        ("", "demcruise — product designer · UI/UX · app UI", TEXT),
        ("$", "cat focus.txt", CYAN),
        ("", "▸ Product design: problem framing → flows → shipped UI", TEXT),
        ("", "▸ UI/UX: research, wireframes, prototypes, usability tests", TEXT),
        ("", "▸ App UI: design systems, components, micro-interactions", TEXT),
        ("$", "cat tools.txt", CYAN),
        ("", "Figma · FigJam · Framer · Pencil · React/Next.js · Tailwind", PURPLE),
        ("$", "cat motto.txt", CYAN),
        ("", "不关我的事  — design the thing, let the pixels talk.", PINK),
    ]
    lh = 30
    top = 72
    H = top + lh * len(lines) + 50
    cycle = 16
    body = []
    css = []
    for i, (prompt, txt, col) in enumerate(lines):
        y = top + i * lh
        appear = 4 + i * 6  # % of cycle
        css.append(f".l{i}{{animation:l{i} {cycle}s steps(1) infinite}}"
                   f"@keyframes l{i}{{0%{{opacity:0}}{appear}%{{opacity:1}}96%{{opacity:0}}}}")
        p = f'<tspan fill="{YELLOW}">{prompt} </tspan>' if prompt else ""
        body.append(f'<text class="l{i}" x="28" y="{y}" font-size="16" font-family="{FONT}" fill="{col}" xml:space="preserve">{p}{html.escape(txt)}</text>')
    cy = top + len(lines) * lh
    body.append(f'<g class="lc"><text x="28" y="{cy}" font-size="16" font-family="{FONT}" fill="{YELLOW}">$</text>'
                f'<rect class="cur" x="46" y="{cy-15}" width="10" height="19" fill="{CYAN}"/></g>')
    css.append(f".lc{{animation:lc {cycle}s steps(1) infinite}}@keyframes lc{{0%{{opacity:0}}{4+len(lines)*6}%{{opacity:1}}96%{{opacity:0}}}}")
    css.append(".cur{animation:cb 1s steps(1) infinite}@keyframes cb{50%{opacity:0}}")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>{''.join(css)}</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="#30363d" stroke-width="2"/>
<path d="M1 13a12 12 0 0 1 12-12h{W-26}a12 12 0 0 1 12 12v23H1z" fill="#161b22"/>
<circle cx="24" cy="19" r="6" fill="#ff5f56"/><circle cx="44" cy="19" r="6" fill="#ffbd2e"/><circle cx="64" cy="19" r="6" fill="#27c93f"/>
<text x="{W/2}" y="24" text-anchor="middle" font-size="13" font-family="{FONT}" fill="{MUTED}">demcruise@studio: ~/about</text>
{''.join(body)}
</svg>"""
    write("terminal.svg", svg)


# ------------------------------------------------------------------- stack ---
def stack():
    groups = [
        ("DESIGN", PINK, ["Figma", "FigJam", "Framer", "Pencil", "Design Systems", "Prototyping"]),
        ("UX", PURPLE, ["User Research", "Wireframing", "Usability Testing", "Info Architecture", "Journey Maps"]),
        ("BUILD", CYAN, ["React", "Next.js", "TypeScript", "Tailwind", "Motion", "Kotlin"]),
    ]
    W, cw = 860, 9.6
    rows, y, k = [], 30, 0
    for label, col, items in groups:
        rows.append(f'<text x="24" y="{y+22}" font-size="13" font-family="{FONT}" fill="{col}" letter-spacing="3">{label}</text>')
        x = 130
        for it in items:
            w = len(it) * cw + 28
            if x + w > W - 20:
                x = 130
                y += 46
            d = k * 0.18
            rows.append(
                f'<g class="chip" style="animation-delay:{d:.2f}s">'
                f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="8" fill="#161b22" stroke="{col}" stroke-opacity=".55"/>'
                f'<rect class="dot" x="{x+12}" y="{y+14}" width="6" height="6" fill="{col}" style="animation-delay:{d:.2f}s"/>'
                f'<text x="{x+24}" y="{y+22}" font-size="15" font-family="{FONT}" fill="{TEXT}">{html.escape(it)}</text></g>'
            )
            x += w + 10
            k += 1
        y += 58
    H = y + 6
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
.chip{{opacity:0;animation:in .6s ease-out forwards, fl 3s ease-in-out infinite}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
@keyframes fl{{0%,100%{{opacity:1;transform:translateY(0)}}50%{{opacity:1;transform:translateY(-3px)}}}}
.dot{{animation:pl 1.6s steps(1) infinite}}
@keyframes pl{{50%{{opacity:.25}}}}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="#30363d" stroke-width="2"/>
{''.join(rows)}
</svg>"""
    write("stack.svg", svg)


# ----------------------------------------------------------------- divider ---
def divider():
    """Mini Osaragi walks across carrying her bowl and snacks on onigiri along the way."""
    W, H, px = 860, 112, 3
    ground = 102
    spr_w, spr_h = 18 * px, (len(MINI_BODY) + len(MINI_LEGS_A)) * px
    start, end, dur = -spr_w - 10, W + 10, 10.0
    sy = ground - spr_h

    frame_a = MINI_BODY + MINI_LEGS_A
    frame_b = MINI_BODY + MINI_LEGS_B
    walker = (
        f'<g class="wA">{sticker(frame_a, px)}{pixels(frame_a, px)}</g>'
        f'<g class="wB">{sticker(frame_b, px)}{pixels(frame_b, px)}</g>'
        f'{layer(MINI_BOWL, px)}{layer(MINI_MOUTH, px)}'
        f'<g class="mbl">{"".join(layer(b, px) for b in MINI_BLINK)}</g>'
    )

    onigiri = ["...OO...", "..OOOO..", ".OOOOOO.", "OOOOOOOO", "OOGGGGOO", "OOGGGGOO"]
    items, pops, css = [], [], []
    for i, ix in enumerate(range(150, W - 60, 140)):
        # moment the walker's bowl reaches this onigiri -> it disappears, "+1" pops
        p = ((ix + 12) - (start + 9 * px)) / (end - start) * 100
        items.append(
            f'<g class="o{i}"><g class="bobo" style="animation-delay:{i*0.2:.1f}s">'
            f'{pixels(onigiri, 3, ix / 3, (ground - 22) / 3)}</g></g>'
        )
        pops.append(
            f'<text class="p{i}" x="{ix + 4}" y="{sy - 4}" font-size="14" font-weight="700" font-family="{FONT}" fill="{YELLOW}">+1</text>'
        )
        css.append(
            f".o{i}{{animation:o{i} {dur}s steps(1) infinite}}"
            f"@keyframes o{i}{{0%{{opacity:1}}{p:.2f}%{{opacity:0}}99%{{opacity:0}}100%{{opacity:1}}}}"
            f".p{i}{{opacity:0;animation:p{i} {dur}s linear infinite}}"
            f"@keyframes p{i}{{0%,{p:.2f}%{{opacity:0;transform:translateY(0)}}"
            f"{p+0.5:.2f}%{{opacity:1;transform:translateY(0)}}{p+6:.2f}%{{opacity:0;transform:translateY(-14px)}}100%{{opacity:0}}}}"
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">
<style>
.walk{{animation:walk {dur}s linear infinite}}
@keyframes walk{{from{{transform:translate({start}px,{sy}px)}}to{{transform:translate({end}px,{sy}px)}}}}
.wA{{animation:wa .5s steps(1) infinite}}
.wB{{opacity:0;animation:wb .5s steps(1) infinite}}
@keyframes wa{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes wb{{0%{{opacity:0}}50%{{opacity:1}}}}
.hop{{animation:hop .5s steps(1) infinite}}
@keyframes hop{{50%{{transform:translateY(-3px)}}}}
.mbl{{opacity:0;animation:mbl 3.5s steps(1) infinite}}
@keyframes mbl{{0%,90%{{opacity:0}}91%,96%{{opacity:1}}97%{{opacity:0}}}}
.bobo{{animation:bo 1s steps(2) infinite}}
@keyframes bo{{50%{{transform:translateY(-3px)}}}}
{''.join(css)}
</style>
<rect x="0" y="{ground}" width="{W}" height="4" fill="#cdb995"/>
<rect x="0" y="{ground + 4}" width="{W}" height="2" fill="#8f7a58"/>
{''.join(items)}
<g class="walk"><g class="hop">{walker}</g></g>
{''.join(pops)}
</svg>"""
    write("divider.svg", svg)


# ------------------------------------------------------------------ footer ---
def footer():
    """Osaragi bust behind a little table, waving her chopsticks: 'gochisousama!'."""
    W, H, px = 860, 190, 4
    table_y = 150
    cx = 250
    cy = table_y - 31 * px

    # two wave poses of the chopstick hand (grid coords inside the sprite)
    wave_a = chopstick_hand(3, 15, 1, 8, px)
    wave_b = chopstick_hand(4, 14, 6, 7, px)

    body = (
        sticker(BUST, px)
        + pixels(BUST, px)
        + layer(BUST_SMILE, px)
        + layer(BUST_BOWL, px)
        + layer(BUST_LEFT_HAND, px)
        + f'<g class="bbl">{"".join(layer(b, px) for b in BUST_BLINK)}</g>'
        + f'<g class="wvA">{wave_a}</g><g class="wvB">{wave_b}</g>'
    )

    sparkles = "".join(
        f'<g class="sp" style="animation-delay:{d}s"><rect x="{x-6}" y="{y-1.5}" width="12" height="3" fill="{c}"/>'
        f'<rect x="{x-1.5}" y="{y-6}" width="3" height="12" fill="{c}"/></g>'
        for x, y, d, c in ((200, 30, 0, PAL["O"]), (430, 22, 0.7, PINK), (720, 40, 1.4, CYAN), (160, 110, 2.1, PURPLE))
    )

    bx, by, bw, bh = 420, 56, 330, 52
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">
<style>
.wvA{{animation:wa .7s steps(1) infinite}}
.wvB{{opacity:0;animation:wb .7s steps(1) infinite}}
@keyframes wa{{0%{{opacity:1}}50%{{opacity:0}}}}
@keyframes wb{{0%{{opacity:0}}50%{{opacity:1}}}}
.bbl{{opacity:0;animation:bbl 4s steps(1) infinite}}
@keyframes bbl{{0%,90%{{opacity:0}}91%,95%{{opacity:1}}96%{{opacity:0}}}}
.bob{{animation:bob 1.4s steps(1) infinite}}
@keyframes bob{{50%{{transform:translateY(-4px)}}}}
.bubble{{animation:bb 3s ease-in-out infinite}}
@keyframes bb{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
.sp{{animation:sp 2.8s steps(1) infinite}}
@keyframes sp{{0%,60%{{opacity:1}}61%,100%{{opacity:.15}}}}
</style>
{sparkles}
<g transform="translate({cx} {cy})"><g class="bob">{body}</g></g>
<rect x="0" y="{table_y}" width="{W}" height="{H - table_y}" fill="#cdb995"/>
<rect x="0" y="{table_y}" width="{W}" height="5" fill="#e3d4b3"/>
<rect x="0" y="{table_y + 5}" width="{W}" height="3" fill="#a8916b"/>
<rect x="0" y="{table_y + 18}" width="{W}" height="2" fill="#b8a27c"/>
<rect x="120" y="{table_y + 28}" width="{W}" height="2" fill="#b8a27c"/>
<g class="bubble">
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{BG}" stroke="{PAL['O']}" stroke-width="3"/>
  <rect x="{bx - 12}" y="{by + 30}" width="12" height="4" fill="{PAL['O']}"/>
  <rect x="{bx - 20}" y="{by + 34}" width="8" height="4" fill="{PAL['O']}"/>
  <text x="{bx + bw / 2}" y="{by + 33}" text-anchor="middle" font-size="16" fill="{TEXT}">
    <tspan font-family="{CJK}" font-weight="700" fill="{PINK}">ごちそうさま!</tspan>
    <tspan font-family="{FONT}"> thanks for visiting ✦</tspan>
  </text>
</g>
</svg>"""
    write("footer.svg", svg)


if __name__ == "__main__":
    terminal()
    stack()
    divider()
    footer()
