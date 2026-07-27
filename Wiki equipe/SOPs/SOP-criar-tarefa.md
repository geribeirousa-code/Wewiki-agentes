# SOP — Criar uma Tarefa

- **Dono:** qualquer agente
- **Acionado por:** um agente ou a usuária identificando uma unidade de trabalho que não terminará nesta rodada e precisa ser retomada depois
- **Saída:** um novo arquivo em `Wiki equipe/tarefas/abertas/`
- **Referências:** [[SOP-reconstruir-indice-tarefas]], [[SOP-assumir-tarefa]], [[DI-001-convencoes-de-nomeacao]]

## Propósito

Uma tarefa é um **ponto de retomada**. Quem abrir o arquivo depois — a Gê, o responsável, um agente diferente — deve conseguir reconstruir o contexto completo de trabalho a um wikilink de distância. Criar uma tarefa bem é tornar essa retomada fácil. A disciplina de preencher as referências cruzadas na criação é a essência deste trabalho.

## Quando acionar

Você está conversando com a usuária (ou outro agente) e uma tarefa é identificada que:
- Não terminará nesta rodada, E
- Precisa ser lembrada/transferida, E
- Não está coberta por uma tarefa existente (primeiro faça grep).

Se as três condições forem verdadeiras, crie uma tarefa. Caso contrário, execute agora.

## Entradas necessárias

| Entrada | Obrigatória | Notas |
|---|---|---|
| Título | sim | Uma frase. Sem ponto final. |
| Descrição | sim | Um parágrafo: o que é o trabalho, como é o sucesso. |
| Responsável | sim | Nome do agente ou `não-atribuído` se o roteamento for incerto. |
| Prioridade | não | 1=urgente, 2=alta, 3=normal (padrão), 4=baixa. |
| Etiquetas | não | Minúsculas, kebab-case ou snake_case. |
| Origem | não | De onde veio a solicitação. |
| Tarefa pai | não | ID da tarefa pai se esta for uma subtarefa. |
| Data-limite | não | Data ISO. |
| **Referências cruzadas** | **sim (cada uma pode ser array vazio)** | Os seis arrays `vinculado_*`. Veja passo 5. |

## Passos

### 1. Verificar duplicatas

```bash
grep -ril "<palavra-chave do título>" \
  "Wiki equipe/tarefas/abertas" \
  "Wiki equipe/tarefas/em-andamento"
```

Se uma tarefa já existir, acrescente uma linha de atualização na seção `## Atualizações` em vez de criar duplicata. Pronto.

### 2. Gerar o ID da tarefa

```bash
TODAY=$(date -u +%Y-%m-%d)
NEXT=$(find "Wiki equipe/tarefas" -name "tsk-${TODAY}-*.md" 2>/dev/null | wc -l | awk '{printf "%03d", $1+1}')
ID="tsk-${TODAY}-${NEXT}"
```

Se a criação falhar porque o arquivo já existe (corrida com outro agente), incremente `NEXT` e tente novamente. Até 5 tentativas.

### 3. Transformar o título em slug

```bash
SLUG=$(echo "<título>" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' | cut -c1-50 | sed -E 's/-+$//')
FILENAME="${ID}-${SLUG}.md"
```

### 4. Confrontar as referências cruzadas (o coração deste SOP)

Antes de escrever o arquivo, percorra os seis tipos de referência e decida o que se aplica. Arrays vazios são válidos; a disciplina é fazer a varredura, não encontrar algo em cada slot.

| Tipo de referência | Pergunte-se |
|---|---|
| `vinculado_sops` | Existe um procedimento em `Wiki equipe/SOPs/` que governa este tipo de trabalho? Liste os nomes base. |
| `vinculado_fluxos` | Existe um arco ativo em `Wiki equipe/Fluxos de Trabalho/` em que isso se encaixa? |
| `vinculado_diretrizes` | Existem padrões em `Wiki equipe/Diretrizes/` que restringem como isto deve ser feito? |
| `vinculado_minha_vida` | Existe um Tópico / Hábito / Meta / Projeto / Pilar em `Wiki pessoal/Minha Vida/` que fornece contexto para a Gê sobre por que isso está acontecendo? |
| `vinculado_logs_sessao` | Qual(is) sessão(ões) originou(aram) ou tocou(aram) nisto? No mínimo, a sessão em que você está agora. |
| `vinculado_entradas_diario` | O responsável (ou alguém) escreveu uma entrada de diário que é aprendizado anterior relevante? |

Para cada um, liste os nomes base. Use grep quando incerto:

```bash
ls "Wiki equipe/SOPs/" | grep -i <palavra-chave>
ls "Wiki equipe/Fluxos de Trabalho/"
ls "Wiki equipe/Diretrizes/"
find "Wiki pessoal/Minha Vida" -name "*.md" | grep -i <palavra-chave>
find "Wiki equipe/logs-de-sessao" -name "*.md" | tail -5
find "Equipe" -path "*/diario/*.md" | grep -i <palavra-chave>
```

### 5. Escrever o arquivo

Copie `Wiki equipe/tarefas/_modelo.md` para `Wiki equipe/tarefas/abertas/${FILENAME}`. Preencha:

- Todos os campos de identidade, propriedade, status, tempo e proveniência
- Todos os seis arrays `vinculado_*` (use `[]` se genuinamente nenhum — mas somente após percorrer o passo 4)
- Etiquetas
- Corpo: `## O que é isto`, `## Contexto a um clique`, `## Critérios de sucesso`, `## Atualizações`

A seção `## Contexto a um clique` no corpo deve espelhar os arrays `vinculado_*` do frontmatter como `[[wikilinks]]` — é assim que a leitora obtém navegação de um clique. O frontmatter é para leitura por máquina; os wikilinks no corpo são para humanos. Ambos preenchidos e mantidos em sincronia.

`criado` e `atualizado` são RFC3339 UTC: `date -u +%Y-%m-%dT%H:%M:%SZ`.

### 6. Acrescentar a primeira linha de atualização

```markdown
- 2026-05-10 12:34 (seu-nome-de-agente) — criado
```

### 7. Reconstruir o índice

Execute [[SOP-reconstruir-indice-tarefas]]. Sempre.

### 8. Reportar de volta

Informe ao usuário/agente que chamou:

```
Criado [[<id>-<slug>]] (prioridade <N>, responsável <nome>).
Refs cruzadas: <contagem de arrays vinculado_* preenchidos> preenchidas.
```

## Erros comuns

- **Pular a varredura de referências cruzadas** porque "não sei o que se aplica." Exatamente quando a varredura é mais importante — ela obriga você a fazer grep e confirmar. Arrays vazios são válidos; não ter feito a varredura não é.
- Criar uma tarefa para algo que você fará nesta rodada. Simplesmente faça agora.
- Pular a verificação de duplicatas.
- Esquecer `criado_por`. O rastro de auditoria morre sem isso.
- Colocar o responsável no corpo em vez do frontmatter. O frontmatter é a fonte de verdade para o roteamento.
- Listar wikilinks no corpo mas esquecer de espelhá-los no frontmatter `vinculado_*` (ou vice-versa). Eles precisam corresponder.
- Envolver nomes base em `[[...]]` dentro do frontmatter YAML — o Obsidian não renderiza wikilinks YAML de forma confiável. O YAML usa nomes base simples; o corpo usa `[[nomebase]]`.
