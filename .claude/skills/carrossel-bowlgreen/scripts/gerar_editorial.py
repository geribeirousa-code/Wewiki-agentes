#!/usr/bin/env python3
"""
Peças editoriais — Bowl Green, foto sangrando e palavra gigante na frente.

Por que existe além de gerar_peças.py: a Gê recusou aquela leva inteira em
2026-07-27 — "tá na paleta, tá na tipologia, mas tá com cara de pobre",
"tá tudo padrãozinho". A crítica tinha três partes e todas viram regra aqui.

  1. PÚBLICO A. As fotos vêm de gerar_lifestyle.py com direção classe alta.
     Nada de "gente simples" — as referências dela são interior de carro
     importado, mármore, joia fina, alfaiataria.
  2. FOTO MANDA. "Botar uma imagem inteira de fundo e a palavra na frente."
     A foto sangra os quatro lados. Nenhum tipo aqui tem tarja de bloco chapado
     ocupando meia peça — era isso que dava cara de material de panfleto.
  3. UM PRATO POR PEÇA. Ela apontou que era sempre o mesmo poke. Wrap, suco,
     tabule, grelhado e os pokes se revezam.

Referências que mandam (Fotos/referencias/):
  · "ЛЮБЛЮ МАТЧУ"    → tipo `cartaz`: fundo texturizado cheio, palavra enorme
  · "Pasta Plate"    → tipo `onda`: split orgânico curvo, prato ao centro
  · "Life lately"    → direção de fotografia das cenas de pessoa
  · "Red & Mango"    → foco raso, molho escorrendo, mármore

Tipos de feed (1080x1350): cartaz · onda · vazado · moldura · etiqueta
Tipos de story (1080x1920): story-cartaz · story-vazado · story-moldura

Uso:
    python gerar_editorial.py <config.json> <pasta_saida>
"""

import importlib.util
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

_p = importlib.util.spec_from_file_location("gp", Path(__file__).with_name("gerar_peças.py"))
gp = importlib.util.module_from_spec(_p); _p.loader.exec_module(gp)
P, fontes, logo, foto = gp.P, gp.fontes, gp.logo, gp.foto
estampa, selo, mosaico = gp.estampa, gp.selo, gp.mosaico


def onda_svg(cor, altura=190, invertida=False):
    """Divisória orgânica — a curva do 'Pasta Plate Poster'. Reta é o que dava
    cara de bloco; a curva é o que faz a peça parecer desenhada."""
    d = ("M0,120 C220,20 420,200 680,110 C860,50 980,120 1080,80 L1080,0 L0,0 Z"
         if invertida else
         "M0,70 C200,170 430,10 690,90 C870,145 980,60 1080,110 L1080,200 L0,200 Z")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 200" '
            f'preserveAspectRatio="none" style="display:block;width:1080px;height:{altura}px">'
            f'<path d="{d}" fill="{cor}"/></svg>')


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__L__px;height:__A__px;overflow:hidden}
body{font-family:'Lufga',sans-serif;-webkit-font-smoothing:antialiased;background:__CREME__}
.peca{position:relative;width:__L__px;height:__A__px;overflow:hidden;background:__CREME__}

.display{font-family:'Luckiest Guy',cursive;text-transform:uppercase;letter-spacing:.006em;
         font-weight:400;line-height:.86}
.giz{font-family:'Chalkiez',cursive;line-height:1.3}
.num{font-family:'Shantell Sans',cursive;font-weight:800;line-height:.86}
.lbl{font-weight:800;letter-spacing:.3em;text-transform:uppercase}

.cobre{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.veu{position:absolute;inset:0;z-index:1}
.frente{position:absolute;z-index:4}
.estampa{position:absolute;inset:0;z-index:0;background-repeat:repeat}
.selo{position:absolute;z-index:6;filter:drop-shadow(0 14px 26px rgba(28,53,39,.3))}
.mosaico{display:flex;width:100%}
.mosaico i{flex:1}

/* Sombra em duas camadas: uma curta e densa para descolar da foto, outra larga
   e difusa para dar peso. Sem ela a palavra branca some no claro da imagem. */
.sombra{text-shadow:0 3px 14px rgba(20,36,26,.5), 0 18px 60px rgba(20,36,26,.42)}
.pill{display:inline-block;border-radius:999px;font-family:'Luckiest Guy',cursive;
      letter-spacing:.04em;text-transform:uppercase;line-height:1}
.assina{position:absolute;z-index:7;font-weight:800;font-size:29px;color:#fff;
        letter-spacing:.02em;text-shadow:0 2px 14px rgba(20,36,26,.65)}

/* Scrim da legenda. O gradiente do véu não resolve sozinho: dependendo da foto o
   bowl cai justamente na faixa do giz e a letra manuscrita — que é fina e sem
   peso — some dentro da comida. O scrim garante contraste em qualquer imagem. */
.scrim{display:inline-block;background:rgba(20,36,26,.58);backdrop-filter:blur(7px);
       border-radius:22px;padding:18px 30px}
"""


# ─── FEED ───────────────────────────────────────────────────────────────────

def t_cartaz(s):
    """Matcha poster. Foto cheia, uma palavra enorme na frente, nada mais.
    A peça mais silenciosa do conjunto — e a que mais para o dedo."""
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 45%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.5) 0%,rgba(20,36,26,.08) 30%,
       rgba(20,36,26,.12) 58%,rgba(20,36,26,.72) 100%)"></div>
  <img src="{logo('branco')}" class="frente" style="top:52px;left:60px;width:212px">
  <div class="frente sombra" style="left:0;right:0;top:{s.get('topo',420)}px;text-align:center;padding:0 48px">
    <div class="display" style="font-size:{s.get('tam',230)}px;color:#fff">{s['palavra']}</div>
  </div>
  <!-- o giz desce para a faixa escura do rodapé. Colado na palavra ele caía em
       cima da comida e sumia — letra de giz não aguenta fundo movimentado. -->
  <div class="frente" style="left:56px;right:56px;bottom:236px;text-align:center">
    <div class="giz scrim" style="font-size:{s.get('tam_giz',46)}px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  <div class="frente" style="left:0;right:0;bottom:126px;text-align:center">
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:34px;padding:20px 44px">{s.get('botao','Link da bio')}</span>
  </div>
  <div class="assina" style="left:60px;bottom:46px">@bowlgreenxerem</div>
  <div class="assina" style="right:60px;bottom:46px;font-family:'Chalkiez',cursive;font-weight:400;font-size:34px">{s.get('canto','Xerém · RJ')}</div>
</div>"""


def t_onda(s):
    """Pasta Plate Poster. Split orgânico, prato recortado ao centro, tipografia
    nos dois lados. É a única peça do conjunto sem foto de pessoa."""
    return f"""
<div class="peca" style="background:{P['creme_claro']}">
  <div style="position:absolute;top:0;left:0;right:0;height:620px;background:{P['verde_escuro']};overflow:hidden">
    {estampa(.12, .9)}
  </div>
  <div style="position:absolute;top:520px;left:0;z-index:2">{onda_svg(P['creme_claro'], 200)}</div>
  <img src="{logo('dourado')}" style="position:absolute;top:52px;left:60px;width:196px;z-index:3">
  <div style="position:absolute;top:64px;right:60px;z-index:3;text-align:right">
    <div class="lbl" style="font-size:24px;color:{P['menta']}">{s.get('rotulo','do cardápio')}</div>
  </div>
  <div style="position:absolute;top:190px;left:60px;right:60px;z-index:3;text-align:center">
    <div class="display" style="font-size:{s.get('tam',132)}px;color:{P['creme']}">{s['titulo']}</div>
  </div>
  <div style="position:absolute;left:50%;top:400px;transform:translateX(-50%);width:520px;height:520px;
       border-radius:50%;background:{P['dourado']};opacity:.16;z-index:3"></div>
  <img src="{foto(s['prato'])}" style="position:absolute;left:50%;top:410px;transform:translateX(-50%);
       height:500px;z-index:4;filter:drop-shadow(0 34px 54px rgba(28,53,39,.34))">
  <div style="position:absolute;left:56px;bottom:150px;right:56px;z-index:5;display:flex;
       justify-content:space-between;align-items:flex-end;gap:20px">
    <div style="text-align:left">
      <div class="num" style="font-size:96px;color:{P['coral']}">{s['numero']}</div>
      <div style="font-weight:800;font-size:32px;color:{P['verde']};margin-top:2px">{s.get('numero_label','')}</div>
    </div>
    <div class="giz" style="font-size:42px;color:{P['dourado_escuro']};text-align:right;max-width:520px">{s.get('giz','')}</div>
  </div>
  {mosaico(20).replace('style="height:20px"', 'style="height:20px;position:absolute;left:0;bottom:104px;z-index:5"')}
  <div style="position:absolute;left:60px;right:60px;bottom:40px;z-index:6;display:flex;
       justify-content:space-between;align-items:center;font-weight:800;font-size:29px;color:{P['verde']}">
    <span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:28px;padding:15px 30px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def t_vazado(s):
    """Foto cheia com a palavra VAZADA — só contorno. Deixa a imagem passar por
    dentro da letra. É o tipo mais caro de olhar e não custa nada."""
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 45%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.62) 0%,rgba(20,36,26,.15) 42%,rgba(20,36,26,.8) 100%)"></div>
  <img src="{logo('branco')}" class="frente" style="top:52px;right:56px;width:190px">
  <div class="frente" style="left:56px;top:56px">
    <span class="lbl" style="font-size:25px;color:#fff;opacity:.9">{s.get('rotulo','bowl green')}</span>
  </div>
  <div class="frente" style="left:56px;right:56px;top:{s.get('topo',300)}px">
    <div class="display" style="font-size:{s.get('tam',186)}px;color:transparent;
         -webkit-text-stroke:5px #fff;paint-order:stroke fill">{s['vazado']}</div>
    <div class="display sombra" style="font-size:{s.get('tam',186)}px;color:#fff;margin-top:6px">{s['cheio']}</div>
  </div>
  <div class="frente" style="left:56px;right:56px;bottom:150px">
    <div class="giz scrim" style="font-size:46px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  {mosaico(18).replace('style="height:18px"', 'style="height:18px;position:absolute;left:0;bottom:104px;z-index:5"')}
  <div class="assina" style="left:56px;bottom:44px">@bowlgreenxerem</div>
  <div class="frente" style="right:56px;bottom:38px">
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:28px;padding:15px 30px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def t_moldura(s):
    """Editorial de revista: a foto sangra, mas um filete creme desenha uma
    moldura por dentro. Caps espaçada em cima, serifa de giz embaixo."""
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 45%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.46) 0%,rgba(20,36,26,.05) 34%,rgba(20,36,26,.66) 100%)"></div>
  <div class="frente" style="inset:34px;border:3px solid rgba(245,241,230,.85);border-radius:6px;pointer-events:none"></div>
  <div class="frente" style="left:0;right:0;top:74px;text-align:center">
    <div class="lbl" style="font-size:26px;color:#fff">{s.get('rotulo','bowl green · xerém')}</div>
  </div>
  <img src="{logo('branco')}" class="frente" style="left:50%;transform:translateX(-50%);top:126px;width:224px">
  <!-- 356px, não 270: o scrim do giz mora em 196 e come ~130 de altura. Com o
       título em 270 a segunda linha ficava por baixo da legenda. -->
  <div class="frente sombra" style="left:70px;right:70px;bottom:356px;text-align:center">
    <div class="display" style="font-size:{s.get('tam',150)}px;color:#fff">{s['titulo']}</div>
  </div>
  <div class="frente" style="left:70px;right:70px;bottom:196px;text-align:center">
    <div class="giz scrim" style="font-size:44px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  {selo(s.get('selo_topo','LACRADO FRESQUINHO'), '✦ BOWL GREEN ✦', s.get('selo_emoji','🥗'),
        s.get('selo_pe','FEITO HOJE'), 188, -10).replace('style="width:188px', 'style="right:64px;top:64px;width:188px')}
  <div class="frente" style="left:0;right:0;bottom:106px;text-align:center">
    <span class="pill" style="background:{P['creme']};color:{P['verde']};font-size:30px;padding:17px 36px">{s.get('botao','Link da bio')}</span>
  </div>
  <div class="assina" style="left:0;right:0;bottom:56px;text-align:center;font-size:27px">@bowlgreenxerem</div>
</div>"""


def t_etiqueta(s):
    """Foto domina; o texto vive numa etiqueta creme inclinada, como carimbo de
    embalagem. Três números empilhados — ficha técnica sem cara de tabela."""
    linhas = "".join(
        f'<div style="display:flex;align-items:baseline;gap:14px;margin-top:10px">'
        f'<span class="num" style="font-size:52px;color:{P["coral"]}">{i["valor"]}</span>'
        f'<span style="font-weight:800;font-size:30px;color:{P["verde"]}">{i["rotulo"]}</span></div>'
        for i in s.get("itens", []))
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 40%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.44) 0%,transparent 32%)"></div>
  <img src="{logo('branco')}" class="frente" style="top:50px;left:58px;width:200px">
  <!-- Etiqueta ancorada no ALTO, não no rodapé: encostada embaixo ela tapava o
       bowl inteiro e sobrava uma peça sem comida. Aqui o prato fica livre. -->
  <div class="frente" style="left:52px;top:{s.get('topo',330)}px;width:560px;background:{P['creme']};
       border-radius:20px;padding:36px 38px 32px;transform:rotate(-1.6deg);
       box-shadow:0 28px 60px rgba(20,36,26,.42)">
    <div class="lbl" style="font-size:22px;color:{P['dourado_escuro']}">{s.get('rotulo','ficha da casa')}</div>
    <div class="display" style="font-size:{s.get('tam',88)}px;color:{P['verde']};margin-top:12px">{s['titulo']}</div>
    <div style="width:78px;height:6px;background:{P['coral']};border-radius:3px;margin:18px 0 2px"></div>
    {linhas}
    <div class="giz" style="font-size:35px;color:{P['dourado_escuro']};margin-top:18px">{s.get('giz','')}</div>
  </div>
  {selo(s.get('selo_topo','PESADO NA BALANÇA'), '✦ BOWL GREEN ✦', s.get('selo_emoji','⚖️'),
        s.get('selo_pe','SEM ACHISMO'), 186, 11).replace('style="width:186px', 'style="right:52px;top:150px;width:186px')}
  <!-- sem faixa mosaico aqui: nesta composição o bowl vive no rodapé e a faixa
       cortava ele no meio. A etiqueta e o selo já carregam a marca. -->
  <div class="veu" style="top:auto;height:210px;bottom:0;z-index:2;
       background:linear-gradient(180deg,transparent 0%,rgba(20,36,26,.72) 78%)"></div>
  <div class="assina" style="left:58px;bottom:44px">@bowlgreenxerem</div>
  <div class="frente" style="right:56px;bottom:38px">
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:28px;padding:15px 30px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


# ─── STORY ──────────────────────────────────────────────────────────────────

def t_story_cartaz(s):
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 42%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.55) 0%,rgba(20,36,26,.05) 26%,
       rgba(20,36,26,.1) 50%,rgba(20,36,26,.85) 88%)"></div>
  <img src="{logo('branco')}" class="frente" style="top:150px;left:60px;width:230px">
  <div class="frente" style="left:60px;top:158px;right:60px;text-align:right">
    <span class="lbl" style="font-size:26px;color:#fff;opacity:.92">{s.get('rotulo','agora')}</span>
  </div>
  <!-- 500px: o scrim do giz começa em 330 e sobe ~130. Em 340 a segunda linha
       da palavra ficava por baixo da legenda. -->
  <div class="frente sombra" style="left:56px;right:56px;bottom:500px">
    <div class="display" style="font-size:{s.get('tam',176)}px;color:#fff">{s['palavra']}</div>
  </div>
  <div class="frente" style="left:56px;right:56px;bottom:330px">
    <div class="giz scrim" style="font-size:48px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  <div class="frente" style="left:56px;bottom:222px">
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:44px;padding:26px 56px">{s.get('botao','Peça agora ↑')}</span>
  </div>
  {mosaico(22).replace('style="height:22px"', 'style="height:22px;position:absolute;left:0;bottom:176px;z-index:5"')}
</div>"""


def t_story_vazado(s):
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 44%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.6) 0%,rgba(20,36,26,.12) 38%,rgba(20,36,26,.86) 86%)"></div>
  <img src="{logo('branco')}" class="frente" style="top:150px;left:60px;width:222px">
  <div class="frente" style="left:56px;right:56px;top:{s.get('topo',560)}px">
    <div class="display" style="font-size:{s.get('tam',168)}px;color:transparent;
         -webkit-text-stroke:5px #fff">{s['vazado']}</div>
    <div class="display sombra" style="font-size:{s.get('tam',168)}px;color:#fff;margin-top:6px">{s['cheio']}</div>
  </div>
  <div class="frente" style="left:56px;right:56px;bottom:300px">
    <div class="giz scrim" style="font-size:48px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  <div class="frente" style="left:56px;bottom:196px">
    <span class="pill" style="background:{P['coral']};color:#fff;font-size:44px;padding:26px 56px">{s.get('botao','Quero esse ↑')}</span>
  </div>
  {mosaico(22).replace('style="height:22px"', 'style="height:22px;position:absolute;left:0;bottom:150px;z-index:5"')}
</div>"""


def t_story_moldura(s):
    """Story de enquete, mas sem o bloco chapado de antes: a foto continua
    sangrando e as duas opções flutuam sobre ela."""
    ops = "".join(
        f'<div style="flex:1;background:{c};border-radius:24px;padding:34px 18px;text-align:center;'
        f'box-shadow:0 18px 40px rgba(20,36,26,.35)">'
        f'<div class="display" style="font-size:60px;color:{t}">{o}</div></div>'
        for o, c, t in zip(s["opcoes"], [P["menta"], P["rosa"]], [P["verde_escuro"], P["coral"]]))
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 40%')}">
  <div class="veu" style="background:linear-gradient(180deg,rgba(20,36,26,.5) 0%,rgba(20,36,26,.08) 30%,rgba(20,36,26,.82) 82%)"></div>
  <div class="frente" style="inset:34px;border:3px solid rgba(245,241,230,.8);border-radius:6px"></div>
  <img src="{logo('branco')}" class="frente" style="left:50%;transform:translateX(-50%);top:158px;width:236px">
  <div class="frente sombra" style="left:56px;right:56px;bottom:520px;text-align:center">
    <div class="lbl" style="font-size:27px;color:{P['menta']};margin-bottom:22px">{s.get('rotulo','enquete do dia')}</div>
    <div class="display" style="font-size:{s.get('tam',148)}px;color:#fff">{s['pergunta']}</div>
  </div>
  <div class="frente" style="left:56px;right:56px;bottom:340px;display:flex;gap:22px">{ops}</div>
  <div class="frente" style="left:56px;right:56px;bottom:230px;text-align:center">
    <div class="giz scrim" style="font-size:46px;color:{P['menta']}">{s.get('giz','')}</div>
  </div>
  {mosaico(22).replace('style="height:22px"', 'style="height:22px;position:absolute;left:0;bottom:160px;z-index:5"')}
</div>"""


TIPOS = {"cartaz": t_cartaz, "onda": t_onda, "vazado": t_vazado,
         "moldura": t_moldura, "etiqueta": t_etiqueta,
         "story-cartaz": t_story_cartaz, "story-vazado": t_story_vazado,
         "story-moldura": t_story_moldura}


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2]); saida.mkdir(parents=True, exist_ok=True)
    css_fontes = fontes()

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for i, s in enumerate(cfg["pecas"], 1):
            if s["tipo"] not in TIPOS:
                raise SystemExit(f"ERRO: tipo '{s['tipo']}' não existe. Tem: {', '.join(TIPOS)}")
            L, A = 1080, (1920 if s["tipo"].startswith("story") else 1350)
            css = CSS.replace("__L__", str(L)).replace("__A__", str(A)).replace("__CREME__", P["creme"])
            html = (f"<!doctype html><html><head><meta charset='utf-8'>"
                    f"<style>{css_fontes}{css}</style></head><body>{TIPOS[s['tipo']](s)}</body></html>")
            pg = nav.new_page(viewport={"width": L, "height": A}, device_scale_factor=1)
            pg.set_content(html)
            pg.wait_for_timeout(700)
            nome = s.get("arquivo") or f"{i:02d}-{s['tipo']}"
            pg.screenshot(path=str(saida / f"{nome}.png"))
            pg.close()
            print(f"OK  {nome}.png  ({L}x{A})")
        nav.close()


if __name__ == "__main__":
    main()
