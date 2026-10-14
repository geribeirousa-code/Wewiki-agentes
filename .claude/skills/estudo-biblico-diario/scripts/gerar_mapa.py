"""Gera o Mapa de Progresso da Bíblia: 1 folha Carta, frente e verso, para dobrar e
guardar dentro da Bíblia. Os capítulos já estudados (progresso.json) saem marcados.

Uso: python gerar_mapa.py [--pdf]
Saída: Bíblia/mapa-de-progresso.html (e .pdf)

Como dobrar: Carta (21,6 x 27,9 cm) ao meio, duas vezes → 10,8 x 14 cm. Cabe em qualquer Bíblia.
"""
import argparse
import math
from datetime import date

import biblia as B
from icones import icone, POR_BLOCO
from pdf import exportar_pdf

# Geometria (polegadas). Mudou aqui? Rode com --medir para checar se algum painel estoura.
PASSO = 0.19            # distância entre quadradinhos
CAIXA = 0.168          # lado do quadradinho
LARG_UTIL = 3.80       # largura útil do painel (4,25" − margens)
POR_LINHA = int(LARG_UTIL / PASSO + 1e-6)   # quadradinhos por linha = 20
ALT_ROTULO, ALT_GAP, ALT_BLOCO = 0.14, 0.06, 0.37
ESPACO_X = 0.12        # folga horizontal entre livros na mesma linha
LARG_LETRA = 0.056     # largura estimada de uma letra do rótulo (6,6pt negrito)
CAPACIDADE = 5.08      # altura útil por painel


def largura_livro(l):
    return max(l["caps"] * PASSO, len(l["nome"]) * LARG_LETRA + 0.1)


def alocar():
    """Simula o fluxo (livros pequenos dividem a linha) e distribui pelos painéis.

    Devolve uma lista de painéis; cada painel é uma lista de ('bloco', chave, continuacao)
    e ('livro', sigla). Não parte livro ao meio.
    """
    paineis, atual = [], []
    usado = 0.0            # altura já gasta no painel
    x = 0.0                # largura gasta na linha de livros pequenos
    alt_linha = 0.0        # altura da linha de livros pequenos em andamento
    bloco_atual = None
    bloco_no_painel = None

    def fechar_linha():
        nonlocal usado, x, alt_linha
        usado += alt_linha
        x, alt_linha = 0.0, 0.0

    def novo_painel():
        nonlocal atual, usado, x, alt_linha, bloco_no_painel
        paineis.append(atual)
        atual, usado, x, alt_linha, bloco_no_painel = [], 0.0, 0.0, 0.0, None

    for l in B.LIVROS:
        larg = largura_livro(l)
        largo = l["caps"] * PASSO > LARG_UTIL
        h1 = ALT_ROTULO + math.ceil(l["caps"] / POR_LINHA) * PASSO + ALT_GAP
        # precisa de cabeçalho de bloco neste painel?
        precisa_cab = bloco_no_painel != l["bloco"]
        cab = ALT_BLOCO if precisa_cab else 0.0
        if largo or x + larg + ESPACO_X > LARG_UTIL:
            fechar_linha()
        extra = h1 if (largo or x == 0) else 0.0
        if usado + alt_linha + cab + max(extra, h1 if x == 0 else 0) > CAPACIDADE:
            fechar_linha()
            novo_painel()
            precisa_cab, cab = True, ALT_BLOCO
        if precisa_cab:
            fechar_linha()
            atual.append(("bloco", l["bloco"], bloco_atual == l["bloco"]))
            usado += cab
            bloco_no_painel = l["bloco"]
        atual.append(("livro", l["sigla"]))
        if largo:
            usado += h1
        else:
            x += larg + ESPACO_X
            alt_linha = max(alt_linha, h1)
        bloco_atual = l["bloco"]
    fechar_linha()
    paineis.append(atual)
    return paineis


def caixas(l, lidos, cor):
    out = []
    for c in range(1, l["caps"] + 1):
        ok = c in lidos
        out.append(f'<i class="cap{" ok" if ok else ""}">{c}</i>')
    return "".join(out)


def html_livro(sigla, p):
    l = B.LIVRO[sigla]
    lidos = B.lidos_de(p, sigla)
    completo = len(lidos) == l["caps"]
    cor = B.BLOCO[l["bloco"]][2]
    forte = B.escurecer(cor, 0.25)
    estrela = " ★" if completo else ""
    largo = " largo" if l["caps"] * PASSO > LARG_UTIL else ""
    return (f'<div class="livro{largo}" style="--cor:{cor};--forte:{forte};--clara:{B.misturar(cor, .78)}">'
            f'<b class="rot">{l["nome"]}{estrela}</b><div class="caps">{caixas(l, lidos, cor)}</div></div>')


def html_bloco(chave, continuacao):
    _, nome, cor, _lema = B.BLOCO[chave]
    i1, i2 = POR_BLOCO[chave]
    forte = B.escurecer(cor, 0.35)
    cont = " (continuação)" if continuacao else ""
    return (f'<div class="bloco" style="background:{cor};color:{B.TINTA}">'
            f'{icone(i1, 26, "#fff", "#FFF3B0", B.TINTA)}<span>{nome}{cont}</span>'
            f'{icone(i2, 26, "#fff", "#FFF3B0", B.TINTA)}</div>')


def barra(frac, n=20, cor="#FF7EB6"):
    cheios = round(frac * n)
    return "".join(f'<i style="background:{cor if k < cheios else "#fff"}"></i>' for k in range(n))


def capa(p, plano):
    lidos, por_bloco = B.totais(p)
    ini = date.fromisoformat(p["inicio"])
    fim = date.fromisoformat(plano[-1]["data_prevista"])
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    legenda = []
    for chave, nome, cor, lema in B.BLOCOS:
        ds = [d for d in plano if d["bloco"] == chave]
        ok, tot = por_bloco[chave]
        selo = "★" if ok == tot else ""
        legenda.append(
            f'<tr><td><span class="bola" style="background:{cor}">{selo}</span></td>'
            f'<td><b>{nome}</b><small>{lema}</small></td>'
            f'<td class="num">dias {ds[0]["dia"]}–{ds[-1]["dia"]}</td>'
            f'<td class="num">{ok}/{tot}</td></tr>')
    return f"""
<div class="capa">
  <div class="topo-capa">{icone("sol", 46, "#FFD63A", "#FFD63A", "#FF7EB6", B.TINTA)}
    <div><h1>Minha Jornada<br>pela Bíblia</h1><p>66 livros · 1.189 capítulos</p></div>
    {icone("palmeira", 46, "#9FD68A", "#FFB3D1", "#C99A5B", B.TINTA)}</div>
  <div class="geral"><b>{lidos}</b> de 1.189 capítulos
    <div class="barra">{barra(lidos / B.TOTAL_CAPS)}</div>
    <small>cada quadradinho = 5% da Bíblia</small></div>
  <table class="leg">{"".join(legenda)}</table>
  <div class="datas">Comecei em <u>&nbsp;{ini.day:02d}/{meses[ini.month - 1]}/{ini.year}&nbsp;</u> ·
     meta: <u>&nbsp;{meses[fim.month - 1]}/{fim.year}&nbsp;</u></div>
  <ol class="como">
    <li>Termine o estudo do dia → <b>pinte os capítulos</b> que leu.</li>
    <li>Fechou um livro? Escreva a data e ganhe a ★.</li>
    <li>Fechou um bloco? <b>Carimbe o selo</b> abaixo!</li>
  </ol>
  <div class="selos">{"".join(f'<span style="--cor:{b[2]}">{"★" if por_bloco[b[0]][0] == por_bloco[b[0]][1] else ""}</span>' for b in B.BLOCOS)}</div>
</div>"""


def painel_notas(altura_rest):
    return (f'<div class="notas"><b>Versículos que marquei ♥</b>'
            + "".join('<div class="linha"></div>' for _ in range(max(3, int(altura_rest / 0.26)))) + '</div>')


CSS = """
@page { size: 8.5in 11in; margin: 0 }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact }
html, body { margin: 0; background: #FFFDF8 }
body { font-family: 'Nunito','Quicksand','Trebuchet MS','Segoe UI',Verdana,sans-serif; color: %(tinta)s }
.folha { width: 8.5in; height: 11in; display: grid; grid-template: 5.5in 5.5in / 4.25in 4.25in;
  position: relative; page-break-after: always; overflow: hidden; background: #FFFDF8 }
.folha::before, .folha::after { content: ''; position: absolute; z-index: 5; pointer-events: none }
.folha::before { left: 4.25in; top: 0; bottom: 0; border-left: 1px dashed #D9CFE8 }
.folha::after  { top: 5.5in; left: 0; right: 0; border-top: 1px dashed #D9CFE8 }
.painel { padding: .2in .2in .15in; overflow: hidden; position: relative }
.bloco { display: flex; align-items: center; justify-content: space-between; gap: 6px; border-radius: 10px;
  padding: 2px 10px; height: .28in; margin-bottom: .06in; font-weight: 800; font-size: 9.5pt; letter-spacing: .2px }
.bloco .ico { flex: none }
.fluxo { display: flex; flex-wrap: wrap; align-items: flex-start; column-gap: %(esp)sin }
.livro { margin-bottom: %(gap)sin; break-inside: avoid }
.livro.largo { width: 100%% }
.rot { display: block; font-size: 6.6pt; font-weight: 800; height: %(rot)sin; line-height: %(rot)sin; color: var(--forte) }
.caps { display: flex; flex-wrap: wrap; max-width: %(util)sin }
.cap { position: relative; display: block; width: %(caixa)sin; height: %(caixa)sin; margin: 0 %(m)sin %(m)sin 0;
  border: 1.1px solid var(--cor); border-radius: 4px; background: #fff; font-style: normal; font-size: 4.9pt;
  line-height: 1; padding: 1.5px 0 0 2px; color: var(--forte); font-weight: 700 }
.cap.ok { background: var(--clara) }
.cap.ok::after { content: '✓'; position: absolute; right: 1px; bottom: -1px; font-size: 11pt; line-height: 1;
  color: var(--forte); font-weight: 900 }
/* capa */
.capa { height: 100%% }
.topo-capa { display: flex; align-items: center; justify-content: space-between; gap: 6px }
.capa h1 { margin: 0; font-size: 19pt; line-height: 1.02; text-align: center; color: #E0518E; font-weight: 900 }
.capa p { margin: 3px 0 0; text-align: center; font-size: 8pt; color: %(suave)s; font-weight: 700 }
.geral { margin: 4px 0 3px; text-align: center; font-size: 9pt }
.geral b { font-size: 14pt; color: #E0518E }
.barra { display: flex; gap: 2px; margin: 3px 0 1px }
.barra i { flex: 1; height: 11px; border: 1.2px solid #E0518E; border-radius: 3px }
small { color: %(suave)s; font-size: 6.2pt; display: block; font-weight: 600 }
.leg { width: 100%%; border-collapse: collapse; font-size: 7.6pt }
.leg td { padding: 1.4px 3px; border-bottom: 1px dotted #E5DDF0; vertical-align: middle }
.leg .num { text-align: right; white-space: nowrap; font-weight: 700; font-size: 7pt }
.bola { display: inline-block; width: 16px; height: 16px; border-radius: 50%%; text-align: center; line-height: 16px;
  font-size: 9pt; color: %(tinta)s; font-weight: 900 }
.datas { margin: 5px 0 2px; font-size: 8pt; text-align: center }
.como { margin: 4px 0 6px; padding-left: 16px; font-size: 7.6pt; line-height: 1.35 }
.selos { display: flex; justify-content: space-between }
.selos span { width: .33in; height: .33in; border-radius: 50%%; border: 2px dashed var(--cor); display: flex;
  align-items: center; justify-content: center; font-size: 14pt; color: var(--cor); background: #fff }
.notas { margin-top: .08in; font-size: 7.5pt; font-weight: 800; color: #E0518E }
.linha { border-bottom: 1px solid #E5DDF0; height: .26in }
.rodape { position: absolute; left: .2in; right: .2in; bottom: .08in; font-size: 6pt; color: %(suave)s; text-align: center }
""" % dict(tinta=B.TINTA, suave=B.TINTA_SUAVE, gap=ALT_GAP, rot=ALT_ROTULO, util=LARG_UTIL,
           caixa=CAIXA, m=round(PASSO - CAIXA, 3), esp=ESPACO_X)


def paginas(p, plano):
    """Só as 2 folhas (sem <html>), para embutir no planner. Devolve (css_escopado, html)."""
    import re
    html, _ = montar(p, plano)
    corpo = html[html.index('<body>') + 6: html.index('</body>')]
    css = CSS
    css = re.sub(r'(^|\})(\s*)(\.[^{}@]+)\{', lambda m: m.group(1) + m.group(2) + ', '.join('.mapaB ' + x.strip() for x in m.group(3).split(',')) + '{', css)
    css = css.replace('.mapaB html', 'html')
    return css, f'<div class="mapaB">{corpo}</div>'


def montar(p, plano):
    paineis = alocar()
    # 8 painéis por folha dupla: [capa] + conteúdo; sobra vira anotações
    todos = [("capa", None)] + [("conteudo", pn) for pn in paineis]
    while len(todos) < 8:
        todos.append(("notas", None))
    if len(todos) > 8:
        raise SystemExit(f"Conteúdo não cabe: {len(todos)} painéis (máx. 8). Reduza PASSO/CAIXA.")
    html = []
    for f in range(2):
        html.append('<section class="folha">')
        for tipo, pn in todos[f * 4:(f + 1) * 4]:
            html.append('<div class="painel">')
            if tipo == "capa":
                html.append(capa(p, plano))
            elif tipo == "notas":
                html.append(painel_notas(4.4))
            else:
                bloco_ant = None
                aberto = False
                for item in pn:
                    if item[0] == "bloco":
                        if aberto:
                            html.append('</div>')
                        html.append(html_bloco(item[1], item[2]))
                        html.append('<div class="fluxo">')
                        aberto = True
                    else:
                        html.append(html_livro(item[1], p))
                if aberto:
                    html.append('</div>')
                if len(pn) <= 3:   # painel quase vazio: sobra espaço para anotações
                    html.append(painel_notas(3.6))
            html.append('</div>')
        html.append('</section>')
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Mapa de Progresso da Bíblia</title>'
            f'<link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>{"".join(html)}</body></html>'), todos


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    p = B.ler_progresso()
    plano = B.ler_plano()
    html, todos = montar(p, plano)
    B.PASTA.mkdir(parents=True, exist_ok=True)
    saida = B.PASTA / "mapa-de-progresso.html"
    saida.write_text(html, encoding="utf-8")
    print(f"OK {saida} · {sum(1 for t, _ in todos if t == 'conteudo')} painéis de conteúdo")
    if a.pdf and exportar_pdf(saida, saida.with_suffix(".pdf")):
        print(f"OK {saida.with_suffix('.pdf')}")
