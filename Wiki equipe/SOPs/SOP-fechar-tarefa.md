# SOP — Fechar uma Tarefa (Concluída ou Cancelada)

- **Dono:** o agente que termina a tarefa (para concluída) ou a Gê/Larry (para cancelar)
- **Acionado por:** entrega do trabalho da tarefa ou abandono
- **Saída:** arquivo de tarefa arquivado em `concluidas/<AAAA>/<MM>/` ou `canceladas/<AAAA>/<MM>/`
- **Referências:** [[SOP-reconstruir-indice-tarefas]], [[SOP-escrever-entrada-diario]]

## Propósito

Fechar uma tarefa é registrar "este ponto de retomada agora é história." A seção `## Resultado` é a carga útil de continuidade — o que foi entregue, onde fica, quais acompanhamentos existem. Quem ler a tarefa fechada deve conseguir reconstruir o que foi realizado sem abrir mais nada.

## Dois subprocedimentos

- **§A Concluída:** sucesso terminal. Mover para `concluidas/<AAAA>/<MM>/`.
- **§B Cancelada:** abandono terminal. Mover para `canceladas/<AAAA>/<MM>/`.

Ambas são terminais. Uma vez que uma tarefa está em `concluidas/` ou `canceladas/`, não a mova de volta. Se o trabalho precisar ser reaberto, crie uma nova tarefa com `pai: <id-antigo>`.

## §A — Marcar como concluída

### Pré-voo

1. **Verificar critérios de sucesso.** Releia a seção `## Critérios de sucesso` do corpo da tarefa. Todos atendidos? Se não, a tarefa não está pronta.

2. **Verificar subtarefas.**
   ```bash
   grep -rl "pai: <id>" "Wiki equipe/tarefas/abertas" "Wiki equipe/tarefas/em-andamento"
   ```
   Se houver subtarefas ainda abertas ou em andamento: superfície-as. Decida explicitamente se vai (a) fechá-las também, (b) deixá-las como acompanhamentos independentes, ou (c) manter este pai aberto até que se resolvam. Documente a decisão no `## Resultado` do pai.

### Passos

1. **Determinar o caminho de arquivamento.**
   ```bash
   ANO=$(date -u +%Y)
   MES=$(date -u +%m)
   DEST="Wiki equipe/tarefas/concluidas/${ANO}/${MES}"
   mkdir -p "$DEST"
   ```

2. **Mover o arquivo.** A origem é `em-andamento/`:
   ```bash
   git mv "Wiki equipe/tarefas/em-andamento/<id>-<slug>.md" "$DEST/<id>-<slug>.md"
   ```

3. **Atualizar frontmatter:** `status: concluida`, atualizar `atualizado`. Limpar `motivo_bloqueio` e `bloqueado_por` se estiverem definidos.

4. **Escrever a seção `## Resultado`.** Obrigatória. Estrutura:

   ```markdown
   ## Resultado

   O que foi entregue: <resumo em um parágrafo>.

   Onde fica: [[<wikilink para commit, arquivo ou log de sessão>]].

   Acompanhamentos: [[<ids de subtarefas se houver>]] ou "nenhum."

   Aprendizados: <opcional, [[wikilink]] para entrada de diário se você escreveu uma>.
   ```

5. **Acrescentar linha final de atualização:**
   ```
   - 2026-05-10 17:42 (seu-nome) — concluída: <resumo em uma linha>
   ```

6. **Se você aprendeu algo durável, escreva uma entrada de diário.** Veja [[SOP-escrever-entrada-diario]]. Faça referência a ela na seção `## Resultado`, e adicione o nome base da entrada a `vinculado_entradas_diario:` no frontmatter desta tarefa.

7. **Acrescentar o fechamento ao log de sessão vinculado.** Se `vinculado_logs_sessao` incluir a sessão atual, nenhuma etapa extra. Se você fechou em uma sessão diferente, adicione o nome base desta sessão ao array.

8. **Reconstruir o índice.**

## §B — Cancelar uma tarefa

### Quando acionar

Requisitos mudaram. Duplicata de outra tarefa. Bloqueador permanente. A Gê decidiu diferente.

### Passos

1. **Determinar o caminho de arquivamento.**
   ```bash
   ANO=$(date -u +%Y)
   MES=$(date -u +%m)
   DEST="Wiki equipe/tarefas/canceladas/${ANO}/${MES}"
   mkdir -p "$DEST"
   ```

2. **Mover o arquivo.** A origem pode ser `abertas/` ou `em-andamento/`:
   ```bash
   git mv "Wiki equipe/tarefas/<origem>/<id>-<slug>.md" "$DEST/<id>-<slug>.md"
   ```

3. **Atualizar frontmatter:** `status: cancelada`, atualizar `atualizado`. Limpar `motivo_bloqueio` e `bloqueado_por`.

4. **Escrever `## Resultado` explicando o cancelamento.**
   ```markdown
   ## Resultado (cancelada)

   Motivo: <por que cancelamos>.

   Substituída por: [[<outro-id-de-tarefa>]] (se aplicável, caso contrário "n/a").
   ```

5. **Acrescentar atualização final:**
   ```
   - 2026-05-10 16:00 (seu-nome) — cancelada: <motivo em uma linha>
   ```

6. **Reconstruir o índice.**

## Erros comuns

- Fechar sem escrever `## Resultado`. O arqueólogo do futuro não aprende nada com este arquivo.
- Fechar um pai enquanto filhos ainda estão abertos sem reconhecê-los.
- Marcar como concluída quando o bloqueador foi resolvido mas os critérios de sucesso não foram realmente verificados.
- Cancelar sem motivo. "Cancelada" sem `## Resultado` é indistinguível de perda de dados.
- Esquecer de adicionar o nome base de uma entrada de diário a `vinculado_entradas_diario` quando você escreveu uma.
