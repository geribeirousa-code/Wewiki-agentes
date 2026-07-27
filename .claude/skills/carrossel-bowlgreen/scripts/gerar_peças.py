#!/usr/bin/env python3
"""
Peças de feed e story — Bowl Green, tipografia grande e layout variado.

Por que este arquivo existe separado de gerar_posts.py: as peças de lá saíram
todas com o mesmo esqueleto (faixa verde no topo, prato no disco, nome, chips)
e display de 76px. De longe, no feed, viravam a mesma peça repetida e o texto
não se lia na miniatura.

As regras aqui:
  · Display nunca abaixo de 120px. Manchete vive entre 150 e 190. Numeral, 300+.
  · Cada tipo tem esqueleto próprio. Dois tipos não podem ter a mesma silhueta.
  · Todo tipo carrega pelo menos um elemento de marca do Design System —
    estampa em marca d'água, faixa mosaico, tile de arcos ou selo dourado.
  · A foto de pessoa é protagonista. Prato em fundo branco é apoio, não capa.

Tipos de feed (1080x1350): manchete · numerao · polaroid · faixa-lateral · duo
Tipos de story (1080x1920): story-manchete · story-enquete · story-selo

Uso:
    python gerar_peças.py <config.json> <pasta_saida>
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
# geradas/ primeiro: é onde vivem as fotos de pessoa, que têm precedência de capa.
PASTAS = [RAIZ_FOTOS / "geradas", RAIZ_FOTOS / "recortados", RAIZ_FOTOS / "pratos"]


def foto(nome):
    alvo = nome.strip().lower()
    for pasta in PASTAS:
        if not pasta.is_dir():
            continue
        for p in sorted(pasta.iterdir()):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.stem.lower() == alvo:
                mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
                return "data:" + mime + ";base64," + base64.b64encode(p.read_bytes()).decode("ascii")
    disp = ", ".join(sorted({x.stem for pa in PASTAS if pa.is_dir() for x in pa.iterdir() if x.is_file()}))
    raise SystemExit(f"ERRO: foto '{nome}' não encontrada.\nDisponíveis: {disp}")


# ─── Elementos de marca (Design System, seção "Estampa e motivos") ───────────

def mosaico(altura=18):
    faixas = "".join(f'<i style="background:{c}"></i>' for c in MOSAICO)
    return f'<div class="mosaico" style="height:{altura}px">{faixas}</div>'


def estampa(opacidade=.13, escala=1.0):
    """Marca d'água: a estampa densa de ingredientes, chapada e repetida.

    Fica atrás de tudo. Opacidade acima de ~.18 começa a brigar com o texto —
    já aconteceu de a manchete sumir dentro do padrão."""
    v, ve, co, dou, mc = P["verde"], P["verde_escuro"], P["coral"], P["dourado"], P["menta_claro"]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 300" width="{380*escala:.0f}">
  <g transform="translate(62,64)">
    <path d="M-34 0 a34 34 0 0 0 68 0 Z" fill="{v}"/>
    <rect x="-12" y="36" width="24" height="7" rx="3.5" fill="{v}"/>
    <path d="M-12 -12 q-7 -10 1 -20" fill="none" stroke="{v}" stroke-width="5" stroke-linecap="round"/>
    <path d="M12 -12 q7 -10 -1 -20" fill="none" stroke="{v}" stroke-width="5" stroke-linecap="round"/>
  </g>
  <g transform="translate(305,72)"><ellipse rx="26" ry="34" fill="{v}"/><ellipse rx="16" ry="23" fill="{mc}"/><circle r="9" cy="6" fill="{ve}"/></g>
  <g transform="translate(182,52) rotate(-15)">
    <path d="M-22 -8 a24 24 0 1 0 30 30 l-12 -4 a12 12 0 1 1 -14 -14 Z" fill="{co}"/>
    <path d="M8 22 l16 10 l-4 -16 Z" fill="{co}"/>
  </g>
  <g transform="translate(90,208) rotate(-14)"><ellipse rx="27" ry="38" fill="{dou}"/><ellipse cx="20" cy="-36" rx="8" ry="14" transform="rotate(35)" fill="{v}"/></g>
  <g transform="translate(250,232)"><circle r="32" fill="{dou}"/><circle r="25" fill="{P['creme_claro']}"/>
    <g fill="{dou}"><path d="M0 0 L-8 -23 A24 24 0 0 1 8 -23 Z"/><path d="M0 0 L20 -13 A24 24 0 0 1 23 6 Z"/><path d="M0 0 L15 19 A24 24 0 0 1 -2 24 Z"/><path d="M0 0 L-21 10 A24 24 0 0 1 -23 -8 Z"/></g></g>
  <g transform="translate(338,190)"><path d="M-18 -30 L18 -30 L12 24 L-12 24 Z" fill="{co}"/><rect x="2" y="-46" width="6" height="24" rx="3" transform="rotate(16 5 -34)" fill="{ve}"/></g>
  <g transform="translate(40,140) rotate(20)"><path d="M0 26 C-16 8 -13 -12 0 -26 C13 -12 16 8 0 26 Z" fill="{v}"/></g>
  <g transform="translate(152,150) rotate(-30)"><path d="M0 22 C-13 7 -11 -10 0 -22 C11 -10 13 7 0 22 Z" fill="{v}"/></g>
  <g transform="translate(212,120)"><path d="M0 14 C-10 6 -13 -3 -8 -9 C-4 -13 2 -11 0 -6 C2 -11 8 -13 12 -9 C17 -3 10 6 0 14 Z" fill="{co}"/></g>
  <g transform="translate(352,36)"><path d="M0 12 C-9 5 -11 -3 -7 -8 C-3 -11 1 -9 0 -5 C1 -9 7 -11 10 -8 C14 -3 9 5 0 12 Z" fill="{co}"/></g>
  <g transform="translate(30,270)"><path d="M0 12 C-9 5 -11 -3 -7 -8 C-3 -11 1 -9 0 -5 C1 -9 7 -11 10 -8 C14 -3 9 5 0 12 Z" fill="{co}"/></g>
  <g fill="{dou}"><path d="M124 22 l3 9 9 3 -9 3 -3 9 -3 -9 -9 -3 9 -3 Z"/><path d="M348 262 l3 9 9 3 -9 3 -3 9 -3 -9 -9 -3 9 -3 Z"/></g>
  <g transform="translate(292,140)"><path d="M-24 10 L0 -10 L24 10 L24 0 L0 -20 L-24 0 Z" fill="{co}"/></g>
  <g transform="translate(118,104)"><path d="M-14 -26 L14 -26 L10 20 L-10 20 Z" fill="{mc}"/><path d="M-13 -26 L13 -26 L11 -6 L-11 -6 Z" fill="{co}"/></g>
</svg>"""
    b64 = base64.b64encode(svg.encode()).decode()
    return (f'<div class="estampa" style="opacity:{opacidade};'
            f'background-image:url(data:image/svg+xml;base64,{b64});'
            f'background-size:{380*escala:.0f}px {300*escala:.0f}px"></div>')


def arcos(opacidade=.5, altura=170):
    """Tile de arcos — bowls empilhados. Usado como rodapé/divisória cheia."""
    v, ve, co, dou, cl = P["verde"], P["verde_escuro"], P["coral"], P["dourado"], P["creme_claro"]
    def fila(y, cores):
        out = []
        for i, c in enumerate(cores):
            x = 10 + i * 60
            out.append(f'<path d="M{x} 96 L{x} 52 a25 25 0 0 1 50 0 L{x+50} 96 Z" fill="{c}"/>')
            out.append(f'<circle cx="{x+25}" cy="68" r="7" fill="{cl if c != cl else v}"/>')
        return f'<g transform="translate(0,{y})">' + "".join(out) + "</g>"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 96" width="360">'
           + fila(0, [co, ve, dou, v, co, dou]) + "</svg>")
    b64 = base64.b64encode(svg.encode()).decode()
    return (f'<div style="height:{altura}px;opacity:{opacidade};background-repeat:repeat-x;'
           f'background-position:bottom center;background-size:auto {altura}px;'
           f'background-image:url(data:image/svg+xml;base64,{b64})"></div>')


def selo(topo="LACRADO FRESQUINHO", base="✦ BOWL GREEN ✦", emoji="🥗",
         pe="FEITO HOJE", tamanho=250, giro=-9):
    """Selo dourado circular com texto em arco. É o carimbo da casa."""
    return f"""
<div class="selo" style="width:{tamanho}px;height:{tamanho}px;transform:rotate({giro}deg)">
  <svg viewBox="0 0 200 200" width="{tamanho}" height="{tamanho}" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="95" fill="none" stroke="{P['dourado']}" stroke-width="7" stroke-dasharray="2.5 6"/>
    <circle cx="100" cy="100" r="88" fill="{P['dourado']}"/>
    <circle cx="100" cy="100" r="80" fill="none" stroke="{P['amarelo']}" stroke-width="1.6" stroke-dasharray="4 5" opacity=".8"/>
    <defs><path id="st{tamanho}" d="M32,100 a68,68 0 0 1 136,0"/><path id="sb{tamanho}" d="M26,100 a74,74 0 0 0 148,0"/></defs>
    <text style="font-family:'Lufga';font-weight:700;font-size:13px;letter-spacing:.2em" fill="{P['amarelo']}"><textPath href="#st{tamanho}" startOffset="50%" text-anchor="middle">{topo}</textPath></text>
    <text style="font-family:'Lufga';font-weight:700;font-size:12px;letter-spacing:.3em" fill="{P['amarelo']}"><textPath href="#sb{tamanho}" startOffset="50%" text-anchor="middle">{base}</textPath></text>
    <circle cx="100" cy="100" r="47" fill="{P['amarelo']}"/>
    <text x="100" y="102" text-anchor="middle" style="font-size:30px">{emoji}</text>
    <text x="100" y="124" text-anchor="middle" style="font-family:'Lufga';font-weight:800;font-size:9.5px;letter-spacing:.18em" fill="{P['dourado_escuro']}">{pe}</text>
  </svg>
</div>"""


def marca_dagua(cor="branco", tamanho=118, opacidade=.42, pos="right:52px;bottom:150px"):
    """A logo chapada em opacidade baixa, canto da peça. Marca d'água literal."""
    return (f'<img class="agua" src="{logo(cor)}" style="{pos};width:{tamanho}px;'
            f'opacity:{opacidade}">')


# ─── CSS ────────────────────────────────────────────────────────────────────

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__L__px;height:__A__px;overflow:hidden}
body{font-family:'Lufga',sans-serif;-webkit-font-smoothing:antialiased;background:__CREME__}
.peca{position:relative;width:__L__px;height:__A__px;overflow:hidden;background:__CREME__}

.display{font-family:'Luckiest Guy',cursive;text-transform:uppercase;letter-spacing:.008em;
         font-weight:400;line-height:.92}
.giz{font-family:'Chalkiez',cursive;line-height:1.32}
.num{font-family:'Shantell Sans',cursive;font-weight:800;line-height:.86}
.lbl{font-weight:800;letter-spacing:.24em;text-transform:uppercase}

.estampa{position:absolute;inset:0;z-index:0;background-repeat:repeat}
.selo{position:absolute;z-index:6;filter:drop-shadow(0 14px 26px rgba(28,53,39,.28))}
.agua{position:absolute;z-index:5}
.mosaico{display:flex;width:100%}
.mosaico i{flex:1}

.cobre{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.chip{border-radius:999px;padding:14px 28px;font-weight:800;font-size:31px;display:inline-block}
.pill{display:inline-block;border-radius:999px;font-family:'Luckiest Guy',cursive;
      letter-spacing:.04em;text-transform:uppercase;line-height:1}
.rodape{position:absolute;left:0;right:0;bottom:0;z-index:7;display:flex;align-items:center;
        justify-content:space-between;padding:0 56px 44px;font-weight:800;font-size:30px}
"""


# ─── Tipos de FEED (1080x1350) ──────────────────────────────────────────────

def t_manchete(s):
    """Foto de pessoa sangrando a peça + bloco creme com manchete gigante.
    A silhueta é: imagem em cima, tarja embaixo. Selo dourado costurando as duas."""
    chips = "".join(f'<span class="chip" style="background:{P["menta_claro"]};color:{P["verde"]}">{c}</span>'
                    for c in s.get("chips", []))
    # 690px de foto deixa 660 de tarja. Manchete de 3 linhas + giz + chips + rodapé
    # cabem em 660 e não cabiam em 520 — a primeira versão jogava o giz por baixo
    # do rodapé e ninguém lia.
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="height:690px;object-position:{s.get('foco','50% 42%')}">
  <div style="position:absolute;top:0;left:0;right:0;height:690px;
       background:linear-gradient(180deg,rgba(28,53,39,.42) 0%,transparent 34%)"></div>
  <img src="{logo('branco')}" style="position:absolute;top:44px;left:56px;width:200px;z-index:4">
  {selo(s.get('selo_topo','LACRADO FRESQUINHO'), '✦ BOWL GREEN ✦', s.get('selo_emoji','🥗'),
        s.get('selo_pe','FEITO HOJE'), 236, -11).replace('class="selo"', 'class="selo" ').replace(
        'style="width:236px', 'style="right:54px;top:520px;width:236px')}
  <div style="position:absolute;top:690px;left:0;right:0;bottom:0;background:{P['creme']};overflow:hidden">
    {estampa(.10, .85)}
    <div style="position:relative;z-index:2;padding:46px 56px 0">
      <div class="display" style="font-size:{s.get('tam',116)}px;color:{P['verde']}">{s['manchete']}</div>
      <div class="giz" style="font-size:40px;color:{P['dourado_escuro']};margin-top:16px">{s.get('giz','')}</div>
      <div style="margin-top:22px;display:flex;gap:11px;flex-wrap:wrap">{chips}</div>
    </div>
  </div>
  {mosaico(20).replace('class="mosaico"', 'class="mosaico" ').replace('style="height:20px"', 'style="height:20px;position:absolute;top:690px;z-index:3"')}
  <div class="rodape" style="color:{P['verde']}">
    <span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:29px;padding:16px 32px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def t_numerao(s):
    """Split vertical: foto à esquerda, bloco verde à direita com o numeral
    gigante em dourado. O número é o assunto — 300px+, lê na miniatura."""
    return f"""
<div class="peca" style="display:flex">
  <div style="width:470px;height:100%;position:relative;overflow:hidden">
    <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','52% 50%')}">
  </div>
  <div style="flex:1;height:100%;background:{P['verde_escuro']};position:relative;overflow:hidden;
       display:flex;flex-direction:column;justify-content:center;padding:0 46px">
    {estampa(.09, .8)}
    <div style="position:relative;z-index:2">
      <div class="lbl" style="font-size:27px;color:{P['menta']};margin-bottom:10px">{s.get('acima','')}</div>
      <!-- 186px é o teto: sobram 518px de coluna e "200g" em Shantell 800 já ocupa
           ~470. Acima disso o número sai cortado na borda direita da peça. -->
      <div class="num" style="font-size:{s.get('tam',186)}px;color:{P['dourado']}">{s['numero']}</div>
      <div class="display" style="font-size:60px;color:{P['creme']};margin-top:18px">{s.get('abaixo','')}</div>
      <div style="width:96px;height:7px;background:{P['coral']};border-radius:4px;margin:28px 0"></div>
      <div class="giz" style="font-size:44px;color:{P['menta']}">{s.get('giz','')}</div>
    </div>
  </div>
  <img src="{logo('branco')}" style="position:absolute;right:46px;top:44px;width:176px;z-index:4;opacity:.9">
  {mosaico(20).replace('style="height:20px"', 'style="height:20px;position:absolute;left:0;bottom:0;z-index:5"')}
  <div style="position:absolute;left:34px;bottom:44px;z-index:6;color:{P['creme']};
       font-weight:800;font-size:28px;text-shadow:0 2px 12px rgba(28,53,39,.6)">@bowlgreenxerem</div>
</div>"""


def t_polaroid(s):
    """Fundo todo de estampa da marca, foto numa moldura branca torta e a frase
    em giz por cima. É a peça mais "mão", quebra a régua das outras."""
    return f"""
<div class="peca" style="background:{P['creme_claro']}">
  {estampa(.20, 1.05)}
  <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;
       align-items:center;justify-content:center;padding:0 58px">
    <div class="display" style="font-size:{s.get('tam',118)}px;color:{P['verde']};text-align:center;
         margin-bottom:34px">{s['manchete']}</div>
    <!-- largura fixa na moldura: sem ela a div encolhe/cresce conforme o texto e
         a legenda em giz sai por fora da polaroid, atravessando a peça. -->
    <div style="width:744px;background:#fff;padding:22px 22px 0;border-radius:10px;transform:rotate(-2.4deg);
         box-shadow:0 26px 54px rgba(28,53,39,.26)">
      <img src="{foto(s['foto'])}" style="display:block;width:700px;height:540px;object-fit:cover;
           object-position:{s.get('foco','50% 45%')};border-radius:4px">
      <div class="giz" style="font-size:38px;color:{P['verde_escuro']};padding:18px 8px 22px;text-align:center">{s.get('giz','')}</div>
    </div>
  </div>
  {selo(s.get('selo_topo','SEM CULPA NENHUMA'), '✦ BOWL GREEN ✦', s.get('selo_emoji','💚'),
        s.get('selo_pe','BOWLOVER'), 196, 12).replace('style="width:196px', 'style="right:40px;top:44px;width:196px')}
  {mosaico(20).replace('style="height:20px"', 'style="height:20px;position:absolute;left:0;bottom:112px;z-index:3"')}
  <div class="rodape" style="color:{P['verde']}">
    <span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['coral']};color:#fff;font-size:29px;padding:16px 32px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def t_faixa_lateral(s):
    """Foto sangra a peça inteira; faixa coral vertical à esquerda com o texto
    girado 90°. Nenhuma outra peça tem eixo vertical — é o contraste do feed."""
    itens = "".join(
        f'<div style="display:flex;align-items:baseline;gap:16px;margin-bottom:16px">'
        f'<span class="num" style="font-size:56px;color:{P["dourado"]}">{i["valor"]}</span>'
        f'<span style="font-weight:700;font-size:33px;color:{P["creme"]}">{i["rotulo"]}</span></div>'
        for i in s.get("itens", []))
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','58% 50%')}">
  <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(28,53,39,.95) 0%,rgba(28,53,39,.86) 42%,rgba(28,53,39,.3) 68%,transparent 82%)"></div>
  <div style="position:absolute;left:0;top:0;bottom:0;width:150px;background:{P['coral']};
       display:flex;align-items:center;justify-content:center;z-index:3">
    <div class="display" style="font-size:66px;color:#fff;transform:rotate(-90deg);white-space:nowrap">{s.get('lateral','Bowl Green')}</div>
  </div>
  <div style="position:absolute;left:150px;top:0;bottom:0;width:560px;z-index:4;
       display:flex;flex-direction:column;justify-content:center;padding:0 44px">
    <div class="display" style="font-size:{s.get('tam',124)}px;color:{P['creme']}">{s['manchete']}</div>
    <div style="width:100px;height:7px;background:{P['dourado']};border-radius:4px;margin:30px 0 28px"></div>
    {itens}
    <div class="giz" style="font-size:42px;color:{P['menta']};margin-top:14px">{s.get('giz','')}</div>
  </div>
  <img src="{logo('branco')}" style="position:absolute;right:52px;top:48px;width:190px;z-index:5">
  {arcos(.9, 150).replace('style="height:150px', 'style="position:absolute;left:0;right:0;bottom:0;z-index:2;height:150px')}
  <div class="rodape" style="color:#fff;padding-bottom:48px">
    <span style="text-shadow:0 2px 12px rgba(28,53,39,.7)">@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:29px;padding:16px 32px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


def t_duo(s):
    """Pessoa em cima, prato recortado embaixo em disco menta. Prova os dois
    lados na mesma peça: quem come e o que come."""
    chips = "".join(f'<span class="chip" style="background:{P["verde"]};color:{P["creme"]};font-size:28px">{c}</span>'
                    for c in s.get("chips", []))
    return f"""
<div class="peca" style="background:{P['creme']}">
  {estampa(.11, .9)}
  <div style="position:absolute;top:0;left:0;right:0;height:540px;overflow:hidden;z-index:2">
    <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 22%')}">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,53,39,.5) 0%,transparent 40%)"></div>
    <img src="{logo('branco')}" style="position:absolute;top:40px;left:52px;width:190px">
  </div>
  {mosaico(20).replace('style="height:20px"', 'style="height:20px;position:absolute;top:540px;left:0;z-index:4"')}
  <div style="position:absolute;top:566px;left:0;right:0;z-index:3;text-align:center;padding:0 54px">
    <div class="display" style="font-size:{s.get('tam',118)}px;color:{P['verde']}">{s['manchete']}</div>
    <div class="giz" style="font-size:42px;color:{P['dourado_escuro']};margin-top:12px">{s.get('giz','')}</div>
  </div>
  <!-- chips ACIMA do prato. Na primeira versão vinham por baixo e o prato,
       posicionado, passava por cima deles. -->
  <div style="position:absolute;left:56px;top:862px;right:56px;z-index:4;display:flex;gap:12px;
       flex-wrap:wrap;justify-content:center">{chips}</div>
  <div style="position:absolute;left:50%;top:940px;transform:translateX(-50%);width:392px;height:392px;
       border-radius:50%;background:{P['menta_claro']};z-index:2"></div>
  <img src="{foto(s['prato'])}" style="position:absolute;left:50%;top:952px;transform:translateX(-50%);
       height:300px;z-index:3;filter:drop-shadow(0 22px 36px rgba(28,53,39,.2))">
  <div class="rodape" style="color:{P['verde']}">
    <span>@bowlgreenxerem</span>
    <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:29px;padding:16px 32px">{s.get('botao','Link da bio')}</span>
  </div>
</div>"""


# ─── Tipos de STORY (1080x1920) ─────────────────────────────────────────────

def t_story_manchete(s):
    """Foto sangrando os 9:16, manchete gigante embaixo, CTA de dedo."""
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 40%')}">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,53,39,.55) 0%,transparent 26%,transparent 46%,rgba(28,53,39,.92) 78%)"></div>
  <img src="{logo('branco')}" style="position:absolute;top:150px;left:60px;width:230px;z-index:4">
  {selo(s.get('selo_topo','LACRADO FRESQUINHO'), '✦ BOWL GREEN ✦', s.get('selo_emoji','🥗'),
        s.get('selo_pe','FEITO HOJE'), 236, 10).replace('style="width:236px', 'style="right:56px;top:150px;width:236px')}
  <div style="position:absolute;left:0;right:0;bottom:0;z-index:4;padding:0 60px 250px">
    <span class="chip" style="background:{P['coral']};color:#fff;font-size:32px">{s.get('rotulo','agora no salão')}</span>
    <div class="display" style="font-size:{s.get('tam',146)}px;color:#fff;margin-top:26px">{s['manchete']}</div>
    <div class="giz" style="font-size:50px;color:{P['menta']};margin-top:20px">{s.get('giz','')}</div>
    <div style="margin-top:40px">
      <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:44px;padding:26px 56px">{s.get('botao','Peça agora ↑')}</span>
    </div>
  </div>
  {mosaico(22).replace('style="height:22px"', 'style="height:22px;position:absolute;left:0;bottom:190px;z-index:3"')}
</div>"""


def t_story_enquete(s):
    """Foto no topo, bloco creme embaixo com a pergunta grande e as duas
    opções em caixas. Story de interação, não de venda."""
    ops = "".join(
        f'<div style="flex:1;background:{c};border-radius:26px;padding:36px 20px;text-align:center">'
        f'<div class="display" style="font-size:62px;color:{t}">{o}</div></div>'
        for o, c, t in zip(s["opcoes"], [P["menta"], P["rosa"]], [P["verde_escuro"], P["coral"]]))
    return f"""
<div class="peca" style="background:{P['creme']}">
  <div style="position:absolute;top:0;left:0;right:0;height:940px;overflow:hidden">
    <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 42%')}">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,53,39,.5) 0%,transparent 30%)"></div>
    <img src="{logo('branco')}" style="position:absolute;top:150px;left:60px;width:220px">
  </div>
  {mosaico(22).replace('style="height:22px"', 'style="height:22px;position:absolute;top:940px;left:0;z-index:3"')}
  <div style="position:absolute;top:962px;left:0;right:0;bottom:0;overflow:hidden">
    {estampa(.13, .95)}
    <div style="position:relative;z-index:2;padding:66px 58px 0">
      <div class="lbl" style="font-size:28px;color:{P['dourado_escuro']}">{s.get('rotulo','enquete do dia')}</div>
      <div class="display" style="font-size:{s.get('tam',118)}px;color:{P['verde']};margin-top:20px">{s['pergunta']}</div>
      <div style="display:flex;gap:22px;margin-top:44px">{ops}</div>
      <div class="giz" style="font-size:46px;color:{P['dourado_escuro']};margin-top:38px;text-align:center">{s.get('giz','')}</div>
    </div>
  </div>
</div>"""


def t_story_selo(s):
    """Fundo verde escuro com estampa forte, foto num círculo, selo dourado
    gigante. É a peça de anúncio — a que mais parece carimbo."""
    return f"""
<div class="peca" style="background:{P['verde_escuro']}">
  {estampa(.16, 1.15)}
  <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;
       align-items:center;justify-content:center;padding:0 56px;text-align:center">
    <img src="{logo('dourado')}" style="width:250px;margin-bottom:44px">
    <div style="width:640px;height:640px;border-radius:50%;overflow:hidden;border:14px solid {P['dourado']};
         box-shadow:0 30px 60px rgba(0,0,0,.4)">
      <img src="{foto(s['foto'])}" style="width:100%;height:100%;object-fit:cover;object-position:{s.get('foco','50% 45%')}">
    </div>
    <div class="display" style="font-size:{s.get('tam',140)}px;color:{P['creme']};margin-top:48px">{s['manchete']}</div>
    <div class="giz" style="font-size:50px;color:{P['menta']};margin-top:20px">{s.get('giz','')}</div>
    <span class="pill" style="background:{P['coral']};color:#fff;font-size:44px;padding:26px 56px;margin-top:44px">{s.get('botao','Peça agora ↑')}</span>
  </div>
  {arcos(.85, 160).replace('style="height:160px', 'style="position:absolute;left:0;right:0;bottom:0;z-index:3;height:160px')}
</div>"""


TIPOS = {"manchete": t_manchete, "numerao": t_numerao, "polaroid": t_polaroid,
         "faixa-lateral": t_faixa_lateral, "duo": t_duo,
         "story-manchete": t_story_manchete, "story-enquete": t_story_enquete,
         "story-selo": t_story_selo}


def render(s, css_fontes):
    largura = 1080
    altura = 1920 if s["tipo"].startswith("story") else 1350
    css = (CSS.replace("__L__", str(largura)).replace("__A__", str(altura))
              .replace("__CREME__", P["creme"]))
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css_fontes}{css}</style></head><body>{TIPOS[s['tipo']](s)}</body></html>", largura, altura


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
            html, L, A = render(s, css_fontes)
            pg = nav.new_page(viewport={"width": L, "height": A}, device_scale_factor=1)
            pg.set_content(html)
            pg.wait_for_timeout(700)  # fontes base64 + SVG precisam assentar
            nome = s.get("arquivo") or f"{i:02d}-{s['tipo']}"
            pg.screenshot(path=str(saida / f"{nome}.png"))
            pg.close()
            print(f"OK  {nome}.png  ({L}x{A})")
        nav.close()


if __name__ == "__main__":
    main()
