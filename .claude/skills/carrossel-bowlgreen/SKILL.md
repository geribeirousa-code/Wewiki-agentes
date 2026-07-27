---
name: carrossel-bowlgreen
description: Gera carrossel do Instagram da Bowl Green desenhado no Design System oficial da marca — fonte Lufga, paleta verde/creme/dourado/coral, logo e arco de tigela. Slides são peças gráficas, não cards de texto. Use para qualquer carrossel, post ou peça visual da Bowl Green (@bowlgreenxerem).
---

# Carrossel Bowl Green — no Design System da marca

Renderiza cada slide como HTML e fotografa em **1080x1350** (4:5 do Instagram) com Playwright. Diferente do [[carrossel-opiniao]], que imita um post de X/Twitter: aqui o slide é peça gráfica da marca.

## Regra zero — a ficha técnica manda

**Antes de escrever qualquer legenda ou chip de ingrediente, consulte `dados/fichas.json`.** Ele tem a composição exata de 28 pratos — ingrediente e gramagem — extraída do `Painel-Precificacao-BowlGreen.html`, que é a fonte de verdade da casa.

```bash
python .claude/skills/carrossel-bowlgreen/scripts/extrair_fichas.py   # reextrai quando o painel mudar
```

Nunca descreva um prato de memória. Já saiu "sunomono" num poke que tem pepino, e "200g" num poke que tem 100g.

**A proteína é somada, não presumida.** Poke Tropical = salmão 100g **+** camarão 100g = **200g**. Poke Frutos do Mar = salmão 100g + peixe branco 100g = 200g. Os demais pokes têm 100g; saladas e pratos da casa, 150g; Salmão Deluxe e Sun Salmão, 160g; wraps e oniguiris, 50g.

## Regra de preço

**Nenhum post de feed leva preço.** A tabela muda e o post fica no ar para sempre com o valor errado.

Preço só em **story**, que expira em 24h — e mesmo assim só quando a Gê pedir explicitamente. O campo `preco` existe nos formatos `produto` e `raio-x`, mas fica de fora por padrão.

## Regra número um

**Não invente layout.** O `Bowl Green — Design System.html` tem os componentes prontos. Cada tipo de slide aqui reproduz um que já existe lá. Antes de criar um tipo novo, abra o Design System e procure — quase sempre já está desenhado.

## As 4 vozes tipográficas

O sistema tem quatro vozes e cada uma tem função. Usar a errada quebra a marca:

| Voz | Fonte | Onde entra |
|---|---|---|
| 1 · Display | **Luckiest Guy** | Badges, números gigantes, palavra de capa. **Sempre CAIXA-ALTA. Nunca em texto corrido.** |
| 2 · Números | **Shantell Sans** | Preços, valores de comparativo, números anotados à mão. |
| 3 · Giz | **Chalkiez** | Confissões, aspas de review, frases manuscritas, assinaturas. |
| 4 · Interface | **Lufga** (400·500·700·800·900) | Título de card, corpo, labels de seção. |

Os arquivos vivem em `.agents/skills/carrossel-opiniao/fonts/bowlgreen/`. Lufga e Chalkiez saíram dos `@font-face` embutidos no próprio Design System; Luckiest Guy e Shantell Sans vieram do Google Fonts que o documento carrega.

> ⚠️ O script **aborta** se faltar qualquer uma. É de propósito: uma vez o caminho estava errado, tudo caiu em fonte de sistema, e o carrossel saiu parecendo genérico sem ninguém perceber.

## Paleta e proporção

```
creme        #EDEADB  40%     verde         #24573A  25%     dourado  #C9A24B  5%
creme claro  #F5F1E6          verde escuro  #1C3527          coral    #E8684A  10%
sálvia       #BACFBB  20%     menta         #BFE3CC          rosa     #FFDFD5
```

**A proporção é regra, não sugestão.** O creme domina — ele é o fundo padrão do slide. Verde escuro é acento de card, não fundo de peça. Dourado aparece em 5%: número gigante e pílula de ação.

## Personalidade

Divertida (nunca boba) · Nobre (nunca esnobe) · Fresca (nunca "fitness").

## Os cinco tipos de slide

| Tipo | Componente do DS | Para quê |
|---|---|---|
| `mito-verdade` | MITOS × VERDADES | Linhas rosa com pílula MITO e texto riscado em coral, fechando num card menta com a VERDADE em Luckiest Guy. |
| `expectativa` | EXPECTATIVA × REALIDADE | Card claro com a fala em giz, disco dourado "vs" no meio, card verde com a realidade e chips. |
| `numerao` | Card de número da comunidade | Card verde escuro, numeral gigante em dourado, label espaçada e linha de giz. |
| `faq` | BOWL GREEN RESPONDE | Balão de pergunta manuscrita + balão verde de resposta + chip de WhatsApp. |
| `cta` | Fechamento com faixa mosaico | Logo dourado, display gigante, chips, pílula dourada e assinatura em giz. |

A **faixa mosaico** (motivos chapados da marca) entra como divisória e banda de capa.

## Posts com foto real — `gerar_posts.py`

Quando a peça é sobre um prato, a foto é a protagonista. Quatro formatos:

| Tipo | Tamanho | Componente |
|---|---|---|
| `produto` | 1080×1350 | Faixa verde + logo, prato em disco menta, nome, preço em Shantell coral, chips |
| `raio-x` | 1080×1350 | Prato ao centro, seis marcações com linha pontilhada dourada. É o que mais traduz valor |
| `comparativo` | 1080×1350 | Dois pratos, badges Luckiest Guy, linhas de comparação em coral |
| `story` | 1080×1920 | Fundo coral cheio, prato grande, pílula creme. Só novidade e urgência |

```bash
python .claude/skills/carrossel-bowlgreen/scripts/gerar_posts.py \
  "Entregas/AAAA-MM-DD-bowlgreen-feed/config.json" \
  "Entregas/AAAA-MM-DD-bowlgreen-feed"
```

O campo `foto` recebe o **nome do arquivo sem extensão**, como está no disco (`POKE SORA`, `POKE TROPICAL`). Não precisa renomear nada.

### Recorte de fundo — `recortar_fundo.py`

As fotos de prato vêm em fundo branco de estúdio. Coladas sobre o creme da marca, viram um quadrado branco. Este script transforma o branco em transparência:

```bash
python .claude/skills/carrossel-bowlgreen/scripts/recortar_fundo.py            # todas
python .claude/skills/carrossel-bowlgreen/scripts/recortar_fundo.py "POKE SORA"  # uma
```

Escreve em `Fotos/recortados/`, e `gerar_posts.py` procura lá primeiro.

> O recorte parte das **bordas para dentro**, nunca por limiar global. Se fosse por limiar, o cream cheese, a maionese e o arroz branco de dentro do bowl sumiriam junto com o fundo. **Foto nova na pasta = rodar o recorte antes de gerar.**
>
> `SUCOS E DETOX` tem fundo bege, não branco — o recorte não pega. Precisa de tratamento manual.

## Peças editoriais — `gerar_editorial.py` ← **use este**

O padrão de feed hoje. Nasceu porque a Gê recusou a leva do `gerar_peças.py` inteira em 2026-07-27: *"tá na paleta, tá com a tipologia, mas tá com cara de pobre"*, *"tá tudo padrãozinho"*.

**A crítica que mais custou: "o meu público é A."** As fotos tinham sido geradas com prompt de "gente simples do subúrbio, roupa do dia a dia". As referências dela em `Fotos/referencias/` dizem o contrário — interior de carro importado, calça de alfaiataria branca, jaqueta de grife, unha feita, joia fina, bancada de mármore.

> **Abra `Fotos/referencias/` antes de escrever qualquer prompt de pessoa.** É direção de arte, não pasta de inspiração solta. As que mandam: `Life lately_.jpg` (o público), `Red & Mango Poké.jpg` (a fotografia de comida), `ЛЮБЛЮ МАТЧУ.jpg` (fundo cheio + palavra gigante), `Pasta Plate Poster.jpg` (o split orgânico).

```bash
python .claude/skills/carrossel-bowlgreen/scripts/gerar_editorial.py \
  "Entregas/AAAA-MM-DD-bowlgreen-editorial/config.json" \
  "Entregas/AAAA-MM-DD-bowlgreen-editorial"
```

| Tipo | Tamanho | Silhueta |
|---|---|---|
| `cartaz` | 1080×1350 | Foto sangrando, uma palavra enorme na frente, nada mais |
| `vazado` | 1080×1350 | Foto sangrando, primeira linha só em contorno — a imagem passa por dentro da letra |
| `moldura` | 1080×1350 | Foto sangrando com filete creme por dentro, caps espaçada, cara de revista |
| `etiqueta` | 1080×1350 | Foto sangrando, ficha técnica numa etiqueta creme inclinada no alto |
| `onda` | 1080×1350 | Split orgânico curvo verde/creme, prato recortado ao centro. Única sem pessoa |
| `story-cartaz` | 1080×1920 | Foto cheia, palavra gigante, pílula de CTA |
| `story-vazado` | 1080×1920 | Foto cheia, contorno + cheio, CTA coral |
| `story-moldura` | 1080×1920 | Enquete flutuando sobre a foto, sem bloco chapado |

### Regras que este gerador impõe

- **A foto sangra os quatro lados.** Bloco chapado ocupando meia peça é o que dava cara de panfleto.
- **Um prato diferente por peça.** Ela apontou que era sempre o mesmo poke. Wrap, suco, tabule, grelhado e os pokes se revezam — confira em `dados/fichas.json`.
- **Display entre 130 e 230px.** Abaixo disso não lê na miniatura.
- Texto em giz só sobre área escura do véu. Sobre comida ele some.

### Tetos aprendidos apanhando

- `cartaz`: o giz vai no rodapé, não colado na palavra — colado ele caía em cima da comida.
- `moldura`: com `foco` em torno de `50% 74%` os bowls sobem e liberam o mármore do rodapé para o título.
- `etiqueta`: etiqueta ancorada no **alto**. Encostada embaixo tapava o bowl inteiro. E sem faixa mosaico — ela cortava o prato no meio.
- `onda`: precisa do prato recortado (`recortar_fundo.py`), não da foto crua.

## Peças com pessoa real — `gerar_lifestyle.py` + `gerar_peças.py`

> `gerar_peças.py` está **aposentado como padrão de feed** — foi a leva recusada. Fica no repo porque os tipos `numerao` e `duo` ainda servem quando a peça é puramente de ficha técnica. Para feed, use `gerar_editorial.py` acima.

Duas queixas da Gê em 2026-07-27 mataram o `gerar_posts.py` como padrão de feed: **letra pequena demais** (display de 76px não lê na miniatura) e **tudo igual** (todo post tinha a mesma silhueta — faixa verde, prato no disco, nome, chips). Somando a terceira: **só prato, nenhuma pessoa**.

### 1. Gerar as fotos de gente

```bash
python .claude/skills/carrossel-bowlgreen/scripts/gerar_lifestyle.py            # todas as cenas
python .claude/skills/carrossel-bowlgreen/scripts/gerar_lifestyle.py garfada    # uma
```

Seis cenas prontas: `garfada` · `suco` · `mesa-dupla` · `maos-bowl` · `trabalho` · `entrega`. Saem em `Fotos/geradas/`.

Usa `/v1/images/edits` da OpenAI com a **foto real do prato como referência** — é isso que faz a embalagem de papel e a logo saírem fiéis em vez de virar uma tigela genérica. A chave sai do `.env` da pasta da marca.

> O CLI da Higgsfield exige `higgsfield auth login` interativo e não roda em sessão headless. Por isso a rota é API direta. Se a Gê logar no CLI algum dia, `higgsfield product-photoshoot create --mode lifestyle_scene` também serve.

### 2. Montar as peças

```bash
python .claude/skills/carrossel-bowlgreen/scripts/gerar_peças.py \
  "Entregas/AAAA-MM-DD-bowlgreen-pecas/config.json" \
  "Entregas/AAAA-MM-DD-bowlgreen-pecas"
```

| Tipo | Tamanho | Silhueta |
|---|---|---|
| `manchete` | 1080×1350 | Foto sangrando em cima, tarja creme embaixo com manchete de 3 linhas, selo costurando as duas |
| `numerao` | 1080×1350 | Split vertical: foto à esquerda, bloco verde à direita com numeral gigante em dourado |
| `polaroid` | 1080×1350 | Fundo todo de estampa, foto em moldura branca torta, legenda em giz |
| `faixa-lateral` | 1080×1350 | Foto cheia, faixa coral vertical com texto girado 90°, três números |
| `duo` | 1080×1350 | Pessoa em cima, prato recortado embaixo no disco menta |
| `story-manchete` | 1080×1920 | Foto cheia, manchete gigante embaixo, pílula de CTA |
| `story-enquete` | 1080×1920 | Foto em cima, bloco creme com pergunta e duas caixas de opção |
| `story-selo` | 1080×1920 | Fundo verde com estampa, foto em círculo dourado, rodapé de arcos |

### Regras que este gerador impõe

- **Display nunca abaixo de 120px.** Manchete vive entre 106 e 190; numeral, entre 180 e 230.
- **Dois tipos não podem ter a mesma silhueta.** Se a peça nova parece uma existente, ela não entra.
- **Toda peça carrega elemento de marca:** `estampa()` como marca d'água, `selo()` dourado com texto em arco, `mosaico()` como divisória, `arcos()` como rodapé. Todos vieram do `Bowl Green — Design System.html`, nenhum foi inventado.

### Tetos aprendidos apanhando

- Numeral `numerao`: **186px é o teto**. A coluna tem 518px e `200g` em Shantell 800 já ocupa ~470. Acima disso o número sai cortado na borda.
- `manchete`: a foto vai até 690px e não além. Com 830 a tarja creme ficava com 520 e o giz caía por baixo do rodapé.
- `polaroid`: a moldura branca precisa de **largura fixa** (744px). Sem ela a div encolhe/cresce conforme o texto e a legenda vaza para fora da peça.
- `duo`: chips vêm **acima** do prato. O prato é posicionado e passa por cima de qualquer coisa que venha depois no fluxo.
- Foto de prato nova em `duo` → rodar `recortar_fundo.py` antes, senão o fundo branco vira um quadrado sobre o creme.

## Uso

```bash
python .claude/skills/carrossel-bowlgreen/scripts/gerar_slides.py \
  "Entregas/AAAA-MM-DD-carrossel-bowlgreen-<slug>/config.json" \
  "Entregas/AAAA-MM-DD-carrossel-bowlgreen-<slug>"
```

### config.json

```json
{
  "marca": "Bowl Green",
  "tema": "do que trata este carrossel",
  "slides": [
    { "tipo": "mito-verdade", "rotulo": "Mitos × Verdades",
      "mitos": ["Mito um.", "Mito dois.", "Mito três."],
      "verdade": "VICIA.<br>SEM CULPA.", "assinatura": "assinado: quem já provou 💚" },

    { "tipo": "expectativa", "expectativa": "fala do cliente", "tom": "dita em tom de sacrifício",
      "realidade": "A frase que desmonta.", "chips": ["🍚 base firme", "zero sacrifício"] },

    { "tipo": "numerao", "acima": "Label de cima", "numero": "200g", "abaixo": "label de baixo",
      "giz": "a frase manuscrita 💚", "chips": ["🐟 salmão"] },

    { "tipo": "faq", "pergunta": "Salada sustenta?", "fonte": "pergunta real de cliente",
      "resposta": "A resposta da casa.", "rodape_chip": "manda a sua no WhatsApp 💬" },

    { "tipo": "cta", "titulo": "VEM PRO CLUBE", "texto": "Chamada.",
      "chips": ["#Bowlovers"], "botao": "Link da bio", "giz": "a gente separa o seu 💚" }
  ]
}
```

## Regras de texto

- **Display: 2 a 4 palavras.** Luckiest Guy em caixa-alta gorda não perdoa frase longa. Use `<br>` para quebrar onde você quer.
- **Mito: uma frase curta.** Ele aparece riscado — precisa ser lido de relance.
- Linha de giz: sempre uma, sempre no fim do card. É a piscadela da marca.
- Sem discurso fitness e sem moralizar comida — ver [[bowl-green]].
- Número sempre que possível, e **sempre número real**. `200g` é o que a marca declara no Design System e no FAQ; não invente outro.

## Depois de gerar

1. Confira com [[carousel-preview]] ou olhando os PNGs.
2. Leve para a [[pauta-diaria]] com legenda e hashtags.
3. Nunca entregue sem mostrar a imagem — ver [[FT-004-conteudo-diario]].

## Notas desta instalação

- Depende de `playwright` + chromium (instalados ✅).
- `python`, não `python3`. Caminhos com espaço e acento entre aspas.
- O caminho da pasta da marca está fixo em `RAIZ_MARCA` no topo do script — se a pasta `GE NEGOCIOS/BOWL GREEN/` mudar de lugar, ajuste ali.
