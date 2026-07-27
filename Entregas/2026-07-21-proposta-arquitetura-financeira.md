# Proposta de Arquitetura Financeira — Empresas/

- **Autor:** Silas (Arquiteto de Dados)
- **Data:** 2026-07-21
- **Status:** PROPOSTA — nada foi criado. Aguarda aprovação da Gê.
- **Decisão de entrada (não reaberta):** três entidades financeiras separadas — Gê pessoa física, CLEAN TOUCH, BOWL GREEN. Pasta `Empresas/` no topo, uma subpasta por entidade. `Wiki pessoal/` permanece conhecimento pessoal.
- **Referências:** [[DI-001-convencoes-de-nomeacao]], [[DI-002-convencoes-de-frontmatter]], [[SOP-002-converter-para-sqlite]], [[AGENTS]]

---

## 1. Estrutura de pastas proposta

```
Empresas/
├── INDEX.md
├── _Compartilhado/
│   ├── INDEX.md
│   └── Plano de Contas/
│       └── <slug>.md              # categoria-financeira, compartilhada pelas 3 entidades
│
├── Clean Touch/
│   ├── INDEX.md
│   ├── empresa.md                 # a entidade em si (SSOT da identidade financeira)
│   ├── Contas/
│   │   └── <slug>.md              # conta-financeira (banco, caixa, cartão)
│   ├── Lançamentos/
│   │   └── AAAA/MM/AAAA-MM-DD-<slug>.md
│   ├── Documentos/
│   │   └── AAAA/MM/AAAA-MM-DD-<slug>.md
│   └── Relatórios/
│       └── AAAA/
│           ├── AAAA-MM-fluxo-de-caixa.md      # rollup mensal (DERIVADO)
│           └── AAAA-resumo-anual.md           # rollup anual (DERIVADO)
│
├── Bowl Green/
│   └── (idêntico)
│
└── <PF da Gê — nome a definir>/
    └── (idêntico, sem campos fiscais de PJ)
```

### Justificativas de forma

- **`Lançamentos/` e `Documentos/` aninham por `AAAA/MM/`** — seguem a Regra Rígida 5 do AGENTS.md. São as duas pastas de alto volume.
- **`Contas/` e `Plano de Contas/` ficam planas** — baixo volume, vocabulário controlado, alinhado com o INDEX da Wiki pessoal ("pastas de conceito ficam planas").
- **`Relatórios/` aninha só por `AAAA/`** — no máximo 12–15 arquivos por ano. Um nível `MM/` seria overhead vazio.
- **`_Compartilhado/` com prefixo `_`** — ordena antes das empresas e sinaliza "não é uma entidade financeira". Ver conflito C4.
- **Nome de pasta em Title Case com espaço** (`Clean Touch`) — segue o padrão vigente do vault (`Wiki pessoal`, `Minha Vida`, `Organizações`). Ver conflito C5.

### Regra de aninhamento dos lançamentos (importante)

O arquivo de lançamento aninha e é nomeado por **`data_competencia`**, nunca por `data_caixa`.

Motivo: `data_caixa` muda quando um previsto é liquidado. Aninhar por ela obrigaria a **mover o arquivo**, quebrando wikilinks e violando idempotência. `data_competencia` é imutável depois de escrita.

### SSOT e a pasta `Relatórios/`

`Relatórios/` contém dados **derivados** — números que já existem nos lançamentos. Isso é, tecnicamente, duplicação.

Resolução proposta: relatórios recebem o mesmo estatuto do espelho SQLite — **derivados, regeneráveis, markdown-nunca-é-fonte-aqui**. Todo relatório carrega `derivado: true` e `gerado_em:` no frontmatter. Se relatório e lançamentos discordarem, os lançamentos vencem e o relatório é regenerado. Sem isso, `Relatórios/` é uma violação da Regra de Ouro por construção.

---

## 2. Esquema de frontmatter — entidades novas

Seis tipos novos. Nenhum campo abaixo existe hoje em DI-002; **todos precisam ser adicionados a DI-002 antes do primeiro arquivo ser escrito**, e cada um precisa de modelo em `Wiki equipe/Modelos/`.

### 2.1 `empresa` — `Empresas/<Empresa>/empresa.md`

```yaml
---
tipo: empresa                         # (obrigatório)
nome: CLEAN TOUCH                     # (obrigatório)
slug: clean-touch                     # (obrigatório) chave primária explícita
natureza: pessoa-juridica             # (obrigatório) pessoa-juridica | pessoa-fisica
situacao: ativa                       # (obrigatório) ativa | inativa | encerrada
moeda_base: BRL                       # (obrigatório)
ramo:                                 # (opcional) LACUNA — não preenchido
cnpj_cpf:                             # (opcional)
regime_tributario:                    # (opcional) mei | simples-nacional | lucro-presumido | lucro-real | nao-aplica
data_abertura:                        # (opcional) AAAA-MM-DD
organizacao_crm:                      # (opcional) FK → CRM/Organizações — ver conflito C1
tags: []                              # (opcional)
---
```

Justificativa dos campos não óbvios:

- **`slug` explícito** — único caso no vault onde o nome do arquivo (`empresa.md`) não é o slug. A pasta carrega o nome. Sem `slug` no frontmatter, as FKs de milhares de lançamentos não resolvem para nada. É a chave primária de todo o subsistema.
- **`natureza`** — a Gê PF é uma das três entidades e **não é uma empresa**. Este campo é o que permite a PF morar em `Empresas/` sem que os relatórios apliquem lógica de PJ a ela. Ver conflito C2.
- **`moeda_base`** — obrigatório e explícito, nunca inferido. Um relatório que soma valores de moedas diferentes está errado silenciosamente, e esse é o pior tipo de erro numa base financeira.
- **`ramo`** — declarado no schema, **deixado vazio**. Não sei o ramo de CLEAN TOUCH nem de BOWL GREEN e não vou inventar.

### 2.2 `lancamento` — `Empresas/<Empresa>/Lançamentos/AAAA/MM/AAAA-MM-DD-<slug>.md`

```yaml
---
tipo: lancamento                      # (obrigatório)
empresa: clean-touch                  # (obrigatório) FK → empresa
direcao: saida                        # (obrigatório) entrada | saida
descricao: Compra de insumos          # (obrigatório)
valor: 1234.56                        # (obrigatório) número decimal, SEMPRE positivo
moeda: BRL                            # (obrigatório)
data_competencia: 2026-07-21          # (obrigatório) quando o fato gerador ocorreu
data_caixa:                           # (opcional) quando o dinheiro moveu; vazio = não liquidado
categoria: insumos-operacionais       # (obrigatório) FK → Plano de Contas
status: liquidado                     # (obrigatório) previsto | liquidado | conciliado | cancelado
conta:                                # (opcional) FK → Contas/
contraparte:                          # (opcional) FK — ver conflito C1
documento:                            # (opcional) FK → documento-financeiro
forma_pagamento:                      # (opcional) pix | boleto | cartao-credito | cartao-debito | dinheiro | transferencia | outro
recorrencia:                          # (opcional) unica | mensal | anual
tags: []                              # (opcional)
---
```

Justificativa dos campos não óbvios:

- **`valor` sempre positivo + `direcao` separada.** A alternativa (valor com sinal) parece mais enxuta e é uma armadilha: em markdown o valor é digitado à mão, e um sinal trocado inverte uma despesa em receita sem nenhum erro visível. Com `direcao`, "somar todas as entradas" é um filtro, não uma inspeção de sinal. Também torna a agregação por LLM muito mais confiável.
- **`data_competencia` + `data_caixa` como par.** Este par é a razão pela qual um **fluxo de caixa** difere de um **resultado do exercício**. Fluxo de caixa agrega por `data_caixa`; resultado agrega por `data_competencia`. Com um campo só, um dos dois relatórios que a Gê pediu é impossível de produzir corretamente. Não é opcional.
- **`status: previsto`** — habilita fluxo de caixa projetado (contas a pagar/receber). Sem ele a Gê só enxerga o passado.
- **`categoria` obrigatória** — sem plano de contas, nenhum relatório agrupa. É o que transforma uma lista de lançamentos em um relatório.

### 2.3 `documento-financeiro` — `Empresas/<Empresa>/Documentos/AAAA/MM/AAAA-MM-DD-<slug>.md`

Deliberadamente **distinto** do `documento` existente. Ver conflito C3.

```yaml
---
tipo: documento-financeiro            # (obrigatório)
titulo: NF-e 001234 — Fornecedor X    # (obrigatório)
empresa: clean-touch                  # (obrigatório) FK → empresa
classe: nota-fiscal                   # (obrigatório) nota-fiscal | recibo | contrato | extrato | boleto | comprovante | guia-imposto | outro
data_emissao: 2026-07-21              # (obrigatório) AAAA-MM-DD
arquivo_real: ~/Documentos/nf-001234.pdf   # (obrigatório) caminho para o PDF/imagem real
numero:                               # (opcional)
competencia:                          # (opcional) AAAA-MM
valor:                                # (opcional) extratos não têm valor único
moeda:                                # (opcional)
contraparte:                          # (opcional) FK — ver conflito C1
lancamentos: []                       # (opcional) FKs → lançamentos que este documento comprova
periodo_inicio:                       # (opcional) AAAA-MM-DD, para extratos
periodo_fim:                          # (opcional) AAAA-MM-DD, para extratos
status_fiscal:                        # (opcional) pendente | escriturado | nao-aplica
tags: []                              # (opcional)
---
```

- **`arquivo_real` obrigatório** — reusa deliberadamente a chave já canonizada em DI-002 para `documento`, em vez de inventar `localizacao_digital`. Um documento financeiro sem o arquivo real é um registro sem valor probatório.
- **`lancamentos` como lista** — um extrato comprova muitos lançamentos; uma NF pode cobrir vários itens. A cardinalidade é 1:N, e a FK mora do lado do documento para que o lançamento permaneça um arquivo pequeno e estável.

### 2.4 `categoria-financeira` — `Empresas/_Compartilhado/Plano de Contas/<slug>.md`

```yaml
---
tipo: categoria-financeira            # (obrigatório)
titulo: Insumos Operacionais          # (obrigatório)
direcao_padrao: saida                 # (obrigatório) entrada | saida | ambas
grupo: custo-variavel                 # (obrigatório) receita | custo-fixo | custo-variavel | imposto | investimento | retirada | transferencia
ativa: true                           # (obrigatório) booleano
descricao:                            # (opcional)
---
```

Compartilhada entre as três entidades **por escolha**: é o que torna os relatórios de CLEAN TOUCH, BOWL GREEN e PF comparáveis entre si. Planos de conta separados por empresa impedem qualquer visão consolidada.

### 2.5 `conta-financeira` — `Empresas/<Empresa>/Contas/<slug>.md`

```yaml
---
tipo: conta-financeira                # (obrigatório)
titulo: Conta Corrente Banco X        # (obrigatório)
empresa: clean-touch                  # (obrigatório) FK → empresa
especie: conta-corrente               # (obrigatório) conta-corrente | poupanca | caixa | cartao-credito | carteira-digital
moeda: BRL                            # (obrigatório)
situacao: ativa                       # (obrigatório) ativa | encerrada
instituicao:                          # (opcional)
saldo_inicial:                        # (opcional) número
data_saldo_inicial:                   # (opcional) AAAA-MM-DD
---
```

`saldo_inicial` + `data_saldo_inicial` existem porque o saldo atual só é calculável se houver um ponto de partida ancorado.

### 2.6 `relatorio-financeiro` — `Empresas/<Empresa>/Relatórios/AAAA/<slug>.md`

```yaml
---
tipo: relatorio-financeiro            # (obrigatório)
titulo: Fluxo de Caixa — 2026-07      # (obrigatório)
empresa: clean-touch                  # (obrigatório) FK → empresa
especie: fluxo-de-caixa               # (obrigatório) fluxo-de-caixa | resultado | rollup-mensal | rollup-anual
periodo_inicio: 2026-07-01            # (obrigatório) AAAA-MM-DD
periodo_fim: 2026-07-31               # (obrigatório) AAAA-MM-DD
base_temporal: caixa                  # (obrigatório) caixa | competencia
derivado: true                        # (obrigatório) sempre true
gerado_em: 2026-08-01                 # (obrigatório) AAAA-MM-DD
---
```

`derivado` e `gerado_em` são o que impedem `Relatórios/` de virar uma violação de SSOT: marcam explicitamente o arquivo como descartável e regenerável. `base_temporal` registra qual das duas datas foi usada — sem ele, dois relatórios do mesmo mês com números diferentes são indistinguíveis e ambos parecem errados.

### Faseamento sugerido

Seis tipos de uma vez é muito. Fase 1 mínima viável: **`empresa`, `categoria-financeira`, `lancamento`**. `documento-financeiro` na Fase 2, `conta-financeira` e `relatorio-financeiro` na Fase 3. Todas as FKs para tipos adiados já nascem opcionais, então nada quebra.

---

## 3. Limiar de SQLite — o número

**Resposta curta: 250 lançamentos/mês por entidade (≈ 750/mês somando as três, ≈ 9.000/ano). Nesse ponto SOP-002 deixa de ser opcional.**

**Limiar leve, muito antes disso: 80 lançamentos/mês por entidade.** Aí não é SQLite ainda — é obrigatoriedade de rollups mensais em `Relatórios/`.

### O raciocínio

O gargalo **não é a contagem de arquivos do vault**. É quantos arquivos precisam ser lidos numa única passagem para produzir um relatório correto.

1. **Custo por lançamento.** Frontmatter de ~14 chaves + corpo curto + overhead de leitura ≈ **200 tokens/arquivo**. Estimativa conservadora.

2. **Teto de agregação confiável numa passagem: ~50.000 tokens, ou ~250 arquivos.** Este é o número operante. Não é o limite de contexto — é o ponto onde a aritmética sobre muitos arquivos começa a produzir erros silenciosos de soma e o custo de reler para conferir passa a dominar. Numa base financeira, um erro silencioso de soma é pior que uma falha.

3. **Relatório mensal.** Lê um mês de uma entidade. A 250 lançamentos/mês, são exatamente 50K tokens — no teto. **Este é o limiar duro.** Acima disso, nem o relatório mais básico que a Gê pediu cabe numa passagem confiável.

4. **Relatório anual.** 12 × 250 = 3.000 arquivos = 600K tokens. Inviável direto — e é por isso que os rollups mensais existem. O relatório anual lê **12 rollups**, não 3.000 lançamentos. É esse degrau hierárquico que mantém markdown viável muito além do que a leitura ingênua sugere, e é por isso que o limiar leve (80/mês) importa: passado ele, o anual sem rollup já não fecha.

5. **Verificação cruzada contra o SOP-002 existente.** O SOP-002 dispara em ~5.000 arquivos markdown. A 750 lançamentos/mês somando as três entidades, o vault cruza 5.000 arquivos **no sétimo mês**. Os dois limiares concordam — o meu, derivado do custo de relatório, e o do SOP-002, derivado do tamanho do vault, apontam para a mesma faixa. É isso que torna o número defensável e não arbitrário.

### Tabela de decisão

| Lançamentos/mês por entidade | Regime |
|---|---|
| até 80 | Markdown puro. Relatórios sob demanda, leitura direta. |
| 80 – 250 | Markdown + **rollups mensais obrigatórios** em `Relatórios/`. Anual lê rollups. |
| acima de 250 | **SOP-002 obrigatório.** Markdown segue canônico; SQLite passa a ser o motor de todo relatório. |

Uma qualificação honesta: se a Gê importar extratos bancários lançamento a lançamento, 250/mês é atingido rápido — uma conta PJ movimentada sozinha faz isso. Se ela lançar de forma consolidada (agrupando por dia ou por categoria), pode ficar em markdown por anos. **A política de granularidade de lançamento decide quando o SQLite chega**, e é uma decisão dela, não uma consequência do tamanho do negócio.

---

## 4. Conflitos com a arquitetura atual

### C1 — `Empresas/` × `Wiki pessoal/CRM/Organizações/` (o risco central de SSOT)

**Minha leitura:** as empresas dela são entidades de `Empresas/`, **não** Organizações do CRM. Não são as duas coisas.

`CRM/Organizações/` é o registro da rede de **terceiros** dela — o modelo canônico (`organizacao.md`) tem seções "Como trabalhamos juntos" e "Pessoas aqui", que só fazem sentido para uma contraparte externa. A Gê não tem um relacionamento com CLEAN TOUCH; ela **é** a CLEAN TOUCH. Espelhar `empresa.md` em `CRM/Organizações/clean-touch.md` duplicaria nome, setor e identidade em dois arquivos — violação direta da Regra de Ouro.

**Recomendação:** `Empresas/<Empresa>/empresa.md` é a SSOT única. O campo `organizacao_crm` que propus fica **vazio por padrão**, e só é usado se a Gê realmente precisar que uma empresa dela apareça na rede de relacionamento por algum motivo específico. Nesse caso o arquivo CRM é um stub com um wikilink, sem fatos próprios.

**Mas o conflito de verdade é outro e é mais grave:** onde ficam os **clientes e fornecedores** de CLEAN TOUCH?

Eles são inequivocamente organizações. E a decisão dela é que `Wiki pessoal/` é exclusivamente pessoal. Essas duas coisas não podem ser verdade ao mesmo tempo:

- **Opção A** — contrapartes vão para `Wiki pessoal/CRM/`. Zero duplicação, reusa tudo que existe. **Mas fura a parede pessoal/negócio** que ela acabou de decidir erguer, e mistura as carteiras de clientes das três entidades num só lugar.
- **Opção B** — CRM por empresa, em `Empresas/<Empresa>/Contatos/`. Separação limpa. **Mas** um contador que atende CLEAN TOUCH, BOWL GREEN e a Gê PF passa a existir em três arquivos. Violação de SSOT garantida.
- **Opção C (minha recomendação)** — promover o CRM para o topo do vault, fora de `Wiki pessoal/`, como registro único de identidade de qualquer contraparte. `Empresas/` nunca guarda identidade, só FKs por slug. Resolve A e B de uma vez.

O custo da Opção C é real e preciso ser explícito: **exige mover `Wiki pessoal/CRM/` e editar `AGENTS.md` (linha 66) e `Wiki pessoal/INDEX.md`**. É a mudança estrutural mais cara desta proposta e ela precisa aprovar sabendo disso. Não toquei em nada.

Enquanto ela não decidir, `contraparte` fica opcional em todos os schemas e nenhum lançamento fica bloqueado.

### C2 — A Gê PF não é uma empresa

A decisão diz "pasta `Empresas/`, uma subpasta por empresa" — mas cobre 2 das 3 entidades. A pessoa física dela não tem nome de empresa e não é uma empresa.

Não estou reabrindo a decisão da separação em três. Estou apontando que ela não especifica onde a PF mora. Opções: `Empresas/Gê PF/` (semanticamente torto mas funciona, e o campo `natureza: pessoa-fisica` absorve a diferença de comportamento), ou renomear a pasta topo para `Financeiro/`. Prefiro a primeira — é menos invasiva e o schema já resolve.

### C3 — `documento-financeiro` × `documento` existente

Propus um tipo novo em vez de reusar `documento`. Justificativa: o `documento` existente é de identidade/patrimônio pessoal (passaporte, contratos), tem `valido_ate`/`gatilho_renovacao` e vive plano em `Wiki pessoal/Documentos/`. Documento financeiro tem `empresa`, `competencia`, `valor`, vínculo com lançamentos, e vive aninhado por data em alto volume. Forçar um tipo só produziria uma entidade onde metade dos campos é sempre nula.

**Risco de fronteira que ela precisa arbitrar:** um contrato de prestação de serviço da CLEAN TOUCH é `documento` (é contrato) ou `documento-financeiro` (é da empresa)? Minha regra proposta: **se pertence a uma das três entidades financeiras, é `documento-financeiro`, sem exceção.** Regra única, sem julgamento caso a caso.

### C4 — Deriva de schema já existente (achado colateral, mas relevante)

Encontrei durante o inventário. Não é causado por esta proposta, mas contamina qualquer coisa nova que se apoie nos modelos:

- **`Wiki equipe/Modelos/organizacao.md` não bate com DI-002.** O modelo usa `tipo_org`, `industria`, `email`, `telefone`, `cidade`. DI-002 especifica `tipo`, `nome`, `setor`, `website`, `primeira_menção`. O modelo **não tem o campo `tipo:`**, que DI-002 marca como estrutural.
- **`Wiki equipe/Modelos/documento.md` não bate com DI-002.** Modelo: `tipo_doc`, `localizacao_fisica`, `localizacao_digital`, `emitido_em`, `data_validade`, `gatilho_renovacao`, `vinculado_pessoas`, `vinculado_organizacoes`. DI-002: `numero`, `valido_ate`, `arquivo_real`. Praticamente disjuntos.
- **`Wiki pessoal/CRM/Organizações/clinica-dra-ana.md` não tem frontmatter nenhum.** Todos os fatos estão em negrito no corpo.

Consequência prática: se a Gê aprovar esta proposta, os modelos novos vão ser mais rigorosos que os antigos, e o script do SOP-002 (que lê nomes de coluna de DI-002, por instrução explícita) vai gerar colunas vazias para organização e documento. **Isto é uma auditoria de frontmatter separada que eu recomendo agendar** — não a executei e não editei nada, conforme instruído.

### C5 — DI-001 não governa nomes de pasta de conteúdo

DI-001 §1 proíbe espaços em slugs; §4 cobre pastas de especialista. Nenhuma regra cobre pastas de conteúdo — e o vault na prática usa Title Case com espaços e acentos (`Wiki pessoal`, `Minha Vida`, `Organizações`).

Segui o padrão de fato (`Empresas/Clean Touch/`). Mas isso significa que o slug da empresa (`clean-touch`, usado em milhares de FKs) **não deriva mecanicamente do nome da pasta** — é exatamente por isso que `slug` é obrigatório no frontmatter de `empresa`. Recomendo adicionar uma §8 a DI-001 fixando a regra de nomes de pasta de conteúdo. Não editei DI-001.

---

## 5. Perguntas em aberto para a Gê

**Bloqueiam a Fase 1:**

1. **Qual o ramo de CLEAN TOUCH e de BOWL GREEN?** Não sei, não inventei. Afeta o plano de contas inteiro.
2. **CNPJ e regime tributário de cada uma?** Determina se guias de imposto e obrigações acessórias entram no plano de contas.
3. **C1 — onde moram clientes e fornecedores?** Opção A, B ou C. Sem isso, `contraparte` fica vazio e nenhum relatório por cliente/fornecedor é possível.
4. **C2 — como nomear a pasta da PF dela?**
5. **Granularidade de lançamento: extrato linha a linha, ou consolidado?** Decide diretamente quando o SQLite vira obrigatório (§3).

**Não bloqueiam, mas moldam o schema:**

6. **Alguma entidade opera em moeda diferente de BRL?** O `moeda_base` é obrigatório justamente para não assumir.
7. **Há histórico a importar** (planilha, app de contabilidade, extratos antigos)? Se sim, isso é FT-002 e muda o plano de execução.
8. **Existe fluxo entre as entidades** — aporte da PF na empresa, pró-labore, transferência entre CLEAN TOUCH e BOWL GREEN? Se sim, um evento gera dois lançamentos espelhados em pastas diferentes, e isso precisa de tratamento explícito para não virar duplicação (provavelmente `categoria: transferencia` + FK cruzada). Não cobri no schema acima.
9. **Ela quer visão consolidada das três?** Se sim, o plano de contas compartilhado deixa de ser conveniência e vira requisito.

---

## 6. Estado

Nada foi criado. Nenhum `AGENTS.md`, `DI-002` ou modelo existente foi modificado. Este arquivo é o único artefato desta rodada.

Ordem de execução após aprovação: **DI-002 primeiro** (registrar os campos), **modelos depois**, **estrutura de pastas por último**. Um arquivo escrito antes de DI-002 estar atualizado usa campos que, pela regra do AGENTS.md, não existem.
