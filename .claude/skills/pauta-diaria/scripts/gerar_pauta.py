#!/usr/bin/env python3
"""
Gerador da Pauta Diária — painel visual de aprovação da WeWiki.

Lê um pauta.json descrevendo as peças do dia (uma por marca/plataforma) e
monta um único arquivo HTML autocontido: imagens embutidas em base64, legenda
copiável, botões de aprovar/refazer com estado salvo no navegador.

Autocontido de propósito — abre offline, pode ser movido de pasta, mandado por
WhatsApp e continua funcionando.

Uso:
    python gerar_pauta.py <pauta.json> [--output pauta.html]
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path

# Cores de marca — espelham CONTEXTO-MARCA.md / tema do gerador de carrossel.
CORES_MARCA = {
    "Bowl Green": {"fundo": "#F2EFE4", "tinta": "#24573A", "acento": "#C9A24B"},
    "Clean Touch Cabinets": {"fundo": "#F0DDD3", "tinta": "#36646E", "acento": "#A9634A"},
}
COR_PADRAO = {"fundo": "#EEF1F4", "tinta": "#2B3A42", "acento": "#6B7C87"}

EXTENSOES_IMAGEM = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def chave_ordem_natural(caminho):
    """slide-2 antes de slide-10."""
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", caminho.name)]


def embutir(caminho):
    """Lê um arquivo de imagem e devolve um data: URI."""
    mime = EXTENSOES_IMAGEM.get(caminho.suffix.lower())
    if not mime:
        return None
    dados = base64.b64encode(caminho.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{dados}"


def escapar(texto):
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def coletar_slides(pasta, excluir, arquivos=None):
    """Devolve os slides de uma peça, em ordem, sem os arquivos de prévia.

    `arquivos` permite apontar imagens específicas dentro da pasta — é o que
    deixa cada post ter a sua própria legenda, em vez de uma legenda para a
    pasta inteira.
    """
    if not pasta.is_dir():
        return []
    if arquivos:
        escolhidos = [pasta / a for a in arquivos]
        faltando = [p.name for p in escolhidos if not p.is_file()]
        if faltando:
            print(f"  ! não achei em {pasta}: {', '.join(faltando)}", file=sys.stderr)
        return [p for p in escolhidos if p.is_file()]
    ignorar = {"preview.png", "preview.mp4"} | set(excluir)
    slides = sorted(
        [p for p in pasta.glob("slide-*") if p.suffix.lower() in EXTENSOES_IMAGEM and p.name not in ignorar],
        key=chave_ordem_natural,
    )
    if not slides:
        slides = sorted(
            [p for p in pasta.glob("*") if p.suffix.lower() in EXTENSOES_IMAGEM and p.name not in ignorar],
            key=chave_ordem_natural,
        )
    return slides


def montar_peca(peca, raiz, indice):
    marca = peca.get("marca", "Sem marca")
    cores = CORES_MARCA.get(marca, COR_PADRAO)
    pasta = raiz / peca["pasta"] if not Path(peca["pasta"]).is_absolute() else Path(peca["pasta"])
    slides = coletar_slides(pasta, peca.get("excluir", []), peca.get("arquivos"))

    if not slides:
        print(f"  ! Nenhum slide encontrado em {pasta}", file=sys.stderr)

    miniaturas = []
    for n, s in enumerate(slides, 1):
        uri = embutir(s)
        if not uri:
            continue
        miniaturas.append(
            f'<figure class="slide"><img src="{uri}" alt="Slide {n}" loading="lazy" '
            f'onclick="ampliar(this.src)"><figcaption>{n:02d}</figcaption></figure>'
        )

    legenda = peca.get("legenda", "")
    hashtags = peca.get("hashtags", "")
    texto_copiavel = legenda + (("\n\n" + hashtags) if hashtags else "")
    nota = peca.get("observacao", "")

    aviso = ""
    if peca.get("atencao"):
        aviso = f'<p class="atencao">⚠ {escapar(peca["atencao"])}</p>'

    return f"""
<section class="peca" id="peca-{indice}" data-peca="{indice}"
         style="--fundo:{cores['fundo']};--tinta:{cores['tinta']};--acento:{cores['acento']}">
  <header class="peca-topo">
    <div class="identidade">
      <span class="chip">{escapar(marca)}</span>
      <span class="handle">{escapar(peca.get('handle', ''))}</span>
    </div>
    <div class="meta">
      <span class="plataforma">{escapar(peca.get('plataforma', ''))}</span>
      <span class="contagem">{len(miniaturas)} {'peça' if len(miniaturas) == 1 else 'peças'}</span>
      <span class="selo" data-selo>pendente</span>
    </div>
  </header>

  {f'<p class="angulo">{escapar(peca["angulo"])}</p>' if peca.get("angulo") else ""}
  {aviso}

  <div class="tira">{''.join(miniaturas) or '<p class="vazio">Sem imagens nesta pasta.</p>'}</div>

  <div class="legenda-bloco">
    <div class="legenda-topo">
      <h3>Legenda</h3>
      <button class="btn-copiar" onclick="copiar({indice}, this)">copiar</button>
    </div>
    <pre class="legenda" id="legenda-{indice}">{escapar(texto_copiavel)}</pre>
  </div>

  {f'<p class="nota"><strong>Nota do time:</strong> {escapar(nota)}</p>' if nota else ""}

  <div class="acoes">
    <button class="btn aprovar" onclick="decidir({indice}, 'aprovada')">✓ Aprovar</button>
    <button class="btn refazer" onclick="decidir({indice}, 'refazer')">✗ Refazer</button>
    <input class="comentario" id="comentario-{indice}" placeholder="o que mudar? (opcional)"
           oninput="salvarComentario({indice}, this.value)">
  </div>
</section>
"""


CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 0 0 80px;
  font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  background: #F5F6F8; color: #14181C; line-height: 1.5;
}
header.topo {
  position: sticky; top: 0; z-index: 50;
  background: rgba(255,255,255,.92); backdrop-filter: blur(10px);
  border-bottom: 1px solid #E2E6EA; padding: 18px 28px;
  display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap;
}
header.topo h1 { margin: 0; font-size: 19px; font-weight: 700; letter-spacing: -.2px; }
header.topo .data { font-size: 14px; color: #63707A; }
header.topo .progresso {
  margin-left: auto; font-size: 13px; font-weight: 600;
  background: #14181C; color: #fff; padding: 5px 12px; border-radius: 999px;
}
main { max-width: 1240px; margin: 0 auto; padding: 28px 20px 0; }

.peca {
  background: #fff; border: 1px solid #E2E6EA; border-radius: 16px;
  padding: 22px; margin-bottom: 26px;
  box-shadow: 0 1px 2px rgba(20,24,28,.04), 0 8px 24px rgba(20,24,28,.05);
  border-left: 5px solid var(--tinta);
}
.peca[data-estado="aprovada"] { border-left-color: #1B9C5B; }
.peca[data-estado="refazer"]  { border-left-color: #D2453A; opacity: .82; }

.peca-topo { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; margin-bottom: 6px; }
.identidade { display: flex; align-items: baseline; gap: 10px; }
.chip {
  background: var(--fundo); color: var(--tinta);
  font-weight: 700; font-size: 14px; padding: 5px 12px; border-radius: 8px;
}
.handle { font-size: 13px; color: #7A8791; }
.meta { margin-left: auto; display: flex; align-items: center; gap: 12px; font-size: 12px; color: #63707A; }
.plataforma { font-weight: 600; color: #46525B; }
.selo { text-transform: uppercase; letter-spacing: .06em; font-weight: 700; font-size: 11px;
        padding: 3px 9px; border-radius: 999px; background: #EDF0F3; color: #63707A; }
.selo[data-v="aprovada"] { background: #E3F5EB; color: #12703F; }
.selo[data-v="refazer"]  { background: #FCE8E6; color: #A32B22; }

.angulo { margin: 4px 0 0; font-size: 14px; color: #46525B; font-style: italic; }
.atencao { margin: 10px 0 0; font-size: 13px; background: #FFF6E5; border-left: 3px solid #E0A526;
           padding: 9px 12px; border-radius: 6px; color: #6B4E12; }

/* Envolve em vez de rolar: a Gê precisa ver o carrossel inteiro de uma vez.
   Carrosséis longos caem para uma segunda linha em vez de esconder slides. */
.tira {
  display: flex; flex-wrap: wrap; gap: 12px; padding: 16px 4px 14px; margin: 12px -4px;
}
.slide { margin: 0; flex: 0 0 auto; text-align: center; }
.slide img {
  height: 260px; width: auto; display: block; border-radius: 10px;
  border: 1px solid #E2E6EA; cursor: zoom-in;
  transition: transform .15s ease, box-shadow .15s ease;
}
.slide img:hover { transform: translateY(-3px); box-shadow: 0 10px 26px rgba(20,24,28,.16); }
.slide figcaption { font-size: 11px; color: #97A2AB; margin-top: 6px; font-variant-numeric: tabular-nums; }
.vazio { color: #97A2AB; font-size: 14px; font-style: italic; }

.legenda-bloco { margin-top: 6px; }
.legenda-topo { display: flex; align-items: center; gap: 10px; }
.legenda-topo h3 { margin: 0; font-size: 12px; text-transform: uppercase; letter-spacing: .07em; color: #7A8791; }
.btn-copiar {
  margin-left: auto; font: inherit; font-size: 12px; font-weight: 600;
  background: #fff; color: var(--tinta); border: 1px solid var(--tinta);
  padding: 4px 12px; border-radius: 7px; cursor: pointer;
}
.btn-copiar:hover { background: var(--fundo); }
.legenda {
  margin: 8px 0 0; padding: 14px 16px; background: var(--fundo); color: #14181C;
  border-radius: 10px; font: inherit; font-size: 14.5px; white-space: pre-wrap;
  word-break: break-word;
}
.nota { font-size: 13px; color: #46525B; background: #F2F4F6; padding: 10px 13px;
        border-radius: 8px; margin: 12px 0 0; }

.acoes { display: flex; gap: 10px; align-items: center; margin-top: 16px; flex-wrap: wrap; }
.btn { font: inherit; font-size: 14px; font-weight: 600; padding: 9px 18px;
       border-radius: 9px; cursor: pointer; border: 1px solid transparent; }
.aprovar { background: #14181C; color: #fff; }
.aprovar:hover { background: #000; }
.refazer { background: #fff; color: #A32B22; border-color: #E8B6B1; }
.refazer:hover { background: #FCE8E6; }
.comentario {
  flex: 1; min-width: 200px; font: inherit; font-size: 14px;
  padding: 9px 13px; border: 1px solid #DDE2E7; border-radius: 9px; background: #FBFCFD;
}
.comentario:focus { outline: 2px solid #14181C; outline-offset: -1px; }

.rodape { max-width: 1240px; margin: 8px auto 0; padding: 0 20px; }
.rodape button {
  font: inherit; font-size: 14px; font-weight: 600; padding: 11px 20px;
  border-radius: 10px; border: 1px solid #14181C; background: #fff; cursor: pointer;
}
.rodape button:hover { background: #14181C; color: #fff; }
#resumo { margin-top: 14px; padding: 16px; background: #fff; border: 1px solid #E2E6EA;
          border-radius: 12px; white-space: pre-wrap; font-size: 14px; display: none; }

#lupa {
  position: fixed; inset: 0; background: rgba(10,12,14,.93); display: none;
  align-items: center; justify-content: center; z-index: 200; cursor: zoom-out; padding: 24px;
}
#lupa img { max-width: 96vw; max-height: 94vh; border-radius: 10px; }

@media (prefers-color-scheme: dark) {
  body { background: #101417; color: #E9EDF0; }
  header.topo { background: rgba(22,27,31,.94); border-bottom-color: #262E34; }
  header.topo .progresso { background: #E9EDF0; color: #101417; }
  .peca { background: #171C20; border-color: #262E34; box-shadow: none; }
  .legenda { color: #14181C; }
  .nota { background: #1D242A; color: #B9C4CC; }
  .comentario { background: #1D242A; border-color: #303941; color: #E9EDF0; }
  .btn-copiar { background: #171C20; }
  .aprovar { background: #E9EDF0; color: #101417; }
  .refazer { background: #171C20; }
  #resumo { background: #171C20; border-color: #262E34; }
  .slide img { border-color: #262E34; }
}
@media (max-width: 640px) {
  .slide img { height: 200px; }
  main { padding: 18px 12px 0; }
  .peca { padding: 16px; }
}
@media print {
  header.topo { position: static; }
  .acoes, .btn-copiar, .rodape { display: none; }
  .tira { overflow: visible; flex-wrap: wrap; }
}
"""

JS = """
const DIA = "%%DIA%%";
const TOTAL = %%TOTAL%%;
const chave = i => `pauta:${DIA}:${i}`;

function decidir(i, valor) {
  const atual = JSON.parse(localStorage.getItem(chave(i)) || "{}");
  atual.estado = atual.estado === valor ? null : valor;
  localStorage.setItem(chave(i), JSON.stringify(atual));
  pintar(i);
  contar();
}

function salvarComentario(i, texto) {
  const atual = JSON.parse(localStorage.getItem(chave(i)) || "{}");
  atual.comentario = texto;
  localStorage.setItem(chave(i), JSON.stringify(atual));
}

function pintar(i) {
  const dados = JSON.parse(localStorage.getItem(chave(i)) || "{}");
  const secao = document.getElementById("peca-" + i);
  if (!secao) return;
  const selo = secao.querySelector("[data-selo]");
  if (dados.estado) {
    secao.dataset.estado = dados.estado;
    selo.dataset.v = dados.estado;
    selo.textContent = dados.estado;
  } else {
    delete secao.dataset.estado;
    delete selo.dataset.v;
    selo.textContent = "pendente";
  }
  const campo = document.getElementById("comentario-" + i);
  if (campo && dados.comentario) campo.value = dados.comentario;
}

function contar() {
  let aprovadas = 0;
  for (let i = 0; i < TOTAL; i++) {
    const d = JSON.parse(localStorage.getItem(chave(i)) || "{}");
    if (d.estado === "aprovada") aprovadas++;
  }
  document.getElementById("progresso").textContent = aprovadas + " de " + TOTAL + " aprovadas";
}

function copiar(i, botao) {
  const texto = document.getElementById("legenda-" + i).textContent;
  navigator.clipboard.writeText(texto).then(() => {
    const antes = botao.textContent;
    botao.textContent = "copiado ✓";
    setTimeout(() => { botao.textContent = antes; }, 1400);
  });
}

function ampliar(src) {
  const lupa = document.getElementById("lupa");
  lupa.querySelector("img").src = src;
  lupa.style.display = "flex";
}

function resumir() {
  const linhas = [];
  document.querySelectorAll(".peca").forEach(secao => {
    const i = secao.dataset.peca;
    const d = JSON.parse(localStorage.getItem(chave(i)) || "{}");
    const marca = secao.querySelector(".chip").textContent;
    const plataforma = secao.querySelector(".plataforma").textContent;
    let linha = `• ${marca} — ${plataforma}: ${d.estado || "pendente"}`;
    if (d.comentario) linha += `\\n    ajuste: ${d.comentario}`;
    linhas.push(linha);
  });
  const caixa = document.getElementById("resumo");
  caixa.textContent = `Pauta de ${DIA}\\n\\n` + linhas.join("\\n");
  caixa.style.display = "block";
  navigator.clipboard.writeText(caixa.textContent);
}

document.addEventListener("DOMContentLoaded", () => {
  for (let i = 0; i < TOTAL; i++) pintar(i);
  contar();
  document.getElementById("lupa").addEventListener("click", e => { e.currentTarget.style.display = "none"; });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") document.getElementById("lupa").style.display = "none";
  });
});
"""

PAGINA = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pauta de %%DIA_BR%% — WeWiki</title>
<style>%%CSS%%</style>
</head>
<body>
<header class="topo">
  <h1>Pauta do dia</h1>
  <span class="data">%%DIA_BR%%</span>
  <span class="progresso" id="progresso">0 de %%TOTAL%% aprovadas</span>
</header>

<main>
%%PECAS%%
</main>

<div class="rodape">
  <button onclick="resumir()">Fechar a pauta e copiar o veredito</button>
  <div id="resumo"></div>
</div>

<div id="lupa"><img alt="slide ampliado"></div>
<script>%%JS%%</script>
</body>
</html>
"""

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def data_por_extenso(iso):
    try:
        ano, mes, dia = iso.split("-")
        return f"{int(dia)} de {MESES[int(mes) - 1]} de {ano}"
    except (ValueError, IndexError):
        return iso


def main():
    ap = argparse.ArgumentParser(description="Gera o painel HTML da pauta diária")
    ap.add_argument("pauta_json", help="Caminho do pauta.json do dia")
    ap.add_argument("--output", default=None, help="Saída (padrão: pauta.html ao lado do JSON)")
    args = ap.parse_args()

    caminho_json = Path(args.pauta_json)
    if not caminho_json.is_file():
        print(f"Erro: não encontrei {caminho_json}", file=sys.stderr)
        sys.exit(1)

    with open(caminho_json, "r", encoding="utf-8") as f:
        pauta = json.load(f)

    raiz = caminho_json.parent.parent  # pauta.json vive em Entregas/<dia>-pauta/
    dia = pauta.get("data", "")
    pecas = pauta.get("pecas", [])

    if not pecas:
        print("Erro: a pauta não tem nenhuma peça.", file=sys.stderr)
        sys.exit(1)

    print(f"Montando a pauta de {dia} — {len(pecas)} peça(s):")
    blocos = []
    for i, peca in enumerate(pecas):
        print(f"  [{i + 1}/{len(pecas)}] {peca.get('marca')} — {peca.get('plataforma')}")
        blocos.append(montar_peca(peca, raiz, i))

    html = (
        PAGINA.replace("%%CSS%%", CSS)
        .replace("%%JS%%", JS.replace("%%DIA%%", dia).replace("%%TOTAL%%", str(len(pecas))))
        .replace("%%PECAS%%", "\n".join(blocos))
        .replace("%%DIA_BR%%", data_por_extenso(dia))
        .replace("%%TOTAL%%", str(len(pecas)))
    )

    saida = Path(args.output) if args.output else caminho_json.parent / "pauta.html"
    saida.write_text(html, encoding="utf-8")
    tamanho = saida.stat().st_size / 1024
    print(f"\nPauta pronta: {saida}")
    print(f"Autocontida — {tamanho:.0f} KB, abre offline.")


if __name__ == "__main__":
    main()
