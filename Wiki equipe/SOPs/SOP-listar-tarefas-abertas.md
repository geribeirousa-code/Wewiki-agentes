# SOP — Listar Tarefas Abertas

- **Dono:** qualquer agente (Larry executa no início de cada sessão)
- **Acionado por:** início de sessão, verificação de status, "onde paramos?"
- **Saída:** resumo imprimível das tarefas abertas e em andamento (com tarefas bloqueadas destacadas)
- **Referências:** [[SOP-reconstruir-indice-tarefas]]

## Propósito

Este é o SOP de retomada em escala. No início da sessão, precisamos responder: "O que está inacabado, quem é o dono, o que está bloqueado e o que acabou de ser entregue?" Sem essa resposta, cada nova sessão começa do zero.

## Duas maneiras de fazer isso

- **§A Rápida:** leia `Wiki equipe/tarefas/INDEX.md`. O índice é reconstruído automaticamente por cada SOP que toca tarefas, então quase sempre está atualizado.
- **§B Autoritativa:** percorra as pastas diretamente com grep. Use quando não confiar no índice ou quando precisar de um filtro que o índice não renderiza.

Padrão: §A. Recorra a §B quando necessário.

## §A — Ler o índice

```bash
cat "Wiki equipe/tarefas/INDEX.md"
```

Seções: Resumo, Abertas (por prioridade), Em andamento (com destaque de bloqueadas), Por responsável, Recentemente fechadas.

Se o timestamp `_Última reconstrução:_` do índice for mais antigo que o arquivo mais recente em `tarefas/`, execute [[SOP-reconstruir-indice-tarefas]] primeiro.

```bash
INDEX_MTIME=$(stat -f %m "Wiki equipe/tarefas/INDEX.md" 2>/dev/null || stat -c %Y "Wiki equipe/tarefas/INDEX.md")
MAIS_RECENTE=$(find "Wiki equipe/tarefas" -name "tsk-*.md" -type f -exec stat -f %m {} \; 2>/dev/null | sort -n | tail -1)
[ "$MAIS_RECENTE" -gt "$INDEX_MTIME" ] && echo "desatualizado, reconstrua primeiro"
```

## §B — Percorrer as pastas diretamente

### Listar todas as tarefas abertas (qualquer responsável)

```bash
for f in "Wiki equipe/tarefas/abertas"/tsk-*.md; do
  [ -f "$f" ] || continue
  awk '/^---$/{c++; next} c==1 && /^(id|title|assignee|priority): /' "$f"
  echo "---"
done
```

### Listar minhas tarefas abertas e em andamento (tudo com que sou responsável)

```bash
EU=mack
grep -rlE "^assignee: ${EU}\b" \
  "Wiki equipe/tarefas/abertas" \
  "Wiki equipe/tarefas/em-andamento"
```

### Listar tarefas bloqueadas (somente em-andamento — é onde ficam)

```bash
grep -rlE "^motivo_bloqueio: [^n]" "Wiki equipe/tarefas/em-andamento"
```

### Listar urgentes (prioridade 1) que ainda não foram concluídas

```bash
grep -rlE "^priority: 1\b" \
  "Wiki equipe/tarefas/abertas" \
  "Wiki equipe/tarefas/em-andamento"
```

### Rotina de início de sessão do Larry

No início de cada sessão, o Larry executa:

1. `cat "Wiki equipe/tarefas/INDEX.md"` — entender o panorama.
2. Filtrar mentalmente para "Abertas prioridade 1" e "Em andamento com responsável provavelmente ativo" — apresentar essas à Gê primeiro.
3. Verificar os destaques de "BLOQUEADO" — algum deles agora pode ser desbloqueado dado o contexto de hoje?
4. Se alguma tarefa aberta estiver parada há mais de 7 dias, ou alguma em andamento estiver bloqueada há mais de 3 dias sem movimento, apresentar para triagem.

A saída que a Gê vê no início é um resumo de um parágrafo:

> Bom dia. Abertas: uma urgente para o Mack (webhook 401). Em andamento: Silas com a tarefa de rotação de segredo bloqueada por acesso Vercel (3º dia — quer acionar?). Fechadas ontem: 4 tarefas. Sem acompanhamentos perdidos.

Esta é a superfície de retomada. A Gê sabe por onde começar sem precisar reler mais nada.

## Erros comuns

- Confiar no índice quando algo acabou de mudar na mesma sessão. Execute novamente [[SOP-reconstruir-indice-tarefas]] se você esteve editando.
- Fazer grep por responsável sem delimitador `\b` — corresponde a `mackenzie` se o responsável for `mack`. Use `^assignee: mack\b` ou `^assignee: mack$`.
- Esquecer que tarefas bloqueadas ficam em `em-andamento/`, não em uma pasta separada. Procure por `motivo_bloqueio: ` diferente de `null`.
- Não apresentar tarefas paradas há muito tempo ou bloqueadas há muito tempo. O alerta de triagem no início da sessão é o que mantém a fila viva.
