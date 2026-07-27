# SOP — Assumir uma Tarefa (com subprocedimentos Bloquear / Desbloquear)

- **Dono:** o agente que vai trabalhar na tarefa
- **Acionado por:** um agente começando trabalho em uma tarefa aberta, encontrando um bloqueio durante o trabalho, ou registrando que um bloqueio foi resolvido
- **Saída:** arquivo de tarefa movido de `abertas/` para `em-andamento/` (assumir), ou frontmatter atualizado no lugar (bloquear/desbloquear)
- **Referências:** [[SOP-reconstruir-indice-tarefas]], [[SOP-fechar-tarefa]], [[SOP-ler-proprio-diario]]

## Propósito

Assumir uma tarefa é registrar "eu peguei isso." O ato de assumir é mover o arquivo de `abertas/` para `em-andamento/`. Isso é atômico — ou a movimentação é bem-sucedida (você é o dono) ou falha (alguém chegou primeiro).

Bloquear e desbloquear não são mudanças de estado — são edições de frontmatter no lugar. Uma tarefa bloqueada permanece em `em-andamento/` para que a varredura da fila normal do responsável ainda a encontre.

## Três subprocedimentos

- **§A Assumir:** `abertas/` → `em-andamento/`
- **§B Bloquear:** edição no lugar, define `motivo_bloqueio` e `bloqueado_por`
- **§C Desbloquear:** edição no lugar, limpa `motivo_bloqueio` e `bloqueado_por`

## §A — Assumir uma tarefa

### Pré-voo: leia as referências cruzadas

Antes de mover o arquivo, abra-o e leia os arrays `vinculado_*`. O criador da tarefa já identificou os SOPs, Fluxos de Trabalho, Diretrizes, entradas de Minha Vida, logs de sessão e entradas de diário relevantes. Leia pelo menos:

- A primeira entrada em `vinculado_sops` se houver (o procedimento que governa este trabalho).
- Todas as `vinculado_entradas_diario` (seu aprendizado anterior que se aplica).
- O `vinculado_logs_sessao` mais recente (onde isso surgiu e por quê).

Este é o movimento de retomada. Pule e você começa do zero.

### Passos

1. **Verificar se o arquivo ainda está em `abertas/`.**
   ```bash
   ls "Wiki equipe/tarefas/abertas/<id>-*.md"
   ```
   Se não estiver, alguém já assumiu. Execute novamente [[SOP-listar-tarefas-abertas]].

2. **Mover o arquivo.**
   ```bash
   git mv "Wiki equipe/tarefas/abertas/<id>-<slug>.md" "Wiki equipe/tarefas/em-andamento/<id>-<slug>.md"
   ```
   Use `git mv`, não `mv`. Preserva o histórico.

3. **Atualizar frontmatter:** definir `status: em-andamento`, atualizar `atualizado` para agora (RFC3339 UTC).

4. **Acrescentar em `## Atualizações`:**
   ```
   - 2026-05-10 09:15 (seu-nome) — assumido, investigando
   ```

5. **Se você leu entradas de diário durante o pré-voo, note na linha de atualização:**
   ```
   - 2026-05-10 09:15 (mack) — assumido; carregados registros de [[2026-05-09-exemplo-de-entrada]]
   ```

6. **Reconstruir o índice.** Execute [[SOP-reconstruir-indice-tarefas]].

## §B — Registrar um bloqueio

### Quando acionar

Você está trabalhando em uma tarefa em `em-andamento/` e encontrou algo que não consegue resolver agora (aguardando uma pessoa, uma credencial, um serviço externo, outra tarefa).

### Passos

1. **O arquivo permanece em `em-andamento/`.** Não o mova.

2. **Editar frontmatter:**
   ```yaml
   motivo_bloqueio: "Aguardando rotação da variável de ambiente pela Gê — desbloquear quando a chave for definida no ambiente de produção"
   bloqueado_por: null         # ou um nome base de tarefa se o bloqueador for uma tarefa
   atualizado: 2026-05-10T11:42:00Z
   ```

   `motivo_bloqueio` deve ser uma única frase com uma condição de desbloqueio concreta. "Bloqueado, vou revisitar" é um sinal de alerta — ou o desbloqueio é concreto, ou a tarefa deve ser cancelada.

3. **Se o bloqueador for uma tarefa** (trabalho aberto de outra pessoa), crie essa tarefa via [[SOP-criar-tarefa]] e faça referência a ela em `bloqueado_por`:
   ```yaml
   bloqueado_por: tsk-2026-05-10-002-rotacionar-variavel-prod
   ```

4. **Acrescentar em `## Atualizações`:**
   ```
   - 2026-05-10 11:42 (mack) — bloqueado: aguardando rotação da variável; condição de desbloqueio: chave definida no ambiente de produção
   ```

5. **Reconstruir o índice.** O destaque "BLOQUEADO" do rebuild vai aparecer na seção em-andamento.

## §C — Registrar um desbloqueio

### Quando acionar

O bloqueador foi resolvido. Você está retomando a tarefa.

### Passos

1. **Editar frontmatter:**
   ```yaml
   motivo_bloqueio: null
   bloqueado_por: null
   atualizado: 2026-05-10T14:20:00Z
   ```

2. **Acrescentar em `## Atualizações`:**
   ```
   - 2026-05-10 14:20 (mack) — desbloqueado: rotação da variável confirmada em produção; retomando
   ```

3. **Reconstruir o índice.**

## Erros comuns

- Usar `mv` em vez de `git mv`. Perde a atribuição de histórico.
- Pular o pré-voo e não ler as referências cruzadas. O ponto de `vinculado_*` é ser lido no momento de assumir.
- Editar `status:` no frontmatter sem mover o arquivo. Agora pasta e frontmatter discordam.
- Definir `motivo_bloqueio` sem uma condição de desbloqueio concreta. Se o desbloqueio não for concreto, cancele a tarefa.
- Mover uma tarefa bloqueada para uma pasta `bloqueadas/` separada. Não existe pasta `bloqueadas/`. Bloqueio é uma edição de frontmatter; o arquivo permanece em `em-andamento/`.
- Pular a reconstrução do índice porque "é só uma transição." Deriva do índice se acumula.
