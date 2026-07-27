# DI-001 - Convenções de Nomenclatura

> **Esta Diretriz é uma regra geral que todo agente lê em toda ação relevante.** Todo arquivo escrito na sua WeWiki — por qualquer especialista, em qualquer pasta — segue as regras abaixo. SOPs e Fluxos de Trabalho apontam via `[[wikilink]]` aqui em vez de reeditar as regras.

Esta é a fonte de verdade de como os arquivos na sua WeWiki são nomeados.

## Regras fundamentais

### 1. kebab-case para slugs

- Tudo em minúsculas.
- Palavras separadas por hifens simples.
- Sem underscores, sem espaços, sem camelCase, sem Título com Maiúscula.
- Apenas ASCII dentro dos slugs. Use o equivalente ASCII mais próximo para letras acentuadas.

Bom: `sessao-matinal-de-construcao`, `dra-ana`, `lançar-mvp-ate-q3`.
Ruim: `Sessao_Matinal_de_Construcao`, `dr.schmidt`, `Lançar MVP Até Q3`.

### 2. Prefixo de data ISO em arquivos por data

Arquivos que pertencem a um dia de calendário específico começam com `AAAA-MM-DD-`.

Padrão: `AAAA-MM-DD-<slug>.<ext>`

Aplica-se a:

- Entradas de diário: `Wiki pessoal/Diário/AAAA/MM/AAAA-MM-DD-<slug>.md`
- Imagens: `Wiki pessoal/Imagens/AAAA/MM/AAAA-MM-DD-<slug>.<ext>`
- Logs de sessão: `Wiki equipe/logs-de-sessao/AAAA/MM/AAAA-MM-DD-<slug>.md`
- Entregas com data: `Entregas/AAAA-MM-DD-<slug>.md`

Exemplos:
- `2026-05-04-primeiro-dia.md`
- `2026-05-04-cartao-visita-dra-ana.png`
- `2026-05-04-kickoff-pesquisa-precos.md`

### 3. Regras de slug

- Derive o slug do assunto principal do arquivo em 2 a 5 palavras.
- Pule palavras de preenchimento ("o", "a", "de") a menos que mudem o significado.
- Para pessoas, use `primeironome-sobrenome` ou `titulo-sobrenome` se o título faz parte de como o usuário se refere a eles. Exemplo: `dra-ana`.
- Para organizações, inclua contexto suficiente para desambiguar. Exemplo: `clinica-dra-ana` em vez de `clinica`.

### 4. Nomenclatura de pastas para contratos de especialistas

Padrão: `Equipe/<Nome> - <Papel>/AGENTS.md` com um literal espaço-hífen-espaço entre nome e papel.

Exemplos:
- `Equipe/Larry - Orquestrador/`
- `Equipe/Penn - Escritor de Diário/`

### 5. Nomenclatura de arquivos da Wiki equipe

| Tipo | Padrão |
|---|---|
| SOPs | `SOP-NNN-<slug>.md` onde NNN é zero-padded (001, 002…) |
| Fluxos de Trabalho | `FT-NNN-<slug>.md` |
| Diretrizes | `DI-NNN-<slug>.md` |

Slugs para SOPs, FTs e DIs: derivados do nome/propósito do procedimento.

### 6. Nomenclatura de tarefas

Padrão: `tsk-AAAA-MM-DD-NNN-<slug>.md` onde NNN é o número de ordem do dia (001, 002…).

### 7. Arquivos de índice e README

- `INDEX.md` — hub de navegação para uma seção. Uma pasta, um INDEX.
- `README.md` — nota explicativa para uma pasta. Geralmente vista por humanos, não pelo LLM.
- Estes dois nomes são reservados. Não nomeie outros arquivos com eles.

## O que nunca fazer

- Não use espaços em nomes de arquivos ou slugs.
- Não use camelCase em slugs de arquivos markdown.
- Não repita o nome da pasta no slug do arquivo se for redundante.
- Não use underscores (exceto em convenções técnicas de outros domínios onde underscore é o padrão).
