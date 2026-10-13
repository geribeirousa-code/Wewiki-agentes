"""Transforma o JSON do estudo do dia na folha impressa (HTML autocontido, Carta, frente e verso).

Uso: python gerar_folha.py "Bíblia/estudos/DIA-001-genesis-1-2.json" [--pdf]
Saída: mesmo nome, .html (e .pdf).

O conteúdo (contexto, palavras no original, conexões) vem do JSON, escrito por quem
pesquisa (Pax) com fonte para cada afirmação. Este script só diagrama.
"""
import argparse
import html as H
import json
import re
from datetime import date
from pathlib import Path

import biblia as B
from geo import mapa_svg
from icones import icone, POR_BLOCO
from pdf import exportar_pdf

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]

CERTEZA = {   # chave: (rótulo, cor de fundo, texto)
    "consenso": ("consenso", "#BFE6A8", "#2F5A1E"),
    "maioria": ("maioria dos estudiosos", "#FFE48A", "#6B5200"),
    "debate": ("em debate", "#FFC2DA", "#8A1F55"),
    "texto": ("está no texto", "#BFEFE8", "#0F5E55"),
}
TIPOS = {   # tipo de conexão: (rótulo, cor)
    "cita": ("citação", "#FFB3D1"), "eco": ("eco", "#7EC8FF"), "paralelo": ("paralelo", "#9FD68A"),
    "cumprimento": ("cumprimento", "#FFD63A"), "tema": ("tema", "#25C2B0"), "contraste": ("contraste", "#F4B41A"),
    "personagem": ("personagem", "#C7B6F0"),
}


def e(t):
    return H.escape(str(t), quote=False)


def fmt(t):
    """Escapa e aplica **negrito** e _itálico_."""
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"<i>\1</i>", t)
    return t


def pilula(chave):
    r, bg, fg = CERTEZA[chave]
    return f'<span class="cert" style="background:{bg};color:{fg}">{r}</span>'


def data_longa(iso):
    d = date.fromisoformat(iso)
    return f"{DIAS[d.weekday()]}, {d.day} de {MESES[d.month - 1]} de {d.year}"


def segmentos(frac, cor, n=20):
    cheios = max(1, round(frac * n))
    return "".join(f'<i style="background:{cor if k < cheios else "#fff"}"></i>' for k in range(n))


def secao(titulo, cor, icon, corpo, classe=""):
    return (f'<section class="sec {classe}"><h2 style="background:{cor}">{icone(icon, 20, "#fff", "#FFF3B0", B.TINTA)}'
            f'<span>{titulo}</span></h2><div class="corpo">{corpo}</div></section>')


def pagina1(d, cor, forte, clara):
    ctx = d["contexto"]
    i1, i2 = POR_BLOCO[d["bloco"]]
    ficha = "".join(
        f'<tr><th>{e(r[0])}</th><td>{fmt(r[1])}{" " + pilula(r[2]) if len(r) > 2 else ""}</td></tr>' for r in ctx["ficha"])
    cultura = "".join(
        f'<div class="card" style="--k:{c.get("cor", cor)}"><div class="t">{icone(c.get("icone", "estrela"), 18, cor, "#FFD63A", "#25C2B0")}'
        f'{e(c["titulo"])}</div><p>{fmt(c["texto"])}</p>{pilula(c.get("certeza", "maioria"))}</div>'
        for c in ctx["cultura"])
    tl = d["linha_do_tempo"]
    itens = "".join(
        f'<li class="{"dest" if it.get("destaque") else ""}"><b>{e(it["rotulo"])}</b><span>{fmt(it["texto"])}</span></li>'
        for it in tl["itens"])
    mapa = d.get("mapa")
    mapa_html = ""
    if mapa:
        mapa_html = (f'<div class="mapa-caixa">{mapa_svg(mapa, cor, 560)}'
                     f'<p class="legenda">{fmt(mapa.get("legenda", ""))} <em>Mapa esquemático, fora de escala. '
                     f'Círculo tracejado = localização incerta.</em></p></div>')
    hora = [("0–5", "Oração e foco"), ("5–15", "Contexto"), ("15–30", "Leitura atenta"),
            ("30–45", "No original"), ("45–55", "Conexões"), ("55–60", "Resumo")]
    hora_html = "".join(f'<div><span class="cx"></span><b>{m}′</b><small>{n}</small></div>' for m, n in hora)
    return f"""
<div class="pagina">
  <header class="topo" style="background:{clara}">
    <div class="ic">{icone(i1, 54, cor, "#FFD63A", "#25C2B0")}</div>
    <div class="tit">
      <div class="linha1"><span class="pill" style="background:{cor}">DIA {d['dia']} de {d['total_dias']}</span>
        <span class="pill suave">{e(B.BLOCO[d['bloco']][1])}</span><span class="data">{data_longa(d['data'])}</span></div>
      <h1>{e(d['passagem'])}</h1>
      <p class="sub">{fmt(d['titulo'])}</p>
    </div>
    <div class="ic">{icone(i2, 54, cor, "#FFD63A", "#25C2B0")}</div>
  </header>
  <div class="prog"><span>Meu progresso</span><div class="barra">{segmentos(d['dia'] / d['total_dias'], cor)}</div></div>

  <div class="pergunta"><div>{icone("sol", 40, "#FFD63A", "#FFD63A", "#FF7EB6")}</div>
    <p><small>PERGUNTA PARA CARREGAR HOJE</small>{fmt(d['pergunta_guia'])}</p></div>

  <div class="duas">
    <div>{secao("Quem, quando, para quem", "#FF7EB6", "livro",
                f'<table class="ficha">{ficha}</table><p class="cenario">{fmt(ctx["cenario"])}</p>')}</div>
    <div>{mapa_html}</div>
  </div>

  {secao(e(tl["titulo"]), "#25C2B0", "estrela",
         f'<ol class="tempo">{itens}</ol>' + (f'<p class="nota">{fmt(tl["nota"])}</p>' if tl.get("nota") else ""))}

  {secao("O mundo daquele tempo", "#F4B41A", "coroa", f'<div class="cards n{len(ctx["cultura"])}">{cultura}</div>')}

  <div class="hora"><b>Minha hora de estudo</b>{hora_html}</div>
  <footer>1/3 · {e(B.LIVRO[d['sigla']]['lingua'])} · tradução de apoio: NVI · legenda: {pilula("consenso")} {pilula("maioria")} {pilula("debate")}</footer>
</div>"""


def pagina2(d, cor, forte, clara):
    l = d["leitura"]
    estrutura = "".join(
        f'<tr><td class="ref">{e(r["ref"])}</td><td><b>{fmt(r["titulo"])}</b></td><td>{fmt(r["observe"])}</td></tr>'
        for r in l["estrutura"])
    extra = "".join(f"<li>{fmt(x)}</li>" for x in l.get("observe_tambem", []))
    orig = []
    for w in d["original"]:
        hebr = w["lingua"].startswith(("hebr", "aram"))
        nvi = (f'<div class="nvi">NVI: <b>{fmt(w["nvi"])}</b></div>' if w.get("nvi") else "")
        orig.append(
            f'<div class="palavra"><div class="grande {"heb" if hebr else "gre"}" dir="{"rtl" if hebr else "ltr"}">{e(w["orig"])}</div>'
            f'<div class="info"><div class="trans"><b>{e(w["translit"])}</b> <span class="tag">{e(w["lingua"])} · {e(w["strong"])}</span></div>'
            f'<div class="pt">“{fmt(w["pt"])}”</div><p>{fmt(w["significado"])}</p>{nvi}'
            f'<div class="minha">Na minha Bíblia: <u></u></div>{pilula(w.get("certeza", "consenso"))}</div></div>')
    con = []
    for c in d["conexoes"]:
        rot, bg = TIPOS.get(c["tipo"], TIPOS["tema"])
        con.append(f'<li><span class="badge" style="background:{bg}">{rot}</span><b>{e(c["ref"])}</b> {fmt(c["texto"])}'
                   f'<span class="ck"></span></li>')
    fontes = "; ".join(e(f) for f in d.get("fontes", []))
    return f"""
<div class="pagina">
  {secao("Leitura guiada — leia o texto na sua Bíblia", "#7EC8FF", "pergaminho",
         f'<table class="est">{estrutura}</table>' + (f'<ul class="obs">{extra}</ul>' if extra else ""))}
  {secao("Palavras no original (o que a tradução esconde)", "#FF7EB6", "lampada", f'<div class="palavras">{"".join(orig)}</div>')}
  {secao("Conexões — outros textos que conversam com este", "#9FD68A", "uvas", f'<ul class="con">{"".join(con)}</ul>')}
  <footer class="fontes">2/3 · Fontes: {fontes or "—"}</footer>
</div>"""


def pagina3(d, cor, forte, clara):
    mem = d.get("memorizar")
    caps = ", ".join(str(c) for c in d["capitulos"])
    refl = "".join(f"<li>{fmt(q)}<div class='ln'></div><div class='ln'></div></li>" for q in d["reflexao"])
    mem_html = (f'<div class="caixa"><h3>♥ Para guardar no coração: {e(mem["ref"])}</h3>'
                f'<p class="peq">{fmt(mem["por_que"]).capitalize()} Escreva o versículo com suas palavras ou copie da sua Bíblia:</p>'
                f'<div class="ln"></div><div class="ln"></div></div>') if mem else ""
    return f"""
<div class="pagina p3">
  <header class="topo mini" style="background:{clara}">
    <div class="tit"><div class="linha1"><span class="pill" style="background:{cor}">DIA {d['dia']}</span>
      <b>{e(d['passagem'])}</b><span class="data">· Registrar</span></div></div>
  </header>
  <div class="caixa"><h3>Penso e respondo</h3><ol class="q">{refl}</ol></div>
  <div class="caixa amarela"><h3>Aplicação para hoje</h3><p class="peq">{fmt(d["aplicacao"])}</p>
    <div class="ln"></div><div class="ln"></div></div>
  {mem_html}
  <div class="caixa"><h3>Resumo em 3 linhas, com as minhas palavras</h3>
    <div class="ln"></div><div class="ln"></div><div class="ln"></div></div>
  <div class="caixa notas"><h3>Minhas anotações e perguntas que ficaram</h3></div>
  <div class="marcar"><b>Fechando o dia:</b> pinte {e(d['livro'])} {e(caps)} no Mapa da Bíblia <span class="cx"></span> ·
    <b>Orei</b> <span class="cx"></span> <b>Li</b> <span class="cx"></span> <b>Estudei</b> <span class="cx"></span> <b>Resumi</b> <span class="cx"></span></div>
  <footer>3/3</footer>
</div>"""


CSS = """
@page { size: 8.5in 11in; margin: 0 }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact }
html, body { margin: 0; background: #FFFDF8 }
body { font-family: 'Nunito','Quicksand','Trebuchet MS','Segoe UI',Verdana,sans-serif; color: %(tinta)s; font-size: 8.6pt; line-height: 1.32 }
.pagina { width: 8.5in; height: 11in; padding: .32in .38in .3in; position: relative; page-break-after: always; overflow: hidden; background: #FFFDF8 }
h1, h2, h3, p { margin: 0 }
.ico { flex: none }
.topo { display: flex; align-items: center; gap: 12px; border-radius: 20px; padding: 8px 16px }
.topo .tit { flex: 1; text-align: center }
.linha1 { display: flex; justify-content: center; align-items: center; gap: 8px; font-size: 8pt }
.pill { color: %(tinta)s; font-weight: 900; border-radius: 99px; padding: 1px 10px; letter-spacing: .4px }
.pill.suave { background: #fff; font-weight: 800 }
.data { color: %(suave)s; font-weight: 700 }
h1 { font-size: 30pt; line-height: 1.05; font-weight: 900; color: var(--forte); margin: 2px 0 }
.sub { font-size: 11pt; font-weight: 800 }
.prog { display: flex; align-items: center; gap: 8px; font-size: 7pt; color: %(suave)s; font-weight: 800; margin: 5px 4px 6px }
.barra { display: flex; gap: 2px; flex: 1 }
.barra i { flex: 1; height: 9px; border: 1.2px solid var(--cor); border-radius: 3px }
.pergunta { display: flex; gap: 10px; align-items: center; background: #FFF1A8; border: 2px dashed #F4B41A; border-radius: 16px; padding: 6px 14px; margin-bottom: 8px }
.pergunta p { font-size: 11pt; font-weight: 800; line-height: 1.25 }
small { display: block; font-size: 6.4pt; letter-spacing: 1px; color: #A07A00; font-weight: 900 }
.duas { display: grid; grid-template-columns: 1fr 1.08fr; gap: 10px; align-items: start; margin-bottom: 8px }
.sec { margin-bottom: 8px }
.sec h2 { display: flex; align-items: center; gap: 6px; border-radius: 99px; padding: 2px 12px 2px 6px; font-size: 9.5pt; font-weight: 900; color: %(tinta)s; width: fit-content; margin-bottom: 4px }
.sec .corpo { padding: 0 2px }
.ficha { border-collapse: collapse; width: 100%% }
.ficha th { text-align: left; vertical-align: top; width: 62px; font-size: 7.6pt; color: var(--forte); padding: 2.5px 4px 2.5px 0; white-space: nowrap }
.ficha td { padding: 2.5px 0; border-bottom: 1px dotted #E2D8F0 }
.cenario { margin-top: 5px; font-size: 8.4pt }
.cert { display: inline-block; font-size: 6pt; font-weight: 900; border-radius: 99px; padding: 0 6px; margin-left: 3px; vertical-align: 1px; white-space: nowrap }
.mapa-caixa .mapa { width: 100%%; height: auto; display: block }
.legenda { font-size: 7pt; color: %(suave)s; margin-top: 3px; line-height: 1.25 }
.tempo { list-style: none; margin: 2px 0 0; padding: 0; display: flex; gap: 4px }
.tempo li { flex: 1; background: #fff; border: 1.6px solid #25C2B0; border-radius: 10px; padding: 3px 5px; position: relative; text-align: center }
.tempo li.dest { background: #D9F5F1; border-width: 2.4px }
.tempo li b { display: block; font-size: 7.6pt; color: #0F7F73 }
.tempo li span { font-size: 7.4pt; line-height: 1.2; display: block }
.nota { font-size: 7.4pt; color: %(suave)s; margin-top: 3px }
.cards { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px }
.cards.n4 { grid-template-columns: 1fr 1fr }
.cards.n2 { grid-template-columns: 1fr 1fr }
.card { background: #fff; border: 1.6px solid var(--k); border-radius: 12px; padding: 5px 7px 6px; break-inside: avoid }
.card .t { display: flex; align-items: center; gap: 4px; font-size: 8.8pt; font-weight: 900; margin-bottom: 2px }
.card p { font-size: 7.9pt; line-height: 1.28; margin-bottom: 2px }
.hora { display: flex; align-items: flex-start; gap: 6px; background: #F0FAF6; border-radius: 14px; padding: 5px 10px; position: absolute; left: .38in; right: .38in; bottom: .58in; font-size: 7.4pt }
.hora > b { align-self: center; width: 66px; font-size: 8.4pt; color: #0F7F73 }
.hora div { flex: 1; text-align: center; display: flex; flex-direction: column; align-items: center }
.hora small { letter-spacing: 0; color: %(suave)s; font-size: 6.8pt; font-weight: 700 }
.cx { display: inline-block; width: 11px; height: 11px; border: 1.6px solid var(--cor); border-radius: 3px; background: #fff; vertical-align: -2px }
footer { position: absolute; left: .38in; right: .38in; bottom: .22in; font-size: 6.4pt; color: %(suave)s; text-align: center }
footer .cert { margin: 0 2px }
/* página 2 */
.est { width: 100%%; border-collapse: collapse; font-size: 8pt }
.est td { padding: 2.2px 5px; border-bottom: 1px dotted #D6E6F5; vertical-align: top }
.est .ref { font-weight: 900; color: #3E86BF; white-space: nowrap; width: 56px }
.obs { margin: 3px 0 0; padding-left: 15px; font-size: 7.9pt }
.palavras { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 8px }
.palavra { display: flex; gap: 7px; background: #fff; border: 1.6px solid #FFB3D1; border-radius: 12px; padding: 5px 7px; break-inside: avoid }
.grande { min-width: 62px; max-width: 74px; display: flex; align-items: center; justify-content: center; text-align: center; background: #FFE3EE; border-radius: 9px; padding: 2px 3px; line-height: 1.1; color: #B2306A }
.grande.heb { font-family: 'SBL Hebrew','Ezra SIL','Times New Roman','Noto Serif Hebrew','DejaVu Serif',serif; font-size: 19pt }
.grande.gre { font-family: 'SBL Greek','Gentium Plus','Times New Roman','Noto Serif','DejaVu Serif',serif; font-size: 14.5pt }
.info { flex: 1; min-width: 0 }
.trans { font-size: 8.4pt }
.tag { font-size: 6.4pt; background: #DFF1FF; color: #2D6FA3; border-radius: 99px; padding: 0 5px; font-weight: 800; white-space: nowrap }
.pt { font-size: 8pt; font-weight: 800; color: #B2306A }
.info p { font-size: 7.6pt; line-height: 1.25 }
.nvi { font-size: 7.2pt; color: %(suave)s }
.minha { font-size: 7pt; color: %(suave)s; display: flex; align-items: flex-end; gap: 3px; margin-top: 1px }
.minha u { flex: 1; border-bottom: 1px solid #CFC4E2; text-decoration: none; height: 9px }
.con { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 12px }
.con li { break-inside: avoid; font-size: 7.8pt; line-height: 1.25; padding: 2.5px 0; border-bottom: 1px dotted #DCEBD2; position: relative; padding-right: 14px }
.badge { font-size: 6pt; font-weight: 900; border-radius: 99px; padding: 0 5px; margin-right: 4px; color: %(tinta)s; vertical-align: 1px }
.con .ck { position: absolute; right: 0; top: 4px; width: 9px; height: 9px; border: 1.4px solid #6DB84F; border-radius: 2.5px }
.fim { display: grid; grid-template-columns: 1.15fr 1fr; gap: 8px; margin-bottom: 7px }
.caixa { background: #fff; border: 1.8px solid var(--cor); border-radius: 14px; padding: 5px 10px 6px }
.caixa.amarela { border-color: #F4B41A; background: #FFF9DC }
.caixa h3 { font-size: 9pt; font-weight: 900; color: var(--forte); margin-bottom: 2px }
.caixa ol { margin: 0; padding-left: 14px; font-size: 7.9pt }
.caixa li { margin-bottom: 1px }
.ln { border-bottom: 1px solid #DDD3EC; height: 25px }
.memo { margin-top: 5px; font-size: 7.9pt; background: #fff; border-radius: 9px; padding: 3px 7px }
.caixa.notas { flex: 1; margin-bottom: 0 }
.pagina.p3 { display: flex; flex-direction: column; gap: 9px; padding-bottom: .95in }
.topo.mini { padding: 5px 12px; border-radius: 14px }
.topo.mini b { font-size: 12pt; color: var(--forte) }
.q { padding-left: 15px; font-size: 8.6pt; font-weight: 700 }
.q li { margin-bottom: 3px }
.peq { font-size: 8.4pt; margin-bottom: 2px }
footer.fontes { text-align: left; line-height: 1.3 }
.marcar { font-size: 8pt; z-index: 2; background: #F0FAF6; border-radius: 12px; padding: 5px 10px; text-align: center; position: absolute; left: .38in; right: .38in; bottom: .5in }
.marcar .cx { margin-right: 5px }
""" % dict(tinta=B.TINTA, suave=B.TINTA_SUAVE)


def montar(d):
    cor = B.BLOCO[d["bloco"]][2]
    forte = B.escurecer(cor, 0.38)
    clara = B.misturar(cor, 0.72)
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Dia {d["dia"]} · {e(d["passagem"])}</title>'
            f'<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">'
            f'<style>{CSS}body{{--cor:{cor};--forte:{forte};--clara:{clara}}}</style></head><body>'
            f'{pagina1(d, cor, forte, clara)}{pagina2(d, cor, forte, clara)}'
            f'{pagina3(d, cor, forte, clara)}</body></html>')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    arq = Path(a.json)
    d = json.loads(arq.read_text(encoding="utf-8"))
    d.setdefault("total_dias", len(B.ler_plano()) if B.ARQ_PLANO.exists() else 562)
    saida = arq.with_suffix(".html")
    saida.write_text(montar(d), encoding="utf-8")
    print(f"OK {saida}")
    if a.pdf and exportar_pdf(saida, saida.with_suffix(".pdf")):
        print(f"OK {saida.with_suffix('.pdf')}")
