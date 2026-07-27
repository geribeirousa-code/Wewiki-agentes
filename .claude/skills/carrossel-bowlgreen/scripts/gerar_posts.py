#!/usr/bin/env python3
"""
Posts com foto — Bowl Green.

Formatos que usam a foto real do prato como protagonista. Fundo sempre claro,
paleta e as 4 vozes do Design System. Reaproveita fontes/paleta de gerar_slides.

Formatos:
  produto      4:5  faixa verde, prato grande, nome, preço, chips
  raio-x       4:5  prato ao centro, linhas pontilhadas para os ingredientes
  comparativo  4:5  dois pratos, badges e linhas de comparação
  story        9:16 fundo coral, prato, chamada de novidade

Uso:
    python gerar_posts.py <config.json> <pasta_saida>
"""

import base64
import importlib.util
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

_spec = importlib.util.spec_from_file_location("gs", Path(__file__).with_name("gerar_slides.py"))
gs = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(gs)
P, fontes, logo, MOSAICO = gs.P, gs.fontes, gs.logo, gs.MOSAICO

RAIZ_FOTOS = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN/Fotos")
# Recortados primeiro: foto com fundo branco colada sobre o creme vira um quadrado
# branco na peça. Ver recortar_fundo.py.
PASTAS = [RAIZ_FOTOS / "recortados", RAIZ_FOTOS / "pratos"]


def foto(nome):
    """Acha a foto do prato pelo nome do arquivo, sem exigir renomear nada."""
    alvo = nome.strip().lower()
    for pasta in PASTAS:
        if not pasta.is_dir():
            continue
        for p in pasta.iterdir():
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.stem.lower() == alvo:
                mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
                return "data:" + mime + ";base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    disponiveis = ", ".join(sorted({x.stem for pa in PASTAS if pa.is_dir() for x in pa.iterdir() if x.is_file()}))
    raise SystemExit(f"ERRO: foto '{nome}' não encontrada em {RAIZ_FOTOS}\nDisponíveis: {disponiveis}")


def mosaico():
    return '<div class="mosaico">' + "".join(f'<i style="background:{c}"></i>' for c in MOSAICO) + "</div>"


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__L__px;height:__A__px;overflow:hidden}
body{font-family:'Lufga',sans-serif;-webkit-font-smoothing:antialiased;background:__CREME__}
.slide{position:relative;width:__L__px;height:__A__px;overflow:hidden;display:flex;flex-direction:column;background:__CREME__}

.display{font-family:'Luckiest Guy',cursive;text-transform:uppercase;letter-spacing:.012em;font-weight:400;line-height:.98}
.giz{font-family:'Chalkiez',cursive;line-height:1.4}
.num{font-family:'Shantell Sans',cursive;font-weight:700}

.faixa{background:__VERDE__;padding:34px 0 30px;display:flex;align-items:center;justify-content:center;gap:18px}
.faixa img{height:62px}
.mosaico{display:flex;height:16px;width:100%}
.mosaico i{flex:1}

.palco{flex:1;position:relative;display:flex;flex-direction:column;align-items:center;
       justify-content:center;padding:26px 62px 0;text-align:center}
/* disco atrás de tudo; todo o resto do palco acima dele, na ordem do DOM —
   sem isso o prato (posicionado) pinta por cima do nome do prato. */
.disco{position:absolute;border-radius:50%;background:__MENTA_CL__;z-index:0}
.palco > *:not(.disco){position:relative;z-index:1}
.moldura{width:640px;height:640px;border-radius:50%;background:__MENTA_CL__;
         display:flex;align-items:center;justify-content:center;flex:0 0 auto}
.moldura .prato{height:540px;width:auto;max-width:600px}
.prato{display:block;object-fit:contain;filter:drop-shadow(0 26px 40px rgba(28,53,39,.18))}

.chips{display:flex;flex-wrap:wrap;gap:11px;justify-content:center;position:relative;z-index:2}
.chip{background:__MENTA_CL__;color:__VERDE__;border-radius:999px;padding:11px 22px;font-weight:700;font-size:26px}

.rodape{padding:0 62px 46px;display:flex;align-items:center;justify-content:space-between;
        font-weight:700;font-size:26px;color:__VERDE__}
.pill{display:inline-block;border-radius:999px;padding:16px 34px;font-family:'Luckiest Guy',cursive;
      font-size:29px;letter-spacing:.05em;text-transform:uppercase;line-height:1}
"""


def slide_produto(s):
    chips = "".join(f'<span class="chip">{c}</span>' for c in s.get("chips", []))
    preco = (f'<div class="num" style="font-size:86px;color:{P["coral"]};line-height:1;margin-top:6px">'
             f'{s["preco"]}</div>') if s.get("preco") else ""
    return f"""
<div class="slide">
  <div class="faixa"><img src="{logo('dourado')}" alt=""></div>
  {mosaico()}
  <div class="palco" style="justify-content:center;padding-top:0">
    <!-- o disco é a moldura do prato, não um elemento solto: assim ele nunca
         escapa para cima da faixa verde nem para cima do nome -->
    <div class="moldura"><img class="prato" src="{foto(s['foto'])}"></div>
    <div class="display" style="font-size:76px;color:{P['verde']};margin-top:18px">{s['nome']}</div>
    <div class="giz" style="font-size:40px;color:{P['dourado_escuro']};margin-top:8px">{s['descricao']}</div>
    {preco}
    <div class="chips" style="margin-top:22px">{chips}</div>
  </div>
  <div class="rodape">
    <span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:25px;padding:13px 26px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def slide_raiox(s):
    def marca(item, lado, topo):
        borda = "right" if lado == "esq" else "left"
        alinha = "right" if lado == "esq" else "left"
        pos = "left:44px" if lado == "esq" else "right:44px"
        return f"""
    <div style="position:absolute;{pos};top:{topo}px;width:240px;text-align:{alinha};z-index:3">
      <div style="font-weight:800;font-size:31px;color:{P['verde']};line-height:1.12">{item['titulo']}</div>
      <div class="giz" style="font-size:29px;color:{P['dourado_escuro']};margin-top:4px">{item['texto']}</div>
      <div style="border-{borda}:0;border-top:4px dashed {P['dourado']};width:74px;margin-top:12px;
                  margin-{'left' if lado=='esq' else 'right'}:auto"></div>
    </div>"""

    esq = s["esquerda"]; dir_ = s["direita"]
    tops_e = [270, 500, 730][:len(esq)]
    tops_d = [270, 500, 730][:len(dir_)]
    marcas = "".join(marca(i, "esq", t) for i, t in zip(esq, tops_e))
    marcas += "".join(marca(i, "dir", t) for i, t in zip(dir_, tops_d))
    return f"""
<div class="slide" style="background:{P['branco']}">
  <div style="padding:52px 56px 0;display:flex;align-items:center;justify-content:space-between">
    <span style="font-weight:700;font-size:24px;letter-spacing:.2em;text-transform:uppercase;color:#9AA396">Raio-X do pedido</span>
    <img src="{logo('verde')}" style="height:54px">
  </div>
  <div class="palco" style="padding-top:0">
    <div class="display" style="font-size:64px;color:{P['verde']};position:absolute;top:96px;width:100%">{s['nome']}</div>
    <div class="disco" style="width:540px;height:540px;top:270px;background:{P['creme']}"></div>
    <img class="prato" src="{foto(s['foto'])}" style="width:450px;margin-top:52px">
    {marcas}
  </div>
  <div style="padding:0 56px 26px;text-align:center">
    <div class="giz" style="font-size:36px;color:{P['verde']}">{s['giz']}</div>
  </div>
  {mosaico()}
  <div class="rodape" style="padding:22px 56px 34px">
    <span>@bowlgreenxerem</span><span class="num" style="color:{P['coral']};font-size:34px">{s.get('preco','')}</span>
  </div>
</div>"""


def slide_comparativo(s):
    a, b = s["a"], s["b"]
    linhas = "".join(f"""
    <div style="display:flex;align-items:center;gap:14px;padding:16px 0;border-top:2px solid {P['menta_claro']}">
      <div class="num" style="flex:1;text-align:right;font-size:34px;color:{P['coral']}">{l['a']}</div>
      <div style="flex:0 0 auto;width:250px;text-align:center;font-weight:700;font-size:22px;
                  letter-spacing:.16em;text-transform:uppercase;color:#9AA396">{l['rotulo']}</div>
      <div class="num" style="flex:1;text-align:left;font-size:34px;color:{P['coral']}">{l['b']}</div>
    </div>""" for l in s["linhas"])
    return f"""
<div class="slide" style="background:{P['creme_claro']}">
  <div style="padding:52px 56px 0;display:flex;align-items:center;justify-content:space-between">
    <span style="font-weight:700;font-size:24px;letter-spacing:.2em;text-transform:uppercase;color:#9AA396">{s.get('rotulo','Tira-teima da casa')}</span>
    <img src="{logo('verde')}" style="height:54px">
  </div>
  <div style="flex:1;padding:14px 56px 0;display:flex;flex-direction:column;justify-content:center">
    <div style="display:flex;align-items:center;gap:16px">
      <div style="flex:1;text-align:center">
        <img src="{foto(a['foto'])}" style="width:330px;filter:drop-shadow(0 18px 30px rgba(28,53,39,.16))">
        <div class="pill display" style="background:{P['verde']};color:{P['branco']};margin-top:6px">{a['nome']}</div>
      </div>
      <div style="flex:0 0 auto;width:92px;height:92px;border-radius:50%;background:{P['dourado']};
                  display:flex;align-items:center;justify-content:center">
        <span class="display" style="font-size:34px;color:{P['branco']}">vs</span>
      </div>
      <div style="flex:1;text-align:center">
        <img src="{foto(b['foto'])}" style="width:330px;filter:drop-shadow(0 18px 30px rgba(28,53,39,.16))">
        <div class="pill display" style="background:{P['dourado']};color:{P['verde_escuro']};margin-top:6px">{b['nome']}</div>
      </div>
    </div>
    <div style="margin-top:26px">{linhas}</div>
    <div class="giz" style="font-size:37px;color:{P['verde']};text-align:center;margin-top:24px">{s['giz']}</div>
  </div>
  {mosaico()}
  <div class="rodape" style="padding:22px 56px 34px"><span>@bowlgreenxerem</span>
    <span style="color:{P['dourado_escuro']}">na dúvida, pede os dois</span></div>
</div>"""


def slide_trio(s):
    """Três itens lado a lado: wraps, sucos, linha de saladas."""
    itens = "".join(f"""
      <div style="flex:1;text-align:center">
        <img src="{foto(i['foto'])}" style="height:330px;width:auto;max-width:290px;
             filter:drop-shadow(0 16px 26px rgba(28,53,39,.16))">
        <div class="display" style="font-size:38px;color:{P['verde']};margin-top:14px">{i['nome']}</div>
        <div class="giz" style="font-size:29px;color:{P['dourado_escuro']};margin-top:6px">{i['nota']}</div>
      </div>""" for i in s["itens"])
    return f"""
<div class="slide">
  <div class="faixa"><img src="{logo('dourado')}" alt=""></div>
  {mosaico()}
  <div class="palco" style="justify-content:center;padding:34px 48px 0">
    <div class="display" style="font-size:70px;color:{P['verde']}">{s['titulo']}</div>
    <div class="giz" style="font-size:38px;color:{P['dourado_escuro']};margin-top:8px">{s['subtitulo']}</div>
    <div style="display:flex;gap:16px;align-items:flex-end;width:100%;margin-top:40px">{itens}</div>
  </div>
  <div class="rodape"><span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:25px;padding:13px 26px">{s.get('botao','Link da bio')}</span></div>
</div>"""


def slide_confissao(s):
    """Card de frase: fundo sálvia, giz gigante. O formato mais salvo."""
    return f"""
<div class="slide" style="background:{P['salvia']}">
  <div style="padding:56px 60px 0;display:flex;align-items:center;justify-content:space-between">
    <span style="font-weight:700;font-size:24px;letter-spacing:.2em;text-transform:uppercase;color:{P['verde']};opacity:.6">{s.get('rotulo','Confissões de bowlover')}</span>
    <img src="{logo('verde')}" style="height:54px">
  </div>
  <div class="palco" style="justify-content:center;padding:0 78px">
    <div class="display" style="font-size:120px;color:{P['creme']};opacity:.85;line-height:.7">“</div>
    <div class="giz" style="font-size:66px;color:{P['verde_escuro']};margin-top:-10px">{s['frase']}</div>
    <div style="font-weight:700;font-size:28px;color:{P['verde']};opacity:.7;margin-top:34px">{s['assinatura']}</div>
  </div>
  {mosaico()}
  <div class="rodape" style="padding:22px 60px 40px"><span>@bowlgreenxerem</span>
    <span style="color:{P['verde_escuro']};opacity:.7">{s.get('cta','manda a sua na DM')}</span></div>
</div>"""


def slide_quiz(s):
    """Duas opções com foto: gera comentário sem exigir esforço de quem responde."""
    opcoes = "".join(f"""
      <div style="flex:1;text-align:center">
        <div style="background:{P['branco']};border-radius:28px;padding:22px 16px 26px">
          <img src="{foto(o['foto'])}" style="height:300px;width:auto;max-width:330px;
               filter:drop-shadow(0 14px 22px rgba(28,53,39,.14))">
          <div class="pill display" style="background:{cor};color:{P['branco']};margin-top:10px;font-size:30px">{o['letra']}</div>
          <div style="font-weight:700;font-size:32px;color:{P['verde']};margin-top:12px">{o['nome']}</div>
          <div class="giz" style="font-size:28px;color:{P['dourado_escuro']};margin-top:4px">{o['perfil']}</div>
        </div>
      </div>""" for o, cor in zip(s["opcoes"], (P["verde"], P["coral"])))
    return f"""
<div class="slide" style="background:{P['creme_claro']}">
  <div style="padding:52px 52px 0;display:flex;align-items:center;justify-content:space-between">
    <span style="font-weight:700;font-size:24px;letter-spacing:.2em;text-transform:uppercase;color:#9AA396">{s.get('rotulo','Qual bowlover é você?')}</span>
    <img src="{logo('verde')}" style="height:54px">
  </div>
  <div class="palco" style="justify-content:center;padding:20px 46px 0">
    <div class="display" style="font-size:64px;color:{P['verde']};line-height:1.02">{s['pergunta']}</div>
    <div style="display:flex;gap:18px;width:100%;margin-top:34px">{opcoes}</div>
    <div class="giz" style="font-size:38px;color:{P['verde']};margin-top:30px">{s['giz']}</div>
  </div>
  {mosaico()}
  <div class="rodape" style="padding:22px 52px 38px"><span>@bowlgreenxerem</span>
    <span style="color:{P['coral']}">comenta A ou B 👇</span></div>
</div>"""


# Fundos de story — o feed até pode repetir, o story não pode.
FUNDOS_STORY = {
    "coral":  (P["coral"],        P["branco"],  P["creme"],   P["coral"],        "branco"),
    "creme":  (P["creme"],        P["verde"],   P["verde"],   P["creme"],        "verde"),
    "verde":  (P["verde"],        P["creme"],   P["dourado"], P["verde_escuro"], "dourado"),
    "menta":  (P["menta_claro"],  P["verde"],   P["coral"],   P["branco"],       "verde"),
    "escuro": (P["verde_escuro"], P["creme"],   P["dourado"], P["verde_escuro"], "dourado"),
}


def slide_story(s):
    fundo, tinta, pill_bg, pill_tinta, var_logo = FUNDOS_STORY[s.get("fundo", "coral")]
    halo = "rgba(255,255,255,.16)" if s.get("fundo", "coral") in ("coral", "verde", "escuro") else "rgba(36,87,58,.07)"
    enquete = ""
    if s.get("enquete"):
        opts = "".join(
            f'<div style="flex:1;background:{P["branco"]};border-radius:18px;padding:18px 10px;'
            f'font-weight:800;font-size:34px;color:{P["verde_escuro"]};text-align:center">{o}</div>'
            for o in s["enquete"]["opcoes"])
        enquete = f"""
    <div style="background:rgba(255,255,255,.92);border-radius:26px;padding:26px 24px;margin:0 0 30px">
      <div style="font-weight:800;font-size:36px;color:{P['verde_escuro']};text-align:center;margin-bottom:18px">{s['enquete']['pergunta']}</div>
      <div style="display:flex;gap:14px">{opts}</div>
    </div>"""

    prato = "" if not s.get("foto") else f"""
    <div style="position:absolute;width:820px;height:820px;border-radius:50%;background:{halo}"></div>
    <img src="{foto(s['foto'])}" style="width:760px;position:relative;z-index:2;
         filter:drop-shadow(0 30px 46px rgba(28,53,39,.28))">"""

    return f"""
<div class="slide" style="background:{fundo};height:1920px">
  <div style="padding:84px 70px 0;text-align:center">
    <img src="{logo(var_logo)}" style="height:74px">
    <div class="giz" style="font-size:44px;color:{tinta};opacity:.9;margin-top:24px">{s['sobretitulo']}</div>
    <div class="display" style="font-size:100px;color:{tinta};margin-top:10px">{s['nome']}</div>
  </div>
  <div style="flex:1;display:flex;align-items:center;justify-content:center;position:relative">{prato}</div>
  <div style="padding:0 70px 92px;text-align:center">
    {enquete}
    <span class="pill" style="background:{pill_bg};color:{pill_tinta};font-size:36px;padding:22px 52px">{s['botao']}</span>
    <div class="giz" style="font-size:38px;color:{tinta};margin-top:26px;opacity:.9">{s['giz']}</div>
  </div>
</div>"""


TIPOS = {"produto": slide_produto, "raio-x": slide_raiox,
         "comparativo": slide_comparativo, "trio": slide_trio,
         "confissao": slide_confissao, "quiz": slide_quiz, "story": slide_story}
TAMANHOS = {"story": (1080, 1920)}


def pagina(slide):
    construtor = TIPOS.get(slide.get("tipo"))
    if not construtor:
        raise ValueError(f"tipo desconhecido: {slide.get('tipo')} — use {list(TIPOS)}")
    L, A = TAMANHOS.get(slide["tipo"], (1080, 1350))
    css = (CSS.replace("__L__", str(L)).replace("__A__", str(A))
           .replace("__CREME__", P["creme"]).replace("__VERDE__", P["verde"])
           .replace("__MENTA_CL__", P["menta_claro"]))
    return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>"
            f"<style>{fontes()}{css}</style></head><body>{construtor(slide)}</body></html>")


def main():
    if len(sys.argv) < 3:
        print("Uso: python gerar_posts.py <config.json> <pasta_saida>", file=sys.stderr)
        sys.exit(1)
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2]); saida.mkdir(parents=True, exist_ok=True)
    posts = config["posts"]

    with sync_playwright() as p:
        nav = p.chromium.launch()
        for i, post in enumerate(posts, 1):
            L, A = TAMANHOS.get(post["tipo"], (1080, 1350))
            pg = nav.new_page(viewport={"width": L, "height": A}, device_scale_factor=1)
            pg.set_content(pagina(post), wait_until="load")
            pg.wait_for_timeout(420)
            destino = saida / f"slide-{i:02d}.png"
            pg.screenshot(path=str(destino))
            pg.close()
            print(f"  [{i}/{len(posts)}] {destino.name}  ({post['tipo']}, {L}x{A})")
        nav.close()
    print(f"\nPronto — {len(posts)} peças em {saida}/")


if __name__ == "__main__":
    main()
