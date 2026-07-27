#!/usr/bin/env python3
"""
Componentes do Design System em formato de post — Bowl Green.

Cada tipo aqui reproduz UM componente que já existe em
"BOWL GREEN/Bowl Green — Design System.html", ampliado para 1080x1350 (feed)
ou 1080x1920 (story). Nenhum layout foi inventado: as coordenadas do DS foram
reescaladas, não redesenhadas.

  capa-reel        → capa de Reel: foto sangrando + palavra gigante na frente
  escala-sabor     → DS "ESCALA DE SABOR" (régua de 5 pontos)
  semana-premium   → DS "UM PRA CADA HORA DO DIA" + "CARD PRODUTO PREMIUM"
  urgencia         → DS "CONTAGEM REGRESSIVA" + "TERMÔMETRO DE UNIDADES"
  torneio          → DS "TORNEIO DOS SABORES" (chaveamento)
  responde         → DS "FAQ — BOWL GREEN RESPONDE" (balões)
  story-urgencia   → urgência em 9:16
  story-escala     → escala de sabor em 9:16 com enquete

Regra de preço da casa: nenhum post de feed leva preço. Story só quando pedido.

Uso:
    python gerar_componentes.py <config.json> <pasta_saida>
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

_spec2 = importlib.util.spec_from_file_location("gp", Path(__file__).with_name("gerar_peças.py"))
gp = importlib.util.module_from_spec(_spec2); _spec2.loader.exec_module(gp)
estampa, arcos, mosaico, selo = gp.estampa, gp.arcos, gp.mosaico, gp.selo

RAIZ_FOTOS = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN/Fotos")
# reels/ primeiro: fotos que a Gê manda para virar capa têm precedência sobre
# qualquer homônimo de estúdio.
PASTAS = [RAIZ_FOTOS / "reels", RAIZ_FOTOS / "geradas", RAIZ_FOTOS / "recortados",
          RAIZ_FOTOS / "pratos"]


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


def posicionar(html, css_extra):
    """Injeta posicionamento num elemento que já veio pronto do gerar_peças.

    Os helpers de marca devolvem o elemento com style próprio; em vez de refazer
    a função, prefixamos o style. Prefixar (e não sufixar) mantém o que o helper
    definiu vencendo em caso de conflito — foi assim que a estampa parou de
    perder o background-size."""
    i = html.index('style="')
    return html[:i + 7] + css_extra + ";" + html[i + 7:]


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
.mosaico{display:flex;width:100%}
.mosaico i{flex:1}

.cobre{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.chip{border-radius:999px;padding:14px 28px;font-weight:800;font-size:30px;display:inline-block}
.pill{display:inline-block;border-radius:999px;font-family:'Luckiest Guy',cursive;
      letter-spacing:.04em;text-transform:uppercase;line-height:1}
.barra{height:26px;border-radius:14px;background:rgba(255,255,255,.35);overflow:hidden}
.barra i{display:block;height:100%;border-radius:14px}
.rodape{position:absolute;left:0;right:0;bottom:0;z-index:7;display:flex;align-items:center;
        justify-content:space-between;padding:0 56px 44px;font-weight:800;font-size:30px}
"""


def rodape(cor=None, botao="Link da bio", fundo=None, texto_botao=None, sombra=False):
    cor = cor or P["verde"]
    fundo = fundo or P["dourado"]
    texto_botao = texto_botao or P["verde_escuro"]
    som = "text-shadow:0 2px 12px rgba(28,53,39,.7)" if sombra else ""
    return (f'<div class="rodape" style="color:{cor}"><span style="{som}">@bowlgreenxerem</span>'
            f'<span class="pill" style="background:{fundo};color:{texto_botao};font-size:29px;'
            f'padding:16px 32px">{botao}</span></div>')


# ─── CAPA DE REEL (1080x1920) ───────────────────────────────────────────────

def t_capa_reel(s):
    """Foto sangrando os quatro lados, palavra gigante na frente. Nada de bloco
    chapado: a peça é a foto + o texto.

    A altura útil é menor do que parece. O Instagram cobre o topo com o nome do
    perfil e o rodapé com legenda, áudio e botões — por isso o texto vive entre
    620 e 1440px, que é também o recorte 1:1 que aparece na grade do feed."""
    veu = s.get("veu", .55)
    # Texto ancorado no rodapé, não no meio. Centralizado ele cobria exatamente o
    # bowl — que é o motivo de a pessoa parar o dedo. O véu escurece de baixo pra
    # cima; a comida fica na parte clara e a palavra na parte escura.
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 42%')}">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,
       rgba(28,53,39,.55) 0%,rgba(28,53,39,.06) 20%,rgba(28,53,39,.06) 44%,
       rgba(28,53,39,{veu}) 62%,rgba(28,53,39,.95) 82%)"></div>
  <img src="{logo('branco')}" style="position:absolute;top:150px;left:60px;width:236px;z-index:4">
  <div style="position:absolute;left:0;right:0;bottom:290px;z-index:4;padding:0 62px">
    <span class="chip" style="background:{P['coral']};color:#fff;font-size:34px">{s.get('rotulo','')}</span>
    <div class="display" style="font-size:{s.get('tam',150)}px;color:#fff;margin-top:26px;
         text-shadow:0 10px 34px rgba(28,53,39,.6)">{s['manchete']}</div>
    <div class="giz" style="font-size:52px;color:{P['menta']};margin-top:22px">{s.get('giz','')}</div>
    <div style="margin-top:32px">
      <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:40px;
            padding:24px 48px">{s.get('botao','Assiste até o fim ▸')}</span>
    </div>
  </div>
  {posicionar(mosaico(22), 'position:absolute;left:0;bottom:230px;z-index:3')}
</div>"""


# ─── ESCALA DE SABOR ────────────────────────────────────────────────────────

NIVEIS = ["LEVE", "REFRESCANTE", "AGRIDOCE", "CREMOSO", "INTENSO"]


def _regua(ativo, cor_trilho, cor_texto, cor_apagado, largura_texto=17):
    """Os 5 pontos da régua do DS. O ativo é maior, coral e com sombra —
    é o único ponto que o olho precisa achar de relance."""
    pontos = []
    for i in range(5):
        if i == ativo:
            pontos.append(f'<div style="height:56px;display:flex;align-items:center;justify-content:center">'
                          f'<div style="width:56px;height:56px;border-radius:50%;background:{P["coral"]};'
                          f'border:9px solid #fff;box-shadow:0 12px 30px rgba(232,104,74,.5)"></div></div>')
        else:
            pontos.append(f'<div style="height:56px;display:flex;align-items:center;justify-content:center">'
                          f'<div style="width:30px;height:30px;border-radius:50%;background:#fff;'
                          f'border:7px solid {P["salvia"]}"></div></div>')
    rotulos = []
    for i, n in enumerate(NIVEIS):
        ativo_i = i == ativo
        rotulos.append(f'<div style="font-size:{largura_texto + (2 if ativo_i else 0)}px;'
                       f'font-weight:{900 if ativo_i else 700};letter-spacing:.1em;text-align:center;'
                       f'color:{cor_texto if ativo_i else cor_apagado}">{n}</div>')
    esq = 10 + ativo * ((1080 - 124 - 20) / 5) + ((1080 - 124 - 20) / 10)
    return f"""
  <div style="position:relative;margin:96px 6px 4px">
    <div class="giz" style="position:absolute;top:-72px;left:{esq:.0f}px;transform:translateX(-50%) rotate(-3deg);
         font-size:44px;color:{P['coral']};white-space:nowrap">mora aqui ↓</div>
    <div style="position:absolute;left:24px;right:24px;top:20px;height:18px;background:{cor_trilho};border-radius:10px"></div>
    <div style="position:relative;display:grid;grid-template-columns:repeat(5,1fr)">{''.join(pontos)}</div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);margin-top:22px">{''.join(rotulos)}</div>"""


def t_escala_sabor(s):
    """DS "ESCALA DE SABOR". Prato recortado no disco menta, nome em display
    gigante e a régua embaixo. O prato precisa vir de recortados/ — cru, o fundo
    branco de estúdio vira um quadrado sobre o creme."""
    ativo = NIVEIS.index(s["nivel"].upper())
    chips = "".join(f'<span class="chip" style="background:{P["menta_claro"]};color:{P["verde"]};'
                    f'font-size:28px">{c}</span>' for c in s.get("chips", []))
    # A coluna tem altura travada (1350 − mosaico − rodapé) e distribui os blocos
    # sozinha. Sem isso a peça saía com um vazio de 300px entre o giz e o rodapé:
    # o conteúdo se empilhava no topo e o resto ficava creme puro.
    return f"""
<div class="peca">
  {estampa(.12, .95)}
  <div style="position:relative;z-index:2;height:1190px;display:flex;flex-direction:column;
       justify-content:space-between;padding:60px 62px 0">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <img src="{logo('verde')}" style="width:196px">
      <div class="lbl" style="font-size:26px;color:{P['dourado_escuro']}">ESCALA DE SABOR</div>
    </div>
    <div style="display:flex;align-items:center;gap:28px">
      <div style="position:relative;width:420px;height:420px;flex-shrink:0">
        <div style="position:absolute;inset:0;border-radius:50%;background:{P['menta_claro']}"></div>
        <img src="{foto(s['prato'])}" style="position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);
             width:400px;filter:drop-shadow(0 22px 38px rgba(28,53,39,.24))">
      </div>
      <div style="flex:1;min-width:0">
        <div class="display" style="font-size:{s.get('tam',118)}px;color:{P['verde']}">{s['nome']}</div>
        <div style="font-size:32px;font-weight:500;color:{P['verde_escuro']};line-height:1.35;margin-top:16px">{s['linha']}</div>
      </div>
    </div>
    {_regua(ativo, P['creme_claro'], P['coral'], '#9A9585', 25)}
    <div style="display:flex;gap:12px;flex-wrap:wrap">{chips}</div>
    <div style="background:{P['verde']};border-radius:26px;padding:30px 34px;display:flex;
         align-items:center;justify-content:space-between;gap:22px;margin-bottom:6px">
      <div class="giz" style="font-size:46px;color:{P['menta']}">{s.get('giz','')}</div>
      <div class="lbl" style="font-size:21px;color:{P['salvia']};text-align:right;flex-shrink:0">28 PRATOS<br>NA RÉGUA</div>
    </div>
  </div>
  {posicionar(mosaico(20), 'position:absolute;left:0;bottom:120px;z-index:3')}
  {rodape(botao=s.get('botao','Todo prato tem o seu ponto'))}
</div>"""


def t_story_escala(s):
    """A mesma régua em 9:16, com a pergunta virando enquete. Story existe para
    a pessoa responder, não para ler."""
    ativo = NIVEIS.index(s["nivel"].upper())
    return f"""
<div class="peca" style="background:{P['verde_escuro']}">
  {estampa(.14, 1.1)}
  <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;
       justify-content:center;padding:0 62px">
    <img src="{logo('dourado')}" style="width:230px;margin-bottom:38px">
    <div class="lbl" style="font-size:28px;color:{P['salvia']}">ESCALA DE SABOR</div>
    <div class="display" style="font-size:{s.get('tam',150)}px;color:{P['creme']};margin-top:18px">{s['nome']}</div>
    <div style="width:520px;height:520px;margin:44px auto 0;position:relative">
      <div style="position:absolute;inset:0;border-radius:50%;background:{P['menta_claro']};opacity:.16"></div>
      <img src="{foto(s['prato'])}" style="position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);
           width:500px;filter:drop-shadow(0 26px 40px rgba(0,0,0,.42))">
    </div>
    {_regua(ativo, 'rgba(255,255,255,.18)', P['dourado'], '#7E9A85', 25)}
    <div class="giz" style="font-size:52px;color:{P['menta']};margin-top:56px;text-align:center">{s.get('giz','')}</div>
    <div style="text-align:center;margin-top:34px">
      <span class="pill" style="background:{P['coral']};color:#fff;font-size:42px;padding:26px 54px">{s.get('botao','Onde mora o seu? ↑')}</span>
    </div>
  </div>
  {posicionar(arcos(.8, 150), 'position:absolute;left:0;right:0;bottom:0;z-index:3')}
</div>"""


# ─── UM PRA CADA DIA · EDIÇÃO PREMIUM ───────────────────────────────────────

def t_semana_premium(s):
    """DS "UM PRA CADA HORA DO DIA" no tratamento do "CARD PRODUTO PREMIUM":
    fundo navy, ✦✦✦✦✦ dourado, filete tracejado entre os dias.

    Sete cards lado a lado não cabem em 1080 sem virar tipografia de bula — por
    isso a semana vira lista vertical. Cada linha é dia · emoji · prato."""
    linhas = []
    for i, d in enumerate(s["dias"]):
        hoje = d.get("hoje", False)
        fundo = f"background:{P['dourado']};box-shadow:0 12px 28px rgba(201,162,75,.34)" if hoje else "background:rgba(255,255,255,.045)"
        cor_dia = P["verde_escuro"] if hoje else P["dourado"]
        cor_nome = P["verde_escuro"] if hoje else P["creme"]
        cor_sub = "rgba(28,53,39,.72)" if hoje else P["salvia"]
        # 16px de padding e 10 de gap não é aperto gratuito: sete linhas mais
        # gordas empurravam domingo e sábado por baixo do rodapé.
        linhas.append(f"""
      <div style="display:flex;align-items:center;gap:20px;padding:16px 24px;border-radius:18px;{fundo};
           margin-bottom:10px">
        <div class="display" style="font-size:36px;color:{cor_dia};width:104px;flex-shrink:0">{d['dia']}</div>
        <div style="font-size:40px;width:54px;flex-shrink:0;text-align:center">{d['emoji']}</div>
        <div style="flex:1;min-width:0">
          <div style="font-size:33px;font-weight:800;color:{cor_nome};line-height:1.1">{d['nome']}</div>
          <div style="font-size:23px;font-weight:500;color:{cor_sub};margin-top:4px">{d['sub']}</div>
        </div>
        {'<div class="lbl" style="font-size:19px;color:' + P['verde_escuro'] + '">hoje</div>' if hoje else ''}
      </div>""")
    return f"""
<div class="peca" style="background:{P['verde_escuro']}">
  {estampa(.10, .95)}
  <div style="position:relative;z-index:2;height:100%;display:flex;flex-direction:column;padding:58px 58px 0">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div class="lbl" style="font-size:25px;color:{P['salvia']}">EDIÇÃO PREMIUM</div>
      <div style="color:{P['dourado']};font-size:30px;letter-spacing:9px">✦✦✦✦✦</div>
    </div>
    <div class="display" style="font-size:{s.get('tam',112)}px;color:{P['creme']};margin-top:18px">{s.get('titulo','UM PRA<br>CADA DIA')}</div>
    <div class="giz" style="font-size:40px;color:{P['dourado']};margin:12px 0 26px">{s.get('giz','')}</div>
    <div style="flex:1">{''.join(linhas)}</div>
  </div>
  <img src="{logo('dourado')}" style="position:absolute;right:56px;top:132px;width:172px;z-index:4;opacity:.95">
  {posicionar(mosaico(20), 'position:absolute;left:0;bottom:118px;z-index:3')}
  {rodape(cor=P['creme'], botao=s.get('botao','Escolhe o teu dia'))}
</div>"""


# ─── PROMOÇÃO & URGÊNCIA ────────────────────────────────────────────────────

def t_urgencia(s):
    """DS "CONTAGEM REGRESSIVA" (coral chapado, numeral gigante) somado ao
    "TERMÔMETRO DE UNIDADES". Urgência só funciona com número real na cara —
    o número é o assunto, o texto é a nota de rodapé."""
    pct = int(s.get("pct", 70))
    # O prato entra como peso de canto, não como assunto: acima de ~580px ele
    # sobe na barra do termômetro e come o giz de "corre!".
    prato = (f'<img src="{foto(s["prato"])}" style="position:absolute;right:-110px;top:520px;width:560px;'
             f'z-index:3;filter:drop-shadow(0 26px 44px rgba(120,40,22,.42))">') if s.get("prato") else ""
    # 1190px = 1350 − mosaico (118) − folga. A primeira versão usava height:100%
    # com margin-top:auto na barra: ela ia para 1306 e passava POR BAIXO do rodapé,
    # que é position:absolute e não empurra nada.
    return f"""
<div class="peca" style="background:{P['coral']}">
  {estampa(.09, 1.0)}
  {prato}
  <div style="position:relative;z-index:4;height:1190px;display:flex;flex-direction:column;
       justify-content:space-between;padding:58px 58px 0">
    <div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <img src="{logo('branco')}" style="width:200px">
        <span class="chip" style="background:rgba(255,255,255,.22);color:#fff;font-size:26px">{s.get('rotulo','acabando')}</span>
      </div>
      <div class="lbl" style="font-size:27px;color:{P['rosa']};margin-top:44px">{s.get('acima','CONTAGEM REGRESSIVA')}</div>
      <div style="display:flex;align-items:center;gap:30px;margin-top:6px">
        <div class="display" style="font-size:270px;color:#fff;line-height:.8;
             text-shadow:0 12px 0 rgba(177,74,47,.55)">{s['numero']}</div>
        <div class="display" style="font-size:{s.get('tam',86)}px;color:#fff;flex:1">{s['manchete']}</div>
      </div>
      <div style="font-size:34px;font-weight:500;color:{P['rosa']};line-height:1.4;margin-top:26px;
           max-width:{s.get('texto_largura',620)}px">{s.get('texto','')}</div>
    </div>
    <div style="margin-bottom:26px">
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px">
        <span style="font-size:30px;font-weight:800;color:#fff">{s.get('barra_rotulo','')}</span>
        <span class="giz" style="font-size:42px;color:{P['amarelo']}">{s.get('barra_giz','')}</span>
      </div>
      <div class="barra"><i style="width:{pct}%;background:linear-gradient(90deg,{P['amarelo']} 0%,{P['dourado']} 60%,#fff 100%)"></i></div>
      <div style="display:flex;justify-content:space-between;margin-top:12px;font-size:24px;
           font-weight:500;color:{P['rosa']}">
        <span>{s.get('barra_esq','')}</span><span>{s.get('barra_dir','')}</span>
      </div>
    </div>
  </div>
  {posicionar(selo(s.get('selo_topo','ENQUANTO DURA'), '✦ BOWL GREEN ✦', s.get('selo_emoji','🔥'),
        s.get('selo_pe','HOJE'), 196, -12), 'left:56px;top:700px')}
  {posicionar(mosaico(20), 'position:absolute;left:0;bottom:118px;z-index:5')}
  {rodape(cor='#fff', botao=s.get('botao','Peça no WhatsApp'), fundo=P['dourado'])}
</div>"""


def t_story_urgencia(s):
    """A mesma urgência sobre foto, em 9:16. Aqui a foto entra porque story de
    promoção sem o prato na tela não converte — a pessoa precisa ver o que
    está acabando."""
    pct = int(s.get("pct", 70))
    return f"""
<div class="peca">
  <img class="cobre" src="{foto(s['foto'])}" style="object-position:{s.get('foco','50% 44%')}">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,
       rgba(232,104,74,.72) 0%,rgba(232,104,74,.30) 34%,rgba(28,53,39,.55) 62%,rgba(28,53,39,.95) 90%)"></div>
  <img src="{logo('branco')}" style="position:absolute;top:150px;left:60px;width:230px;z-index:4">
  <div style="position:absolute;left:0;right:0;top:300px;z-index:4;padding:0 62px">
    <span class="chip" style="background:{P['coral']};color:#fff;font-size:32px">{s.get('rotulo','acabando hoje')}</span>
    <div style="display:flex;align-items:center;gap:26px;margin-top:22px">
      <div class="display" style="font-size:300px;color:#fff;line-height:.78;
           text-shadow:0 14px 0 rgba(177,74,47,.5)">{s['numero']}</div>
      <div class="display" style="font-size:{s.get('tam',80)}px;color:#fff;flex:1">{s['manchete']}</div>
    </div>
  </div>
  <div style="position:absolute;left:62px;right:62px;bottom:330px;z-index:4">
    <div style="font-size:36px;font-weight:500;color:{P['rosa']};line-height:1.4;margin-bottom:30px">{s.get('texto','')}</div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px">
      <span style="font-size:32px;font-weight:800;color:#fff">{s.get('barra_rotulo','')}</span>
      <span class="giz" style="font-size:44px;color:{P['amarelo']}">{s.get('barra_giz','')}</span>
    </div>
    <div class="barra" style="height:30px"><i style="width:{pct}%;background:linear-gradient(90deg,{P['amarelo']} 0%,{P['dourado']} 60%,#fff 100%)"></i></div>
    <div style="text-align:center;margin-top:44px">
      <span class="pill" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:44px;padding:28px 58px">{s.get('botao','Peça agora ↑')}</span>
    </div>
  </div>
  {posicionar(mosaico(22), 'position:absolute;left:0;bottom:250px;z-index:3')}
</div>"""


# ─── TORNEIO DOS SABORES ────────────────────────────────────────────────────

def t_torneio(s):
    """DS "TORNEIO DOS SABORES" — chaveamento em três colunas: semifinais,
    final, campeão em card dourado com coroa.

    O peso é todo do campeão. As colunas anteriores existem para provar que a
    disputa foi real: sem elas o post é só "esse é o melhor", e ninguém acredita."""
    def chave(par):
        blocos = []
        for nome, venceu in par:
            fundo = P["verde"] if venceu else P["salvia"]
            cor = P["creme"] if venceu else "#6E7A6E"
            blocos.append(f'<div class="display" style="font-size:30px;text-align:center;padding:20px 8px;'
                          f'border-radius:14px;background:{fundo};color:{cor}">{nome}</div>')
        return (f'<div style="background:{P["creme_claro"]};border-radius:18px;padding:10px;display:flex;'
                f'flex-direction:column;gap:9px">{"".join(blocos)}</div>')

    semis = "".join(chave(p) for p in s["semis"])
    final = chave([(s["final"][0], True), (s["final"][1], False)])
    return f"""
<div class="peca">
  {estampa(.12, .95)}
  <div style="position:relative;z-index:2;height:1190px;display:flex;flex-direction:column;
       justify-content:space-between;padding:60px 56px 0">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <img src="{logo('verde')}" style="width:192px">
      <span class="chip" style="background:{P['menta_claro']};color:{P['verde']};font-size:25px">{s.get('rotulo','você decidiu nos stories 📲')}</span>
    </div>
    <div>
      <div class="lbl" style="font-size:26px;color:{P['dourado_escuro']}">TORNEIO DOS SABORES</div>
      <div class="display" style="font-size:{s.get('tam',120)}px;color:{P['verde']};margin-top:12px">{s.get('titulo','QUEM LEVA<br>A COROA?')}</div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1.15fr;gap:22px;align-items:center">
      <div>
        <div class="lbl" style="font-size:21px;color:#8C8878;margin-bottom:14px">SEMIFINAIS</div>
        <div style="display:flex;flex-direction:column;gap:18px">{semis}</div>
      </div>
      <div>
        <div class="lbl" style="font-size:21px;color:#8C8878;margin-bottom:14px">FINAL</div>
        {final}
      </div>
      <div>
        <div class="lbl" style="font-size:21px;color:#8C8878;margin-bottom:14px">CAMPEÃO</div>
        <div style="background:{P['dourado']};border-radius:24px;padding:30px 18px;text-align:center;
             box-shadow:0 16px 34px rgba(201,162,75,.42)">
          <div style="font-size:58px;line-height:1">👑</div>
          <div class="display" style="font-size:52px;color:#fff;margin-top:10px">{s['campeao']}</div>
          <div class="giz" style="font-size:32px;color:{P['amarelo']};margin-top:10px">{s.get('campeao_giz','')}</div>
        </div>
      </div>
    </div>
    <div style="background:{P['verde']};border-radius:26px;padding:30px 36px;text-align:center;margin-bottom:6px">
      <div style="font-size:31px;font-weight:500;color:{P['creme']};line-height:1.4">{s.get('texto','')}</div>
      <div class="giz" style="font-size:44px;color:{P['menta']};margin-top:14px">{s.get('giz','')}</div>
    </div>
  </div>
  {posicionar(mosaico(20), 'position:absolute;left:0;bottom:118px;z-index:3')}
  {rodape(botao=s.get('botao','Próxima chave nos stories'))}
</div>"""


# ─── BOWL GREEN RESPONDE ────────────────────────────────────────────────────

def t_responde(s):
    """DS "FAQ — BOWL GREEN RESPONDE": balão de pergunta manuscrito à esquerda,
    balão verde de resposta à direita, chip de WhatsApp no pé.

    A pergunta vai em giz porque é fala de cliente; a resposta em Lufga porque é
    a casa falando. Trocar as vozes desmonta o componente."""
    # Três pares de balões em 1350px só fecham com esta escala: pergunta 40 /
    # resposta 27. Com 46/30 o terceiro par saía por baixo do rodapé — e o
    # terceiro é justamente a dor mais forte, a que não pode faltar.
    pares = []
    for q in s["perguntas"]:
        pares.append(f"""
      <div style="display:flex;align-items:flex-end;gap:14px;margin-bottom:12px">
        <div style="width:66px;height:66px;border-radius:50%;background:{P['creme_claro']};display:flex;
             align-items:center;justify-content:center;font-size:30px;flex-shrink:0">🙋</div>
        <div style="background:{P['creme_claro']};border-radius:26px 26px 26px 8px;padding:18px 26px;max-width:78%">
          <div class="giz" style="font-size:40px;color:{P['verde_escuro']};line-height:1.26">“{q['pergunta']}”</div>
        </div>
      </div>
      <div style="display:flex;align-items:flex-end;gap:14px;justify-content:flex-end;margin-bottom:26px">
        <div style="background:{P['verde']};border-radius:26px 26px 8px 26px;padding:18px 26px;max-width:80%">
          <div style="font-weight:700;font-size:27px;line-height:1.42;color:#fff">{q['resposta']}</div>
        </div>
        <div style="width:66px;height:66px;border-radius:50%;background:{P['menta_claro']};display:flex;
             align-items:center;justify-content:center;font-size:30px;flex-shrink:0">{q.get('emoji','🥗')}</div>
      </div>""")
    return f"""
<div class="peca">
  {estampa(.11, .95)}
  <div style="position:relative;z-index:2;height:1190px;display:flex;flex-direction:column;
       justify-content:space-between;padding:56px 56px 0">
    <div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <img src="{logo('verde')}" style="width:192px">
        <div class="lbl" style="font-size:25px;color:{P['dourado_escuro']}">BOWL GREEN RESPONDE</div>
      </div>
      <div class="display" style="font-size:{s.get('tam',96)}px;color:{P['verde']};margin-top:22px">{s.get('titulo','')}</div>
    </div>
    <div>{''.join(pares)}</div>
    <div style="margin-bottom:22px;text-align:center">
      <span class="chip" style="background:{P['dourado']};color:{P['verde_escuro']};font-size:30px">{s.get('chip','manda a sua no WhatsApp 💬')}</span>
    </div>
  </div>
  {posicionar(mosaico(20), 'position:absolute;left:0;bottom:118px;z-index:3')}
  {rodape(botao=s.get('botao','Link da bio'))}
</div>"""


TIPOS = {"capa-reel": t_capa_reel, "escala-sabor": t_escala_sabor,
         "story-escala": t_story_escala, "semana-premium": t_semana_premium,
         "urgencia": t_urgencia, "story-urgencia": t_story_urgencia,
         "torneio": t_torneio, "responde": t_responde}

NOVE_DEZESSEIS = {"capa-reel", "story-escala", "story-urgencia"}


def render(s, css_fontes):
    largura = 1080
    altura = 1920 if s["tipo"] in NOVE_DEZESSEIS else 1350
    css = (CSS.replace("__L__", str(largura)).replace("__A__", str(altura))
              .replace("__CREME__", P["creme"]))
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{css_fontes}{css}</style>"
            f"</head><body>{TIPOS[s['tipo']](s)}</body></html>", largura, altura)


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
