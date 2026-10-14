"""Figuras de mulheres da Bíblia em vetor (busto com véu e manto, mãos juntas).

Estilo plano em aquarela simplificada, na paleta do planner. Cada mulher tem uma
configuração (manto, véu, cabelo, pele, coroa). São figuras ilustrativas e genéricas,
não retratos: ninguém sabe como elas eram.
"""

PELES = {"clara": "#F4D6C0", "media": "#E9BE98", "morena": "#C98E62", "escura": "#9A6443"}
CABELOS = {"castanho": "#6B4630", "preto": "#2F2220", "ruivo": "#A5552B", "grisalho": "#BDB8B4", "loiro": "#C9A15A"}

# Mulheres já desenhadas (acrescente novas aqui; o planner só pede pelo nome).
CATALOGO = {
    "Eva": dict(manto="#9DBFA8", veu="#F4E4C8", cabelo="castanho", pele="media", flor=True),
    "Sara": dict(manto="#B7A6D8", veu="#EFE6F7", cabelo="grisalho", pele="clara"),
    "Hagar": dict(manto="#9DBFA8", veu="#D9E8DB", cabelo="castanho", pele="morena"),
    "Raabe": dict(manto="#C88AB0", veu="#F1D9E6", cabelo="castanho", pele="media"),
    "Ana": dict(manto="#E3A19A", veu="#F6E3C9", cabelo="castanho", pele="clara"),
    "Rute": dict(manto="#8FB09E", veu="#BFD6C3", cabelo="preto", pele="media"),
    "Ester": dict(manto="#E4B93E", veu="#F7EAC2", cabelo="castanho", pele="clara", coroa=True),
    "Maria": dict(manto="#C99AC4", veu="#F4EBD6", cabelo="castanho", pele="media"),
    "Débora": dict(manto="#E08C6A", veu="#F8E3D2", cabelo="preto", pele="morena"),
    "Miriã": dict(manto="#7FB3D5", veu="#E2EFF7", cabelo="preto", pele="morena"),
}


def figura(nome, tam=150, cfg=None):
    c = dict(manto="#9DBFA8", veu="#F4E4C8", cabelo="castanho", pele="media", coroa=False, flor=False)
    c.update(CATALOGO.get(nome, {}))
    if cfg:
        c.update(cfg)
    pele, cab = PELES[c["pele"]], CABELOS[c["cabelo"]]
    manto, veu = c["manto"], c["veu"]
    sombra = "#00000014"
    o = [f'<svg width="{tam}" height="{tam * 1.22:.0f}" viewBox="0 0 150 183" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ilustração: {nome}">']
    # véu (atrás da cabeça e caindo nos ombros)
    o.append(f'<path d="M75 8 C40 8 26 40 28 78 C30 104 20 118 14 132 C40 140 58 138 75 138 C92 138 110 140 136 132 C130 118 120 104 122 78 C124 40 110 8 75 8Z" fill="{veu}"/>')
    # manto / corpo
    o.append(f'<path d="M14 183 C16 150 28 128 52 120 L98 120 C122 128 134 150 136 183Z" fill="{manto}"/>')
    o.append(f'<path d="M52 120 C60 134 90 134 98 120 C92 140 84 150 75 183 C66 150 58 140 52 120Z" fill="#FFFFFF" opacity=".22"/>')
    o.append(f'<path d="M14 183 C16 150 28 128 52 120 C44 140 40 160 38 183Z" fill="{sombra}"/>')
    # cabelo
    o.append(f'<path d="M46 62 C46 36 60 26 75 26 C90 26 104 36 104 62 C98 50 88 44 75 44 C62 44 52 50 46 62Z" fill="{cab}"/>')
    # rosto (cabeça levemente baixa)
    o.append(f'<ellipse cx="75" cy="76" rx="25" ry="30" fill="{pele}"/>')
    o.append(f'<path d="M50 70 C54 52 64 46 75 46 C86 46 96 52 100 70 C92 60 84 58 75 58 C66 58 58 60 50 70Z" fill="{cab}"/>')
    # olhos baixos, nariz e boca
    o.append('<path d="M62 80 q6 5 12 0 M80 80 q6 5 12 0" fill="none" stroke="#5A3A2E" stroke-width="2" stroke-linecap="round"/>')
    o.append('<path d="M75 84 q-2 6 1 8" fill="none" stroke="#B8845F" stroke-width="1.6" stroke-linecap="round"/>')
    o.append('<path d="M68 99 q7 5 14 0" fill="none" stroke="#B5524F" stroke-width="2.4" stroke-linecap="round"/>')
    o.append('<ellipse cx="60" cy="92" rx="5" ry="3" fill="#F2A59B" opacity=".45"/><ellipse cx="90" cy="92" rx="5" ry="3" fill="#F2A59B" opacity=".45"/>')
    # pescoço sombra + mãos juntas
    o.append(f'<path d="M64 104 C66 116 84 116 86 104 C84 112 66 112 64 104Z" fill="#00000010"/>')
    o.append(f'<ellipse cx="75" cy="146" rx="15" ry="11" fill="{pele}"/><path d="M66 142 q9 8 18 0 M68 148 q7 5 14 0" fill="none" stroke="#B8845F" stroke-width="1.6" stroke-linecap="round" opacity=".7"/>')
    # véu dobra frontal (ombros)
    o.append(f'<path d="M28 78 C30 104 20 118 14 132 C22 134 30 134 38 134 C34 114 36 98 40 84Z" fill="{veu}" opacity=".95"/>')
    o.append(f'<path d="M122 78 C120 104 130 118 136 132 C128 134 120 134 112 134 C116 114 114 98 110 84Z" fill="{veu}" opacity=".95"/>')
    if c.get("coroa"):
        o.append('<path d="M52 30 L58 12 L68 24 L75 8 L82 24 L92 12 L98 30Z" fill="#E9B949" stroke="#C58A1C" stroke-width="1.6" stroke-linejoin="round"/>'
                 '<circle cx="58" cy="12" r="2.6" fill="#F4C9C2"/><circle cx="75" cy="8" r="2.6" fill="#F4C9C2"/><circle cx="92" cy="12" r="2.6" fill="#F4C9C2"/>')
    if c.get("flor"):
        o.append('<g transform="translate(103 34)"><g fill="#F4C9C2">' + "".join(
            f'<ellipse cx="0" cy="-6" rx="3.4" ry="6" transform="rotate({a})"/>' for a in range(0, 360, 72)) +
            '</g><circle r="3" fill="#E9B949"/></g>')
    o.append('</svg>')
    return "".join(o)


def nomes():
    return sorted(CATALOGO)
