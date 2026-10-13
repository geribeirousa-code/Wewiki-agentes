---
name: estudo-biblico-diario
description: Monta o estudo bíblico do dia da Gê — folha impressa de 3 páginas (contexto histórico e cultural, mapa, linha do tempo, palavras no hebraico/grego original, conexões entre livros, espaço para anotar) e mantém o Mapa de Progresso da Bíblia para imprimir e marcar. Use quando ela disser "estudo de hoje", "estudo bíblico", "próximo estudo", "monta o estudo do dia", "terminei o estudo", "marca como lido", "atualiza meu mapa da Bíblia" ou "reimprime o mapa".
---

# Estudo Bíblico Diário

**Objetivo da Gê:** 1 hora de estudo por dia, 6 dias por semana (domingo livre), indo fundo no **contexto, na cultura e no texto original**, não só lendo um capítulo. Plano de 562 dias (~21 meses) cobrindo os 1.189 capítulos, na ordem que ela já usava:
Lei → Históricos → Poéticos → Profetas → Evangelhos → Atos → Cartas de Paulo → Cartas Gerais → Apocalipse.

Tradução de apoio dela: **NVI** (Bíblia de estudo). Sempre citar por referência (ex.: Gn 1:27), nunca copiar capítulos inteiros.

## O que existe

| Onde | O que é |
|---|---|
| `Bíblia/plano.json` | os 562 dias (livro, capítulos, data prevista) |
| `Bíblia/progresso.json` | capítulos já estudados (o "cursor" do plano) |
| `Bíblia/mapa-de-progresso.html/.pdf` | folha Carta frente e verso, dobrada cabe na Bíblia; capítulos feitos saem marcados |
| `Bíblia/estudos/DIA-NNN-slug.json/.html/.pdf` | o estudo de cada dia (JSON = conteúdo; HTML/PDF = folha) |
| `.claude/skills/estudo-biblico-diario/scripts/` | geradores (Python, só biblioteca padrão; PDF opcional com Playwright) |

**Modelo de referência do JSON:** `Bíblia/estudos/DIA-001-genesis-1-2.json`. Copie a estrutura; não invente campos.

## Regra de ouro: fidelidade ao original

Foi o pedido central da Gê: **o mais próximo possível do hebraico/aramaico/grego**, sempre apontando onde a tradução esconde ou muda algo (ex.: "amor" → *agapē*, *philía*…).

1. **Texto-base:** AT = hebraico (Texto Massorético; aramaico em Ed 4:8–6:18, 7:12–26, Dn 2:4b–7:28, Jr 10:11). NT = grego koiné.
2. **Cada palavra do original precisa de fonte consultada na sessão** (léxico Strong + BDB/HALOT para hebraico; BDAG/Thayer para grego; Blue Letter Bible, STEP Bible, Bible Hub ou Sefaria). Se não conseguiu verificar, **não coloque o cartão**. Nunca chute número de Strong ou grafia.
3. **Selo de certeza em tudo que é afirmação:** `consenso` (aceito pela grande maioria), `maioria` (maioria dos estudiosos, com divergentes), `debate` (posições legítimas diferentes), `texto` (está literalmente no texto). Em debate, apresente as posições com justiça; não escolha lado pela Gê.
4. **Não infle diferença entre sinônimos.** Ex.: *agapaō* × *phileō* em Jo 21:15–17: muitos estudiosos veem variação de estilo, não dois "níveis" de amor. Cuidado com a falácia da raiz (D. A. Carson, *Exegetical Fallacies*): o sentido vem do uso no contexto, não só da etimologia.
5. **Tradução:** só frases curtas da NVI e só quando você tem certeza do texto; senão deixe vazio (a folha já tem a linha "Na minha Bíblia: ___" para ela preencher). NVI tem direitos autorais (Biblica).
6. **Contexto histórico/cultural:** cite a fonte (comentário, dicionário bíblico, obra acadêmica). Datas e autoria quase sempre são `debate`; diga as duas linhas.
7. **Sem viés denominacional.** A Gê pediu para não se preocupar com a igreja: o estudo mostra o texto e as leituras, sem doutrinar.
8. **Nunca invente lugares ou coordenadas.** Mapa só usa lugares de `dados/lugares.json`; sítios incertos levam o marcador `"inc"` (aparecem tracejados). Precisa de lugar novo? Adicione ao `lugares.json` com fonte.

## Roteiro de uma sessão ("estudo de hoje")

1. **Onde estamos.** `python .claude/skills/estudo-biblico-diario/scripts/marcar.py --status` (próximo capítulo) e ache a linha correspondente em `Bíblia/plano.json`. Se `plano.json` não existir: `python .../gerar_plano.py`.
2. **Corte do dia.** O plano é nominal. Ajuste ±1 capítulo para não partir uma narrativa ao meio (ex.: o dilúvio). O que vale é o cursor de capítulos em `progresso.json`. O dia pode ser mais leve ou pesado conforme a densidade (Levítico, Isaías e Romanos pedem mais tempo por capítulo).
3. **Pesquisa (Larry → Pax).** Larry roteia para o **Pax** um briefing: passagem do dia, perguntas de contexto (autor, data, destinatários, cenário político/cultural, geografia), palavras-chave candidatas (4–8) e conexões. Pax devolve com fontes e selos de certeza. Larry não escreve conteúdo bíblico de memória sem checar.
4. **Escrever o JSON** `Bíblia/estudos/DIA-<NNN>-<livro>-<cap>.json` (NNN com 3 dígitos; slug sem acento, ex.: `DIA-002-genesis-3-4`).
5. **Gerar a folha:** `python .../gerar_folha.py "Bíblia/estudos/DIA-002-genesis-3-4.json" --pdf` (sem `--pdf` se não houver Playwright; o HTML imprime direto).
6. **Mostrar:** rode uma captura das 3 páginas (a Gê é visual: ela aprova olhando) e confira que nada estourou a página.
7. **Quando ela disser que terminou:** `python .../marcar.py <Livro> <cap-cap>` e depois `python .../gerar_mapa.py --pdf` (o mapa sai atualizado, com ✓ nos capítulos feitos). Ela só reimprime quando quiser.
8. **Feriado/atraso:** não existe "dia perdido". O cursor segue de onde parou; as datas do plano são previsões.

### Lente por bloco (o que priorizar no contexto)

| Bloco | Olhe para |
|---|---|
| Lei | aliança e leis no contexto do Antigo Oriente Próximo (tratados, ritos, vizinhos); estrutura do livro |
| Históricos | linha do tempo dos reis (Israel × Judá), potências (Assíria, Babilônia, Pérsia), geografia das batalhas |
| Poéticos | paralelismo hebraico, gênero do salmo (lamento, louvor, realeza), autoria/título, vida cotidiana |
| Profetas | rei e potência da época, a crise que o profeta enfrenta, o gênero do oráculo, o que o NT cita |
| Evangelhos | Jesus judeu do século I, paralelos entre os evangelhos, termos aramaicos, o público de cada autor |
| Atos e Cartas | a cidade, a igreja e a ocasião de cada carta; mapa das viagens (`regiao: "mediterraneo"` + `rotas`) |
| Apocalipse | gênero apocalíptico, alusões ao AT (cada símbolo tem fonte), as 7 cidades (`regiao: "asia-menor"`) |

## Formato do JSON do dia

Chaves obrigatórias: `dia`, `data`, `bloco`, `sigla`, `livro`, `capitulos`, `passagem`, `titulo`, `pergunta_guia`, `contexto` (`ficha`, `cenario`, `cultura` com 2–4 cartões), `linha_do_tempo`, `leitura` (`estrutura`, `observe_tambem`), `original` (4–8 palavras), `conexoes` (8–12), `reflexao` (3 perguntas), `aplicacao`, `fontes`. Opcionais: `mapa`, `memorizar`.

- `bloco`: `lei`, `historicos`, `poeticos`, `profetas`, `evangelhos`, `atos`, `paulinas`, `gerais`, `apocalipse`.
- `ficha`: lista de `[rótulo, texto, certeza]`. `cultura[]`: `titulo`, `texto`, `certeza`, `icone`.
- `linha_do_tempo.itens`: `rotulo` (ano ou dia) + `texto`; `destaque: true` marca o que importa hoje. Para livros datados, use anos a.C./d.C. com o selo de certeza em `nota`.
- `mapa`: `regiao` (`canaa`, `egito`, `oriente-medio`, `mesopotamia`, `asia-menor`, `mediterraneo`, `auto`), `lugares[]` (nomes de `dados/lugares.json`), `rotas[{lugares, cor}]`, `rios_destaque[]`, `textos[{texto, lon, lat}]` (nomes de regiões/impérios), `legenda`.
- `original[]`: `pt`, `orig` (em hebraico/grego, com vogais), `translit`, `lingua`, `strong`, `significado`, `certeza`, opcional `nvi`.
- `conexoes[]`: `ref`, `tipo` (`cita`, `eco`, `paralelo`, `cumprimento`, `tema`, `contraste`, `personagem`), `texto`.
- Marcação leve em texto: `**negrito**` e `_itálico_`.
- Ícones disponíveis: `python -c "import icones; print(icones.nomes())"` (rode de dentro de `scripts/`).

## Folha impressa (3 páginas, Carta)

1. **Entender:** cabeçalho do bloco, pergunta do dia, ficha do livro, mapa, linha do tempo, "O mundo daquele tempo", e a faixa da hora de estudo (0–5 oração · 5–15 contexto · 15–30 leitura · 30–45 original · 45–55 conexões · 55–60 resumo).
2. **Estudar:** leitura guiada por trechos, palavras no original, conexões com caixinha para marcar.
3. **Registrar:** perguntas, aplicação, versículo para guardar, resumo, anotações e fechamento do dia. Imprima 1–2 frente e verso; a 3ª pode usar o verso em branco para anotar.

**Cores:** fundo claro; paleta rosa babalu/candy, amarelo ouro/girassol, verde pistache, azul turquesa e azul candy. Mantenha (ver `scripts/biblia.py`, `BLOCOS`).

## Mapa de Progresso (impressão e dobra)

`python .../gerar_mapa.py --pdf` gera `Bíblia/mapa-de-progresso.pdf`: **1 folha Carta frente e verso**, dobrada duas vezes (fica com ~10,8 × 14 cm) para guardar dentro da Bíblia. Um quadradinho por capítulo, uma cor por bloco, selos dos 9 blocos, barra geral de progresso e linhas para versículos marcados. Impressão: papel Carta, **sem margens**, **gráficos de plano de fundo ligados**, frente e verso (virar pela borda longa).

## Planner impresso (estilo botânico, para encadernar)

Direção visual da Gê (referência: planner floral em espiral): fundo creme, verde-sálvia, rosa-blush, mostarda, terracota e azul; títulos serifados com toques manuscritos; ilustrações de tulipas, margaridas e folhas; cada semana com uma cor própria. **Não copiar marca, logotipo nem texto do produto de referência**; só a estética.

`python .../planner.py --pdf` gera `Bíblia/planner/planner-prototipo.pdf` (Carta; margem da espiral à esquerda nas páginas ímpares e à direita nas pares).

Estrutura planejada: **capa → boas-vindas → sumário → [por semana: abertura (2 páginas) + 6 páginas de dia]**. Conteúdo em `Bíblia/planner/semanas/SEMANA-NN.json` (visão geral, pano de fundo, mapa, linha do tempo, plano de leitura, palavras da semana, bênção) e nos `DIA-NNN-*.json` (use `leitura.estrutura_planner` com 6 linhas; o planner mostra até 6 palavras e 6 conexões, 2 perguntas). As mesmas regras de fidelidade ao original e de selos de certeza valem aqui.

Status: **protótipo de 6 páginas** (capa, boas-vindas, sumário, semana 1 em 2 páginas, dia 1). Falta produzir as 94 semanas e dividir em volumes para encadernar.

## Limites honestos

- Mapas são **esquemáticos** (contorno Natural Earth, domínio público; rios desenhados à mão). Não servem como cartografia.
- Strong/BDB são ferramentas de apoio, não a última palavra: o estudo cita, mas a Gê pode e deve cruzar com a Bíblia de estudo dela.
- Capas de bloco (visão geral e linha do tempo de cada bloco) ainda **não estão automatizadas**; peça ao Larry se quiser.
