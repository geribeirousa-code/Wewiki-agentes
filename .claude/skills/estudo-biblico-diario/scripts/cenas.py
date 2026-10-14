"""Cenas ilustradas para as páginas de pausa: Jesus e as mulheres do Evangelho.

Vetor, em estilo de pintura suave (gradientes e grão de papel). Figuras sem traços de
rosto além do essencial, por respeito e porque ninguém sabe como eles eram: são cenas
devocionais, não retratos. Cada cena ilustra um texto bíblico (referência na página).
"""
import math
import random

import flora

W, H = 816, 640
PELE = "#E8C3A0"
CAB_J = "#6A4A36"
MANTO_J = "#FBF6EC"


def _defs(uid, topo, base, luz=True):
    return (f'<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{topo}"/><stop offset="1" stop-color="{base}"/></linearGradient>'
            f'<filter id="grao{uid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="n"/>'
            f'<feColorMatrix in="n" type="matrix" values="0 0 0 0 .45  0 0 0 0 .36  0 0 0 0 .26  0 0 0 .22 0"/></filter>'
            f'<radialGradient id="luz{uid}" cx=".5" cy=".35" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".65"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="rc{uid}"><rect width="{W}" height="{H}"/></clipPath></defs>')


def _moldura(uid, corpo, topo, base, luz=True):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img">{_defs(uid, topo, base)}'
            f'<g clip-path="url(#rc{uid})"><rect width="{W}" height="{H}" fill="url(#g{uid})"/>'
            f'{f"<rect width={chr(34)}{W}{chr(34)} height={chr(34)}{H}{chr(34)} fill={chr(34)}url(#luz{uid}){chr(34)}/>" if luz else ""}'
            f'{corpo}<rect width="{W}" height="{H}" filter="url(#grao{uid})" opacity=".55"/></g></svg>')


# ---------------------------------------------------------------- figuras
def cabeca(x, y, s=1.0, dir=1, pele=PELE, cabelo=CAB_J, barba=True, veu=None, inclinada=0):
    """Cabeça de perfil olhando para a direita (dir=1) ou esquerda (dir=-1)."""
    c = []
    if veu:
        c.append(f'<path d="M-20,-4 C-26,-32 -2,-46 16,-30 C26,-20 24,10 20,40 C6,46 -10,44 -22,38 C-24,22 -22,8 -20,-4Z" fill="{veu}"/>')
    else:
        c.append(f'<path d="M-16,-6 C-30,2 -28,32 -20,50 C-6,48 6,40 10,24Z" fill="{cabelo}"/>')
    c.append(f'<ellipse cx="0" cy="0" rx="14" ry="18" fill="{pele}"/>')
    c.append(f'<path d="M13,-2 L19,6 L12,8Z" fill="{pele}"/>')
    if not veu:
        c.append(f'<path d="M-15,-6 C-16,-28 8,-32 15,-14 C8,-17 -1,-14 -7,-5Z" fill="{cabelo}"/>')
    else:
        c.append(f'<path d="M-15,-8 C-10,-26 12,-26 15,-10 C8,-14 -4,-14 -15,-8Z" fill="{veu}"/>')
    if barba:
        c.append(f'<path d="M-8,8 C-6,32 17,32 14,9 C10,18 2,20 -8,8Z" fill="{cabelo}"/>')
    c.append('<path d="M5,-3 q4,2 8,0" fill="none" stroke="#4B3226" stroke-width="1.7" stroke-linecap="round"/>')
    flip = "scale(-1,1)" if dir < 0 else ""
    return f'<g transform="translate({x},{y}) rotate({inclinada}) scale({s}) {flip}">{"".join(c)}</g>'


def jesus_em_pe(x, y, s=1.0, dir=1, inclinado=0, manto="#FBF6EC", faixa="#E9C98A"):
    """Em pé, de perfil. (x, y) = pés. Altura ~ 330*s."""
    f = "scale(-1,1)" if dir < 0 else ""
    corpo = (f'<path d="M-38,0 C-30,-120 -26,-215 -16,-262 L22,-262 C34,-215 40,-120 46,0 C20,8 -10,8 -38,0Z" fill="{manto}"/>'
             f'<path d="M-38,0 C-30,-120 -26,-215 -16,-262 C-26,-200 -34,-100 -38,0Z" fill="#0000000F"/>'
             f'<path d="M-14,-250 C20,-232 36,-190 44,-130 C30,-170 10,-206 -14,-250Z" fill="{faixa}" opacity=".85"/>'
             f'<path d="M-20,-150 C10,-146 30,-150 40,-158" fill="none" stroke="#00000012" stroke-width="2"/>')
    cab = cabeca(2, -290, 1.05, 1, inclinada=inclinado)
    return f'<g transform="translate({x},{y}) scale({s}) {f}">{corpo}{cab}</g>'


def jesus_sentado(x, y, s=1.0, dir=-1, manto="#FBF6EC"):
    """Sentado numa cadeira/banco, de perfil. (x, y) = assento. dir=-1 olha para a esquerda."""
    f = "scale(-1,1)" if dir < 0 else ""
    corpo = (f'<path d="M-30,0 C-34,-60 -28,-120 -14,-150 L24,-150 C34,-110 32,-50 30,0Z" fill="{manto}"/>'
             f'<path d="M-30,0 L70,0 C74,10 72,34 66,34 L-30,34Z" fill="{manto}"/>'
             f'<path d="M60,2 C72,30 74,90 70,128 C60,132 50,132 48,126 C52,90 50,40 44,10Z" fill="{manto}"/>'
             f'<ellipse cx="70" cy="136" rx="22" ry="7" fill="{PELE}"/>'
             f'<path d="M-30,0 L70,0 C72,6 72,12 70,16 L-30,16Z" fill="#0000000C"/>'
             f'<ellipse cx="34" cy="-30" rx="14" ry="8" fill="{PELE}"/>'
             f'<path d="M-6,-132 C14,-120 26,-96 32,-40" fill="none" stroke="#0000000F" stroke-width="3"/>')
    cab = cabeca(4, -170, 1.02, 1, inclinada=6)
    return f'<g transform="translate({x},{y}) scale({s}) {f}">{corpo}{cab}</g>'


def mulher_agachada(x, y, s=1.0, dir=-1, manto="#F7EFE2", cabelo="#7A5238"):
    f = "scale(-1,1)" if dir < 0 else ""
    corpo = (f'<path d="M-26,0 C-34,-26 -24,-52 -6,-62 L22,-62 C34,-48 40,-22 38,0Z" fill="{manto}"/>'
             f'<path d="M-30,0 C-40,-16 -30,-30 -12,-30 C4,-30 18,-14 26,0Z" fill="{manto}"/>'
             f'<ellipse cx="46" cy="-4" rx="9" ry="6" fill="{PELE}"/>')
    cab = cabeca(4, -80, .72, 1, cabelo=cabelo, barba=False, inclinada=24)
    return f'<g transform="translate({x},{y}) scale({s}) {f}">{corpo}{cab}</g>'


def mulher_sentada_chao(x, y, s=1.0, dir=1, manto="#E7A5A5", veu="#F6E7D8"):
    f = "scale(-1,1)" if dir < 0 else ""
    corpo = (f'<path d="M-40,0 C-44,-30 -30,-60 -8,-70 L22,-70 C34,-50 40,-20 44,0Z" fill="{manto}"/>'
             f'<path d="M-52,0 C-50,-14 -20,-22 40,-18 C60,-16 70,-8 70,0Z" fill="{manto}"/>'
             f'<path d="M-52,0 C-50,-6 -20,-10 40,-8 C60,-8 70,-4 70,0Z" fill="#0000000F"/>')
    cab = cabeca(6, -90, .78, 1, barba=False, veu=veu, inclinada=-6)
    return f'<g transform="translate({x},{y}) scale({s}) {f}">{corpo}{cab}</g>'


def mulher_em_pe(x, y, s=1.0, dir=-1, manto="#D99A7C", veu="#F4E4C8", avental=None):
    f = "scale(-1,1)" if dir < 0 else ""
    corpo = (f'<path d="M-34,0 C-30,-110 -26,-190 -14,-232 L20,-232 C32,-190 36,-110 40,0Z" fill="{manto}"/>'
             f'<path d="M-34,0 C-30,-110 -26,-190 -14,-232 C-24,-180 -30,-100 -34,0Z" fill="#0000000F"/>'
             + (f'<path d="M-24,-130 L30,-130 L34,0 L-28,0Z" fill="{avental}" opacity=".9"/>' if avental else ""))
    cab = cabeca(2, -256, .98, 1, barba=False, veu=veu)
    return f'<g transform="translate({x},{y}) scale({s}) {f}">{corpo}{cab}</g>'


def sombra(x, y, rx, ry=8, op=.18):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#5A3A22" opacity="{op}"/>'


# ---------------------------------------------------------------- cenas
def cena_mesa():
    """Ap 3:20 — a mesa posta, a cadeira ao lado de Jesus à espera."""
    o = []
    o.append('<path d="M-40,0 L420,0 L700,640 L-200,640Z" fill="#fff" opacity=".35"/>')           # feixe de luz
    o.append(f'<rect y="470" width="{W}" height="170" fill="#EBD5B8"/>'
             '<path d="M0,500 C200,480 400,520 816,490 L816,640 L0,640Z" fill="#E2C8A4" opacity=".7"/>')
    # cadeira vazia (esquerda)
    o.append(sombra(215, 556, 70))
    o.append('<g fill="#C99A66"><rect x="150" y="410" width="10" height="150"/><rect x="262" y="450" width="10" height="106"/>'
             '<rect x="170" y="466" width="9" height="90" opacity=".8"/><rect x="244" y="466" width="9" height="90" opacity=".8"/></g>'
             '<path d="M142,452 L284,452 L270,474 L156,474Z" fill="#D7AB78"/>'
             '<g fill="#D7AB78"><rect x="152" y="320" width="9" height="130"/><rect x="170" y="324" width="9" height="126"/>'
             '<rect x="188" y="328" width="9" height="122"/><rect x="206" y="332" width="9" height="118"/></g>'
             '<rect x="148" y="310" width="76" height="12" rx="4" fill="#C99A66"/>')
    # mesa
    o.append(sombra(420, 560, 120))
    o.append('<rect x="408" y="455" width="22" height="100" fill="#B98552"/><ellipse cx="419" cy="556" rx="64" ry="12" fill="#B98552"/>'
             '<ellipse cx="419" cy="452" rx="150" ry="26" fill="#D9AF7C"/><ellipse cx="419" cy="448" rx="150" ry="24" fill="#E6C292"/>')
    # Bíblia aberta, xícaras e flor
    o.append('<path d="M360,438 L420,426 L420,448 L366,458Z" fill="#fff"/><path d="M420,426 L482,438 L474,458 L420,448Z" fill="#FBF2E2"/>'
             '<path d="M420,426 L420,448" stroke="#C9A674" stroke-width="2"/>'
             '<g stroke="#C9B493" stroke-width="1.2"><path d="M372,442 L412,434 M374,448 L412,440 M428,436 L468,444 M428,442 L466,450"/></g>')
    o.append('<g><ellipse cx="318" cy="448" rx="16" ry="5" fill="#fff"/><path d="M302,436 L334,436 L330,450 C326,456 310,456 306,450Z" fill="#FFF8EE" stroke="#E7D9C0"/>'
             '<path d="M312,424 C308,414 316,410 312,400 M322,424 C318,414 326,410 322,400" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/></g>')
    o.append('<g><path d="M508,436 L540,436 L536,450 C532,456 516,456 512,450Z" fill="#FFF8EE" stroke="#E7D9C0"/>'
             '<path d="M518,424 C514,414 522,410 518,400 M528,424 C524,414 532,410 528,400" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/></g>')
    o.append('<path d="M419,426 L419,360" stroke="#86AA98" stroke-width="3"/><g transform="translate(419,350)">'
             + "".join(f'<circle cx="{dx}" cy="{dy}" r="9" fill="{c}"/>' for dx, dy, c in [(-8, 8, "#93AEDD"), (8, 6, "#7896CF"), (0, -4, "#B7CBEA"), (-6, -16, "#5F7FC0"), (6, -18, "#93AEDD")]) + '</g>')
    # cadeira de Jesus (direita)
    o.append(sombra(640, 560, 80))
    o.append('<g fill="#C99A66"><rect x="594" y="450" width="10" height="106"/><rect x="700" y="410" width="10" height="150"/></g>'
             '<path d="M590,452 L716,452 L704,474 L602,474Z" fill="#D7AB78"/>'
             '<g fill="#D7AB78"><rect x="686" y="314" width="9" height="136"/><rect x="668" y="318" width="9" height="132"/><rect x="704" y="310" width="9" height="140"/></g>'
             '<rect x="660" y="302" width="60" height="12" rx="4" fill="#C99A66"/>')
    o.append(jesus_sentado(648, 454, 1.02, -1))
    # delicadeza: pétalas caídas
    o.append('<g opacity=".85">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="5" ry="3" fill="#F3B3C1" transform="rotate({a} {x} {y})"/>' for x, y, a in [(250, 590, 20), (300, 604, 60), (470, 596, 10), (520, 610, 40)]) + '</g>')
    return _moldura("mesa", "".join(o), "#FBF4E8", "#F2E2CC")


def cena_poco():
    """Jo 4:6–7 — Jesus senta junto ao poço, ao meio-dia, e espera."""
    o = []
    o.append('<circle cx="620" cy="130" r="54" fill="#FFF3C9" opacity=".9"/><circle cx="620" cy="130" r="90" fill="#FFF3C9" opacity=".35"/>')
    o.append('<path d="M0,330 C120,280 220,300 330,320 C440,270 560,290 816,310 L816,420 L0,420Z" fill="#E4D5E0" opacity=".9"/>'
             '<path d="M0,370 C160,340 300,360 420,372 C560,340 700,360 816,356 L816,430 L0,430Z" fill="#E9D3BB"/>')
    o.append(f'<path d="M0,420 C200,400 420,430 816,410 L816,640 L0,640Z" fill="#E6C39A"/>'
             '<path d="M0,470 C200,450 420,486 816,460 L816,640 L0,640Z" fill="#DDB486" opacity=".8"/>')
    # caminho até o horizonte
    o.append('<path d="M700,400 C640,430 520,450 470,500 C420,550 520,600 560,640 L690,640 C640,590 560,560 590,520 C630,480 730,440 740,400Z" fill="#F1DDBF" opacity=".8"/>')
    # palmeira distante
    o.append('<g transform="translate(760,330)"><path d="M0,0 C4,-30 4,-60 0,-90" stroke="#9A7A52" stroke-width="6" fill="none"/>'
             + "".join(f'<path d="M0,-90 Q{20 * math.cos(math.radians(a)):.0f},{-90 - 26 * abs(math.sin(math.radians(a))) :.0f} {52 * math.cos(math.radians(a)):.0f},{-90 + 8 * math.sin(math.radians(a)):.0f}" stroke="#86AA98" stroke-width="5" fill="none" stroke-linecap="round"/>' for a in (-30, 20, 160, 210, 270)) + '</g>')
    # mulher ao longe com jarro
    o.append('<g transform="translate(722,398) scale(.34)">' + f'<path d="M-30,0 C-26,-90 -20,-150 -10,-176 L18,-176 C28,-150 34,-90 38,0Z" fill="#C98E82"/>'
             '<ellipse cx="4" cy="-196" rx="13" ry="16" fill="#E8C3A0"/><path d="M-12,-200 C-10,-224 20,-224 22,-200 C22,-170 18,-160 14,-156 L-14,-156Z" fill="#F4E4C8"/>'
             '<path d="M-14,-222 C-30,-228 -26,-250 -6,-252 C14,-254 28,-250 24,-232Z" fill="#C98E82" transform="translate(0,-4)"/>'
             '<path d="M-10,-240 L18,-240 C22,-262 12,-274 4,-274 C-6,-274 -14,-262 -10,-240Z" fill="#B6784F"/></g>')
    # poço
    o.append(sombra(250, 548, 130, 12, .22))
    o.append('<g><path d="M130,420 L130,540 C130,566 370,566 370,540 L370,420Z" fill="#CDB9A0"/><ellipse cx="250" cy="420" rx="120" ry="30" fill="#DDCBB3"/>'
             '<ellipse cx="250" cy="420" rx="100" ry="22" fill="#5E7C86"/><ellipse cx="250" cy="426" rx="90" ry="15" fill="#2E4A55" opacity=".8"/>'
             '<g stroke="#B5A088" stroke-width="2" fill="none"><path d="M130,460 L370,460 M130,500 L370,500 M170,420 L170,556 M214,420 L214,566 M258,420 L258,568 M304,420 L304,562 M346,420 L346,552"/></g></g>')
    o.append('<g stroke="#8A6A46" stroke-width="9" stroke-linecap="round"><path d="M150,420 L150,300 M350,420 L350,300 M138,300 L362,300"/></g>'
             '<path d="M250,300 L250,396" stroke="#B49A72" stroke-width="3"/><path d="M236,396 L264,396 L260,424 L240,424Z" fill="#A5703F"/>')
    # Jesus sentado à beira do poço, olhando para a direita
    o.append(sombra(310, 566, 80, 8))
    o.append('<g transform="translate(440,548)"><g transform="scale(1.02)">'
             '<path d="M-30,-40 C-30,-100 -22,-150 -10,-176 L24,-176 C34,-136 36,-80 34,-40Z" fill="#FBF6EC"/>'
             '<path d="M-30,-40 L66,-40 C72,-30 70,-6 64,-6 L-30,-6Z" fill="#FBF6EC"/>'
             '<path d="M56,-36 C68,-10 70,40 66,78 C56,82 46,82 44,76 C48,40 46,-6 40,-34Z" fill="#FBF6EC"/>'
             '<ellipse cx="66" cy="84" rx="22" ry="7" fill="#E8C3A0"/><ellipse cx="30" cy="-70" rx="14" ry="8" fill="#E8C3A0"/>'
             '<path d="M-30,-40 L66,-40 L66,-30 L-30,-30Z" fill="#0000000C"/></g>'
             + cabeca(4, -196, 1.02, 1, inclinada=4) + '</g>')
    o.append('<g transform="translate(300,560)"><rect x="-40" y="-40" width="100" height="40" rx="10" fill="#CDB9A0"/></g>')
    return _moldura("poco", "".join(o), "#FBE3D2", "#F6EBDD")


def cena_marta_maria():
    """Lc 10:38–42 — Maria aos pés de Jesus; Marta, ocupada com muitas coisas."""
    o = []
    o.append(f'<rect y="440" width="{W}" height="200" fill="#E8CFA9"/><path d="M0,470 C260,452 520,486 816,466 L816,640 L0,640Z" fill="#DDBE92" opacity=".8"/>')
    o.append('<path d="M230,40 L230,330 C230,210 410,210 410,330 L410,40Z" fill="#FFF7E6" opacity=".8"/>'
             '<path d="M246,40 L246,320 C246,226 394,226 394,320 L394,40Z" fill="#FFFDF5"/>')                                 # janela em arco
    o.append('<path d="M60,0 L260,0 L520,640 L-80,640Z" fill="#fff" opacity=".22"/>')
    # Jesus sentado no banco (esquerda), olhando para a direita? (olha para Maria, à direita)
    o.append(sombra(210, 556, 90))
    o.append('<rect x="130" y="470" width="150" height="18" rx="6" fill="#C99A66"/><rect x="142" y="486" width="10" height="70" fill="#B98552"/><rect x="258" y="486" width="10" height="70" fill="#B98552"/>')
    o.append(jesus_sentado(196, 470, 1.0, 1))
    # Maria sentada no chão, de frente para Jesus (olha para a esquerda)
    o.append(sombra(360, 566, 80, 9))
    o.append(mulher_sentada_chao(372, 560, 1.0, -1, "#E7A5A5", "#F6E7D8"))
    # Marta (direita), em pé, atarefada, com panela
    o.append(sombra(640, 566, 60))
    o.append('<rect x="560" y="410" width="200" height="16" rx="6" fill="#B98552"/><rect x="580" y="424" width="10" height="132" fill="#A5703F"/><rect x="730" y="424" width="10" height="132" fill="#A5703F"/>')
    o.append('<ellipse cx="620" cy="404" rx="42" ry="9" fill="#8A8A8A"/><path d="M580,404 L580,372 C580,360 660,360 660,372 L660,404Z" fill="#A5ABB0"/>'
             '<path d="M596,356 C590,340 602,334 596,318 M620,354 C614,336 628,330 620,312 M644,356 C638,340 650,334 644,318" fill="none" stroke="#fff" stroke-width="3" opacity=".85" stroke-linecap="round"/>')
    o.append('<g><ellipse cx="704" cy="404" rx="26" ry="8" fill="#E7BE7A"/><path d="M680,404 C684,388 724,388 728,404Z" fill="#F0CD8E"/></g>')
    o.append(mulher_em_pe(540, 556, 1.0, 1, "#D99A7C", "#F4E4C8", "#F7EBD8"))
    o.append('<g fill="#F3B3C1"><ellipse cx="470" cy="596" rx="5" ry="3"/><ellipse cx="500" cy="608" rx="5" ry="3"/><ellipse cx="410" cy="604" rx="5" ry="3"/></g>')
    return _moldura("marta", "".join(o), "#FAEBD7", "#F4E2C8")


def cena_buque():
    """Lc 12:27 — a mulher colhe uma flor; Ele guarda o buquê inteiro."""
    o = []
    o.append('<path d="M0,380 C200,356 420,392 816,366 L816,640 L0,640Z" fill="#CF8E6C"/>'
             '<path d="M0,420 C240,400 460,440 816,414 L816,640 L0,640Z" fill="#C27D5C" opacity=".9"/>'
             '<path d="M0,500 C260,480 520,520 816,490 L816,640 L0,640Z" fill="#B56F52" opacity=".9"/>'
             '<g fill="none" stroke="#E2A988" stroke-width="5" opacity=".5" stroke-linecap="round"><path d="M40,440 C160,430 260,452 360,440"/><path d="M420,470 C520,458 640,480 780,466"/><path d="M80,540 C200,530 300,548 420,540"/></g>')
    # buquê enorme às costas de Jesus
    o.append(flora.cacho(238, 330, 1.9, 91, ("peonia", "pessego", "dourada", "lilas"), True, (-150, -40)))
    o.append(sombra(300, 392, 90, 8, .2))
    o.append(jesus_em_pe(300, 392, 0.95, 1, inclinado=14))
    # mulher agachada colhendo uma só flor
    o.append(sombra(560, 428, 50, 6))
    o.append(mulher_agachada(556, 424, 1.2, -1))
    o.append('<g><path d="M512,420 C508,408 506,400 508,392" stroke="#86AA98" stroke-width="3" fill="none"/>'
             + flora.flor_camadas(508, 388, 11, 0, "peonia") + '</g>')
    return _moldura("buque", "".join(o), "#F2E8EE", "#EBDDE0", luz=False)


def cena_porta():
    """Ap 3:20 — Eis que estou à porta e bato."""
    o = []
    o.append(f'<rect width="{W}" height="{H}" fill="#EBD8BC"/><path d="M0,0 L0,640 L300,640 C300,420 200,200 0,0Z" fill="#fff" opacity=".18"/>')
    o.append('<path d="M250,640 L250,230 C250,110 566,110 566,230 L566,640Z" fill="#C7AE8A"/>')                                 # moldura
    o.append('<path d="M272,640 L272,236 C272,140 544,140 544,236 L544,640Z" fill="#6A4A32"/>'
             '<path d="M408,640 L408,168" stroke="#4E3524" stroke-width="3"/><g stroke="#5A3F2B" stroke-width="2" opacity=".7"><path d="M300,200 L300,640 M340,184 L340,640 M376,172 L376,640 M440,172 L440,640 M476,184 L476,640 M514,200 L514,640"/></g>'
             '<circle cx="392" cy="420" r="7" fill="#D9B05A"/><circle cx="424" cy="420" r="7" fill="#D9B05A"/>')
    o.append(f'<path d="M0,590 C260,570 520,610 816,580 L816,640 L0,640Z" fill="#CBB28C"/><path d="M240,640 C260,600 330,580 408,580 C486,580 560,600 580,640Z" fill="#E7D3B0"/>')
    # trepadeira de rosas
    r = random.Random(5)
    for lado, xs in ((-1, 250), (1, 566)):
        for k in range(16):
            yy = 600 - k * 26 + r.uniform(-6, 6)
            xx = xs + lado * r.uniform(-14, 42) - (0 if k < 8 else lado * (k - 8) * 3)
            o.append(f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{r.uniform(14, 22):.0f}" ry="{r.uniform(7, 10):.0f}" fill="{r.choice(flora.VERDES)}" transform="rotate({r.uniform(-60, 60):.0f} {xx:.0f} {yy:.0f})"/>')
        for k in range(7):
            yy = 560 - k * 62 + r.uniform(-10, 10)
            xx = xs + lado * r.uniform(-4, 46)
            o.append(flora.flor_camadas(xx, yy, r.uniform(15, 24), r.uniform(0, 60), r.choice(["peonia", "pessego", "peonia"]), False))
    for k in range(10):                                         # arco sobre a porta
        t = k / 9
        xx = 250 + t * 316
        yy = 168 - math.sin(t * math.pi) * 78 + 62
        o.append(flora.flor_camadas(xx, yy, r.uniform(14, 20), r.uniform(0, 60), "peonia", False))
        o.append(f'<ellipse cx="{xx + 16:.0f}" cy="{yy + 12:.0f}" rx="16" ry="7" fill="{r.choice(flora.VERDES)}" transform="rotate({r.uniform(-40, 40):.0f} {xx:.0f} {yy:.0f})"/>')
    o.append(sombra(160, 596, 70, 7, .22))
    o.append(jesus_em_pe(170, 596, 0.9, 1, inclinado=0))
    o.append('<path d="M214,420 C236,404 246,396 250,392" stroke="#FBF6EC" stroke-width="13" stroke-linecap="round" fill="none"/><circle cx="254" cy="390" r="8" fill="#E8C3A0"/>')
    return _moldura("porta", "".join(o), "#F4E6CF", "#EAD6B8")


CENAS = {
    "mesa": dict(fn=cena_mesa, titulo="Ele guardou um lugar para você", ref="Apocalipse 3:20",
                 texto="Cear, na Bíblia, é estar junto sem pressa. Jesus não pede que você chegue com a casa em ordem, a agenda resolvida ou a culpa em dia. A cadeira ao lado dele está livre e a mesa já está posta.",
                 oracao="“Senhor, hoje eu me sento. Do jeito que estou.”"),
    "poco": dict(fn=cena_poco, titulo="Ele esperou por ela, ao meio-dia", ref="João 4:6–29",
                 texto="A mulher samaritana foi ao poço sozinha, na hora mais quente do dia, e encontrou Jesus já sentado, esperando. Ele conhecia a vida dela inteira e, mesmo assim, ficou, conversou e a chamou para perto.",
                 oracao="“Senhor, tu já me esperavas. Obrigada por não teres desistido de mim.”"),
    "marta": dict(fn=cena_marta_maria, titulo="Marta, Marta…", ref="Lucas 10:38–42",
                  texto="Marta recebeu Jesus em casa e ficou “ocupada com muitas coisas”. Ele não a repreendeu por servir; chamou-a pelo nome, duas vezes, com carinho, e lembrou que “uma só coisa é necessária”. Se você vive correndo, este convite também é para você.",
                  oracao="“Senhor, ensina-me a parar um minuto sem culpa.”"),
    "buque": dict(fn=cena_buque, titulo="Ele guarda o buquê inteiro", ref="Lucas 12:27",
                  texto="Jesus disse para olharmos os lírios do campo: ninguém os força a crescer. Há dias em que você colhe uma florzinha de cada vez, cansada, enquanto Ele já guarda o buquê inteiro para você.",
                  oracao="“Senhor, eu aceito o que Tu preparaste.”"),
    "porta": dict(fn=cena_porta, titulo="Ele bate com delicadeza", ref="Apocalipse 3:20",
                  texto="Jesus não arromba a porta; ele bate e espera. Você não precisa estar pronta, nem sentir algo especial. Basta abrir um pouquinho, no meio da correria mesmo.",
                  oracao="“Senhor, a porta está aberta. Entra.”"),
}
