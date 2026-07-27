# SOP — Reconstruir Índice de Tarefas

- **Dono:** qualquer agente (chamado automaticamente por cada SOP que toca tarefas)
- **Acionado por:** fim de [[SOP-criar-tarefa]], [[SOP-assumir-tarefa]], [[SOP-fechar-tarefa]]; ou início de sessão se `INDEX.md` estiver desatualizado
- **Saída:** `Wiki equipe/tarefas/INDEX.md` reescrito
- **Referências:** todos os SOPs de tarefas

## Propósito

`INDEX.md` é a visão de resumo de retomada da pasta de tarefas. Existe para que um agente ou a Gê possam ler um único arquivo no início da sessão e saber o que está aberto, em andamento, bloqueado e recentemente fechado sem percorrer a árvore.

Este SOP mantém essa visão atualizada. Cada SOP que toca tarefas o chama como último passo. O Larry também o chama no início da sessão se o mtime do índice for mais antigo que o mtime do arquivo de tarefa mais recente.

## Orçamento de desempenho

Critério de aceite: deve funcionar em 50+ tarefas, rápido. A implementação usa `awk` para análise de frontmatter — passo único, sem dependência de biblioteca yaml. Meta de menos de 500ms em 1000 tarefas.

## Passos

### 1. Coletar todos os arquivos de tarefa

```bash
RAIZ_TAREFAS="Wiki equipe/tarefas"
ARQUIVOS=$(find "$RAIZ_TAREFAS/abertas" "$RAIZ_TAREFAS/em-andamento" "$RAIZ_TAREFAS/concluidas" "$RAIZ_TAREFAS/canceladas" -name "tsk-*.md" -type f 2>/dev/null)
```

### 2. Analisar o frontmatter de cada arquivo

Para cada arquivo, extrair `id`, `titulo`, `atribuido_a`, `prioridade`, `status`, `criado`, `atualizado`, `pai`, `motivo_bloqueio`, `bloqueado_por`. O frontmatter está entre as duas primeiras linhas `---`. Passo único de awk.

### 3. Agrupar por status

- `abertas` (ordenadas por prioridade, depois por data dentro da prioridade)
- `em-andamento` (data de assunção, decrescente; tarefas bloqueadas sinalizadas)
- `recentemente_concluidas`: somente de `concluidas/`, últimos 7 dias, decrescente
- `recentemente_canceladas`: somente de `canceladas/`, últimos 7 dias, decrescente

### 4. Renderizar INDEX.md

```markdown
# Índice de Tarefas

_Gerado automaticamente. Não edite manualmente. Execute `SOP-reconstruir-indice-tarefas` para regenerar._

_Última reconstrução: <RFC3339 UTC>_

## Resumo
- Abertas: <N>
- Em andamento: <N> (<M> bloqueadas)
- Concluídas (este mês): <N>
- Canceladas (este mês): <N>

## Abertas (<N>)

### Prioridade 1 — urgente
- [[<id>-<slug>]] — <título> — responsável: <nome> — criada <data>

### Prioridade 2 — alta
...

### Prioridade 3 — normal
...

### Prioridade 4 — baixa
...

## Em andamento (<N>)
- [[<id>-<slug>]] — responsável: <nome> — assumida <data>
- [[<id>-<slug>]] — responsável: <nome> — BLOQUEADA: <motivo em uma linha>

## Por responsável
- mack: <N> abertas, <N> em andamento (<M> bloqueadas)
- silas: ...

## Recentemente fechadas (últimos 7 dias)
- <data> [[<id>-<slug>]] — concluída — <nome-de-quem-fechou>
- <data> [[<id>-<slug>]] — cancelada — <nome-de-quem-fechou>
```

### 5. Escrever atomicamente

```bash
TMP=$(mktemp)
# renderizar para $TMP
mv "$TMP" "$RAIZ_TAREFAS/INDEX.md"
```

Movimentação atômica para que leitores concorrentes nunca vejam um arquivo parcial.

### 6. Validar

```bash
grep -q "^_Gerado automaticamente\." "$RAIZ_TAREFAS/INDEX.md" || { echo "reconstrução falhou"; exit 1; }
```

## Correção de deriva

Ao iterar, o SOP de reconstrução corrige dois tipos de deriva que encontrar:

### Divergência status-vs-pasta

Se o campo `status:` de uma tarefa discordar de sua localização de pasta, **a pasta vence**. O SOP de reconstrução atualiza o campo `status:` do frontmatter no lugar, atualiza `atualizado` e acrescenta uma linha de atualização:

```
- <data> <hora> (reconstrução) — campo status corrigido para corresponder à pasta
```

### Deriva nome-de-arquivo-vs-id

Se o slug do nome de arquivo de uma tarefa não corresponder ao slug do `titulo` do frontmatter (porque o título foi editado), o SOP de reconstrução renomeia o arquivo com `git mv` para alinhá-los. A parte id do nome de arquivo é autoritativa e nunca muda.

## Erros comuns

- Editar `INDEX.md` manualmente. As edições são perdidas na próxima reconstrução.
- Esquecer de percorrer `concluidas/<AAAA>/<MM>/` e `canceladas/<AAAA>/<MM>/`. A seção "recentemente fechadas" precisa delas.
- Procurar tarefas bloqueadas em uma pasta `bloqueadas/`. Não existe tal pasta. Tarefas bloqueadas estão em `em-andamento/` com `motivo_bloqueio` definido.
- Executar a reconstrução durante um `git mv` (corrida). Não faça. Execute após cada SOP completar sua movimentação; essa ordem está incorporada nos outros SOPs.
