# SOP — Escrever uma Entrada de Diário

- **Dono:** qualquer agente especialista (cada agente é dono do seu próprio `diario/`)
- **Acionado por:** um aprendizado que se aplicará a sessões futuras, não apenas a esta
- **Saída:** um novo arquivo em `Equipe/<Nome> - <Papel>/diario/`
- **Referências:** [[SOP-ler-proprio-diario]], [[SOP-escrever-log-de-sessao]]

## Propósito

Uma entrada de diário é a superfície de continuidade do responsável para aprendizado entre sessões. Captura algo durável — uma lição, uma regra de decisão, um antipadrão — que o você-do-futuro (ou outra instância de você) vai querer aplicar quando surgir uma situação semelhante.

## O que uma entrada de diário É

Uma nota temática e durável. Primeira pessoa. Com opinião. Exemplos:
- "Webhook 401 em produção — sempre verificar deriva de variáveis de ambiente primeiro."
- "Quando o índice pgvector tem mais de 1M de linhas, mudar de IVFFlat para HNSW."
- "Disciplina de paleta quente: nunca usar cinzas frios com o acento dourado."

## O que uma entrada de diário NÃO É

- Um log de sessão (cronológico, efêmero, fica em `Wiki equipe/logs-de-sessao/`).
- Uma tarefa (trabalho a fazer, fica em `Wiki equipe/tarefas/`).
- Uma Diretriz (referência para toda a equipe; fica em `Wiki equipe/Diretrizes/`).
- Um diário pessoal. Não escreva uma por dia por escrever.

Se o aprendizado se aplica a toda a equipe e é permanente, pertence a `Wiki equipe/Diretrizes/` como `DI-xxx.md`. Diários são com escopo de agente. Diretrizes são com escopo de equipe.

## Quando escrever

O teste de gatilho:

> "Eu (ou outra instância de mim) vou querer encontrar este aprendizado daqui a três meses, no meio de uma tarefa diferente, e que ele mude o que faço?"

Sim → escreva. Talvez → escreva curto. Não → não escreva.

## Passos

### 1. Escolher um slug de tópico

Frase curta única em kebab-case. Torna-se parte do nome do arquivo e do campo `topico` do frontmatter.

Bom: `pipelines-de-construcao`, `dimensionamento-indice-vetor`, `disciplina-paleta-quente`.
Ruim: `aprendizados`, `notas`, `pensamentos-de-sexta`.

### 2. Escolher um nome de arquivo

```
Equipe/<Nome> - <Papel>/diario/AAAA-MM-DD-<slug-topico>.md
```

A data é **hoje** — a data de nascimento do aprendizado. O slug descreve o *aprendizado*, não o *evento* que o gerou.

### 3. Copiar o modelo

```bash
cp "Equipe/<Nome> - <Papel>/diario/_modelo.md" \
   "Equipe/<Nome> - <Papel>/diario/AAAA-MM-DD-<slug>.md"
```

### 4. Preencher o frontmatter

```yaml
---
id_agente: <eu-mesmo>
tipo: entrada-diario
criado: <RFC3339 UTC>
atualizado: <RFC3339 UTC>
topico: <slug-topico>
tags: [tag1, tag2]
vinculado_logs_sessao: [<nome-base-do-log-de-sessao>]
vinculado_tarefas: [<id-de-tarefa-se-relevante>]
entradas_diario_relacionadas: []
status: duravel
---
```

`status: duravel` é o padrão. Marque `superado` depois se uma entrada mais nova substituir esta.

### 5. Preencher o corpo

Use os cabeçalhos de seção do modelo. Conciso é melhor:

```markdown
# {O aprendizado em uma frase — este é o título}

## Contexto
{Duas frases no máximo. O que aconteceu que me fez escrever isto.}

## O que aprendi
{O aprendizado real. Direto, com opinião, sem rodeios. Ressalvas vão em "Quando NÃO se aplica."}

## Quando se aplica
{Condições de gatilho concretas. "Na próxima vez que eu estiver empacotando um app para Linux e o sidecar for um binário auto-extraível..."}

## Quando NÃO se aplica
{Anti-aplicabilidade. Igualmente importante.}

## Evidências
{Wikilinks para logs de sessão, tarefas, commits, documentos externos.}
```

### 6. Fazer referência cruzada a partir da origem

Se o aprendizado veio de uma sessão, acrescente um wikilink de uma linha no final do log de sessão: `Diário: [[AAAA-MM-DD-<slug>]]`.

Se veio do `## Resultado` de uma tarefa, faça referência a partir daí E adicione o nome base do diário ao array `vinculado_entradas_diario` do frontmatter da tarefa.

### 7. Verificação de orçamento de etiquetas

As etiquetas devem ser funcionalmente distintas, não sinônimos. `webhook` e `webhook-autenticacao` está bem; `webhook` e `webhooks` não. Mira de 2 a 5 etiquetas.

## Erros comuns

- Escrever uma entrada de diário que é apenas um resumo de log de sessão. Se não passar no teste dos três meses, é um log de sessão.
- Títulos vagos ("aprendizados de hoje"). O título É o aprendizado. Declare-o.
- Sem seção "Quando NÃO se aplica". Sem ela, o você-do-futuro aplica o aprendizado onde não se encaixa.
- Escrever uma entrada de diário em vez de propor uma Diretriz. Se a regra se aplica à equipe toda e é permanente, é uma Diretriz.
- Editar uma entrada de diário antiga para atualizá-la. Em vez disso: escreva uma nova, marque a antiga como `status: superado`, vincule-as via `entradas_diario_relacionadas`. Preserva o rastro de auditoria.
- Esquecer de adicionar o nome base da entrada ao `vinculado_entradas_diario` da tarefa que originou o aprendizado.
