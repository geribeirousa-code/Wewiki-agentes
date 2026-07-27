# FT-004 - Conteúdo Diário

> **Gatilho:** "monta a pauta", "o que tem pra hoje", "gera o conteúdo do dia", início de qualquer dia útil. Também roda sozinho quando a Gê pede conteúdo para uma das marcas.
>
> **Dono padrão:** Larry (orquestra). Executa com [[carrossel-opiniao]] → [[carousel-preview]] → [[pauta-diaria]].

## O acordo

A Gê não escreve conteúdo. O time gera, ela **analisa e libera**. A entrega do dia é uma página, não uma conversa — ela abre, olha, aprova ou manda refazer, e cola o veredito de volta.

Isso existe porque a Gê é completamente visual. Peça descrita em texto é peça que ela não consegue avaliar. **Nenhuma etapa deste fluxo termina sem imagem.**

## As duas marcas

Só existem duas. Não invente uma terceira nem crie nome paralelo para as que existem.

| Marca | Handle | Nota canônica | Idioma |
|---|---|---|---|
| Bowl Green | `@bowlgreenxerem` | [[bowl-green]] | Português |
| Clean Touch Cabinets | `@cleantouchcabinets` | [[clean-touch-cabinets]] | **Inglês** |

O handle no frontmatter da nota é a fonte de verdade. Nunca digite um `@` direto num `config.json` sem conferir lá — já nasceu errado uma vez (`@bowlgreen.xerem`, com ponto).

## Plataformas cobertas

Instagram carrossel + legenda · Instagram Stories/Reels · WhatsApp/Status.

Uma matéria-prima, três embalagens. O carrossel é a peça-mãe do dia; story e WhatsApp saem dele.

> **Status:** só o carrossel está automatizado hoje. Stories (9:16) e WhatsApp ainda não têm gerador — ver §Pendências.

## O fluxo

```
1. ÂNGULO      Larry escolhe a tese do dia por marca
2. TEXTO       Escreve a thread nas regras da marca
3. GERAR       carrossel-opiniao → slide-01.png … slide-NN.png
4. CONFERIR    carousel-preview → tira única, lida com os próprios olhos
5. PAUTA       pauta-diaria → Entregas/AAAA-MM-DD-pauta/pauta.html
6. GÊ DECIDE   aprova, ou escreve o ajuste e manda refazer
7. REFAZ       volta ao passo 2 só para o que caiu em "refazer"
8. PUBLICA     Gê posta
```

O passo 4 não é burocracia. Foi ele que pegou, no primeiro dia, um bug de encoding que transformava **todo** acento em lixo (`saudÃ¡vel`) em **todos** os carrosséis. Olhar a peça antes de mostrar é obrigatório.

## Estrutura de pastas

```
Entregas/
├── AAAA-MM-DD-carrossel-<marca>-<slug>/
│   ├── config.json
│   ├── slide-01.png …
│   └── preview.png
└── AAAA-MM-DD-pauta/
    ├── pauta.json
    └── pauta.html          ← o que a Gê abre
```

## Regras por marca

### Bowl Green — português, apetite, sem culpa

Tema visual `bowlgreen` (creme, verde, dourado). Fontes Baloo2 + Nunito.

O eixo permanente: **provar que comida saudável sustenta**. O público de Xerém associa bowl a salada — toda peça trabalha contra isso. Base de arroz, proteína pesada na balança, número na mesa. Tom direto, sem discurso fitness, sem moralizar comida. Público é *bowlover*. Pedido fecha no WhatsApp pelo link da bio.

### Clean Touch Cabinets — inglês, fato, nunca pede

Tema visual `cleantouch` (teal sobre terracota). Fonte Inter.

> **Leia `GE NEGOCIOS/CLEAN TOUCH CABINETS/CONTEXTO-MARCA.md` antes de escrever uma única linha.** As regras absolutas de lá não são preferências de estilo, são proibições. As que mais pegam: nunca citar fundadores, nunca citar país de origem, nenhum adjetivo de qualidade, **nenhum ponto de exclamação**, nunca pedir nada, nunca inventar depoimento.

A autoridade vem do fato, não do tom. Se um texto precisa de adjetivo para ficar forte, o fato dele está fraco.

### Cadência declarada vs. sistema diário

⚠️ **Conflito real, registrado de propósito.**

O `CONTEXTO-MARCA.md` do Clean Touch define a presença no Instagram como *"portfólio e prova. Não caça ninguém"* e a cadência como *"a foto padronizada que a obra já produz. Nada além."* Isso é incompatível com um carrossel de opinião publicado todo dia.

**Como foi conciliado:** para o Clean Touch, a peça diária **não é opinião** — é uma das três formas que a bíblia da marca já autoriza:

1. **Prova de obra** — a foto padronizada do dia, com legenda concreta (peça, medida, o que foi antecipado).
2. **Antes/depois de resgate** — a porta de entrada declarada da marca.
3. **A cadeia do erro** — peças como a de 2026-07-25, que expõem o mecanismo (`projeto ruim → ligação → atraso → armário amassado`). Informa que existe, não pede obra.

Se num dia não houver foto de obra nem resgate, o Clean Touch **pode ficar sem peça**. É melhor do que quebrar o posicionamento por volume. A Bowl Green não tem essa restrição — pode publicar todo dia.

## Pendências

| # | O que falta | Trava o quê |
|---|---|---|
| 1 | Logo do Clean Touch — não existe arquivo de imagem na pasta da marca | Avatar do carrossel sai como círculo teal de reserva |
| 2 | Handle do Clean Touch diverge: a Gê diz `@cleantouchcabinets`, o `CONTEXTO-MARCA.md` §Contato diz `@cleantouch_cabinets` | Um dos dois está errado no ar |
| 3 | Gerador de Stories/Reels (9:16) | Plataforma pedida, ainda manual |
| 4 | Gerador de peça de WhatsApp/Status | Plataforma pedida, ainda manual |
| 5 | Fotos reais de bowl para o slide de abertura | A skill pede imagem no slide 1 para segurar o scroll; hoje sai só texto |
| 6 | Slogan do Clean Touch segue em aberto por decisão da marca | Não usar nenhum. Onde faltar, usar a missão |

## Ver também

- [[DI-002-convencoes-de-frontmatter]] — campo `instagram`, adicionado para este fluxo
- [[bowl-green]] · [[clean-touch-cabinets]]
