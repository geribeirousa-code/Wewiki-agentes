#!/usr/bin/env python3
"""
Carrossel Bowl Green — componentes do Design System oficial.

Cada tipo de slide reproduz um componente que JÁ EXISTE em
"BOWL GREEN/Bowl Green — Design System.html". Não inventamos layout:
o documento manda.

As 4 vozes tipográficas do sistema:
  VOZ 1 · DISPLAY    Luckiest Guy   caixa-alta gorda. Badges, números gigantes, capa.
  VOZ 2 · NÚMEROS    Shantell Sans  preços, valores, anotações à mão.
  VOZ 3 · GIZ        Chalkiez       confissões, aspas, frases manuscritas.
  VOZ 4 · INTERFACE  Lufga          títulos de card, corpo, labels.

Proporção de paleta obrigatória: creme 40 · verde 25 · sálvia 20 · coral 10 · dourado 5.
O creme domina. Verde escuro é acento, não fundo padrão.

Uso:
    python gerar_slides.py <config.json> <pasta_saida>
"""

import base64
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ_MARCA = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN")
# scripts/ → carrossel-bowlgreen/ → skills/ → .claude/ → AGENTES/  = parents[4]
PASTA_FONTES = Path(__file__).resolve().parents[4] / ".agents/skills/carrossel-opiniao/fonts/bowlgreen"

P = {
    "creme": "#EDEADB",
    "creme_claro": "#F5F1E6",
    "branco": "#FFFFFF",
    "verde": "#24573A",
    "verde_escuro": "#1C3527",
    "dourado": "#C9A24B",
    "dourado_escuro": "#8A6314",
    "coral": "#E8684A",
    "salvia": "#BACFBB",
    "menta": "#BFE3CC",
    "menta_claro": "#EDF2E6",
    "rosa": "#FFDFD5",
    "rosa_claro": "#F6D9D0",
    "amarelo": "#FFF3D6",
}

LARGURA, ALTURA = 1080, 1350

# Faixa mosaico — motivos chapados, divisória e banda de capa do sistema.
MOSAICO = [P["coral"], P["menta_claro"], P["verde_escuro"], P["creme_claro"],
           P["dourado"], P["verde"], P["rosa"], P["menta"]]


def b64(caminho, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(caminho).read_bytes()).decode("ascii")


# As 4 vozes e os arquivos que as sustentam. Nenhuma é opcional:
# sem elas o slide sai em fonte de sistema e deixa de ser da marca.
VOZES = (
    [("Lufga", f"Lufga-{p}.otf", p) for p in (400, 500, 700, 800, 900)]
    + [("Luckiest Guy", "LuckiestGuy-400.ttf", 400)]
    + [("Chalkiez", "Chalkiez-400.otf", 400)]
    + [("Shantell Sans", f"ShantellSans-{p}.ttf", p) for p in (500, 600, 700, 800)]
)


def _formato(caminho):
    """Detecta o formato pelos bytes, não pela extensão — Chalkiez.otf é TTF por dentro
    e declarar 'opentype' faz o Chrome recusar a fonte em silêncio."""
    magic = caminho.read_bytes()[:4]
    if magic == b"OTTO":
        return "font/otf", "opentype"
    if magic in (b"\x00\x01\x00\x00", b"true", b"ttcf"):
        return "font/ttf", "truetype"
    if magic == b"wOF2":
        return "font/woff2", "woff2"
    if magic == b"wOFF":
        return "font/woff", "woff"
    raise ValueError(f"formato de fonte não reconhecido: {caminho.name} ({magic!r})")


def fontes():
    faltando = [a for _, a, _ in VOZES if not (PASTA_FONTES / a).exists()]
    if faltando:
        raise SystemExit(
            "ERRO: fontes da marca não encontradas em\n"
            f"  {PASTA_FONTES}\n"
            f"  faltando: {', '.join(faltando)}\n"
            "Sem elas o slide sai em fonte de sistema e não é Bowl Green. "
            "Reextraia do Design System antes de gerar."
        )

    faces = []
    for familia, arquivo, peso in VOZES:
        caminho = PASTA_FONTES / arquivo
        mime, fmt = _formato(caminho)
        faces.append(f"@font-face{{font-family:'{familia}';font-weight:{peso};font-display:block;"
                     f"src:url({b64(caminho, mime)}) format('{fmt}');}}")
    return "".join(faces)


def logo(variante="verde"):
    arquivos = {"dourado": "Bowl Green - logo dourado (transparente).png",
                "verde": "Bowl Green - logo verde (transparente).png",
                "branco": "Bowl Green - logo branco (transparente).png"}
    caminho = RAIZ_MARCA / arquivos[variante]
    return b64(caminho, "image/png") if caminho.exists() else ""


CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:__L__px;height:__A__px;overflow:hidden;}
body{font-family:'Lufga',sans-serif;-webkit-font-smoothing:antialiased;background:__CREME__;}

.slide{position:relative;width:__L__px;height:__A__px;overflow:hidden;
       display:flex;flex-direction:column;padding:64px 60px 52px;background:__CREME__;}

/* VOZ 1 — display */
.display{font-family:'Luckiest Guy',cursive;text-transform:uppercase;
         letter-spacing:.012em;line-height:.98;font-weight:400;}
/* VOZ 2 — números e anotações */
.num{font-family:'Shantell Sans',cursive;font-weight:700;}
/* VOZ 3 — giz */
.giz{font-family:'Chalkiez',cursive;line-height:1.5;}

.rotulo{font-family:'Lufga';font-weight:700;font-size:23px;letter-spacing:.2em;
        text-transform:uppercase;color:#9AA396;}

/* Card branco sobre creme — a unidade base do sistema */
.card{background:__BRANCO__;border-radius:34px;padding:44px 42px;
      box-shadow:0 10px 34px rgba(28,53,39,.07);}

.pill{display:inline-block;border-radius:999px;padding:11px 26px;
      font-family:'Luckiest Guy',cursive;font-size:26px;letter-spacing:.06em;
      text-transform:uppercase;line-height:1;}
.chip{display:inline-flex;align-items:center;gap:9px;border-radius:999px;
      padding:12px 22px;font-family:'Lufga';font-weight:700;font-size:26px;}

.riscado{text-decoration:line-through;text-decoration-thickness:5px;}

.topo{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px;}
.topo img{height:56px;}
.corpo{flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;}
.rodape{display:flex;align-items:center;justify-content:space-between;margin-top:30px;
        font-family:'Lufga';font-weight:700;font-size:26px;color:__VERDE__;letter-spacing:.02em;}
.rodape img{height:48px;opacity:.85;}

.mosaico{display:flex;height:22px;border-radius:999px;overflow:hidden;}
.mosaico i{flex:1;}
"""


def mosaico():
    return '<div class="mosaico">' + "".join(f'<i style="background:{c}"></i>' for c in MOSAICO) + "</div>"


def topo(rotulo, variante_logo="verde"):
    return (f'<div class="topo"><span class="rotulo">{rotulo}</span>'
            f'<img src="{logo(variante_logo)}" alt=""></div>')


def rodape(texto_dir="@bowlgreenxerem", com_logo=False):
    dir_html = f'<img src="{logo()}" alt="">' if com_logo else f"<span>{texto_dir}</span>"
    return (f'<div class="rodape"><span>@bowlgreenxerem</span>{dir_html if com_logo else ""}</div>'
            if com_logo else f'<div class="rodape"><span>{texto_dir}</span></div>')


# ---------------------------------------------------------------------------
# Componentes — cada um existe no Design System
# ---------------------------------------------------------------------------

def slide_mito_verdade(s):
    """Componente MITOS × VERDADES: coluna de mitos riscados + card de verdade."""
    mitos = "".join(
        f'<div style="background:{P["rosa"]};border-radius:26px;padding:30px 28px;'
        f'display:flex;align-items:center;gap:20px">'
        f'<span class="pill" style="background:{P["coral"]};color:{P["branco"]};'
        f'font-size:21px;padding:9px 20px;flex:0 0 auto">Mito</span>'
        f'<span class="riscado" style="font-family:\'Lufga\';font-weight:800;font-size:39px;'
        f'line-height:1.18;color:{P["coral"]}">{m}</span></div>'
        for m in s["mitos"]
    )
    return f"""
<div class="slide">
  {topo(s.get("rotulo", "Mitos × Verdades"))}
  <div class="corpo">
    <div class="card" style="display:flex;flex-direction:column;gap:20px">
      {mitos}
      <div style="background:{P['menta_claro']};border-radius:26px;padding:40px 32px;
                  display:flex;flex-direction:column;gap:20px;align-items:flex-start">
        <span class="pill" style="background:{P['verde']};color:{P['branco']};font-size:22px;padding:10px 22px">Verdade</span>
        <div class="display" style="font-size:88px;color:{P['verde']}">{s['verdade']}</div>
        <div class="giz" style="font-size:41px;color:{P['verde']}">{s['assinatura']}</div>
      </div>
    </div>
  </div>
  {mosaico()}
  <div class="rodape" style="margin-top:26px"><span>@bowlgreenxerem</span>
    <span style="color:{P['dourado_escuro']}">Xerém</span></div>
</div>"""


def slide_expectativa(s):
    """Componente EXPECTATIVA × REALIDADE, com o disco dourado 'vs'."""
    chips = "".join(
        f'<span class="chip" style="background:rgba(255,255,255,.14);color:{P["menta"]}">{c}</span>'
        for c in s.get("chips", [])
    )
    return f"""
<div class="slide">
  {topo(s.get("rotulo", "Expectativa × Realidade"))}
  <div class="corpo" style="justify-content:center;gap:0;position:relative">
    <div class="card" style="background:{P['creme_claro']};box-shadow:none;padding:62px 50px">
      <span class="rotulo" style="font-size:22px">Expectativa</span>
      <div class="giz" style="font-size:60px;color:{P['verde_escuro']};margin-top:22px">“{s['expectativa']}”</div>
      <div style="font-family:'Lufga';font-weight:500;font-size:29px;color:#8A9384;margin-top:24px">{s['tom']}</div>
    </div>

    <div style="align-self:center;width:104px;height:104px;border-radius:50%;background:{P['dourado']};
                display:flex;align-items:center;justify-content:center;margin:-26px 0;z-index:4;
                border:9px solid {P['creme']}">
      <span class="display" style="font-size:38px;color:{P['branco']}">vs</span>
    </div>

    <div class="card" style="background:{P['verde']};box-shadow:none;padding:62px 50px">
      <span class="rotulo" style="font-size:22px;color:{P['menta']}">Realidade</span>
      <div style="font-family:'Lufga';font-weight:900;font-size:66px;line-height:1.1;
                  color:{P['branco']};margin-top:22px">{s['realidade']}</div>
      <div style="display:flex;gap:13px;flex-wrap:wrap;margin-top:32px">{chips}</div>
    </div>
  </div>
  {rodape()}
</div>"""


def slide_numerao(s):
    """Componente de número gigante: Luckiest Guy dourado sobre verde escuro."""
    chips = "".join(
        f'<span class="chip" style="background:rgba(255,255,255,.12);color:{P["menta"]}">{c}</span>'
        for c in s.get("chips", [])
    )
    return f"""
<div class="slide">
  {topo(s.get("rotulo", "Números da casa"))}
  <div class="corpo">
    <div class="card" style="background:{P['verde_escuro']};box-shadow:none;padding:92px 52px;
                             display:flex;flex-direction:column;align-items:center;text-align:center;gap:16px">
      <span class="rotulo" style="color:{P['salvia']};font-size:24px">{s['acima']}</span>
      <div class="display" style="font-size:240px;color:{P['dourado']};line-height:.88">{s['numero']}</div>
      <div style="font-family:'Lufga';font-weight:700;font-size:34px;letter-spacing:.19em;
                  text-transform:uppercase;color:{P['branco']}">{s['abaixo']}</div>
      <div class="giz" style="font-size:45px;color:{P['menta']};margin-top:20px">{s['giz']}</div>
      <div style="display:flex;gap:13px;flex-wrap:wrap;justify-content:center;margin-top:26px">{chips}</div>
    </div>
  </div>
  {rodape()}
</div>"""


def slide_faq(s):
    """Componente BOWL GREEN RESPONDE: pergunta manuscrita + balão verde."""
    return f"""
<div class="slide">
  {topo(s.get("rotulo", "Bowl Green responde"))}
  <div class="corpo">
    <div class="card" style="display:flex;flex-direction:column;gap:26px">
      <div style="display:flex;gap:18px;align-items:flex-start">
        <div style="flex:0 0 auto;width:66px;height:66px;border-radius:50%;background:{P['rosa']};
                    display:flex;align-items:center;justify-content:center;font-size:32px">🙋</div>
        <div style="background:{P['creme_claro']};border-radius:26px;border-top-left-radius:8px;padding:34px 34px">
          <div class="giz" style="font-size:52px;color:{P['verde_escuro']}">“{s['pergunta']}”</div>
          <div style="font-family:'Lufga';font-weight:500;font-size:25px;color:#9AA396;margin-top:12px">{s['fonte']}</div>
        </div>
      </div>
      <div style="display:flex;gap:18px;align-items:flex-end;flex-direction:row-reverse">
        <div style="flex:0 0 auto;width:66px;height:66px;border-radius:50%;background:{P['menta']};
                    display:flex;align-items:center;justify-content:center;font-size:32px">🥗</div>
        <div style="background:{P['verde']};border-radius:26px;border-bottom-right-radius:8px;padding:38px 36px">
          <div style="font-family:'Lufga';font-weight:700;font-size:45px;line-height:1.3;color:{P['branco']}">{s['resposta']}</div>
        </div>
      </div>
      <span class="chip" style="background:{P['amarelo']};color:{P['dourado_escuro']};align-self:center;
                                font-size:27px;padding:15px 30px">{s['rodape_chip']}</span>
    </div>
  </div>
  {rodape()}
</div>"""


def slide_cta(s):
    """Fechamento: banda mosaico, display gigante e pílula dourada."""
    chips = "".join(
        f'<span class="chip" style="background:rgba(255,255,255,.14);color:{P["menta"]}">{c}</span>'
        for c in s.get("chips", [])
    )
    return f"""
<div class="slide" style="background:{P['verde']};padding:0">
  <div style="padding:64px 60px 52px;display:flex;flex-direction:column;height:100%">
    <div class="topo" style="justify-content:center;margin-bottom:0">
      <img src="{logo('dourado')}" alt="" style="height:108px">
    </div>
    <div class="corpo" style="align-items:center;text-align:center">
      <div class="display" style="font-size:106px;color:{P['creme']}">{s['titulo']}</div>
      <div style="font-family:'Lufga';font-weight:500;font-size:36px;line-height:1.4;
                  color:{P['menta']};max-width:780px">{s['texto']}</div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">{chips}</div>
      <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};
                                font-size:32px;padding:20px 44px;margin-top:14px">{s['botao']}</span>
      <div class="giz" style="font-size:36px;color:{P['salvia']}">{s['giz']}</div>
    </div>
    <div style="margin-top:auto">{mosaico()}</div>
    <div class="rodape" style="justify-content:center;color:{P['dourado']};margin-top:26px">
      <span>@bowlgreenxerem</span>
    </div>
  </div>
</div>"""


TIPOS = {
    "mito-verdade": slide_mito_verdade,
    "expectativa": slide_expectativa,
    "numerao": slide_numerao,
    "faq": slide_faq,
    "cta": slide_cta,
}


def pagina(slide):
    construtor = TIPOS.get(slide.get("tipo"))
    if not construtor:
        raise ValueError(f"tipo desconhecido: {slide.get('tipo')} — use um de {list(TIPOS)}")
    css = (CSS.replace("__L__", str(LARGURA)).replace("__A__", str(ALTURA))
              .replace("__CREME__", P["creme"]).replace("__BRANCO__", P["branco"])
              .replace("__VERDE__", P["verde"]))
    return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>"
            f"<style>{fontes()}{css}</style></head><body>{construtor(slide)}</body></html>")


def main():
    if len(sys.argv) < 3:
        print("Uso: python gerar_slides.py <config.json> <pasta_saida>", file=sys.stderr)
        sys.exit(1)

    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2])
    saida.mkdir(parents=True, exist_ok=True)
    slides = config["slides"]

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pg = navegador.new_page(viewport={"width": LARGURA, "height": ALTURA}, device_scale_factor=1)
        for i, slide in enumerate(slides, 1):
            pg.set_content(pagina(slide), wait_until="load")
            pg.wait_for_timeout(340)
            destino = saida / f"slide-{i:02d}.png"
            pg.screenshot(path=str(destino))
            print(f"  [{i}/{len(slides)}] {destino.name}  ({slide['tipo']})")
        navegador.close()

    print(f"\nPronto — {len(slides)} slides em {saida}/  ({LARGURA}x{ALTURA}, 4:5)")


if __name__ == "__main__":
    main()
