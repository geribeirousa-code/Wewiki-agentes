"""Planner impresso (estilo botânico) para encadernar em espiral.

Uso: python planner.py [--pdf]
Entrada: Bíblia/planner/semanas/SEMANA-NN.json e Bíblia/estudos/DIA-NNN-*.json
Saída:   Bíblia/planner/planner-prototipo.html (e .pdf)

Papel Carta. Páginas ímpares (recto) têm a margem da espiral à esquerda; as pares (verso),
à direita, para a perfuração nunca comer texto.
"""
import argparse
import html as H
import json
import re
from pathlib import Path

import biblia as B
import flora
import mulheres
from geo import mapa_svg
from pdf import exportar_pdf

PASTA_PLANNER = B.PASTA / "planner"
MAX_PALAVRAS_DIA = 3   # a página do dia é uma folha só: 3 palavras no original, bem ligadas ao texto

# cor de destaque por paleta: (tinta do título, fundo suave, forte)
ACENTO = {
    "salvia":    ("#2F6F68", "#E4EFE8", "#2F5F5A"),
    "terracota": ("#C9482A", "#FBE6DA", "#A93A20"),
    "azul":      ("#3E78A8", "#E1ECF5", "#2F5F8F"),
    "mostarda":  ("#B7790F", "#FAEDC8", "#8F5F0A"),
    "rosa":      ("#C25673", "#FADFE4", "#A5435F"),
}
CERTEZA = {"consenso": ("consenso", "#CFE5D4", "#2F5F3A"), "maioria": ("maioria dos estudiosos", "#F6E3A6", "#6B5200"),
           "debate": ("em debate", "#F7CFD6", "#8A1F45"), "texto": ("está no texto", "#CDE7E3", "#1F5A52")}
TIPOS = {"cita": "citação", "eco": "eco", "paralelo": "paralelo", "cumprimento": "cumprimento", "tema": "tema",
         "contraste": "contraste", "personagem": "personagem"}
CORES_TIPO = {"cita": "#F4C9C2", "eco": "#CFE0EE", "paralelo": "#CFE5D4", "cumprimento": "#F6E3A6", "tema": "#D9E8E2",
              "contraste": "#F9D8B8", "personagem": "#E3DAF0"}
TITULOS_SEMANAS = [
    "Do Éden a Babel", "Abraão: promessa e fé", "Isaque e Jacó: a promessa em família", "José: do poço ao palácio",
    "De José a Moisés: Deus ouve o clamor", "Páscoa, mar e Sinai", "A aliança e o bezerro de ouro",
    "Tabernáculo e sacrifícios", "Santidade e pureza",
]


def e(t):
    return H.escape(str(t), quote=False)


def fmt(t):
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"<i>\1</i>", t)


def pilula(k):
    r, bg, fg = CERTEZA[k]
    return f'<span class="cert" style="background:{bg};color:{fg}">{r}</span>'


def emblema(tam=44, cor="#F1B9B1", tinta="#2F5F5A"):
    return (f'<svg width="{tam}" height="{tam}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="{cor}"/>'
            f'<path d="M32 40c-5-4-12-5-18-4V20c6-1 13 0 18 4z" fill="#fff"/><path d="M32 40c5-4 12-5 18-4V20c-6-1-13 0-18 4z" fill="#FFF7F2"/>'
            f'<path d="M32 24v16" stroke="{cor}" stroke-width="2"/>'
            f'<path d="M32 46c-1 5 1 9 4 12M32 46c-3 4-8 6-12 5" fill="none" stroke="{tinta}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<ellipse cx="38" cy="53" rx="3" ry="1.8" fill="{tinta}" transform="rotate(-50 38 53)"/>'
            f'<ellipse cx="25" cy="50" rx="3" ry="1.8" fill="{tinta}" transform="rotate(30 25 50)"/></svg>')


def semanas_do_plano():
    pl = B.ler_plano()
    return [pl[i:i + 6] for i in range(0, len(pl), 6)]


def faixa_passagem(dias):
    a, b = dias[0], dias[-1]
    if a["sigla"] == b["sigla"]:
        return f"{a['livro']} {a['de']}–{b['ate']}"
    return f"{a['livro']} {a['de']} – {b['livro']} {b['ate']}"


# ---------------------------------------------------------------------------
def pg(conteudo, n, extra=""):
    lado = "recto" if n % 2 == 1 else "verso"
    return f'<section class="pg {lado} {extra}">{conteudo}<div class="num">{n}</div></section>'


def capa(n):
    return pg(f"""
<div class="capa-bg">{flora.capa_svg(816, 1056, 7)}</div>
<div class="capa-banda">
  <div class="emb">{emblema(70, "#F4C3BB", "#FFF")}</div>
  <div class="t1"><span class="scr">Estudo</span><span class="cap">BÍBLIA</span></div>
  <div class="t2">EM PROFUNDIDADE</div>
  <div class="t3">Uma jornada de 94 semanas pelo contexto,<br>pela cultura e pelo texto original</div>
</div>""", n, "capa")


def boas_vindas(n):
    passos = [("Leia a abertura da semana", "visão geral, pano de fundo, mapa e palavras-chave."),
              ("Estude um dia por vez", "1 hora: oração, contexto, leitura, original, conexões, resumo."),
              ("Leia o texto na sua Bíblia", "as folhas indicam o caminho; o texto é sempre o da sua Bíblia."),
              ("Observe os selos de certeza", "consenso, maioria dos estudiosos ou em debate."),
              ("Pinte o mapa da Bíblia", "cada capítulo estudado vira um quadradinho colorido."),
              ("Descanse no domingo", "o plano tem 6 dias por semana, sem culpa pelo sétimo.")]
    lista = "".join(f'<li><span class="bol">{i}</span><div><b>{a}</b><small>{b}</small></div></li>' for i, (a, b) in enumerate(passos, 1))
    return pg(f"""
<div class="canto-fl">{flora.faixa(300, 150, 41, "salvia", 0)}</div>
<div class="base-fl">{flora.faixa(816, 250, 77, "salvia", 0, 0.42, 0.55)}</div>
<h1 class="scr gr">Esta jornada é de</h1>
<div class="linha-nome"></div>
<div class="datas2"><span>Comecei em ______ / ______ / ______</span><span>Termino em ______ / ______ / ______</span></div>
<h2 class="sub">Como ler a Bíblia sem medo</h2>
<div class="tres"><div><b>1 · Observar</b>O que o texto diz? Leia devagar e procure palavras repetidas, nomes e lugares.</div><div><b>2 · Entender</b>O que quis dizer para quem ouviu primeiro? Época, cultura e palavras no original ajudam.</div><div><b>3 · Aplicar</b>O que muda na minha casa, no meu trabalho, no meu coração?</div></div>
<h2 class="sub">Como usar este planner</h2>
<ol class="passos">{lista}</ol>
<div class="hora2"><b>Minha hora de estudo</b>
  <div class="relogio"><div><i>0–5′</i>Oração</div><div><i>5–15′</i>Contexto</div><div><i>15–30′</i>Leitura</div><div><i>30–45′</i>Original</div><div><i>45–55′</i>Conexões</div><div><i>55–60′</i>Resumo</div></div></div>
""", n, "boas")


def sumario(n, semanas, pagina_inicial):
    linhas = []
    for i, w in enumerate(semanas[:len(TITULOS_SEMANAS)], 1):
        pal = flora.ORDEM[(i - 1) % 5]
        ink, tint, _ = ACENTO[pal]
        pag = pagina_inicial + (i - 1) * 8
        linhas.append(
            f'<div class="linha-s" style="background:{tint}"><div class="txt"><small style="color:{ink}">SEMANA {i}</small>'
            f'<b style="color:{ink}">{e(TITULOS_SEMANAS[i - 1])}</b><em>{e(faixa_passagem(w))}</em></div>'
            f'<span class="pag" style="color:{ink}">{pag}</span><div class="fx">{flora.faixa(190, 62, 100 + i, pal)}</div></div>')
    return pg(f"""
<header class="faixa-t" style="background:#E4EFE8"><h1>Sumário</h1><div>{emblema(48)}</div></header>
<div class="sumario">{"".join(linhas)}<p class="cont">… e assim por diante, até a semana 94 (Apocalipse). Esta é a amostra das 9 primeiras.</p></div>
""", n, "sumario")


def semana_esq(n, s, w):
    ink, tint, forte = ACENTO[s["paleta"]]
    ficha = "".join(f'<tr><th style="color:{ink}">{e(r[0])}</th><td>{fmt(r[1])} {pilula(r[2])}</td></tr>' for r in s["ficha"])
    tl = s["linha_do_tempo"]
    itens = "".join(f'<li class="{"d" if i.get("destaque") else ""}" style="--c:{ink}"><b>{e(i["rotulo"])}</b><span>{fmt(i["texto"])}</span></li>' for i in tl["itens"])
    mapa = mapa_svg(s["mapa"], ink, 600, agua="#DCEBF2", terra="#FBF3E1", borda="#E5D3A8")
    bloco = B.BLOCO[s["bloco"]][1].upper()
    return pg(f"""
<header class="faixa-s" style="background:{tint}">
  <div><small style="color:{ink}">{e(bloco)} · {e(s["passagem"]).upper()}</small><h1 style="color:{ink}">{e(s["titulo"])}</h1></div>
  <div class="sem" style="color:{ink};border-color:{ink}"><span>SEMANA</span><b>{s["numero"]}</b></div>
</header>
<h2 class="h" style="color:{ink}">Visão geral</h2>
<p class="vg">{fmt(s["visao_geral"])}</p>
<h2 class="h" style="color:{ink}">{e(s["fundo_titulo"])}</h2>
<div class="dois"><table class="ficha2">{ficha}</table><p class="cen">{fmt(s["cenario"])}</p></div>
<div class="mapa-c">{mapa}<p class="leg">{fmt(s["mapa"]["legenda"])}</p></div>
<h2 class="h" style="color:{ink}">{e(tl["titulo"])}</h2>
<ol class="tl">{itens}</ol><p class="nt">{fmt(tl["nota"])}</p>
""", n, "semana-esq")


def semana_dir(n, s, w):
    ink, tint, forte = ACENTO[s["paleta"]]
    plano = "".join(
        f'<li><span class="ck" style="border-color:{ink}"></span><div><b><i style="color:{ink}">DIA {i}</i> | {e(p["ref"])}</b><em>{e(p["nota"])}</em></div></li>'
        for i, p in enumerate(s["plano"], 1))
    palavras = "".join(
        f'<div class="pw"><div class="hb" dir="rtl" style="background:{tint};color:{forte}">{e(p["orig"])}</div>'
        f'<div><b>{e(p["translit"])}</b> <small>{e(p["strong"])}</small><em>“{e(p["pt"])}” · {fmt(p["texto"])}</em></div></div>'
        for p in s["palavras"])
    chips = "".join(f'<div class="chip" style="border-color:{ink}">{mulheres.figura(m["nome"].replace("A esposa de Noé", "Sara"), 26)}'
                    f'<div><b>{e(m["nome"])}</b><br><small>{e(m["ref"])}</small></div></div>' for m in s["mulheres"])
    con = "".join(f'<li><b style="color:{ink}">{e(c["ref"])}</b> {fmt(c["texto"])}</li>' for c in s["conexoes"])
    glos = "".join(f'<b>{e(g["termo"])}:</b> {e(g["texto"])}. ' for g in s["glossario"])
    return pg(f"""
<div class="plano" style="border-color:{ink};background:#FFFBF4">
  <div class="top-i">{emblema(40, tint, forte)}</div>
  <h2 class="scr" style="color:{ink}">Plano de leitura</h2>
  <ul>{plano}</ul>
</div>
<h2 class="h" style="color:{ink}">Mulheres desta semana</h2>
<div class="chips">{chips}</div>
<h2 class="h" style="color:{ink}">Palavras da semana, no original</h2>
<div class="pws">{palavras}</div>
<h2 class="h" style="color:{ink}">Conexões da semana</h2>
<ul class="con2">{con}</ul>
<h2 class="h" style="color:{ink}">Palavras difíceis</h2>
<p class="glos">{glos}</p>
<div class="bencao" style="background:{ink}"><small>BÊNÇÃO DA SEMANA</small><h3 class="scr">Bênção</h3><p>{fmt(s["bencao"])}</p></div>
<div class="notas2"><b style="color:{ink}">Anotações da semana</b>{"".join('<div class="ln"></div>' for _ in range(2))}</div>
""", n, "semana-dir")


def pagina_dia(n, d, s):
    ink, tint, forte = ACENTO[s["paleta"]]
    nt = d["naquele_tempo"]
    obs = "".join(f"<li>{fmt(x)}</li>" for x in d["observar"])
    veja = " · ".join(e(x) for x in d.get("veja_tambem", []))
    cards = []
    for w in d.get("original_planner", d["original"])[:MAX_PALAVRAS_DIA]:
        heb = w["lingua"].startswith(("hebr", "aram"))
        cards.append(
            f'<div class="pw3"><div class="hb {"g" if not heb else ""}" dir="{"rtl" if heb else "ltr"}" style="background:{tint};color:{forte}">{e(w["orig"])}</div>'
            f'<div class="tx"><div class="l1"><b>{e(w["translit"])}</b> <span class="pt2">“{fmt(w["pt"])}”</span> <small>{e(w["strong"])}</small> {pilula(w.get("certeza", "consenso"))}</div>'
            f'<p>{fmt(w["significado"])}</p>'
            f'<p class="no"><i style="color:{ink}">NO TEXTO</i> {fmt(w["no_texto"])}</p>'
            f'<p class="mu"><i style="color:{ink}">O QUE MUDA</i> {fmt(w["muda"])}</p></div></div>')
    mapa = ""
    if d.get("mapa"):
        mapa = (f'<div class="mapa-l">{mapa_svg(d["mapa"], ink, 300, agua="#DCEBF2", terra="#FBF3E1", borda="#E5D3A8", aspecto=1.0)}'
                f'<p>{fmt(d["mapa"]["legenda"])}</p></div>')
    m = d["mulher"]
    fig = mulheres.figura(m["nome"], 128, m.get("figura"))
    return pg(f"""
<header class="faixa-d" style="background:{tint}">
  <div><small style="color:{ink}">SEMANA {s["numero"]} · DIA {d["dia"]} · {e(B.BLOCO[d["bloco"]][1]).upper()}</small>
    <h1 style="color:{ink}">{e(d["passagem"])}</h1><p>{fmt(d["titulo"])}</p></div>
  <div class="sem" style="color:{ink};border-color:{ink}"><span>DIA</span><b>{d["dia"]}</b></div>
</header>
<div class="linhaA">
  <div class="tempo">
    <h2 class="h" style="color:{ink}"><i class="et" style="background:{ink}">ENTENDER</i> Naquele tempo</h2>
    <div class="bl"><b style="color:{ink}">Quando?</b> {fmt(nt["quando"]["texto"])} {pilula(nt["quando"]["certeza"])}</div>
    <div class="bl"><b style="color:{ink}">O que era comum</b> {fmt(nt["comum"]["texto"])} {pilula(nt["comum"]["certeza"])}</div>
    <div class="cur"><b>✦ Curiosidade</b> {fmt(nt["curiosidade"])}</div>
  </div>
  {mapa}
</div>
<div class="perg"><span class="scr">Para carregar hoje</span><p>{fmt(d["pergunta_guia"])}</p></div>
<h2 class="h" style="color:{ink}"><i class="et" style="background:{ink}">OBSERVAR</i> Leia na sua Bíblia e procure</h2>
<ul class="obs3">{obs}</ul><p class="vt"><b style="color:{ink}">Veja também:</b> {veja}</p>
<h2 class="h" style="color:{ink}"><i class="et" style="background:{ink}">ENTENDER</i> No original, ligado ao texto</h2>
<div class="pws3">{"".join(cards)}</div>
<div class="mulher" style="background:{tint}">
  <div class="fig">{fig}</div>
  <div class="mt">
    <small style="color:{ink}"><i class="et" style="background:{ink}">APLICAR</i> UMA MULHER NA HISTÓRIA</small>
    <h3 style="color:{ink}">{e(m["titulo"])} <em>{e(m["ref"])}</em></h3>
    <p class="cz">“{fmt(m["cartaz"])}”</p>
    <p>{fmt(m["reflexao"])}</p>
    <p class="ph"><b style="color:{ink}">Para o meu dia:</b> {fmt(m["para_hoje"])}</p>
    <div class="ln"></div>
  </div>
</div>
<div class="fecha"><span class="ck" style="border-color:{ink}"></span>Orei <span class="ck" style="border-color:{ink}"></span>Li <span class="ck" style="border-color:{ink}"></span>Estudei <span class="ck" style="border-color:{ink}"></span>Resumi
  <span class="ck" style="border-color:{ink}"></span>Pintei o mapa</div>
""", n, "dia")


CSS = """
@page { size: 8.5in 11in; margin: 0 }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact }
html, body { margin: 0; background: #FBF6EC }
body { font-family: 'Lora', Georgia, 'Times New Roman', serif; color: #2E3B3A; font-size: 8.7pt; line-height: 1.42 }
.scr { font-family: 'Parisienne', 'Brush Script MT', cursive; font-weight: 400 }
small, .cert, .num, .sem span, header small { font-family: 'Nunito Sans', 'Segoe UI', Arial, sans-serif }
h1, h2, h3, p, ul, ol { margin: 0; padding: 0 }
.pg { width: 8.5in; height: 11in; position: relative; overflow: hidden; page-break-after: always; background: #FFFDF8; padding: .5in .5in .55in .85in }
.pg.verso { padding: .5in .85in .55in .5in }
.num { position: absolute; bottom: .22in; font-size: 7pt; color: #9AA8A4; letter-spacing: 1px }
.recto .num { right: .5in } .verso .num { left: .5in }
.cert { display: inline-block; font-size: 5.8pt; font-weight: 700; border-radius: 99px; padding: 0 6px; vertical-align: 1px; white-space: nowrap }
/* capa */
.pg.capa { padding: 0; background: #FBF6EC }
.capa-bg { position: absolute; inset: 0 } .capa-bg svg { width: 8.5in; height: 11in }
.capa-banda { position: absolute; left: 0; right: 0; top: 4.23in; height: 2.54in; text-align: center; color: #2F5F5A }
.emb { position: absolute; left: 50%; top: -.37in; transform: translateX(-50%) }
.t1 { margin-top: .62in; display: flex; align-items: baseline; justify-content: center; gap: 10px }
.t1 .scr { font-size: 58pt; line-height: 1; transform: translateY(6px) }
.t1 .cap { font-size: 50pt; letter-spacing: .14em; font-weight: 500; line-height: 1 }
.t2 { font-size: 17pt; letter-spacing: .32em; margin-top: 10px; font-weight: 500 }
.t3 { font-style: italic; font-size: 10.5pt; margin-top: 14px; color: #3F6A66; line-height: 1.5 }
/* boas-vindas */
.boas .canto-fl { position: absolute; right: .5in; top: .5in; width: 3.1in; opacity: .95 } .boas .canto-fl svg { width: 100%; height: auto; border-radius: 16px }
.gr { font-size: 40pt; color: #2F6F68; margin-top: .55in; line-height: 1.1 }
.linha-nome { border-bottom: 1.5px solid #CFC9B8; height: 30px; width: 3.7in }
.boas .base-fl { position: absolute; left: 0; right: 0; bottom: 0; height: 2.6in } .boas .base-fl svg { width: 8.5in; height: 2.6in; display: block }
.datas2 { display: flex; flex-direction: column; gap: 6px; margin: 10px 0 22px; font-size: 9pt; color: #5A6B68 }
.sub { font-size: 16pt; color: #2F6F68; font-weight: 600; margin: 4px 0 10px }
.passos { list-style: none; display: grid; gap: 7px }
.passos li { display: flex; gap: 11px; align-items: flex-start }
.passos .bol { flex: none; width: 24px; height: 24px; border-radius: 50%; background: #F4C9C2; color: #8A3B30; font: 700 10pt 'Nunito Sans', sans-serif; display: flex; align-items: center; justify-content: center }
.passos b { font-size: 10pt; display: block } .passos small { font-size: 8pt; color: #5A6B68 }
.hora2 { margin-top: 24px; background: #E4EFE8; border-radius: 18px; padding: 10px 16px }
.hora2 > b { font-size: 10pt; color: #2F6F68 }
.relogio { display: flex; margin-top: 6px; gap: 4px }
.relogio div { flex: 1; text-align: center; font-size: 8pt; background: #fff; border-radius: 12px; padding: 5px 2px }
.relogio i { display: block; font-style: normal; font: 800 9pt 'Nunito Sans', sans-serif; color: #2F6F68 }
/* faixa de título */
.faixa-t { margin: -.5in -.5in 0 -.85in; padding: .45in .5in .2in .85in; display: flex; justify-content: space-between; align-items: center; height: 1.3in }
.verso .faixa-t { margin: -.5in -.85in 0 -.5in; padding: .45in .85in .2in .5in }
.faixa-t h1 { font-size: 34pt; font-weight: 500; color: #2F5F5A }
.sumario { margin-top: .22in; display: grid; gap: 8px }
.linha-s { display: flex; align-items: center; gap: 10px; border-radius: 16px; padding: 0 0 0 16px; height: .74in; overflow: hidden }
.linha-s .txt { flex: 1; min-width: 0 }
.linha-s small { display: block; font-size: 7pt; letter-spacing: .14em; font-weight: 700 }
.linha-s b { display: block; font-size: 12.5pt; font-weight: 500; line-height: 1.15 }
.linha-s em { font-size: 8pt; color: #6B7B78 }
.linha-s .pag { font: 700 11pt 'Nunito Sans', sans-serif }
.linha-s .fx { width: 190px; height: 100%; margin-right: 0 } .linha-s .fx svg { width: 190px; height: 100%; border-radius: 0 16px 16px 0; display: block }
.cont { text-align: center; font-style: italic; font-size: 8.5pt; color: #6B7B78; margin-top: 8px }
/* semana */
.faixa-s, .faixa-d { margin: -.5in -.5in 0 -.85in; padding: .5in .5in .22in .85in; display: flex; justify-content: space-between; align-items: center; gap: 12px }
.verso .faixa-s, .verso .faixa-d { margin: -.5in -.85in 0 -.5in; padding: .5in .85in .22in .5in }
.faixa-s { height: 1.6in } .faixa-d { height: 1.02in }
.faixa-s small, .faixa-d small { font-size: 7pt; letter-spacing: .16em; font-weight: 700; display: block }
.faixa-s h1 { font-size: 30pt; font-weight: 500; line-height: 1.1; margin-top: 4px }
.faixa-d h1 { font-size: 23pt; font-weight: 500; line-height: 1.1 } .faixa-d p { font-size: 10pt; font-style: italic; margin-top: 2px }
.sem { flex: none; width: .86in; height: .86in; border: 1.6px solid; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FFFDF8 }
.sem span { font-size: 6.2pt; letter-spacing: .16em; font-weight: 700 } .sem b { font-size: 24pt; font-weight: 500; line-height: 1 }
h2.h { font-size: 14pt; font-weight: 500; margin: 11px 0 4px } h2.h small { font-size: 7pt; color: #7B8A87; margin-left: 6px; font-weight: 600; letter-spacing: .04em }
.vg { font-size: 9.3pt; line-height: 1.55 }
.dois { display: grid; grid-template-columns: 2.35in 1fr; gap: 16px }
.ficha2 { border-collapse: collapse; font-size: 8pt } .ficha2 th { text-align: left; vertical-align: top; padding: 3px 8px 3px 0; font-family: 'Nunito Sans', sans-serif; font-size: 7pt; letter-spacing: .08em; text-transform: uppercase }
.ficha2 td { padding: 3px 0; border-bottom: 1px dotted #D8D2C0 }
.cen { font-size: 8.8pt }
.mapa-c { margin-top: 12px } .mapa-c svg { width: 100%; height: auto; display: block } .leg { font-size: 7.5pt; color: #6B7B78; margin-top: 3px; font-style: italic }
.tl { list-style: none; display: flex; gap: 5px } .tl li { flex: 1; text-align: center; border: 1.5px solid var(--c); border-radius: 12px; padding: 4px 4px; background: #fff }
.tl li.d { background: #F6E3A6; border-color: #E9B949 } .tl b { display: block; font: 800 7.4pt 'Nunito Sans', sans-serif; color: var(--c) } .tl span { font-size: 8pt; line-height: 1.2; display: block }
.nt { font-size: 7.6pt; color: #6B7B78; margin-top: 4px; font-style: italic }
/* direita */
.plano { border: 1.6px solid; border-radius: 22px; padding: 12px 20px 14px; position: relative }
.plano .top-i { position: absolute; right: 20px; top: 12px }
.plano h2.scr { font-size: 28pt; line-height: 1.1; margin-bottom: 6px }
.plano ul { list-style: none; display: grid; gap: 7px }
.plano li { display: flex; gap: 12px; align-items: flex-start }
.ck { display: inline-block; flex: none; width: 12px; height: 12px; border: 1.5px solid; border-radius: 50%; background: #fff; vertical-align: -2px; margin-right: 4px }
.plano b { font-size: 10pt; font-weight: 500; display: block } .plano b i { font: 800 7.4pt 'Nunito Sans', sans-serif; letter-spacing: .06em; font-style: normal }
.plano em { font-size: 8.4pt; color: #5E6F6C }
.pws { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px }
.pw { display: flex; gap: 9px; align-items: center } .hb { flex: none; width: .95in; height: .52in; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-family: 'SBL Hebrew', 'Ezra SIL', 'Times New Roman', 'DejaVu Serif', serif; font-size: 17pt; text-align: center; line-height: 1.05 }
.hb.g { font-family: 'SBL Greek', 'Times New Roman', 'DejaVu Serif', serif }
.pw b { font-size: 9.4pt; font-weight: 600 } .pw small { font-size: 6.4pt; color: #6B7B78 } .pw em { display: block; font-size: 7.8pt; line-height: 1.25; color: #4D5E5B }
.ccs { display: grid; gap: 7px } .cc { border-left: 4px solid; background: #FFFBF4; border-radius: 4px 14px 14px 4px; padding: 6px 10px; font-size: 8.4pt } .cc b { display: block; font-size: 9.6pt; font-weight: 600 }
.bencao { margin-top: 10px; border-radius: 20px; color: #fff; padding: 11px 20px 13px; text-align: left }
.bencao small { font-size: 6.4pt; letter-spacing: .2em; font-weight: 700; opacity: .9 } .bencao h3 { font-size: 26pt; line-height: 1.05 } .bencao p { font-size: 9.2pt; line-height: 1.5; margin-top: 3px }
.notas2 { margin-top: 10px; font-size: 9pt } .ln { border-bottom: 1px solid #E1DACB; height: 22px }
/* dia */
.perg { margin-top: 6px; border: 1.8px dashed; border-radius: 16px; background: #FFF6D6; padding: 5px 14px 7px }
.perg .scr { font-size: 15pt; color: #A06F0A; line-height: 1.1 } .perg p { font-size: 9.8pt; font-weight: 600; line-height: 1.35 }
.est2 { border-collapse: collapse; font-size: 8.2pt; width: 100% } .est2 td { padding: 2px 4px; border-bottom: 1px dotted #D8D2C0; vertical-align: top } .est2 .rf { font: 800 7.6pt 'Nunito Sans', sans-serif; white-space: nowrap; width: .62in }
.pws2 { display: grid; grid-template-columns: 1fr 1fr; gap: 7px 14px }
.pw2 { display: flex; gap: 8px; align-items: flex-start; font-size: 7.9pt; line-height: 1.3 } .pw2 .hb { width: .84in; height: .66in; font-size: 16pt }
.pw2 b { font-size: 9.2pt; font-weight: 600 } .pw2 small { font-size: 6.2pt; color: #6B7B78 } .pt2 { font-style: italic; font-weight: 600; color: #6A3A45 }
.con2 { list-style: none; columns: 2; column-gap: 18px } .con2 li { break-inside: avoid; font-size: 8pt; line-height: 1.28; padding: 3px 0; border-bottom: 1px dotted #E0DACB }
.con2 i { font: 700 5.9pt 'Nunito Sans', sans-serif; font-style: normal; border-radius: 99px; padding: 0 6px; margin-right: 4px; vertical-align: 1px }
.fim2 { display: grid; grid-template-columns: 1.35fr 1fr; gap: 14px; margin-top: -6px } .fim2 ol { padding-left: 16px; font-size: 8.6pt; font-weight: 500 } .fim2 .ln { height: 19px }
.ap { border-radius: 16px; padding: 9px 14px; font-size: 8.8pt; margin-top: 14px; line-height: 1.4 } .ap b { display: block; font-size: 10pt; margin-bottom: 2px }
.fecha { position: absolute; left: .85in; right: .5in; bottom: .45in; font: 700 7.8pt 'Nunito Sans', sans-serif; color: #5A6B68; display: flex; gap: 6px; align-items: center }
.verso .fecha { left: .5in; right: .85in }

/* dia v2 */
.et { font: 800 6pt 'Nunito Sans', sans-serif; font-style: normal; letter-spacing: .12em; color: #fff; border-radius: 99px; padding: 1px 7px; margin-right: 6px; vertical-align: 2px }
.linhaA { display: grid; grid-template-columns: 1fr 1.95in; gap: 14px; align-items: start; margin-top: 2px }
.tempo .bl { font-size: 8.3pt; line-height: 1.38; margin-bottom: 4px } .tempo .bl b { font-weight: 700 }
.cur { background: #FFF2C9; border-radius: 12px; padding: 6px 11px; font-size: 8.4pt; line-height: 1.4 } .cur b { color: #A06F0A }
.mapa-l { margin-top: 12px } .mapa-l svg { width: 100%; height: auto; display: block } .mapa-l p { font-size: 6.9pt; color: #6B7B78; font-style: italic; line-height: 1.3; margin-top: 3px }
.obs3 { padding-left: 18px; font-size: 8.8pt; line-height: 1.4 } .obs3 li { margin-bottom: 2px } .vt { font-size: 8pt; margin-top: 3px }
.pws3 { display: grid; gap: 6px }
.pw3 { display: flex; gap: 10px; align-items: flex-start; background: #FFFBF4; border-radius: 14px; padding: 5px 9px }
.pw3 .hb { width: .9in; height: .74in; font-size: 17pt }
.pw3 .tx { flex: 1; font-size: 7.8pt; line-height: 1.3 } .pw3 .tx p { margin: 1px 0 0 } .pw3 .l1 b { font-size: 10pt; font-weight: 600 } .pw3 .l1 small { font-size: 6.2pt; color: #6B7B78 }
.pw3 i { font: 800 5.9pt 'Nunito Sans', sans-serif; font-style: normal; letter-spacing: .1em; margin-right: 4px }
.mulher { display: flex; gap: 12px; border-radius: 22px; padding: 8px 16px 8px 10px; margin-top: 8px; align-items: flex-start }
.mulher .fig { flex: none; width: 1.15in } .mulher .fig svg { width: 100%; height: auto; display: block }
.mulher .mt { flex: 1; font-size: 8.2pt; line-height: 1.38 } .mulher small { font-size: 6.4pt; letter-spacing: .14em; font-weight: 800; display: block }
.mulher h3 { font-size: 15pt; font-weight: 500; line-height: 1.15 } .mulher h3 em { font: 600 7.4pt 'Nunito Sans', sans-serif; color: #6B7B78; font-style: normal; margin-left: 4px }
.mulher .cz { font-style: italic; font-weight: 600; font-size: 10pt; margin: 2px 0 3px } .mulher .ph { margin-top: 4px } .mulher .ln { height: 17px }
.glos { font-size: 8pt; line-height: 1.35 } .glos b { font-weight: 700 }
.chips { display: flex; gap: 6px; flex-wrap: wrap } .chip { background: #FFFBF4; border: 1.4px solid; border-radius: 99px; padding: 2px 11px 2px 3px; display: flex; align-items: center; gap: 6px; font-size: 8.4pt }
.chip svg { width: 26px; height: auto; border-radius: 50% } .chip small { font-size: 6.4pt; color: #6B7B78 }
.tres { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 6px 0 14px }
.tres div { background: #fff; border-radius: 16px; padding: 7px 10px; font-size: 8.2pt; line-height: 1.35; border: 1.5px solid #F4C9C2 } .tres b { display: block; font-size: 10pt; color: #2F6F68 }
"""

FONTES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?'
          'family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Nunito+Sans:wght@600;700;800'
          '&family=Parisienne&display=swap" rel="stylesheet">')


def montar():
    sems = semanas_do_plano()
    s1 = json.loads((PASTA_PLANNER / "semanas" / "SEMANA-01.json").read_text(encoding="utf-8"))
    d1 = json.loads(next((B.PASTA / "estudos").glob("DIA-001-*.json")).read_text(encoding="utf-8"))
    paginas = [capa(1), boas_vindas(2), sumario(3, sems, 4), semana_esq(4, s1, sems[0]), semana_dir(5, s1, sems[0]),
               pagina_dia(6, d1, s1)]
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Estudo Bíblia em Profundidade (protótipo)</title>'
            f'{FONTES}<style>{CSS}</style></head><body>{"".join(paginas)}</body></html>')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    PASTA_PLANNER.mkdir(parents=True, exist_ok=True)
    saida = PASTA_PLANNER / "planner-prototipo.html"
    saida.write_text(montar(), encoding="utf-8")
    print(f"OK {saida}")
    if a.pdf and exportar_pdf(saida, saida.with_suffix(".pdf")):
        print(f"OK {saida.with_suffix('.pdf')}")
