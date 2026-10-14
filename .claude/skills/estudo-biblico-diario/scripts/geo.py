"""Mapas esquemáticos (SVG) para a folha de estudo.

Base: contorno de terra do Natural Earth (domínio público, via world-atlas), recortado para a
região bíblica em dados/terra.json. Rios e lagos pequenos foram desenhados à mão: são
aproximações pedagógicas, NÃO cartografia. O mapa sempre diz "esquemático, fora de escala".
"""
import json
import math

import biblia as B

TERRA = json.loads((B.DADOS / "terra.json").read_text(encoding="utf-8"))
LUGARES = {k: v for k, v in json.loads((B.DADOS / "lugares.json").read_text(encoding="utf-8")).items()
           if not k.startswith("_")}

REGIOES = {   # lon0, lat0, lon1, lat1
    "canaa": (33.7, 30.7, 37.5, 33.8),
    "egito": (28.0, 22.0, 40.0, 33.0),
    "oriente-medio": (24.0, 24.0, 56.0, 42.0),
    "mesopotamia": (36.0, 28.0, 52.0, 39.0),
    "asia-menor": (24.0, 35.0, 38.0, 42.0),
    "mediterraneo": (8.0, 30.0, 38.0, 46.0),
}

RIOS = {   # nome: (pontos lon/lat, ponto do rótulo)
    "Nilo": ([(31.2, 31.5), (31.25, 30.0), (31.0, 27.5), (32.6, 25.7), (32.9, 24.1), (32.9, 22.0), (31.5, 19.5)], (31.0, 27.3)),
    "Eufrates": ([(39.5, 38.8), (38.0, 36.8), (39.0, 35.9), (40.5, 34.9), (42.4, 34.4), (43.8, 33.4), (44.4, 32.5), (46.0, 31.0), (47.6, 30.4)], (41.2, 35.0)),
    "Tigre": ([(39.7, 38.5), (41.0, 37.9), (42.4, 37.1), (43.15, 36.36), (43.5, 35.4), (44.4, 33.3), (45.6, 32.4), (46.7, 31.5), (47.6, 30.4)], (44.4, 34.5)),
    "Jordão": ([(35.65, 33.25), (35.6, 32.9), (35.57, 32.69), (35.55, 32.3), (35.53, 32.0), (35.55, 31.76)], (35.62, 32.2)),
}
LAGOS = {
    "Mar Morto": ([(35.5, 31.77), (35.55, 31.55), (35.52, 31.3), (35.43, 31.05), (35.38, 31.2), (35.45, 31.5), (35.47, 31.75)], (35.55, 31.4)),
    "Mar da Galileia": ([(35.55, 32.88), (35.64, 32.8), (35.64, 32.7), (35.57, 32.69), (35.52, 32.78)], (35.66, 32.82)),
}
MARES = {
    "Mar Mediterrâneo": (30.5, 36.0), "Mar Vermelho": (36.5, 25.5), "Golfo Pérsico": (50.5, 27.2),
    "Mar Negro": (34.0, 43.0), "Mar Cáspio": (51.0, 41.5), "Mar Egeu": (25.3, 38.9), "Mar Mediterrâneo ": (15.0, 34.2), "Mar Mediterrâneo  ": (33.9, 32.1), "Mar Mediterrâneo   ": (30.0, 33.3),
}
IMPERIO_PERSA = [(24.5, 31.3), (26, 36), (26.5, 40.2), (29, 41), (36, 41.8), (41.5, 41.3), (44, 41.2), (48, 40), (52.5, 37), (56, 37.8),
                 (61, 37.2), (66, 37.5), (71, 34), (70.5, 28), (66.5, 25.2), (61, 25.2), (57, 27), (54, 26.8), (50.5, 29.5), (48, 29.9),
                 (43, 31), (39, 30.2), (36, 29.5), (34.9, 29.5), (33.3, 28), (32.8, 24), (32.6, 22.3), (24.5, 22.3)]   # esquemático
REFERENCIAS = ["Jerusalém", "Babilônia", "Mênfis", "Roma", "Nínive", "Damasco", "Atenas", "Éfeso", "Antioquia da Síria"]

AGUA, TERRA_COR, BORDA = "#D8F0FF", "#FFF7DC", "#E9CF8C"
FONTE_TXT = "font-family:'Nunito','Trebuchet MS',Verdana,sans-serif"


def _proj(bb, W):
    lon0, lat0, lon1, lat1 = bb
    c = math.cos(math.radians((lat0 + lat1) / 2))
    k = W / ((lon1 - lon0) * c)
    H = (lat1 - lat0) * k
    return (lambda lon, lat: ((lon - lon0) * c * k, (lat1 - lat) * k)), H, k, c


def _caminho(pts, f, fechar=True):
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (f(*p) for p in pts))
    return s + ("Z" if fechar else "")


def _suave(pts, f):
    """Linha aberta suavizada (curvas quadráticas pelos pontos médios)."""
    p = [f(*q) for q in pts]
    if len(p) < 3:
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in p)
    d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for a, b in zip(p[1:-1], p[2:]):
        d += f" Q{a[0]:.1f},{a[1]:.1f} {(a[0] + b[0]) / 2:.1f},{(a[1] + b[1]) / 2:.1f}"
    return d + f" L{p[-1][0]:.1f},{p[-1][1]:.1f}"


def lugares_numerados(mapa, bbox_ok=None):
    """Ordem dos pinos numerados (mesma do desenho): nomes em mapa['lugares'] que existem na gazeta."""
    return [n for n in mapa.get("lugares", []) if n in LUGARES]


def _bbox_auto(nomes, pad=0.22, minimo=(3.6, 2.6)):
    pts = [LUGARES[n][:2] for n in nomes if n in LUGARES]
    if not pts:
        return REGIOES["oriente-medio"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(max(xs) - min(xs), minimo[0]), max(max(ys) - min(ys), minimo[1])
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return (cx - w * (0.5 + pad), cy - h * (0.5 + pad), cx + w * (0.5 + pad), cy + h * (0.5 + pad))


def _colide(r, caixas):
    for o in caixas:
        if not (r[2] < o[0] or r[0] > o[2] or r[3] < o[1] or r[1] > o[3]):
            return True
    return False


_N_MAPA = [0]


def mapa_svg(mapa, cor="#FF7EB6", largura=520, agua=None, terra=None, borda=None, tinta=None, aspecto=None):
    """`mapa` (do JSON do dia): regiao, lugares[], rotas[], rios_destaque[], textos[], nota."""
    nomes = mapa.get("lugares", [])
    for r in mapa.get("rotas", []):
        nomes = nomes + [n for n in r["lugares"] if n not in nomes]
    AGUA, TERRA_COR, BORDA = agua or globals()["AGUA"], terra or globals()["TERRA_COR"], borda or globals()["BORDA"]
    _N_MAPA[0] += 1
    uid = f"m{_N_MAPA[0]}"   # ids únicos: vários mapas na mesma página não podem dividir clipPath
    desconhecidos = [n for n in nomes if n not in LUGARES]
    if desconhecidos:
        raise SystemExit("Lugares fora de dados/lugares.json (adicione com fonte): " + ", ".join(desconhecidos))
    regiao = mapa.get("regiao", "auto")
    bb = _bbox_auto(nomes) if regiao == "auto" else (tuple(mapa["bbox"]) if regiao == "bbox" else REGIOES[regiao])
    if aspecto:   # ajusta o recorte à proporção altura/largura pedida (mapa estreito na lateral)
        lon0, lat0, lon1, lat1 = bb
        cx, cy = (lon0 + lon1) / 2, (lat0 + lat1) / 2
        cs = math.cos(math.radians(cy))
        w, h = (lon1 - lon0) * cs, lat1 - lat0
        if h / w < aspecto:
            h = w * aspecto
        else:
            w = h / aspecto
        bb = (cx - w / cs / 2, cy - h / 2, cx + w / cs / 2, cy + h / 2)
    f, H, k, c = _proj(bb, largura)
    H = round(H)
    forte = B.escurecer(cor, 0.35)
    o = [f'<svg class="mapa" viewBox="0 0 {largura} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Mapa esquemático">',
         f'<defs><clipPath id="rec{uid}"><rect width="{largura}" height="{H}" rx="14"/></clipPath>'
         f'<marker id="seta{uid}" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
         f'<path d="M0,0L10,5L0,10z" fill="{forte}"/></marker></defs>',
         f'<pattern id="ond{uid}" width="34" height="14" patternUnits="userSpaceOnUse"><path d="M0,8 q8.5,-6 17,0 t17,0" fill="none" stroke="#FFFFFF" stroke-width="1.3" opacity=".55"/></pattern>',
         f'<g clip-path="url(#rec{uid})"><rect width="{largura}" height="{H}" fill="{AGUA}"/><rect width="{largura}" height="{H}" fill="url(#ond{uid})"/>']
    for r in TERRA["aneis"]:
        o.append(f'<path d="{_caminho(r, f)}" fill="{TERRA_COR}" stroke="{BORDA}" stroke-width="1.1" stroke-linejoin="round"/>')
    for r in TERRA["lagos"]:
        o.append(f'<path d="{_caminho(r, f)}" fill="{AGUA}" stroke="{BORDA}" stroke-width="1"/>')
    for nome, (pts, _) in LAGOS.items():
        o.append(f'<path d="{_caminho(pts, f)}" fill="{AGUA}" stroke="#8CCBEF" stroke-width="1"/>')
    if mapa.get("imperio"):   # preenchimento só sobre a terra (clip), contorno tracejado por cima
        terra_d = " ".join(_caminho(r, f) for r in TERRA["aneis"])
        o.append(f'<clipPath id="terra{uid}"><path d="{terra_d}"/></clipPath>'
                 f'<path d="{_caminho(IMPERIO_PERSA, f)}" fill="{cor}" fill-opacity=".16" clip-path="url(#terra{uid})"/>'
                 f'<path d="{_caminho(IMPERIO_PERSA, f)}" fill="none" stroke="{forte}" stroke-width="2.2" stroke-dasharray="10 6" stroke-linejoin="round"/>')
    destaque = set(mapa.get("rios_destaque", []))
    for nome, (pts, _) in RIOS.items():
        forte_rio = nome in destaque
        o.append(f'<path d="{_suave(pts, f)}" fill="none" stroke="{"#1BA5B8" if forte_rio else "#8CCBEF"}" '
                 f'stroke-width="{3.2 if forte_rio else 2}" stroke-linecap="round" stroke-linejoin="round"/>')

    caixas, rotulos = [], []

    def txt(x, y, s, tam, cortxt, peso=800, estilo="", anchor="start", extra=""):
        return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="{FONTE_TXT};font-size:{tam}px;font-weight:{peso};{estilo}" '
                f'fill="{cortxt}" stroke="#fff" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round" {extra}>{s}</text>')

    # mares, rios e lagos (rótulos) — só se estiverem dentro do quadro
    def dentro(lon, lat):
        return bb[0] + .1 < lon < bb[2] - .1 and bb[1] + .1 < lat < bb[3] - .1
    def reserva(x, y, s, tam, anc="start"):
        w = len(s) * tam * 0.56 + 6
        x0 = x if anc == "start" else x - w / 2
        caixas.append((x0, y - tam, x0 + w, y + 3))
    ja_mar = set()
    for nome, (lon, lat) in ({} if mapa.get("sem_nomes") else MARES).items():
        if dentro(lon, lat) and nome.strip() not in ja_mar:
            x, y = f(lon, lat)
            meia = len(nome.strip()) * 9.5 * 0.56 / 2 + 8
            if x - meia < 4 or x + meia > largura - 4:
                continue
            ja_mar.add(nome.strip())
            reserva(x, y, nome.strip(), 9.5, "middle")
            o.append(txt(x, y, nome.strip(), 9.5, "#6BA8CC", 700, "font-style:italic;letter-spacing:1px", "middle"))
    for nome, (_, (lon, lat)) in ({} if mapa.get("sem_nomes") else RIOS).items():
        if dentro(lon, lat) and f(lon, lat)[0] + 90 < largura:
            x, y = f(lon, lat)
            reserva(x + 6, y, f"Rio {nome}", 8.5)
            o.append(txt(x + 6, y, f"Rio {nome}" if nome != "Jordão" else "Rio Jordão", 8.5, "#1496A8" if nome in destaque else "#5FA6C4", 700, "font-style:italic"))
    for nome, (_, (lon, lat)) in ({} if mapa.get("sem_nomes") else LAGOS).items():
        if dentro(lon, lat) and f(lon, lat)[0] + 90 < largura:
            x, y = f(lon, lat)
            reserva(x + 7, y, nome, 8)
            o.append(txt(x + 7, y, nome, 8, "#5FA6C4", 700, "font-style:italic"))
    for t in mapa.get("textos", []):   # nomes de regiões/impérios: {"texto","lon","lat"}
        x, y = f(t["lon"], t["lat"])
        o.append(txt(x, y, t["texto"].upper(), 11, "#B9A5D6", 900, "letter-spacing:3px", "middle"))

    # rotas
    for r in mapa.get("rotas", []):
        cr = r.get("cor", forte)
        pts = [f(*LUGARES[n][:2]) for n in r["lugares"]]
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            nx, ny = -(y1 - y0), (x1 - x0)
            n = math.hypot(nx, ny) or 1
            q = 0.13 * n
            d += f" Q{mx + nx / n * q:.1f},{my + ny / n * q:.1f} {x1:.1f},{y1:.1f}"
        o.append(f'<path d="{d}" fill="none" stroke="{cr}" stroke-width="3" stroke-dasharray="7 5" '
                 f'stroke-linecap="round" marker-end="url(#seta{uid})" opacity=".95"/>')

    # pinos principais
    marcados = []
    for n in nomes:
        lon, lat = LUGARES[n][:2]
        if not (bb[0] < lon < bb[2] and bb[1] < lat < bb[3]):
            continue
        marcados.append(n)
        x, y = f(lon, lat)
        inc = len(LUGARES[n]) > 2
        caixas.append((x - 11, y - 11, x + 11, y + 11))
        tracejado = ' stroke-dasharray="2.5 2"' if inc else ""
        preench = "#fff" if inc else cor
        if mapa.get("numerar"):
            num = marcados.index(n) + 1
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9.5" fill="{forte}" stroke="#fff" stroke-width="2"{tracejado}/>'
                     f'<text x="{x:.1f}" y="{y + 3.6:.1f}" text-anchor="middle" style="{FONTE_TXT};font-size:10px;font-weight:900" fill="#fff">{num}</text>')
        else:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.2" fill="{preench}" stroke="{forte}" '
                     f'stroke-width="2.2"{tracejado}/>')
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{forte}"/>')
    # referências (cinza) — só se não colidirem
    refs = []
    for n in REFERENCIAS:
        if n in marcados or n not in LUGARES:
            continue
        lon, lat = LUGARES[n][:2]
        if bb[0] + .05 < lon < bb[2] - .05 and bb[1] + .05 < lat < bb[3] - .05:
            refs.append(n)

    def colocar(n, tam, corpo, peso, principal):
        x, y = f(*LUGARES[n][:2])
        w = len(n) * tam * 0.56 + 6
        h = tam + 3
        opcoes = [(10, 4, "start"), (-10, 4, "end"), (0, -10, "middle"), (0, 17, "middle"),
                  (9, -7, "start"), (-9, -7, "end"), (9, 15, "start"), (-9, 15, "end")]
        for dx, dy, anc in opcoes:
            tx, ty = x + dx, y + dy
            x0 = tx if anc == "start" else tx - w if anc == "end" else tx - w / 2
            r = (x0, ty - tam, x0 + w, ty + 3)
            if r[0] < 2 or r[2] > largura - 2 or r[1] < 2 or r[3] > H - 2:
                continue
            if not _colide(r, caixas):
                caixas.append(r)
                rotulos.append(txt(tx, ty, n, tam, corpo, peso, "", anc))
                return True
        if principal:   # sem espaço livre: escreve mesmo assim, à esquerda
            rotulos.append(txt(x - 10, y + 4, n, tam, corpo, peso, "", "end"))
            return True
        return False
    if not mapa.get("sem_nomes"):
        for n in marcados:
            colocar(n, 10.5, B.TINTA, 800, True) or colocar(n, 8.5, B.TINTA, 800, True)
    for n in ([] if (mapa.get("sem_nomes") or mapa.get("numerar")) else refs):
        x, y = f(*LUGARES[n][:2])
        if _colide((x - 4, y - 4, x + 4, y + 4), caixas):
            continue
        if colocar(n, 8, "#9A90B0", 700, False):
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#B9AED0" stroke="#fff" stroke-width="1"/>')
    o.extend(rotulos)

    # norte + barra de escala (~100 km)
    km100 = 100 / 111.0 * k
    o.append(f'<g transform="translate({largura - 26},24)"><path d="M0,-12 L6,6 L0,2 L-6,6z" fill="{forte}"/>'
             f'<text y="19" text-anchor="middle" style="{FONTE_TXT};font-size:9px;font-weight:900" fill="{forte}">N</text></g>')
    o.append(f'<g transform="translate(12,{H - 14})"><rect width="{km100:.1f}" height="5" fill="#fff" stroke="{forte}" stroke-width="1.2"/>'
             f'<text x="{km100 + 5:.1f}" y="6" style="{FONTE_TXT};font-size:8px;font-weight:700" fill="{forte}">≈ 100 km</text></g>')
    o.append('</g>')
    o.append(f'<rect width="{largura}" height="{H}" rx="14" fill="none" stroke="{forte}" stroke-width="2.2"/></svg>')
    return "".join(o)
