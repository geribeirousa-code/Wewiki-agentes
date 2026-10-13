"""Ilustrações simples em SVG (viewBox 64x64), no clima alegre da paleta da Gê.

Cada ícone usa variáveis CSS (--c1 principal, --c2 apoio, --c3 detalhe, --tinta) que a
folha define; assim as cores mudam por bloco sem redesenhar.
"""

_I = {
    "sol": '<circle cx="32" cy="32" r="12" fill="var(--c1)"/>'
           '<g stroke="var(--c1)" stroke-width="4" stroke-linecap="round">'
           '<path d="M32 6v8M32 50v8M6 32h8M50 32h8M13.6 13.6l5.7 5.7M44.7 44.7l5.7 5.7M13.6 50.4l5.7-5.7M44.7 19.3l5.7-5.7"/></g>'
           '<circle cx="28" cy="29" r="2" fill="var(--tinta)"/><circle cx="36" cy="29" r="2" fill="var(--tinta)"/>'
           '<path d="M27 35q5 5 10 0" stroke="var(--tinta)" stroke-width="2" fill="none" stroke-linecap="round"/>',
    "palmeira": '<path d="M32 58c1-14 0-26-3-38" stroke="var(--c3)" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<g fill="var(--c1)"><path d="M29 20C20 12 10 14 6 22c9-3 16-1 23-2z"/>'
                '<path d="M29 20C26 9 16 5 9 9c9 1 14 5 20 11z"/>'
                '<path d="M29 20c3-11 13-14 21-10-9 0-15 4-21 10z"/>'
                '<path d="M29 20c9-8 19-6 24 1-9-3-16-1-24-1z"/></g>'
                '<circle cx="28" cy="23" r="2.5" fill="var(--c2)"/><circle cx="32" cy="24" r="2.5" fill="var(--c2)"/>',
    "pergaminho": '<rect x="14" y="10" width="36" height="44" rx="3" fill="#fff" stroke="var(--c1)" stroke-width="3"/>'
                  '<rect x="9" y="6" width="46" height="9" rx="4.5" fill="var(--c1)"/>'
                  '<rect x="9" y="49" width="46" height="9" rx="4.5" fill="var(--c1)"/>'
                  '<g stroke="var(--c2)" stroke-width="3" stroke-linecap="round"><path d="M21 24h22M21 31h22M21 38h14"/></g>',
    "ovelha": '<g fill="#fff" stroke="var(--c1)" stroke-width="2.5"><circle cx="22" cy="30" r="9"/><circle cx="32" cy="25" r="10"/>'
              '<circle cx="42" cy="30" r="9"/><circle cx="32" cy="36" r="10"/></g>'
              '<ellipse cx="50" cy="34" rx="7" ry="6" fill="var(--c3)"/><circle cx="52" cy="32" r="1.6" fill="var(--tinta)"/>'
              '<path d="M24 45v10M40 45v10" stroke="var(--c3)" stroke-width="4" stroke-linecap="round"/>',
    "trigo": '<path d="M32 58V16" stroke="var(--c3)" stroke-width="3" stroke-linecap="round"/>'
             '<g fill="var(--c1)"><ellipse cx="25" cy="22" rx="4" ry="7" transform="rotate(-25 25 22)"/>'
             '<ellipse cx="39" cy="22" rx="4" ry="7" transform="rotate(25 39 22)"/>'
             '<ellipse cx="24" cy="34" rx="4" ry="7" transform="rotate(-25 24 34)"/>'
             '<ellipse cx="40" cy="34" rx="4" ry="7" transform="rotate(25 40 34)"/>'
             '<ellipse cx="32" cy="12" rx="4" ry="7"/></g>',
    "barco": '<path d="M8 40h48l-8 14H16z" fill="var(--c1)"/>'
             '<path d="M32 8v32" stroke="var(--c3)" stroke-width="3"/>'
             '<path d="M34 10c12 6 16 16 16 26H34z" fill="#fff" stroke="var(--c2)" stroke-width="2.5"/>'
             '<path d="M30 16c-8 5-12 12-12 20h12z" fill="var(--c2)"/>'
             '<path d="M4 58q7-5 14 0t14 0 14 0 14 0" stroke="var(--c2)" stroke-width="3" fill="none" stroke-linecap="round"/>',
    "montanha": '<path d="M2 56L24 16l14 22 8-12 16 30z" fill="var(--c1)"/>'
                '<path d="M24 16l-8 14 6-3 4 5 4-5 4 3z" fill="#fff"/>'
                '<circle cx="50" cy="14" r="6" fill="var(--c2)"/>',
    "coroa": '<path d="M8 48V22l14 14 10-18 10 18 14-14v26z" fill="var(--c1)"/>'
             '<rect x="8" y="48" width="48" height="7" rx="3" fill="var(--c3)"/>'
             '<circle cx="8" cy="20" r="3.5" fill="var(--c2)"/><circle cx="32" cy="15" r="3.5" fill="var(--c2)"/>'
             '<circle cx="56" cy="20" r="3.5" fill="var(--c2)"/>',
    "estrela": '<path d="M32 5l8 18 19 2-14 13 4 19-17-10-17 10 4-19L5 25l19-2z" fill="var(--c1)" stroke="var(--c3)" stroke-width="2" stroke-linejoin="round"/>',
    "pomba": '<path d="M10 36c4-12 16-16 26-12 6-6 14-6 18-2-4 2-6 4-6 6 0 12-10 24-26 22l8-8c-8 0-14-2-20-6z" fill="#fff" stroke="var(--c1)" stroke-width="3" stroke-linejoin="round"/>'
             '<circle cx="46" cy="25" r="1.8" fill="var(--tinta)"/>'
             '<path d="M8 52c6-2 12-2 18-8" stroke="var(--c3)" stroke-width="3" fill="none" stroke-linecap="round"/>'
             '<g fill="var(--c3)"><ellipse cx="14" cy="50" rx="4" ry="2" transform="rotate(-30 14 50)"/><ellipse cx="20" cy="46" rx="4" ry="2" transform="rotate(-30 20 46)"/></g>',
    "tenda": '<path d="M4 54L32 10l28 44z" fill="var(--c1)"/><path d="M32 10l8 44H24z" fill="var(--c2)"/>'
             '<path d="M32 28l8 26H24z" fill="var(--tinta)" opacity=".25"/><path d="M32 10V4" stroke="var(--c3)" stroke-width="3"/>',
    "peixe": '<ellipse cx="28" cy="32" rx="20" ry="13" fill="var(--c1)"/><path d="M46 32l14-12v24z" fill="var(--c2)"/>'
             '<circle cx="17" cy="29" r="2.8" fill="#fff"/><circle cx="16.5" cy="29" r="1.3" fill="var(--tinta)"/>'
             '<path d="M30 21q6 11 0 22M38 24q4 8 0 16" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/>',
    "lampada": '<path d="M10 34c0-8 8-12 22-12 8 0 14 4 18 8l8-2-4 10c-2 8-10 12-22 12-12 0-22-4-22-16z" fill="var(--c1)"/>'
               '<path d="M50 30l8-2" stroke="var(--c3)" stroke-width="3" stroke-linecap="round"/>'
               '<path d="M60 24c-3 3-3 6 0 8 3-2 3-5 0-8z" fill="var(--c2)"/>'
               '<path d="M16 34h24" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>',
    "coracao": '<path d="M32 56C10 40 6 28 10 20c4-8 16-8 22 2 6-10 18-10 22-2 4 8 0 20-22 36z" fill="var(--c1)" stroke="var(--c3)" stroke-width="2.5" stroke-linejoin="round"/>',
    "livro": '<path d="M32 16c-6-5-16-6-24-4v38c8-2 18-1 24 4z" fill="var(--c1)"/>'
             '<path d="M32 16c6-5 16-6 24-4v38c-8-2-18-1-24 4z" fill="var(--c2)"/>'
             '<path d="M32 16v38" stroke="#fff" stroke-width="2.5"/>'
             '<g stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".8"><path d="M14 22c4-1 9 0 13 2M14 30c4-1 9 0 13 2M37 24c4-2 9-3 13-2M37 32c4-2 9-3 13-2"/></g>',
    "arcoiris": '<g fill="none" stroke-width="5" stroke-linecap="round">'
                '<path d="M8 50a24 24 0 0148 0" stroke="var(--c1)"/><path d="M15 50a17 17 0 0134 0" stroke="var(--c2)"/>'
                '<path d="M22 50a10 10 0 0120 0" stroke="var(--c3)"/></g>'
                '<g fill="#fff" stroke="var(--c2)" stroke-width="2"><circle cx="10" cy="52" r="6"/><circle cx="18" cy="54" r="6"/>'
                '<circle cx="54" cy="52" r="6"/><circle cx="46" cy="54" r="6"/></g>',
    "uvas": '<g fill="var(--c1)"><circle cx="22" cy="30" r="7"/><circle cx="36" cy="30" r="7"/><circle cx="29" cy="40" r="7"/>'
            '<circle cx="43" cy="40" r="7"/><circle cx="36" cy="50" r="7"/><circle cx="22" cy="43" r="1"/></g>'
            '<path d="M29 24c0-8 4-12 12-14" stroke="var(--c3)" stroke-width="3" fill="none" stroke-linecap="round"/>'
            '<path d="M40 10c6-2 12 2 12 8-6 0-11-2-12-8z" fill="var(--c2)"/>',
    "envelope": '<rect x="6" y="14" width="52" height="36" rx="5" fill="#fff" stroke="var(--c1)" stroke-width="3"/>'
                '<path d="M8 17l24 19 24-19" fill="none" stroke="var(--c1)" stroke-width="3" stroke-linejoin="round"/>'
                '<circle cx="48" cy="44" r="6" fill="var(--c2)"/><path d="M48 41v6M45 44h6" stroke="#fff" stroke-width="1.8"/>',
}

# Dupla de ícones que enfeita o cabeçalho de cada bloco.
POR_BLOCO = {
    "lei": ("pergaminho", "tenda"),
    "historicos": ("coroa", "montanha"),
    "poeticos": ("coracao", "estrela"),
    "profetas": ("lampada", "palmeira"),
    "evangelhos": ("peixe", "trigo"),
    "atos": ("barco", "pomba"),
    "paulinas": ("envelope", "livro"),
    "gerais": ("pomba", "uvas"),
    "apocalipse": ("arcoiris", "estrela"),
}


def icone(nome, tam=40, c1="#FF7EB6", c2="#FFD63A", c3="#25C2B0", tinta="#3B3350"):
    corpo = _I.get(nome, _I["estrela"])
    return (f'<svg class="ico" width="{tam}" height="{tam}" viewBox="0 0 64 64" '
            f'style="--c1:{c1};--c2:{c2};--c3:{c3};--tinta:{tinta}" aria-hidden="true">{corpo}</svg>')


def nomes():
    return sorted(_I)
