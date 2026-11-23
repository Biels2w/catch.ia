"""
Garoto de cabelo prata - versão IA "Circuitos Pulsantes" (mesmo estilo e mesma respiração da menina de roxo)

Gera, a partir de sprite_humano.png (nesta pasta):
  humano.gif / humano_estatico.png   versão humana respirando / parada
  ia.gif / ia_estatico.png           versão IA respirando / parada

Como funciona (v3, tudo alinhado à grade de pixels da arte):
  1. mede a grade real do sprite (largura e altura de 1 "pixel" da arte e o deslocamento);
  2. as linhas de circuito são pintadas em CÉLULAS INTEIRAS dessa grade, nunca por cima;
  3. a respiração move a arte em passos de células inteiras (cabeça 1, peito 2), com
     pulso que sobe do peito para a cabeça, igual ao robo_respirando.gif da menina de roxo;
     nenhum pixel é interpolado nem pulado: só se copiam linhas originais do sprite.
Uso:  pip install numpy pillow   e depois   python gerar.py
Para usar no pygame: carregue os quadros do GIF (ex.: PIL ImageSequence) e toque em loop, FRAME_MS ms cada.
"""
import math, os
import numpy as np
from PIL import Image

N = 56            # quadros por ciclo (2,24 s, mesmo tempo do GIF de referência)
MS = 40           # ms por quadro

# ---------------- configuração deste personagem ----------------
NOME = 'Garoto de cabelo prata'
COR = (70, 140, 255)                 # cor das linhas e dos olhos
OLHOS = ((119, 260), (214, 260))             # centros dos olhos (px do sprite)
QUEIXO, APICE, TESTA = 50, 58, (28, 24) # referências em unidades de 7 px
PRONTO = False           # True: a arte IA já vem pronta em sprite_ia.png (menina de roxo)
GRADE = None             # None = mede a grade do sprite; ou (largura, altura) exatas de 1 pixel da arte
RAIO_OLHO = (14, 16)          # raio (x, y) da íris em px
# ------------------------------------------------------------------

GIRL = {
    'face': {'mirror': 95, 'L': [
        [(32, 52), (36, 52)], [(39, 52), (41, 52)],
        [(34, 54), (34, 57), (40, 63)], [(34, 55), (32, 55)],
        [(40, 63), (40, 66), (43, 69)],
    ]},
    'fore': {'mirror': None, 'L': [[(53, 33), (53, 36), (56, 36), (56, 37)]]},
    'neck': {'mirror': 95, 'L': [[(43, 77), (43, 82)], [(43, 82), (45, 82)]]},
    'cnode': {'mirror': None, 'L': [[(47, 84), (48, 84)]]},
}
G_EYE_ROW, G_FACE_AX, G_CHIN, G_APEX = 48.0, 47.5, 70.0, 84.0


# ---------------- grade de pixels da arte ----------------
def edge_score(d):
    k = np.maximum(d, np.maximum(np.roll(d, 1), np.roll(d, -1)) * 0.8)
    def best(per):
        n = len(d); bs = None
        for ph in np.arange(0, per, 0.2):
            idx = np.round(np.arange(ph, n, per)).astype(int); idx = idx[idx < n]
            mid = np.round(np.arange(ph + per / 2, n, per)).astype(int); mid = mid[mid < n]
            s = k[idx].mean() - k[mid].mean()          # bordas fortes e meio das células liso
            if bs is None or s > bs[0]: bs = (s, ph)
        return bs
    return best


def measure_grid(a):
    """Mede o tamanho e a fase das células da arte em cada eixo."""
    g = a.astype(float).mean(2)
    bg = ~((a[..., 0] > 235) & (a[..., 1] > 225))
    dx = (np.abs(np.diff(g, axis=1)) * (bg[:, 1:] & bg[:, :-1])).sum(0)
    dy = (np.abs(np.diff(g, axis=0)) * (bg[1:] & bg[:-1])).sum(1)
    bx_, by_ = edge_score(dx / dx.max()), edge_score(dy / dy.max())
    def fit(f, lo, hi):
        best = None
        for per in np.arange(lo, hi, 0.005):
            sc, ph = f(per)
            if best is None or sc > best[0]: best = (sc, per, ph)
        return best[1], best[2] + 1             # +1: o índice j do diff é a borda entre j e j+1
    return fit(bx_, 6.4, 8.2), fit(by_, 5.4, 7.6)    # a arte original é um pouco mais larga que alta


def bounds(per, ph, n):
    b = [0]
    x = ph
    while x < n - per * 0.4:
        if x > per * 0.4: b.append(int(round(x)))
        x += per
    b.append(n)
    return np.array(sorted(set(b)))


class Grid:
    def __init__(self, a):
        h, w, _ = a.shape
        if GRADE: (px, fx), (py, fy) = (GRADE[0], 0), (GRADE[1], 0)
        else: (px, fx), (py, fy) = measure_grid(a)
        self.bx, self.by = bounds(px, fx, w), bounds(py, fy, h)
        self.nc, self.nr = len(self.bx) - 1, len(self.by) - 1
        self.w, self.h = w, h
        self.row_of = np.searchsorted(self.by, np.arange(h), 'right') - 1
        self.col_of = np.searchsorted(self.bx, np.arange(w), 'right') - 1
        self.px, self.py = px, py

    def cell_at(self, x, y):
        return (int(np.clip(np.searchsorted(self.bx, x, 'right') - 1, 0, self.nc - 1)),
                int(np.clip(np.searchsorted(self.by, y, 'right') - 1, 0, self.nr - 1)))

    def paint(self, a, c, r, col):
        if 0 <= c < self.nc and 0 <= r < self.nr:
            a[self.by[r]:self.by[r + 1], self.bx[c]:self.bx[c + 1]] = col


# ---------------- respiração por células (igual ao GIF da menina de roxo) ----------------
def smooth(t): return t * t * (3 - 2 * t)


def plateau(t):
    """0 = expirou, 1 = inspirou. Sobe, segura em cima, desce, repousa."""
    t %= 1.0
    if t < 0.10: return 0.0
    if t < 0.38: return smooth((t - 0.10) / 0.28)
    if t < 0.58: return 1.0
    if t < 0.90: return 1.0 - smooth((t - 0.58) / 0.32)
    return 0.0


def row_shift(G, k):
    """Deslocamento (em células, inteiro) de cada linha de células no quadro k."""
    R = G.nr
    r = np.arange(R) / R
    amp = np.where(r < 0.80, 1.0, 2.0)               # cabeça/pescoço 1 célula, peito/ombros 2
    amp = np.where(np.arange(R) >= R - 2, 0.0, amp)  # barra de baixo fica ancorada
    lag = np.interp(r, [0.0, 0.80, 1.0], [0.045, 0.02, 0.0])   # peito sobe primeiro, cabeça segue
    t = k / N
    return np.array([int(round(amp[i] * plateau(t - lag[i]))) for i in range(R)])


def breathe(a, G, k):
    sh = row_shift(G, k)
    r = G.row_of
    off = np.arange(G.h) - G.by[r]
    rs = np.clip(r + sh[r], 0, G.nr - 1)
    src = np.minimum(G.by[rs] + off, G.by[rs + 1] - 1)
    return a[src]


# ---------------- desenho das linhas ----------------
def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def shades(c):
    c = np.array(c, float)
    return tuple(int(v) for v in c * 0.5), tuple(int(v) for v in c + (255 - c) * 0.30)


def bres(x0, y0, x1, y1):
    pts = []; dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1; err = dx - dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1): break
        e2 = 2 * err
        if e2 > -dy: err -= dy; x0 += sx
        if e2 < dx: err += dx; y0 += sy
    return pts


def raster(poly):
    out = []
    for (a, b), (c, d) in zip(poly, poly[1:]):
        for p in bres(a, b, c, d):
            if not out or out[-1] != p: out.append(p)
    return out or [poly[0]]


def polylines():
    """Desenho da menina de roxo escalado ao rosto deste personagem. Saída em PIXELS do sprite."""
    (xl, y), (xr, _) = OLHOS
    u = lambda p: p / 7.0 - 0.5
    f = (u(xr) - u(xl)) / 20.4
    ey, fx = u(y), (u(xl) + u(xr)) / 2

    def ymap(yy):
        if yy <= G_CHIN: return ey + (yy - G_EYE_ROW) * f
        return QUEIXO + (yy - G_CHIN) / (G_APEX - G_CHIN) * (APICE - QUEIXO)

    xmap = lambda xx: fx + (xx - G_FACE_AX) * f
    out = []
    for name, g in GIRL.items():
        for poly in g['L']:
            if name == 'fore':
                fx0, fy0 = TESTA
                out.append((name, [((fx0 + x * f * 1.1 + 0.5) * 7, (fy0 + yy * f * 1.1 + 0.5) * 7)
                                   for x, yy in [(0, 0), (0, 3), (3, 3), (3, 4)]]))
                continue
            out.append((name, [((xmap(x) + 0.5) * 7, (ymap(yy) + 0.5) * 7) for x, yy in poly]))
            if g['mirror'] is not None:
                out.append((name, [((xmap(g['mirror'] - x) + 0.5) * 7, (ymap(yy) + 0.5) * 7) for x, yy in poly]))
    return out


def build_traces(G, bgm):
    traces = []
    for name, poly in polylines():
        q = []
        for x, y in poly:
            c = G.cell_at(x, y)
            if not q or q[-1] != c: q.append(c)
        cells = raster(q) if len(q) > 1 else q
        keep = []
        for c, r in cells:
            cy, cx = (G.by[r] + G.by[r + 1]) // 2, (G.bx[c] + G.bx[c + 1]) // 2
            if not bgm[cy, cx]: keep.append((c, r))
        if keep: traces.append((name, keep))
    return traces


def draw_lines(a, G, traces, k, g):
    dim, br = shades(COR)
    for i, (name, cells) in enumerate(traces):
        L = len(cells)
        pos = (k * L / N + i * 0.17 * L) % L
        for j, (c, r) in enumerate(cells):
            d = min(abs(j - pos), L - abs(j - pos))
            t = max(0.0, 1 - d / 3.0)
            col = lerp(dim, br, min(1, t * g + 0.30 * g))
            if j == L - 1 and L > 2: col = lerp(dim, br, min(1, 0.55 + 0.45 * g))   # nó aceso
            G.paint(a, c, r, col)


def eye_glow(a, g):
    """Só a íris vira a cor da IA (luminância original preservada); o resto do olho não muda."""
    rx, ry = RAIO_OLHO
    h, w, _ = a.shape; ref = a.copy()
    Y, X = np.mgrid[0:h, 0:w]
    lum = 0.3 * ref[..., 0] + 0.59 * ref[..., 1] + 0.11 * ref[..., 2]
    base = np.array(COR, float)
    for (cx, cy) in OLHOS:
        m = ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2 <= 1
        iris = m & (lum > 48) & (lum < 190)
        kk = np.clip(lum / 130, 0.45, 1.25)[..., None]
        a[iris] = np.clip(base * kk * (0.75 + 0.25 * g), 0, 255)[iris]


def glow_ready(a, g):
    """Menina de roxo: pulsa os detalhes ciano que já existem na arte."""
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]
    m = (b > 140) & (gg > 130) & (r < 130) & (b - r > 60)
    kk = 0.20 * g - 0.10
    for ch in range(3):
        v = a[..., ch]
        a[..., ch] = np.where(m, np.clip(v + (255 - v) * max(kk, 0) + v * min(kk, 0) * 0.8, 0, 255), v)
    dim = (r < 45) & (b > 80) & (b > r + 60) & (gg > r + 50) & ~m
    tgt = np.array([40, 200, 225], float)
    for ch in range(3):
        v = a[..., ch]
        a[..., ch] = np.where(dim, v + (tgt[ch] - v) * (0.45 * g - 0.10), v)


def pulse(t):                      # brilho 0..1 acompanhando a respiração
    return 0.5 - 0.5 * math.cos(2 * math.pi * (t % 1.0))


def save_gif(frames, path):
    ims = [Image.fromarray(x) for x in frames]
    mos = Image.new('RGB', (ims[0].width * 4, ims[0].height * 2))
    for i, kk in enumerate(np.linspace(0, N, 8, endpoint=False).astype(int)):
        mos.paste(ims[kk], ((i % 4) * ims[0].width, (i // 4) * ims[0].height))
    pal = mos.quantize(colors=255, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE)
    q = [im.quantize(palette=pal, dither=Image.Dither.NONE) for im in ims]
    q[0].save(path, save_all=True, append_images=q[1:], duration=MS, loop=0, disposal=1)


def ia_base(sprite, G, bgm, traces, k, g, ready=None):
    a = (ready if ready is not None else sprite).astype(np.float32).copy()
    if ready is not None:
        glow_ready(a, g)
    else:
        eye_glow(a, g)
    a = np.clip(a, 0, 255).astype(np.uint8)
    if ready is None: draw_lines(a, G, traces, k, g)
    return a


def gerar():
    aqui = os.path.dirname(os.path.abspath(__file__))
    sprite = np.array(Image.open(os.path.join(aqui, 'sprite_humano.png')).convert('RGB'))
    ready = np.array(Image.open(os.path.join(aqui, 'sprite_ia.png')).convert('RGB')) if PRONTO else None
    G = Grid(sprite)
    bgm = (sprite[..., 0] > 235) & (sprite[..., 1] > 225)
    traces = [] if PRONTO else build_traces(G, bgm)
    humano = [breathe(sprite, G, k) for k in range(N)]
    ia = []
    for k in range(N):
        g = 0.45 + 0.55 * pulse(k / N)
        ia.append(breathe(ia_base(sprite, G, bgm, traces, k, g, ready), G, k))
    save_gif(humano, os.path.join(aqui, 'humano.gif'))
    save_gif(ia, os.path.join(aqui, 'ia.gif'))
    Image.fromarray(sprite).save(os.path.join(aqui, 'humano_estatico.png'))
    est = ia_base(sprite, G, bgm, traces, int(N * 0.4), 1.0, ready)
    Image.fromarray(est).save(os.path.join(aqui, 'ia_estatico.png'))
    print('ok:', NOME, '| grade', G.nc, 'x', G.nr, 'células de %.2f x %.2f px' % (G.px, G.py))


if __name__ == '__main__':
    gerar()
