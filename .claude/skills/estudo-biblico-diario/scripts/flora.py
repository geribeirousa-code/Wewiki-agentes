"""Ilustração botânica em SVG para o planner (estilo recorte plano: folhas sálvia com nervura,
tulipas, margaridas e flores abstratas). Tudo procedural e determinístico por `semente`,
para cada semana ter sua própria faixa floral.
"""
import math
import random

# Paletas florais (folhas + flores). A cor de destaque da semana vem do mesmo conjunto.
PALETAS = {
    "salvia":    dict(folhas=["#A9C5B4", "#8FB09E", "#C2D8C9"], nervura="#2F5F5A", flores=["#F4C9C2", "#E9B949", "#F2D98B"], tinta="#2F5F5A"),
    "terracota": dict(folhas=["#B9CDBB", "#9DB9A5"], nervura="#2F5F5A", flores=["#D6532A", "#F0826A", "#FBD6C7", "#E9B949"], tinta="#B8431F"),
    "azul":      dict(folhas=["#A9C5B4", "#C2D8C9"], nervura="#2F5F5A", flores=["#2F5F8F", "#5B8DB8", "#F4C9C2", "#E9B949"], tinta="#2F5F8F"),
    "mostarda":  dict(folhas=["#A9C5B4", "#8FB09E"], nervura="#2F5F5A", flores=["#E9B949", "#F2CF6E", "#F4C9C2"], tinta="#9A6B10"),
    "rosa":      dict(folhas=["#A9C5B4", "#8FB09E", "#C2D8C9"], nervura="#2F5F5A", flores=["#E88FA0", "#F4C9C2", "#F7DDD8", "#E9B949"], tinta="#B04A63"),
}
ORDEM = ["salvia", "terracota", "azul", "mostarda", "rosa"]
CREME = "#FBF6EC"


def _g(x, y, ang, s, corpo):
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f}) scale({s:.3f})">{corpo}</g>'


def folha(x, y, comp, larg, ang, cor, nervura, curva=0.0):
    c = curva * larg
    corpo = (f'<path d="M0,0 C{.3 * comp:.1f},{-larg + c:.1f} {.72 * comp:.1f},{-larg - c:.1f} {comp:.1f},{c * .6:.1f} '
             f'C{.7 * comp:.1f},{larg + c:.1f} {.28 * comp:.1f},{larg - c:.1f} 0,0Z" fill="{cor}"/>'
             f'<path d="M2,0 Q{.5 * comp:.1f},{c * .5:.1f} {.94 * comp:.1f},{c * .55:.1f}" fill="none" stroke="{nervura}" '
             f'stroke-width="{max(1.1, comp / 150):.1f}" stroke-linecap="round" opacity=".85"/>')
    return _g(x, y, ang, 1, corpo)


def tulipa(x, y, s, ang, c1, c2, caule="#8FB09E"):
    corpo = (f'<path d="M0,0 C-5,70 5,130 0,190" fill="none" stroke="{caule}" stroke-width="5" stroke-linecap="round"/>'
             f'<path d="M-27,-8 C-34,-48 -14,-82 0,-98 C14,-82 34,-48 27,-8 C14,6 -14,6 -27,-8Z" fill="{c1}"/>'
             f'<path d="M-9,-6 C-15,-46 -5,-74 0,-90 C5,-74 15,-46 9,-6Z" fill="{c2}"/>'
             f'<path d="M-20,-20 C-22,-40 -14,-58 -8,-70" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".55"/>')
    return _g(x, y, ang, s, corpo)


def margarida(x, y, s, ang, petala="#F7DDD8", miolo="#E9B949", n=14):
    p = "".join(f'<ellipse cx="0" cy="-26" rx="7.5" ry="23" fill="{petala}" transform="rotate({i * 360 / n:.1f})"/>' for i in range(n))
    corpo = (p + f'<circle r="14" fill="{miolo}"/><circle r="14" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="1.5 4.5" opacity=".7"/>')
    return _g(x, y, ang, s, corpo)


def flor_abstrata(x, y, s, ang, cor="#2F5F8F", miolo="#E9B949"):
    petalas = ""
    for i in range(5):
        a = i * 72
        petalas += (f'<g transform="rotate({a})"><path d="M0,-6 C-26,-22 -24,-62 0,-66 C24,-62 26,-22 0,-6Z" fill="{cor}"/>'
                    f'<ellipse cx="0" cy="-34" rx="3.6" ry="6" fill="#fff" opacity=".85"/>'
                    f'<ellipse cx="-10" cy="-48" rx="2.6" ry="4.4" fill="#fff" opacity=".75"/>'
                    f'<ellipse cx="10" cy="-48" rx="2.6" ry="4.4" fill="#fff" opacity=".75"/></g>')
    return _g(x, y, ang, s, petalas + f'<circle r="11" fill="{miolo}"/>')


def botao(x, y, s, cor, miolo):
    return _g(x, y, 0, s, f'<circle r="12" fill="{cor}"/><circle r="4.5" fill="{miolo}"/>')


def composicao(larg, alt, semente, paleta="salvia", densidade=1.0, escala=1.0):
    """Faixa/canto floral: folhas sálvia compridas + 2–4 flores da paleta. Devolve o miolo do SVG."""
    r = random.Random(semente)
    P = PALETAS[paleta]
    o = []
    nf = max(5, int(larg * alt / 2400 * densidade))
    for _ in range(nf):
        comp = r.uniform(.5, 1.0) * alt * 1.1 * escala
        o.append(folha(r.uniform(-.05, 1.05) * larg, r.uniform(.1, 1.1) * alt, comp, comp * r.uniform(.14, .22),
                       r.uniform(-120, -40) if r.random() < .5 else r.uniform(40, 130),
                       r.choice(P["folhas"]), P["nervura"], r.uniform(-.25, .25)))
    nfl = max(3, int(larg * alt / 3600 * densidade))
    for i in range(nfl):
        x, y = r.uniform(.08, .92) * larg, r.uniform(.15, .85) * alt
        tipo = r.choice(["tulipa", "margarida", "abstrata", "botao"])
        s = r.uniform(.8, 1.25) * escala * (alt / 135)
        cor = r.choice(P["flores"])
        if tipo == "tulipa":
            o.append(tulipa(x, y, s, r.uniform(-25, 25), cor, r.choice(P["flores"])))
        elif tipo == "margarida":
            o.append(margarida(x, y, s * 1.1, r.uniform(0, 30), "#F7DDD8" if r.random() < .6 else cor, "#E9B949"))
        elif tipo == "abstrata":
            o.append(flor_abstrata(x, y, s * 1.05, r.uniform(0, 70), cor, "#E9B949"))
        else:
            o.append(botao(x, y, s * 1.6, cor, "#E9B949"))
    return "".join(o)


def faixa(larg, alt, semente, paleta="salvia", raio=14, escala=1.0, densidade=1.0):
    """Retângulo arredondado com recorte floral (usado no sumário e nos cabeçalhos)."""
    return (f'<svg width="{larg}" height="{alt}" viewBox="0 0 {larg} {alt}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><clipPath id="c{semente}"><rect width="{larg}" height="{alt}" rx="{raio}"/></clipPath></defs>'
            f'<g clip-path="url(#c{semente})"><rect width="{larg}" height="{alt}" fill="{CREME}"/>'
            f'{composicao(larg, alt, semente, paleta, densidade, escala)}</g></svg>')


def capa_svg(w=816, h=1056, semente=7):
    """Capa: folhas verticais compridas em cima e embaixo, tulipas, e uma faixa creme no meio."""
    r = random.Random(semente)
    o = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
         f'<rect width="{w}" height="{h}" fill="{CREME}"/>']
    P = PALETAS["salvia"]
    def metade(topo):
        sinal = 1 if topo else -1
        y0 = 0 if topo else h
        # folhas longas descendo (topo) ou subindo (base)
        base = [(.30, 230, 54, 78), (.42, 300, 62, 92), (.55, 340, 64, 100), (.66, 280, 56, 80), (.80, 260, 52, 72), (.18, 200, 46, 70),
                (.92, 220, 50, 100), (.06, 230, 50, 82)]
        for fx, comp, lg, ang in base:
            a = (ang if topo else -ang) + r.uniform(-8, 8)
            o.append(folha(fx * w + r.uniform(-20, 20), y0, comp * 1.55, lg * 1.5, a if topo else a, r.choice(P["folhas"]), P["nervura"], r.uniform(-.3, .3)))
        if topo:
            o.append(tulipa(.19 * w, 20, 1.5, 172, "#F4C9C2", "#F8DCD6", "#8FB09E"))
            o.append(tulipa(.12 * w, 380, 1.2, 4, "#E9B949", "#F2CF6E", "#8FB09E"))
            o.append(tulipa(.84 * w, 70, 1.15, 0, "#E9B949", "#F2CF6E", "#8FB09E"))
        else:
            o.append(tulipa(.30 * w, h - 40, 1.5, 4, "#E9B949", "#F2CF6E", "#8FB09E"))
            o.append(tulipa(.76 * w, h - 40, 1.4, -6, "#E9B949", "#F2CF6E", "#8FB09E"))
            o.append(margarida(.56 * w, h - 120, 1.3, 0, "#F7DDD8", "#E9B949"))
    metade(True)
    metade(False)
    # faixa central
    y1, y2 = h * .385, h * .615
    o.append(f'<rect x="0" y="{y1:.1f}" width="{w}" height="{y2 - y1:.1f}" fill="#FFFCF6"/>')
    for yy in (y1, y2):
        o.append(f'<line x1="0" x2="{w}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#F1C9C3" stroke-width="2.5"/>'
                 f'<line x1="0" x2="{w}" y1="{yy + 7:.1f}" y2="{yy + 7:.1f}" stroke="#F1C9C3" stroke-width="1" />' if yy == y1 else
                 f'<line x1="0" x2="{w}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#F1C9C3" stroke-width="2.5"/>')
    o.append('</svg>')
    return "".join(o)
