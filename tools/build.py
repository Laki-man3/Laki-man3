"""Собирает пиксельные SVG для README профиля.

    python tools/build.py

Нужен только Pillow. Шрифт — Press Start 2P (OFL), рисуется в SVG
пикселями, поэтому на GitHub ничего не подгружается.
Тексты лежат в блоке CONTENT ниже — правьте их и пересобирайте.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, 'assets')

PX = 2          # один «пиксель» макета в экранных px
WU = 420        # ширина всех блоков в пикселях макета (840px)

# палитра снята с аватарки
INK = '#5e202a'
INK2 = '#6b2b35'
BROWN = '#7e4344'
BRICK = '#b05355'
MAUVE = '#ac7475'
SALMON = '#dc9279'
PEACH = '#e9b194'
PAPER = '#f6ecdc'
CREAM = '#ecdac4'
SAND = '#dec3b4'
STONE = '#d2c1b3'
GREY = '#b8aca3'
SAGE = '#acac9f'
TAUPE = '#887973'
TEAL = '#83a7a9'
TEAL_DK = '#6d9597'
TEAL_DKK = '#4f7477'
TEAL_LT = '#9cb8b4'
RAY = '#afc3bb'


# ───────────────────────────── CONTENT ──────────────────────────────

NAME = 'Semyon Maksimovich'
NAME_TAG = 'Semyon'
TAGLINE = 'QA Engineer · Backend & APIs'

ABOUT = ("Hi, I'm Semyon, a QA engineer. For the past three years I've been testing "
         'banking backends: microservices talking over REST and Kafka, '
         'data in PostgreSQL and Redis, logs in Kibana.')

TITLES = dict(experience='EXPERIENCE', results='HIGHLIGHTS',
              stack='STACK', contacts='CONTACT')

EXPERIENCE = [
    dict(org='Innotech Group', dates='Jul 2023 — Present',
         role='QA Engineer · remote',
         text=['Three parallel projects for VTB Bank: a product operations '
               'orchestrator for the central depository system, a settlement '
               'processor for the depository and a payment documents registry.',
               'Planned and ran functional, regression and smoke testing, '
               'prepared test data and environments, handled defects and docs, '
               'demoed new features to the client.']),
    dict(org='Eltex', dates='Mar 2023 — Jun 2023',
         role='QA Engineer, intern',
         text=['Manual testing of MES network switches: reading specs, '
               'writing test cases, filing defects in Jira.']),
]

RESULTS = [
    ('relay', 'Relay — desktop API client',
     'Built a desktop app for API testing inside an isolated network '
     "segment, where the usual cloud tools aren't an option."),
    ('tms','TMS in the testing workflow',
     'Brought the Sfera TMS into the process, so test cases and other '
     'test artifacts take less time to write.'),
    ('redis', 'Redis as a testing tool',
     'By changing values in the cache the service reads first, we could '
     'reproduce rare errors and push through requests the system would '
     'normally reject.'),
    ('folder', 'Shared test data',
     'One common place and format for test data that anyone on the team '
     'can use.'),
    ('switch', 'Traffic generation with scapy',
     'First at Eltex to generate network traffic with Python and scapy '
     'scripts.'),
]

STACK = [
    ('API', ['REST', 'SOAP', 'GraphQL', 'RPC', 'Webhooks']),
    ('TESTING', ['pytest', 'JUnit', 'TestNG', 'REST Assured', 'Cucumber', 'Allure']),
    ('DEBUG', ['Postman', 'cURL', 'WireMock', 'DevTools']),
    ('DATA', ['PostgreSQL', 'MySQL', 'Redis', 'Kafka', 'DBeaver']),
    ('INFRA', ['Docker', 'Kubernetes', 'CI/CD', 'Git', 'Linux']),
    ('LOGS', ['Kibana', 'ELK', 'k8s logs']),
    ('PROCESS', ['Jira', 'Confluence', 'Kaiten', 'TestIT', 'Sfera']),
    ('METHODS', ['test design', 'Scrum', 'BDD', 'TDD', 'SDLC']),
    ('CODE', ['Python', 'Java', 'C#', 'C/C++', 'JS']),
    ('NETWORK', ['TCP/IP', 'OSI', 'HTTP', 'FTP', 'Wireshark', 'scapy']),
]
STACK_FOCUS = ['pytest', 'REST Assured', 'Postman', 'Kafka', 'Redis', 'PostgreSQL']

CONTACT_TEXT = ['Open to new opportunities.', 'Reach me on Telegram or by email ↓']
TELEGRAM = '@PowerOfNsk'
EMAIL = 'semend2005@mail.ru'


# ───────────────────────────── font ─────────────────────────────────

class PixelFont:
    """Press Start 2P на родном размере 8px: каждый глиф — сетка 8×8."""

    def __init__(self, path):
        self.font = ImageFont.truetype(path, 8)
        self.cache = {}

    def runs(self, ch):
        if ch not in self.cache:
            img = Image.new('L', (14, 14), 0)
            d = ImageDraw.Draw(img)
            d.fontmode = '1'
            d.text((3, 3), ch, font=self.font, fill=255)
            px = img.load()
            runs = []
            for y in range(14):
                x = 0
                while x < 14:
                    if px[x, y]:
                        s = x
                        while x < 14 and px[x, y]:
                            x += 1
                        runs.append((s - 3, y - 3, x - s))
                    else:
                        x += 1
            assert all(0 <= y < 8 and 0 <= x and x + w <= 8 for x, y, w in runs), ch
            self.cache[ch] = runs
        return self.cache[ch]

    def pixels(self, s):
        out = set()
        for i, ch in enumerate(s):
            for x, y, w in self.runs(ch):
                for k in range(w):
                    out.add((i * 8 + x + k, y))
        return out


FONT = PixelFont(os.path.join(HERE, 'fonts', 'PressStart2P-Regular.ttf'))


def tw(s, scale=1):
    return len(s) * 8 * scale


def wrap(text, width):
    lines, cur = [], ''
    for word in text.split():
        cand = f'{cur} {word}' if cur else word
        if len(cand) <= width:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


# ───────────────────────────── svg ──────────────────────────────────

BASE_CSS = (
    '@keyframes drift{to{transform:translateX(-420px)}}'
    '@keyframes hide{from,to{opacity:0}}'
    '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
    '@keyframes bob{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(2px)}}'
    '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
)


class Svg:
    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.css, self.defs, self.body = [BASE_CSS], [], []
        self.glyphs = {}
        self.ids = 0

    def uid(self, p):
        self.ids += 1
        return f'{p}{self.ids}'

    def add(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill, attrs=''):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{attrs}/>')

    def glyph(self, ch):
        gid = 'g%x' % ord(ch)
        if gid not in self.glyphs:
            d = ''.join(f'M{x} {y}h{w}v1h-{w}z' for x, y, w in FONT.runs(ch))
            self.glyphs[gid] = f'<path id="{gid}" d="{d}"/>'
        return gid

    def text(self, x, y, s, fill, scale=1, attrs='', char_attrs=None):
        uses, cx = [], 0
        for i, ch in enumerate(s):
            if ch != ' ':
                extra = char_attrs(i) if char_attrs else ''
                uses.append(f'<use href="#{self.glyph(ch)}" x="{cx}"{extra}/>')
            cx += 8
        tr = f'translate({x} {y})' + (f' scale({scale})' if scale != 1 else '')
        self.add(f'<g transform="{tr}" fill="{fill}"{attrs}>{"".join(uses)}</g>')

    def stext(self, x, y, s, fill, shadow, scale=1, attrs=''):
        self.text(x + scale, y + scale, s, shadow, scale, attrs)
        self.text(x, y, s, fill, scale, attrs)

    def render(self):
        defs = ''.join(self.glyphs.values()) + ''.join(self.defs)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w * PX}" '
            f'height="{self.h * PX}" viewBox="0 0 {self.w} {self.h}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{esc(self.label)}">'
            f'<title>{esc(self.label)}</title>'
            f'<style>{"".join(self.css)}</style>'
            f'<defs>{defs}</defs>{"".join(self.body)}</svg>')

    def save(self, name):
        path = os.path.join(ASSETS, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.render())
        print(f'{name:22s} {os.path.getsize(path) / 1024:6.1f} KB')


def rrect_d(x, y, w, h, r=2):
    if r == 0:
        rs = [(x, y, w, h)]
    elif r == 1:
        rs = [(x + 1, y, w - 2, h), (x, y + 1, w, h - 2)]
    else:
        rs = [(x + 2, y, w - 4, h), (x + 1, y + 1, w - 2, h - 2), (x, y + 2, w, h - 4)]
    return ''.join(f'M{a} {b}h{c}v{e}h-{c}z' for a, b, c, e in rs)


def rrect(svg, x, y, w, h, fill, r=2, attrs=''):
    svg.add(f'<path fill="{fill}" d="{rrect_d(x, y, w, h, r)}"{attrs}/>')


def pixels_to_paths(grid):
    """{(x, y): color} → по одному <path> на цвет, строки склеены в отрезки."""
    rows = {}
    for (x, y), c in grid.items():
        rows.setdefault((y, c), []).append(x)
    by_color = {}
    for (y, c), xs in sorted(rows.items()):
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            by_color.setdefault(c, []).append(f'M{start} {y}h{prev - start + 1}v1h-{prev - start + 1}z')
            if x is not None:
                start = prev = x
    return ''.join(f'<path fill="{c}" d="{"".join(d)}"/>' for c, d in by_color.items())


def sprite(rows, colors):
    return {(x, y): colors[ch] for y, row in enumerate(rows)
            for x, ch in enumerate(row) if ch in colors}


def place(grid, x, y, scale=1):
    tr = f'translate({x} {y})' + (f' scale({scale})' if scale != 1 else '')
    return f'<g transform="{tr}">{pixels_to_paths(grid)}</g>'


SPRITE_COLORS = dict(K=INK, k=INK2, B=BRICK, S=SALMON, P=PEACH, W=PAPER,
                     C=CREAM, N=SAND, T=TEAL, D=TEAL_DKK, G=GREY, L=TEAL_LT,
                     M=MAUVE)


# ───────────────────────────── chrome ───────────────────────────────

def window(svg, x, y, w, h, title=None):
    """Пиксельное окно: тень, рамка, фаска и заголовок."""
    rrect(svg, x + 2, y + 2, w, h, INK, 2, ' opacity=".35"')
    rrect(svg, x, y, w, h, INK, 2)
    rrect(svg, x + 2, y + 2, w - 4, h - 4, PAPER, 1)
    svg.rect(x + 3, y + h - 4, w - 6, 1, SAND)
    svg.rect(x + w - 4, y + 3, 1, h - 6, SAND)
    if not title:
        return y + 4
    svg.rect(x + 3, y + 2, w - 6, 1, TEAL_LT)
    svg.rect(x + 2, y + 3, w - 4, 13, TEAL)
    svg.rect(x + 2, y + 15, w - 4, 1, TEAL_DK)
    svg.rect(x + 2, y + 16, w - 4, 2, INK)
    svg.stext(x + 9, y + 5, title, PAPER, INK)
    for i, c in enumerate([PEACH, SALMON, BRICK]):
        bx = x + w - 34 + i * 9
        svg.rect(bx, y + 5, 7, 7, INK)
        svg.rect(bx + 1, y + 6, 5, 5, c)
        svg.rect(bx + 1, y + 6, 5, 1, PAPER, ' opacity=".5"')
    return y + 18


# ───────────────────────────── clouds ───────────────────────────────

def cloud_bank(width, height, base, seed, pal, size, gap):
    """Полоса кучевых облаков, бесшовная по горизонтали с периодом width.

    base — линия, на которой «стоят» облака, size — радиус главного клуба,
    gap — расстояние между облаками.
    """
    hi, mid, sh1, sh2 = pal
    rnd = random.Random(seed)
    puffs, x = [], rnd.randint(0, gap[0])
    while x < width:
        R = rnd.randint(*size)
        cy = base - R // 3 + rnd.randint(-2, 2)
        puffs.append((x, cy, R))
        for _ in range(rnd.randint(2, 4)):
            side = rnd.choice((-1, 1))
            r = max(3, int(R * rnd.uniform(.45, .8)))
            puffs.append((x + side * int(R * rnd.uniform(.6, 1.2)),
                          cy + int(R * rnd.uniform(.15, .55)), r))
        if rnd.random() < .6:
            r = max(3, int(R * rnd.uniform(.4, .6)))
            puffs.append((x + rnd.randint(-R // 2, R // 2), cy - int(R * .55), r))
        x += rnd.randint(*gap)
    grid = {}
    for yy in range(base + 4, height):
        for xx in range(width):
            grid[xx, yy] = mid
    # сверху вниз: нижние клубы ложатся поверх верхних, как на аватарке
    for cx, cy, r in sorted(puffs, key=lambda p: p[1]):
        for ox in (-width, 0, width):
            for yy in range(max(0, cy - r), min(height, cy + r + 1)):
                for xx in range(max(0, cx + ox - r), min(width, cx + ox + r + 1)):
                    dx, dy = xx + .5 - (cx + ox), yy + .5 - cy
                    d = math.hypot(dx, dy)
                    if d > r:
                        continue
                    v = (dx * .4 + dy) / r
                    odd = (xx + yy) % 2
                    if d > r - 1 and dy < 0 or v < -.42:
                        c = hi
                    elif v < -.26:
                        c = hi if odd else mid
                    elif v < .3:
                        c = mid
                    elif v < .44:
                        c = sh1 if odd else mid
                    elif v < .72:
                        c = sh1
                    else:
                        c = sh2
                    grid[xx, yy] = c
    return grid


FRONT = (PAPER, CREAM, SAND, STONE)
BACK = (STONE, '#c9bbb0', GREY, SAGE)


def drifting(svg, grid, dur, cls):
    gid = svg.uid('cl')
    svg.defs.append(f'<g id="{gid}">{pixels_to_paths(grid)}</g>')
    svg.css.append(f'.{cls}{{animation:drift {dur}s steps(420) infinite}}')
    svg.add(f'<g class="{cls}"><use href="#{gid}"/><use href="#{gid}" x="420"/></g>')


def sky(svg, w, h, rays=True):
    svg.rect(0, 0, w, h, TEAL)
    svg.rect(0, 0, w, 3, TEAL_DK)
    d = ''.join(f'M{xx} {yy}h1v1h-1z' for yy in range(3, 7) for xx in range((yy % 2) * 1, w, 2 + (yy - 3)))
    svg.add(f'<path fill="{TEAL_DK}" d="{d}"/>')
    if not rays:
        return
    # косые лучи, как на аватарке
    for x0, width, c, cls in [(150, 16, TEAL_LT, 'r1'), (178, 4, RAY, 'r2'),
                              (226, 26, TEAL_LT, 'r1'), (262, 3, RAY, 'r2')]:
        d = ''.join(f'M{x0 - yy} {yy}h{width}v1h-{width}z' for yy in range(h))
        svg.add(f'<path class="{cls}" fill="{c}" d="{d}"/>')
    svg.css.append('@keyframes shim{0%,49%{opacity:1}50%,100%{opacity:.55}}'
                   '.r1{animation:shim 5s steps(1) infinite}'
                   '.r2{animation:shim 3.4s steps(1) 1.2s infinite}')


def specks(svg, pts, color=PAPER):
    for i, (x, y, s) in enumerate(pts):
        cls = f'sp{i % 3}'
        svg.rect(x, y, s, s, color, f' class="{cls}"')
    svg.css.append('.sp0{animation:blink 2.6s steps(1) infinite}'
                   '.sp1{animation:blink 3.7s steps(1) .9s infinite}'
                   '.sp2{animation:blink 4.3s steps(1) 1.7s infinite}')


# ───────────────────────────── blocks ───────────────────────────────

def hero():
    H = 150
    s = Svg(WU, H, f'{NAME} — {TAGLINE}')
    w, h = WU - 2, H - 2
    clip = s.uid('c')
    s.defs.append(f'<clipPath id="{clip}"><path d="{rrect_d(2, 2, w - 4, h - 4, 1)}"/></clipPath>')
    rrect(s, 2, 2, w, h, INK, 2, ' opacity=".35"')
    rrect(s, 0, 0, w, h, INK, 2)
    s.add(f'<g clip-path="url(#{clip})">')
    sky(s, WU, H)
    specks(s, [(330, 18, 2), (352, 28, 1), (372, 14, 2), (392, 36, 1), (312, 40, 1),
               (40, 22, 1), (64, 46, 2), (24, 60, 1), (384, 58, 2), (98, 16, 1)])
    drifting(s, cloud_bank(WU, H, 112, 7, BACK, (8, 14), (24, 42)), 140, 'da')
    drifting(s, cloud_bank(WU, H, 134, 12, FRONT, (10, 17), (28, 48)), 70, 'db')

    # имя: контур, тень и «закатный» градиент по строкам
    scale = 2
    px = FONT.pixels(NAME.upper())
    grid = {}
    for (x, y) in px:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1, 2):
                grid[x + dx + 1, y + dy + 1] = INK
    for (x, y) in px:
        grid[x + 1, y + 1] = [PAPER, PAPER, PAPER, CREAM, PEACH, SALMON, SALMON, BRICK][y]
    tx = (WU - tw(NAME, scale)) // 2
    s.add(place(grid, tx - scale, 30, scale))

    # плашка с ролью
    label = TAGLINE
    pw = tw(label) + 32
    px0 = (WU - pw) // 2
    py0 = 64
    rrect(s, px0 + 2, py0 + 2, pw, 16, INK, 1, ' opacity=".35"')
    rrect(s, px0, py0, pw, 16, INK, 1)
    s.rect(px0 + 1, py0 + 1, pw - 2, 14, BRICK)
    s.rect(px0 + 2, py0 + 1, pw - 4, 1, SALMON)
    s.rect(px0 + 1, py0 + 13, pw - 2, 2, INK2)
    s.stext(px0 + 10, py0 + 4, label, PAPER, INK)
    s.rect(px0 + pw - 16, py0 + 4, 6, 8, PAPER, ' class="cur"')
    s.css.append('.cur{animation:blink 1.1s steps(1) infinite}')
    s.add('</g>')
    s.save('hero.svg')


def portrait(size, box=(36, 14, 346, 324)):
    im = Image.open(os.path.join(HERE, 'avatar.png')).convert('RGB').crop(box)
    cols = ['ecdac4', '83a7a9', 'd2c1b3', 'b8aca3', 'acac9f', 'e9b194', 'dc9279',
            'b05355', 'dec3b4', '5e202a', '6b2b35', '7e4344', '5d2826', 'ac7475',
            '887973', 'f4e8d6']
    pal = Image.new('P', (1, 1))
    flat = [int(c[i:i + 2], 16) for c in cols for i in (0, 2, 4)]
    pal.putpalette(flat + [0] * (768 - len(flat)))
    small = im.resize((size, size), Image.Resampling.BOX)
    small = small.quantize(palette=pal, dither=Image.Dither.NONE).convert('RGB')
    px = small.load()
    return {(x, y): '#%02x%02x%02x' % px[x, y] for y in range(size) for x in range(size)}


def about():
    lines = wrap(ABOUT, 37)
    top = 8
    tx = 108
    body_h = max(84, len(lines) * 13 - 5) + 26
    H = top + body_h + 2
    s = Svg(WU, H, ABOUT)
    window(s, 0, top, WU - 2, body_h)
    # двойная рамка, как в диалоговых окнах
    s.add(f'<path fill="none" stroke="{SALMON}" stroke-width="1" '
          f'd="M5.5 {top + 5.5}h{WU - 14}v{body_h - 11}h-{WU - 14}z"/>')

    # портрет
    pxl, py = 14, top + 12
    rrect(s, pxl - 2, py - 2, 84, 84, INK, 1)
    s.add(place(portrait(80), pxl, py))
    s.rect(pxl, py, 80, 1, PAPER, ' opacity=".35"')

    # табличка с именем поверх рамки
    tag = NAME_TAG
    tgw = tw(tag) + 14
    rrect(s, 16, 0, tgw, 15, INK, 1)
    s.rect(17, 1, tgw - 2, 13, BRICK)
    s.rect(18, 1, tgw - 4, 1, SALMON)
    s.rect(17, 12, tgw - 2, 2, INK2)
    s.stext(23, 4, tag, PAPER, INK)

    # печатная машинка: каждая буква спрятана, пока не «напечатана»
    t, step = 0.5, 0.032
    for i, line in enumerate(lines):
        delays = []
        for ch in line:
            delays.append(t)
            t += step if ch != ' ' else step / 2
        t += 0.18
        s.text(tx, top + 13 + i * 13, line, INK2, char_attrs=lambda k, d=delays:
               f' style="animation-duration:{d[k]:.2f}s"', attrs=' class="tw"')
    s.css.append('.tw use{animation-name:hide;animation-timing-function:steps(1)}')
    # стрелка «дальше»
    ax, ay = WU - 22, top + body_h - 16
    s.add(f'<g class="nx">'
          f'{place(sprite(["KKKKKKK", ".KKKKK.", "..KKK..", "...K..."], SPRITE_COLORS), ax, ay)}</g>')
    s.css.append(f'.nx{{animation:hide {t:.2f}s steps(1),bob .9s steps(1) {t:.2f}s infinite}}')
    s.save('about.svg')


def experience():
    x0 = 32
    blocks, y = [], 28
    for e in EXPERIENCE:
        lines, yy = [], y + 26
        for k, para in enumerate(e['text']):
            for line in wrap(para, 46):
                lines.append((yy, line))
                yy += 12
            yy += 6
        blocks.append((y, e, lines))
        y = yy - 6 + 12
    H = y + 2
    s = Svg(WU, H, 'Experience: ' + '; '.join(f"{e['org']}, {e['role']}, {e['dates']}" for e in EXPERIENCE))
    window(s, 0, 0, WU - 2, H - 2, TITLES['experience'])
    nodes = []
    for y, e, lines in blocks:
        nodes.append(y)
        s.text(x0, y, e['org'], BRICK)
        s.text(WU - 14 - tw(e['dates']), y, e['dates'], TAUPE)
        s.text(x0, y + 13, e['role'], TEAL_DKK)
        for yy, line in lines:
            s.text(x0, yy, line, INK2)
    # пунктир таймлайна и узлы
    for a, b in zip(nodes, nodes[1:]):
        d = ''.join(f'M15 {yy}h2v2h-2z' for yy in range(a + 12, b - 4, 4))
        s.add(f'<path fill="{GREY}" d="{d}"/>')
    for i, ny in enumerate(nodes):
        s.rect(12, ny - 1, 8, 8, INK)
        s.rect(13, ny, 6, 6, BRICK if i == 0 else (SALMON if i == 1 else TEAL))
        s.rect(13, ny, 6, 1, PAPER, ' opacity=".45"')
    s.save('experience.svg')


ICONS = {
    'relay': [
        "................",
        ".KKKKKKKKKKKKKK.",
        ".KTTTTTTTTPSBTK.",
        ".KKKKKKKKKKKKKK.",
        ".KWWWWWWWWWWWWK.",
        ".KWWWWWWWDWWWWK.",
        ".KWDDDDDDDDWWWK.",
        ".KWWWWWWWDWWWWK.",
        ".KWWWWWWWWWWWWK.",
        ".KWWWWBWWWWWWWK.",
        ".KWWWBBBBBBBBWK.",
        ".KWWWWBWWWWWWWK.",
        ".KKKKKKKKKKKKKK.",
        "......KKKK......",
        "....KKKKKKKK....",
        "................"],
    'tms': [
        "................",
        "......KKKK......",
        "...KKKKNNKKKK...",
        "..KCCKKKKKKCCK..",
        "..KWWWWWWWWWWK..",
        "..KWTTWWKKKKWK..",
        "..KWTTWWWWWWWK..",
        "..KWWWWWWWWWWK..",
        "..KWTTWWKKKKWK..",
        "..KWTTWWWWWWWK..",
        "..KWWWWWWWWWWK..",
        "..KWBBWWKKKWWK..",
        "..KWBBWWWWWWWK..",
        "..KNNNNNNNNNNK..",
        "..KKKKKKKKKKKK..",
        "................"],
    'redis': [
        "................",
        "....KKKKKKKK....",
        "..KKPPPPPPPPKK..",
        ".KPPWWPPPPPPPPK.",
        ".KKPPPPPPPPPPKK.",
        ".KSKKPPPPPPKKBK.",
        ".KSBBKKKKKKBBBK.",
        ".KSBBBBBBBBBBBK.",
        ".KKBBBBBBBBBBKK.",
        ".KSKKBBBBBBKKBK.",
        ".KSBBKKKKKKBBBK.",
        ".KSBBBBBBBBBBBK.",
        ".KKBBBBBBBBBBKK.",
        "..KKBBBBBBBBKK..",
        "....KKKKKKKK....",
        "................"],
    'folder': [
        "................",
        "................",
        ".KKKKKK.........",
        ".KSSSSSK........",
        ".KSSSSSSKKKKKKK.",
        ".KSWWWWWWWWWWSK.",
        ".KSWKKKKKKKWWSK.",
        ".KKKKKKKKKKKKKK.",
        ".KPPPPPPPPPPPPK.",
        ".KPWWPPPPPPPPPK.",
        ".KPPPPPPPPPPPPK.",
        ".KPPPPKKKKPPPPK.",
        ".KPPPPPPPPPPPPK.",
        ".KSSSSSSSSSSSSK.",
        ".KKKKKKKKKKKKKK.",
        "................"],
    'switch': [
        "................",
        "................",
        "................",
        "..TT....TT....TT",
        "................",
        ".KKKKKKKKKKKKKK.",
        ".KCCCCCCCCCCCCK.",
        ".KNKKNKKNKKNNNK.",
        ".KNKKNKKNKKNNNK.",
        ".KNNNNNNNNNNNNK.",
        ".KGGGGGGGGGGGGK.",
        ".KKKKKKKKKKKKKK.",
        "..KK........KK..",
        "................",
        "................",
        "................"],
}


def results():
    rows = [(k, t, wrap(b, 44)) for k, t, b in RESULTS]
    H = 18 + 10 + sum(max(13 + 12 * len(b), 30) + 10 for _, _, b in rows) + 4
    s = Svg(WU, H, 'Highlights: ' + '; '.join(f'{t} — {b}' for _, t, b in RESULTS))
    y = window(s, 0, 0, WU - 2, H - 2, TITLES['results']) + 10
    for i, (key, title, body) in enumerate(rows):
        rh = max(13 + 12 * len(body), 30)
        # ячейка с иконкой
        rrect(s, 12, y - 2, 30, 30, INK, 1)
        s.rect(13, y - 1, 28, 28, CREAM)
        s.rect(13, y - 1, 28, 1, PAPER)
        s.rect(13, y + 25, 28, 2, SAND)
        s.add(place(sprite(ICONS[key], SPRITE_COLORS), 19, y + 5))
        if key == 'switch':
            s.rect(32, y + 12, 1, 1, TEAL, ' class="led1"')
            s.rect(33, y + 13, 1, 1, BRICK, ' class="led2"')
            s.rect(31, y + 13, 1, 1, PEACH, ' class="led1"')
            s.css.append('.led1{animation:blink .7s steps(1) infinite}'
                         '.led2{animation:blink 1.3s steps(1) .3s infinite}')
        s.text(52, y + 1, title, BRICK)
        for j, line in enumerate(body):
            s.text(52, y + 14 + j * 12, line, INK2)
        y += rh + 10
        if i < len(rows) - 1:
            d = ''.join(f'M{xx} {y - 6}h2v1h-2z' for xx in range(52, WU - 14, 4))
            s.add(f'<path fill="{SAND}" d="{d}"/>')
    s.save('results.svg')


def stack():
    label_w = 66
    x_start = 12 + label_w
    x_end = WU - 14
    layout, y = [], 0
    for label, items in STACK:
        x, row_y, slots = x_start, y, []
        for it in items:
            w = tw(it) + 10
            if x + w > x_end:
                x, row_y = x_start, row_y + 17
            slots.append((it, x, row_y, w))
            x += w + 4
        layout.append((label, y, slots))
        y = row_y + 17 + 3
    H = 18 + 10 + y + 6
    s = Svg(WU, H, 'Stack: ' + '; '.join(f'{l}: {", ".join(i)}' for l, i in STACK))
    top = window(s, 0, 0, WU - 2, H - 2, TITLES['stack']) + 10
    colors = [TEAL_DKK, BRICK, MAUVE, TAUPE, SALMON, TEAL_DK, BROWN, MAUVE]
    focus = []
    for i, (label, ly, slots) in enumerate(layout):
        c = colors[i % len(colors)]
        s.text(14, top + ly + 3, label, c)
        for it, x, sy, w in slots:
            yy = top + sy
            rrect(s, x, yy, w, 14, INK, 1)
            s.rect(x + 1, yy + 1, w - 2, 12, CREAM)
            s.rect(x + 1, yy + 1, w - 2, 1, PAPER)
            s.rect(x + 1, yy + 11, w - 2, 2, SAND)
            s.rect(x + 1, yy + 2, 2, 9, c)
            s.text(x + 6, yy + 3, it, INK2)
            if it in STACK_FOCUS:
                focus.append((STACK_FOCUS.index(it), x, yy, w))
    # курсор выбора прыгает по основным инструментам
    n = len(STACK_FOCUS)
    period = n * 1.6
    s.css.append(f'@keyframes sel{{0%{{opacity:1}}{100 / n:.2f}%,100%{{opacity:0}}}}'
                 f'.sel{{animation:sel {period:.1f}s steps(1) infinite}}')
    for k, x, yy, w in sorted(focus):
        d = ''
        for cx, cy, sx, sy in [(x - 2, yy - 2, 1, 1), (x + w + 1, yy - 2, -1, 1),
                               (x - 2, yy + 15, 1, -1), (x + w + 1, yy + 15, -1, -1)]:
            d += f'M{min(cx, cx + sx * 3)} {cy}h4v1h-4z'
            d += f'M{cx} {min(cy, cy + sy * 3)}h1v4h-1z'
        s.add(f'<path class="sel" style="animation-delay:{-(n - k) * 1.6:.1f}s" fill="{BRICK}" d="{d}"/>')
    s.save('stack.svg')


def contacts():
    H = 18 + 10 + 13 * len(CONTACT_TEXT) + 8
    s = Svg(WU, H, 'Contact. ' + ' '.join(CONTACT_TEXT))
    y = window(s, 0, 0, WU - 2, H - 2, TITLES['contacts']) + 10
    for i, line in enumerate(CONTACT_TEXT):
        s.text(14, y + i * 13, line, INK2)
    s.save('contacts.svg')


PLANE = [
    "...........WW",
    ".........WWWW",
    ".......WWWWWW",
    ".....WWWWWNWW",
    "...WWWWWNNWW.",
    ".WWWWWWNNWWW.",
    "...WWWNNWWW..",
    ".....NNWWWW..",
    ".....NWWWW...",
    ".....WW..W...",
]
ENVELOPE = [
    "WWWWWWWWWWWWW",
    "WNWWWWWWWWWNW",
    "WWNWWWWWWWNWW",
    "WWWNWWWWWNWWW",
    "WWWWNNWNNWWWW",
    "WWWWWWNWWWWWW",
    "WWWWWWWWWWWWW",
    "WWWWWWWWWWWWW",
    "WWWWWWWWWWWWW",
]


def button(name, icon, text, label):
    w = tw(text) + 13 + 30
    H = 30
    s = Svg(w + 2, H, label)
    rrect(s, 2, 2, w, H - 2, INK, 2, ' opacity=".35"')
    rrect(s, 0, 0, w, H - 2, INK, 2)
    s.rect(2, 2, w - 4, H - 6, BRICK)
    s.rect(3, 2, w - 6, 1, SALMON)
    s.rect(2, 3, 1, H - 8, SALMON)
    s.rect(2, H - 7, w - 4, 3, INK2)
    s.add(place(sprite(icon, SPRITE_COLORS), 11, 8 if len(icon) == 10 else 9))
    s.stext(32, 10, text, PAPER, INK)
    s.save(name)


def footer():
    H = 46
    s = Svg(WU, H, '')
    w, h = WU - 2, H - 2
    clip = s.uid('c')
    s.defs.append(f'<clipPath id="{clip}"><path d="{rrect_d(2, 2, w - 4, h - 4, 1)}"/></clipPath>')
    rrect(s, 2, 2, w, h, INK, 2, ' opacity=".35"')
    rrect(s, 0, 0, w, h, INK, 2)
    s.add(f'<g clip-path="url(#{clip})">')
    sky(s, WU, H, rays=False)
    specks(s, [(60, 10, 1), (140, 6, 2), (250, 12, 1), (330, 8, 2), (395, 14, 1)])
    drifting(s, cloud_bank(WU, H, 26, 23, BACK, (5, 9), (16, 30)), 160, 'da')
    drifting(s, cloud_bank(WU, H, 38, 29, FRONT, (6, 11), (18, 34)), 90, 'db')
    s.add('</g>')
    s.save('footer.svg')


if __name__ == '__main__':
    os.makedirs(ASSETS, exist_ok=True)
    hero()
    about()
    experience()
    results()
    stack()
    contacts()
    button('btn-telegram.svg', PLANE, TELEGRAM, f'Telegram {TELEGRAM}')
    button('btn-mail.svg', ENVELOPE, EMAIL, f'Email {EMAIL}')
    footer()
