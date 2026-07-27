---
titulo: "Bowl Green — Auditoria Financeira sobre Extratos Oficiais"
data: 2026-07-21
autor: Silas (Arquiteto de Dados)
fontes:
  - "C:/Users/gerib/Downloads/99 Food translation_statement_br*.xlsx (7 arquivos)"
  - "C:/Users/gerib/Downloads/99 Food Extrato*.xlsx (9 arquivos)"
  - "C:/Users/gerib/Downloads/brendi-extrato.csv (+ duplicata)"
  - "scratchpad/planilha.txt (fichas técnicas e custos fixos — auditoria anterior)"
status: concluido
---

# Bowl Green — Auditoria Financeira sobre Extratos Oficiais

> **Convenção:** `[LIDO]` = valor extraído literalmente do extrato. `[CALCULADO]` = soma/razão de valores lidos. `[INFERIDO]` = estimativa com premissa declarada. `AUSENTE` = não existe nos arquivos.

---

## 1. Inventário e período

### Deduplicação

**Duplicatas byte-a-byte (MD5 idêntico) — descartadas:**

| Arquivo descartado | Idêntico a |
|---|---|
| `99 Food Extrato (5).xlsx` | `99 Food Extrato.xlsx` |
| `99 Food Extrato (6).xlsx` | `99 Food Extrato (1).xlsx` |
| `99 Food Extrato (7).xlsx` | `99 Food Extrato (2).xlsx` |
| `99 Food Extrato (8).xlsx` | `99 Food Extrato (4).xlsx` |
| `brendi-extrato (1).csv` | `brendi-extrato.csv` |

**Duplicatas de conteúdo (MD5 diferente, mesmas linhas) — deduplicadas por chave `ID transação + data cobrança + tipo + data pedido`:**

| Par redundante | Mês coberto |
|---|---|
| `translation_statement_br (4)` ≡ `Extrato (5)/Extrato` | Jan/2026 |
| `translation_statement_br (3)` ≡ `Extrato (1)` | Fev/2026 |
| `translation_statement_br (2)` ≡ `Extrato (2)` | Mar/2026 |
| `translation_statement_br (1)` ≡ `Extrato (3)` | Abr/2026 |
| `Extrato (4)` ⊂ `translation_statement_br.xlsx` | Mai/2026 (subconjunto de 11 linhas) |

**Resultado:** 1.758 linhas lidas → 601 removidas → **1.157 linhas únicas** `[CALCULADO]`.

### Cobertura

| Mês | Pedidos 99Food | Janela real de pedidos | Pedidos Brendi |
|---|---|---|---|
| 2026-01 | 96 | 06/01 → 31/01 | — |
| 2026-02 | 145 | 01/02 → 28/02 | — |
| 2026-03 | 136 | 02/03 → 31/03 | — |
| 2026-04 | 162 | 01/04 → 30/04 | — |
| 2026-05 | 162 | 01/05 → 31/05 | 58 (a partir de 12/05) |
| 2026-06 | 170 | 01/06 → 30/06 | 60 |
| 2026-07 | 156 | 01/07 → 21/07 (**parcial**) | 64 (até 21/07, **parcial**) |
| **Total** | **1.027** | **06/01/2026 → 21/07/2026** | **182** |

- **99Food:** 6,5 meses completos + julho parcial. Zero meses faltando na série.
- **Brendi:** 2,3 meses (12/05 → 21/07). Não existe dado Brendi anterior a 12/05/2026.
- **iFood:** `AUSENTE` — nenhum extrato iFood foi fornecido, apesar de a planilha listar "Mensalidade iFood R$150".

### Validação do parser

A identidade fornecida pelo Larry foi testada contra **todas as 1.027 linhas de pedido**:

```
Ganhos = Preço + TaxaPedidoMín + TaxaEntregaLoja + Gorjeta
       + InvestimentoLojaItens + Contrib99Itens
       + InvestimentoLojaLogística + Contrib99Logística
       + InvestimentoLojaEntrega + Contrib99Entrega
       + CustosComissão + TaxaProcessamento + CustosLogísticos
       + Mensalidade + Anúncio + Reembolso + Compensação
```

**Resultado: 1.027 OK / 0 divergentes** (tolerância R$0,01) `[CALCULADO]`.

Reconciliação independente contra a coluna `Valor da cobrança` (o depósito bancário):

```
Ganhos 48.593,99 + Ads (2.609,35) + Reembolso (155,15)
+ Compensação 100,70 + Dinheiro coletado (4.334,98)
= 41.595,21  ≡  Σ Valor da cobrança = 41.595,21   ✔ exato ao centavo
```

---

## 2. 99Food — onde o dinheiro vaza

### 2.1 Consolidado do período (06/01 → 21/07/2026) `[LIDO]`/`[CALCULADO]`

| Linha | R$ | % do bruto |
|---|---:|---:|
| **Faturamento bruto (Preço total dos itens sem as ofertas)** | **57.409,46** | 100,00% |
| (+) Taxa de entrega da loja (receita) | +1.425,00 | +2,48% |
| (+) Taxa de pedido mínimo (receita) | +3,10 | +0,01% |
| (+) Compensação de contestação | +100,70 | +0,18% |
| **= Receita total cobrada do cliente** | **58.837,56** | — |
| (−) Investimento da loja em itens em oferta | −5.950,35 | **10,36%** |
| (−) Investimento da loja em custos de entrega | −1.180,50 | 2,06% |
| (+) Contribuição 99Food em custos de entrega | +384,25 | +0,67% |
| **(=) Frete grátis líquido bancado pela loja** | **−796,25** | **1,39%** |
| (−) Custos Logísticos | −1.246,05 | 2,17% |
| (−) Taxa de processamento de pagamento | −1.509,15 | 2,63% |
| (−) Despesas com anúncio (109 linhas próprias, sem pedido) | −2.609,35 | 4,55% |
| (−) Mensalidade | **0,00** | 0,00% |
| (−) Comissão do pedido | **0,00** | 0,00% |
| (−) Reembolsos/cancelamentos (20 linhas) | −155,15 | 0,27% |
| **= NET real na mão da Bowl Green** | **45.930,19** | **80,00%** |
| ↳ depositado em conta (Valor da cobrança) | 41.595,21 | 72,45% |
| ↳ recebido em dinheiro/POS na porta | 4.334,98 | 7,55% |

- Investimento da loja em **custos logísticos de ofertas**: R$ 0,00 em 100% das linhas `[LIDO]`.
- Contribuição 99Food em **itens** em oferta: R$ 0,00 — **a 99Food não banca nenhum centavo dos descontos de item; a loja banca 100%** `[LIDO]`.
- Gorjeta: R$ 0,00 em todo o período `[LIDO]`.

### 2.2 Deduções mês a mês, em % do bruto `[CALCULADO]`

| Mês | Bruto R$ | Desc. item (loja) | Frete líq. loja | Logística | Tx. proc. | Ads | Reemb. | **Retenção** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-01 | 4.904,50 | 0,00% | 0,33% | 0,39% | 2,37% | 5,09% | 2,23% | **91,47%** |
| 2026-02 | 8.303,90 | 3,27% | 0,10% | 0,08% | 2,84% | 5,28% | 0,26% | **85,99%** |
| 2026-03 | 7.288,80 | 6,64% | 1,10% | 1,36% | 2,64% | 0,00% | 0,00% | **90,00%** |
| 2026-04 | 9.497,10 | 12,49% | 0,25% | 0,27% | 2,60% | 3,31% | 0,00% | **84,70%** |
| 2026-05 | 9.319,75 | 13,08% | 0,82% | 1,12% | 2,64% | 7,54% | 0,00% | **77,76%** |
| 2026-06 | 9.575,50 | 12,17% | 1,49% | 2,29% | 2,61% | 5,42% | 0,25% | **77,11%** |
| 2026-07* | 8.519,91 | **19,07%** | **5,27%** | **9,05%** | 2,60% | 4,52% | 0,00% | **59,49%** |
| **TOTAL** | **57.409,46** | **10,36%** | **1,39%** | **2,17%** | **2,63%** | **4,55%** | **0,27%** | **80,00%** |

\* julho parcial (01→21). **Retenção** = NET (ganhos + ads + reembolsos + compensação) ÷ bruto de itens.

**A retenção caiu 32 pontos percentuais em 6 meses: 91,5% → 59,5%.** Nenhuma taxa cobrada pela 99Food aumentou. A queda é 100% composta de decisões da própria loja (desconto em item) e de migração para entrega da plataforma.

### 2.3 Confirmação: comissão é 0%

**CONFIRMADO.** A coluna `Comissão do pedido` vale ` 0% ` em **1.157 de 1.157 linhas (100%)** `[LIDO]`. A coluna `Custos com comissão e distribuição` soma **R$ 0,00**, sobre uma `Base da comissão` de R$ 53.647,03. A coluna `Mensalidade` soma **R$ 0,00** em todo o período.

### 2.4 O "frete grátis nas 3 primeiras entregas" — quantificado

Pergunta direta da Gê. Resposta:

| Métrica | Valor |
|---|---:|
| Investimento da loja em custos de entrega (7 meses) | −R$ 1.180,50 |
| Contribuição 99Food em custos de entrega | +R$ 384,25 |
| **Custo líquido do frete bancado pela loja** | **−R$ 796,25** |
| **% do faturamento bruto do período** | **1,39%** |
| Pedidos afetados | 175 de 1.027 (17,0%) |
| Custo médio por pedido afetado | R$ 4,55 |

**Só em julho:** −R$ 708,04 bruto / +R$ 259,10 contribuição = **−R$ 448,94 líquido = 5,27% do bruto do mês**. Ou seja: 56% de todo o frete bancado no ano aconteceu nos 21 dias de julho.

**Causa mecânica:** a loja migrou de `Entrega feita pela loja` para `Entrega da plataforma`.

| Método de entrega | Pedidos | Ticket | Logística/ped | Frete bancado/ped | Taxa entrega recebida/ped | Retenção |
|---|---:|---:|---:|---:|---:|---:|
| Entrega feita pela loja | 782 | R$ 55,90 | R$ 0,00 | R$ 0,00 | +R$ 1,82 | **89,1%** |
| Entrega da plataforma | 245 | R$ 55,91 | −R$ 5,09 | −R$ 3,25 | R$ 0,00 | **65,3%** |

Mesmo ticket, **24 pontos percentuais de diferença na retenção**. Entrega pela plataforma custa ~R$ 10,16/pedido a mais (logística + frete bancado + perda da taxa de entrega).

### 2.5 Taxa de processamento — 3,21% fixo

`[CALCULADO]` A taxa de processamento é **exatamente 3,21% da base da comissão, independente da forma de pagamento**:

| Forma | n | Base R$ | Taxa R$ | Taxa % |
|---|---:|---:|---:|---:|
| Pix | 564 | 29.010,66 | 931,19 | 3,21% |
| Cartão crédito (todas bandeiras) | 186 | 9.509,49 | 305,25 | 3,21% |
| Cartão débito (todas bandeiras) | 30 | 1.679,67 | 53,90 | 3,21% |
| Nubank Crédito | 71 | 3.258,77 | 104,64 | 3,21% |
| Dinheiro | 36 | 1.953,38 | 31,10 | 1,59% |
| POS – débito / POS – crédito | 90 | 4.887,35 | 0,00 | **0,00%** |
| Saldo / não identificado | 50 | 2.587,89 | 83,07 | 3,21% |

**Pix no 99Food não é mais barato que cartão.** Os 90 pedidos POS (maquininha da loja) tiveram taxa zero na 99Food — mas o custo da adquirente da maquininha é `AUSENTE` nestes arquivos.

### 2.6 Distribuição da retenção por pedido `[CALCULADO]`

n = 1.027 pedidos. Retenção = Ganhos ÷ Preço (pode passar de 100% quando a taxa de entrega da loja entra como receita).

| Faixa | Pedidos | % |
|---|---:|---:|
| < 60% | 84 | 8,2% |
| 60–70% | 85 | 8,3% |
| 70–80% | 201 | 19,6% |
| 80–90% | 143 | 13,9% |
| 90–97% | 307 | 29,9% |
| ≥ 97% | 207 | 20,2% |

Mín 18,5% · p10 62,1% · p25 77,4% · **mediana 90,2%** · p75 96,8% · p90 105,4% · máx 136,1% · média 86,8%.

**48,9% dos pedidos (502) carregam desconto bancado pela loja.** Os piores casos:

| Data | Preço | Desconto loja | % | Ganhos |
|---|---:|---:|---:|---:|
| 30/05/2026 11:37 | 52,35 | −42,35 | **81%** | **9,68** |
| 30/05/2026 11:39 | 52,35 | −42,35 | **81%** | 15,48 |
| 07/04/2026 13:14 | 109,80 | −43,92 | 40% | 65,88 |
| 02/07/2026 18:22 | 92,80 | −34,72 | 37% | 38,74 |
| 02/07/2026 21:22 | 92,80 | −34,72 | 37% | 51,73 |
| 18/07/2026 21:37 | 92,80 | −34,72 | 37% | 47,74 |
| 20/07/2026 19:52 | 92,80 | −34,72 | 37% | 47,74 |

Os dois pedidos de 30/05 com 81% de desconto renderam R$ 9,68 e R$ 15,48 — **abaixo do CMV** (~R$ 19,63 para um ticket de R$52,35). Prejuízo direto.

---

## 3. Brendi — taxa efetiva real

Período: 12/05/2026 → 21/07/2026. 235 linhas, 182 `Pedido online`.

### 3.1 Taxa por forma de pagamento `[LIDO]`/`[CALCULADO]`

| Forma de pagamento | n | Bruto R$ | Taxa R$ | Líquido R$ | Taxa agregada | Taxa mediana | Ticket |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pix | 162 | 8.467,24 | 107,19 | 8.360,05 | **1,27%** | 1,39% | 52,27 |
| Crédito | 10 | 468,09 | 26,59 | 441,50 | **5,68%** | 5,68% | 46,81 |
| Apple Pay (Crédito) | 5 | 337,30 | 17,51 | 319,79 | **5,19%** | 5,19% | 67,46 |
| Apple Pay (Débito) | 5 | 265,26 | 6,60 | 258,66 | **2,49%** | 2,49% | 53,05 |
| **Débito (avulso)** | **0** | — | — | — | **AUSENTE** | — | — |
| **TOTAL pedidos** | **182** | **9.537,89** | **157,89** | **9.380,00** | **1,66%** | — | **52,41** |

**Não existe forma de pagamento "Débito" isolada nos dados** — só "Apple Pay (Débito)". `AUSENTE`.

### 3.2 Estrutura da taxa (regressão linear taxa = a + b × bruto) `[CALCULADO]`

| Forma | n | Modelo ajustado |
|---|---:|---|
| Pix | 162 | **R$ 0,399 fixo + 0,503% variável** |
| Apple Pay (Débito) | 5 | 0,00 fixo + 2,483% |
| Crédito | 10 | 0,00 fixo + 5,682% |
| Apple Pay (Crédito) | 5 | 0,00 fixo + 5,186% |

**Achado:** o Pix da Brendi **não é um percentual** — é R$ 0,40 fixo + 0,50%. O ajuste é praticamente perfeito e bate com a taxa de `Transferência de saldo` (R$ 0,40 fixo, 49 ocorrências). Por isso a taxa efetiva **cai** conforme o ticket sobe: 1,66% num ticket de R$31,60, 1,15% num ticket de R$109,10.

### 3.3 Linhas que NÃO são pedido `[LIDO]`

| Descrição | n | Bruto R$ | Taxa R$ | Detalhe |
|---|---:|---:|---:|---|
| Transferência de saldo | 49 | 8.352,06 | **19,60** | saques; R$0,40 cada |
| Pagamento da mensalidade Brendi | 2 | 600,00 | 0,00 | 12/06 R$300 + 12/07 R$300 |
| Investimento em ads (Tráfego Pago) | 1 | 300,00 | 0,00 | 23/06/2026 |
| Depósito para pagamento da mensalidade Brendi | 1 | 60,00 | 0,00 | 12/05/2026 |

- **Ads + mensalidade somados: R$ 960,00** no período (600 + 300 + 60).
- Custo de saque (R$19,60) é real e recorrente — não está em nenhuma planilha dela.
- Só 2 mensalidades de R$300 aparecem (jun e jul). Maio pagou R$60 de depósito. `[LIDO]`

### 3.4 Reembolsos `[LIDO]`

2 pedidos com Status `Reembolsado`, ambos Pix:

| Data | Bruto | Taxa | Líquido |
|---|---:|---:|---:|
| 28/06/2026 15:15 | 34,70 | 0,57 | 34,13 |
| 03/07/2026 13:53 | 61,50 | 0,71 | 60,79 |

Total R$ 96,20 (1,01% do bruto). **A taxa não foi estornada** nos dois casos.

### 3.5 Brendi mês a mês `[CALCULADO]`

| Mês | Pedidos | Bruto R$ | Ticket | Taxa R$ | Taxa % | Líquido R$ | Reembolsos |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-05 (a partir 12/05) | 58 | 3.265,94 | 56,31 | 48,94 | 1,50% | 3.217,00 | 0 |
| 2026-06 | 60 | 2.819,29 | 46,99 | 56,05 | 1,99% | 2.763,24 | 1 (R$34,70) |
| 2026-07 (até 21/07) | 64 | 3.452,66 | 53,95 | 52,90 | 1,53% | 3.399,76 | 1 (R$61,50) |
| **Total** | **182** | **9.537,89** | **52,41** | **157,89** | **1,66%** | **9.380,00** | 2 |

---

## 4. O comparativo que decide tudo

### 4.1 De cada R$ 100 vendidos, quanto entra na Bowl Green

Janela comum **mai–jul/2026** para ambos os canais. Ads e mensalidades **rateados**.

| Item | **Brendi** | **99Food** |
|---|---:|---:|
| Faturamento bruto (100%) | R$ 100,00 | R$ 100,00 |
| (−) Desconto em item bancado pela loja | 0,00 | **−14,62** |
| (−) Frete/entrega bancado pela loja (líq. contribuição 99Food) | 0,00 | −2,44 |
| (−) Custos logísticos da plataforma | 0,00 | −4,00 |
| (−) Taxa de processamento / gateway | −1,66 | −2,62 |
| (−) Comissão da plataforma | **0,00** | **0,00** |
| (−) Mensalidade rateada | **−6,92** | **0,00** |
| (−) Ads rateados | −3,15 | −5,86 |
| (−) Reembolsos / estornos | −1,01 | −0,38 |
| (−) Custo de saque/transferência | −0,21 | 0,00 |
| (+) Taxa de entrega recebida do cliente | +0,00 | +1,77 |
| **= LÍQUIDO NA CONTA DA BOWL GREEN** | **R$ 87,07** | **R$ 71,86** |

Base exata `[CALCULADO]`:
- **Brendi** (12/05→21/07): bruto R$9.537,89 − taxa R$157,89 − mensalidade/depósito R$660,00 − ads R$300,00 − saques R$19,60 − reembolsos R$96,20 = **NET R$8.304,20**.
- **99Food** (01/05→21/07): bruto R$27.415,16 → **NET R$19.699,23**. O item "reembolsos/estornos" (−0,38) inclui a coluna Reembolso (−R$23,84) e o estorno de Ganhos nas linhas de reembolso (−R$80,05).

**Diferença: 15,21 pontos percentuais a favor da Brendi.**

Consolidado 7 meses do 99Food (jan–jul, período mais longo): **R$ 80,00 líquido por R$100** — mas a tendência é decrescente e julho já está em **R$ 59,49**.

### 4.2 Veredito sobre sair da Brendi

| Cenário | Efeito mensal |
|---|---:|
| Economia da mensalidade Brendi | +R$ 300,00 |
| Perda da margem de contribuição Brendi (60 ped × R$18,33) | −R$ 1.099,96 |
| **RESULTADO LÍQUIDO DE SAIR DA BRENDI** | **−R$ 799,96/mês** |

**⚠️ SAIR DA BRENDI PIORA O RESULTADO EM ~R$ 800/MÊS.** A Brendi é o canal **mais eficiente** dos dois: entrega R$87,07 líquidos por R$100 contra R$71,86 da 99Food. O problema da Brendi não é a taxa (1,66%) — é o **volume baixo diluindo mal a mensalidade de R$300** (R$5,00/pedido a 60 pedidos/mês).

**A pergunta certa não é "saio da Brendi?" e sim "como levo a Brendi de 60 para 150 pedidos/mês?"** — a R$300 fixos, cada pedido adicional na Brendi tem custo marginal de apenas 1,66%. A 150 pedidos/mês a mensalidade cai para R$2,00/pedido e o líquido sobe para ~R$92 por R$100.

---

## 5. Volume real e ticket médio

| Canal | Mês | Pedidos | Pedidos/dia útil | Ticket médio |
|---|---|---:|---:|---:|
| 99Food | 2026-01 | 96 | 4,80 | R$ 51,09 |
| 99Food | 2026-02 | 145 | 6,59 | R$ 57,27 |
| 99Food | 2026-03 | 136 | 5,23 | R$ 53,59 |
| 99Food | 2026-04 | 162 | 6,00 | R$ 58,62 |
| 99Food | 2026-05 | 162 | 5,59 | R$ 57,53 |
| 99Food | 2026-06 | 170 | 6,54 | R$ 56,33 |
| 99Food | 2026-07* | 156 | **8,67** | R$ 54,61 |
| **99Food média** | — | **~160/mês** | **6,2** | **R$ 55,90** |
| Brendi | 2026-05* | 58 | — | R$ 56,31 |
| Brendi | 2026-06 | 60 | 2,00 | R$ 46,99 |
| Brendi | 2026-07* | 64 | — | R$ 53,95 |
| **Brendi média** | — | **~60/mês** | **2,0** | **R$ 52,41** |

\* mês parcial.

### ⚠️ Correção do custo fixo unitário

| | Planilha atual | **REAL (junho/2026)** |
|---|---:|---:|
| Pedidos/mês | 3.000 | **230** |
| Custo fixo mensal | R$ 12.725,00 | R$ 12.725,00 |
| **Custo fixo por pedido** | **R$ 4,24** | **R$ 55,33** |
| Ticket médio | R$ 20,56 | R$ 53,89 |

**O volume real é 7,7% do que a planilha assume. O custo fixo unitário está subestimado em 13 vezes.** Todo o preço sugerido, markup (1,77) e "lucro líquido" da planilha estão errados por essa razão.

Faturamento anual projetado na planilha: R$ 740.100,00. Faturamento real anualizado (base jun: 99Food R$9.575,50 + Brendi R$2.819,29 = R$12.394,79/mês) ≈ **R$ 148.737/ano** — **20% do projetado**.

---

## 6. CMV e custo fixo

### 6.1 Top insumos por peso no CMV

Base: 24 fichas técnicas. **Mix de vendas por produto é `AUSENTE`** (os extratos 99Food e Brendi não trazem detalhe de item). Peso = soma do custo do insumo em todas as fichas ÷ soma total. Aproxima frequência, não mix real.

| # | Insumo | R$ somado | % do custo total | Fichas | R$/ficha |
|---|---|---:|---:|---:|---:|
| 1 | **SALMÃO** | 43,78 | **16,5%** | 5 | 8,76 |
| 2 | **BOWL (embalagem)** | 37,60 | **14,2%** | 22 | 1,71 |
| 3 | **CAMARÃO** | 24,00 | **9,1%** | 4 | 6,00 |
| 4 | **SACO DELIVERY (embalagem)** | 22,00 | **8,3%** | 22 | 1,00 |
| 5 | CARNE ASSADA | 13,58 | 5,1% | 4 | 3,39 |
| 6 | GÁS | 11,00 | 4,2% | 22 | 0,50 |
| 7 | KIT TALHER (embalagem) | 11,00 | 4,2% | 22 | 0,50 |
| 8 | TEMPEROS/AZEITE | 10,00 | 3,8% | 22 | 0,45 |
| 9 | ARROZ JAPONÊS | 9,20 | 3,5% | 9 | 1,02 |
| 10 | CREAM CHEESE | 8,40 | 3,2% | 8 | 1,05 |
| 11 | CARNE DESFIADA | 7,76 | 2,9% | 2 | 3,88 |
| 12 | POTINHO MOLHO (embalagem) | 6,60 | 2,5% | 22 | 0,30 |

**Onde negociar tem retorno, em ordem:**
1. **Proteínas (salmão R$84,21/kg + camarão R$60,00/kg + carne assada) = 30,7% do custo.** Salmão sozinho é 16,5%. Cada 10% negociado no salmão = ~1,65% de CMV.
2. **Embalagem = 29,2% do custo somado (R$3,22/prato medido).** É o segundo maior bloco e é 100% negociável por volume.
3. Cream cheese a R$52,63/kg em 8 fichas — preço alto para o papel que cumpre.

### 6.2 CMV por prato

CMV médio simples: **36,5%** · mediana 35,2% · min 23,7% · máx 56,5%. Custo médio c/ perda R$11,68 · preço praticado médio R$31,18 · **CMV ponderado por valor: 37,5%**.

**Pratos com CMV crítico (>50%) — reprecificar ou retirar:**

| Prato | Custo c/ perda | Praticado | CMV% |
|---|---:|---:|---:|
| SUN SALMÃO | 22,59 | 40,00 | **56,5%** |
| SALMÃO DELUXE | 21,03 | 37,40 | **56,2%** |
| TABULE DE CAMARÃO | 16,84 | 38,90 | 43,3% |
| POKE SORA | 16,75 | 38,70 | 43,3% |
| CAMARÃO TROPICAL | 15,67 | 37,50 | 41,8% |

Os dois pratos de salmão estão vendendo a CMV de 56% — **antes** de qualquer taxa de app, ads ou custo fixo. Com desconto de 12% bancado pela loja na 99Food, esses pratos vendem no prejuízo.

### 6.3 Custos fixos — linha a linha `[LIDO]`

| Linha | R$/mês | Classificação | Observação |
|---|---:|---|---|
| Pró-labore | 5.000,00 | **Retirada das sócias** | Não é "custo cortável" — é a remuneração da Gê e da Ju. Suspender é decisão pessoal, não operacional. |
| Funcionários | 4.000,00 | **Estrutural** | A 230 pedidos/mês = R$17,39/pedido. Dimensionamento superior ao volume. |
| Aluguel | 1.500,00 | **Estrutural** | Renegociável no reajuste; não cortável no curto prazo. |
| Motoboy fixo | 1.000,00 | **⚠️ CORTÁVEL** | 782 dos 1.027 pedidos foram entrega própria; mas veja §7 — migrar 100% para entrega própria justifica o motoboy. Decisão acoplada. |
| Banner ciclovia | 425,00 | **✂️ CORTÁVEL** | Mídia offline sem rastreio de conversão. Nenhum dado nos extratos atribui pedido a este banner. |
| Brendi Mensal | 300,00 | **Estrutural (mantém)** | Confirmado nos extratos (12/06 e 12/07). Cortar custa R$800/mês líquidos — ver §4.2. |
| Gás | 200,00 | **Estrutural** | Já aparece também como R$0,50/prato nas fichas — **possível dupla contagem**. |
| Mensalidade iFood | 150,00 | **✂️ CORTÁVEL (verificar)** | **Nenhum extrato iFood foi fornecido.** Se o canal não está operando, são R$150/mês de puro desperdício. `AUSENTE` |
| Telefone/Internet | 100,00 | **Estrutural** | |
| Telefone/Internet (2ª linha) | 50,00 | **✂️ CORTÁVEL** | **Duas linhas de Telefone/Internet na mesma planilha.** Provável duplicidade de lançamento ou de contrato. |
| Encargos, Férias, 13º, VT, Combustível, Sistema de Gestão | 0,00 | — | Zerados na planilha. **Encargos zerados com R$4.000 de folha é irrealista** — provisão ausente. |
| **TOTAL** | **12.725,00** | | |

**Corte imediato sem impacto operacional: R$ 425 (banner) + R$ 150 (iFood, se inativo) + R$ 50 (2ª linha) = R$ 625/mês = R$ 7.500/ano.**

### 6.4 Embalagem no volume real

Composição por pedido `[LIDO]`: bowl R$1,70 + kit talher R$0,50 + saco delivery R$1,00 + potinho molho R$0,30 = **R$3,50**.

| Base | Pedidos/mês | R$/mês | R$/ano |
|---|---:|---:|---:|
| **Volume real (jun/2026)** | 230 | **805,00** | **9.660,00** |
| Volume da planilha (fictício) | 3.000 | 10.500,00 | 126.000,00 |

Embalagem = **29,2% do custo somado das fichas** e **6,5% do ticket médio de R$53,89**. Uma negociação de 20% no pacote de embalagens vale **R$ 1.932/ano** no volume atual — mais do que o banner da ciclovia.

⚠️ Nota: o custo de embalagem medido nas fichas é R$3,22/prato, e a loja vende ~1,7 pratos/pedido → o custo real de embalagem por pedido é **~R$5,47**, não R$3,50, porque bowl/talher/potinho se repetem por prato e só o saco delivery é por pedido.

---

## 7. O veredito

### 7.1 Resultado por pedido — junho/2026 (único mês completo nos dois canais)

Premissas: CMV = 37,5% do ticket `[CALCULADO das fichas]`. Custo fixo R$12.725/mês rateado por 230 pedidos.

| Canal | Pedidos | Ticket | Receita líq./ped | CMV/ped | **MC/ped** | CF/ped | **RESULTADO/ped** | **RESULTADO/mês** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **99Food** | 170 | 56,33 | 43,43 | 21,11 | **+22,33** | 55,33 | **−33,00** | **−5.609,90** |
| **Brendi** | 60 | 46,99 | 35,94 | 17,61 | **+18,33** | 55,33 | **−36,99** | **−2.219,61** |
| **TOTAL** | **230** | 53,89 | 41,48 | 20,20 | **+21,28** | 55,33 | **−34,04** | **−7.829,51** |

### 7.2 Leitura

**A Bowl Green PERDE dinheiro: −R$ 7.829,51/mês, ou −R$ 34,04 por pedido.**

Mas a distinção crítica:

- **Cada pedido individual GANHA dinheiro na margem de contribuição:** +R$22,33 na 99Food e +R$18,33 na Brendi. **Nenhum canal vende no prejuízo por pedido.**
- **O prejuízo é de VOLUME, não de canal.** MC total de R$4.895,50/mês contra custo fixo de R$12.725,00.
- **Breakeven: 598 pedidos/mês** (MC média R$21,28) = **2,6× o volume atual** = faturamento de **R$ 32.218/mês**. Hoje: R$12.394,79.

⚠️ Se o pró-labore de R$5.000 for tratado como retirada e não como custo, o custo fixo operacional cai para R$7.725 e o **breakeven vai para 363 pedidos/mês** — 1,6× o volume atual. Meta bem mais alcançável.

### 7.3 Mudança de maior impacto em R$/mês — ranqueada

| # | Ação | Impacto R$/mês | Esforço | Confiança |
|---|---|---:|---|---|
| 1 | **Zerar/limitar o desconto em item bancado pela loja na 99Food** (12,17% em jun, 19,07% em jul) | **+1.165 a +1.625** | Baixo — é configuração no painel | **Alta** — `[LIDO]` direto |
| 2 | **Voltar 100% para entrega própria** (245 pedidos de plataforma × R$10,16 de diferença, base período) | **+830** (base jul: +1.219) | Médio — depende do motoboy | **Alta** |
| 3 | **Cortar ads** 99Food R$519 + Brendi R$300 | **+819** | Baixo | Alta — mas pode reduzir volume |
| 4 | **Corte fixo limpo**: banner ciclovia R$425 + iFood R$150 + 2ª linha R$50 | **+625** | Baixo | Média (iFood a confirmar) |
| 5 | **Renegociar salmão + camarão −10%** (30,7% do CMV) | **+143** | Médio | Média |
| 6 | **Renegociar embalagem −20%** | **+161** | Baixo | Média |
| **Σ** | **Ações 1+2+4** (sem cortar ads, preservando volume) | **+2.620 a +3.374** | | |

**Nenhuma combinação de cortes chega ao breakeven.** Somando tudo (+3.593/mês no melhor caso) o prejuízo cai de −R$7.830 para −R$4.237. **O gargalo é volume, não custo.**

### 7.4 O que a ação #1 significa na prática

O desconto bancado pela loja saiu de 0% em janeiro para 19,07% em julho. Em 7 meses custou **R$ 5.950,35** — mais do que:
- todos os custos logísticos (R$1.246,05) **e**
- todo o frete grátis (R$796,25) **e**
- toda a taxa de processamento (R$1.509,15) **somados** (R$3.551,45).

**⚠️ A 99Food cobra 0% de comissão e R$0 de mensalidade. O único dinheiro que a 99Food efetivamente tira é a taxa de processamento de 3,21%. Todo o resto da "perda" na 99Food é decisão de desconto da própria loja.**

---

## Anomalias e pontos `AUSENTE`

1. **iFood:** nenhum extrato fornecido, mas R$150/mês de mensalidade lançados. Confirmar se o canal opera.
2. **Balcão/WhatsApp:** nenhum registro em nenhum extrato. Se há venda presencial, ela está invisível nesta auditoria.
3. **Mix de vendas por produto:** os extratos 99Food e Brendi não detalham itens. A ponderação de CMV é por frequência nas fichas, não por mix real. Para precisão, exportar o relatório de itens vendidos do painel 99Food.
4. **Custo da maquininha POS:** 90 pedidos com taxa zero na 99Food — a taxa da adquirente da loja não aparece em nenhum arquivo.
5. **Gás lançado duas vezes:** R$200/mês no custo fixo **e** R$0,50/prato nas fichas técnicas. Dupla contagem provável.
6. **Encargos trabalhistas zerados** com R$4.000/mês de folha — provisão de FGTS/INSS/férias/13º ausente. O custo fixo real é maior que R$12.725.
7. **Duas linhas "Telefone/Internet"** (R$50 e R$100) na mesma lista de custos fixos.
8. **Aba "Detalhes do pedidos - taxa mensalidade"** existe em todos os workbooks 99Food mas contém apenas cabeçalho, sem dados — consistente com mensalidade R$0,00.
9. **Julho/2026 é parcial** (até 21/07) em ambos os canais. A tendência de julho é real mas não é um mês fechado.
10. **Reembolsos Brendi:** a taxa não foi estornada nos 2 casos reembolsados.

---

## Arquivos de trabalho

- `scratchpad/p99_inv.py` — dedup e inventário dos 16 workbooks
- `scratchpad/p99_rows.json` — 1.157 linhas únicas normalizadas
- `scratchpad/p99_calc.py`, `p99_calc2.py` — agregações e validação de identidade
- `scratchpad/brendi.py` — parser Brendi e regressão de taxa
- `scratchpad/cmv.py` — extração de fichas técnicas e peso de insumos
- `scratchpad/veredito.py` — economia unitária e breakeven

Nenhum arquivo em `Downloads/` foi modificado. Nenhum arquivo do Drive foi tocado.
