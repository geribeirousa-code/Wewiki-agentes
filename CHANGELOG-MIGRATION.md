# CHANGELOG-MIGRATION

Este arquivo é **acionável por máquina**. Um LLM lendo apenas este arquivo deve conseguir migrar qualquer pasta de WeWiki mais antiga para a versão mais recente de forma determinística. Cada seção é estruturada para esse propósito.

As seções por versão aparecem da mais recente para a mais antiga. Para migrar, encontre a versão mais alta mais nova que a registrada em `<raiz>/.wewiki-version` e aplique cada receita de versão em ordem da mais antiga para a mais nova.

Se `.wewiki-version` estiver ausente, assuma v1.x e aplique todas as receitas a partir de v1.10.0 em diante.

## Por que este arquivo é estruturado desta forma

O princípio da WeWiki é que a pasta é o banco de dados. Isso implica que a especificação de migração também vive na pasta, em markdown simples, legível por qualquer LLM. A receita usa **etapas numeradas e nomeadas** para que um LLM executando a receita possa anunciar "Etapa 3/9: criando pastas de tarefas/" e o usuário possa auditar. O script de validação prova que a migração foi bem-sucedida estruturalmente.

Esta é a disciplina WeWiki: nada que o usuário precise aceitar por fé, tudo inspecionável.

---

## v1.10.0 (2026-05-10)

### Resumo

Adiciona gerenciamento de tarefas interno do time e diários tópicos por agente. **Puramente aditivo — nenhum arquivo existente é movido, renomeado ou modificado.** As pastas v1.x ganham novos diretórios e alguns arquivos de modelo. Nenhum conteúdo é destruído.

### Adicionado

- `Wiki equipe/tarefas/` — gerenciamento de tarefas em markdown. A pasta é o status (abertas / em-andamento / concluidas / canceladas). Um `.md` por tarefa. `INDEX.md` autoreconstruído.
- `Wiki equipe/tarefas/_modelo.md` — arquivo inicial para novas tarefas. O frontmatter inclui os seis arrays de referência cruzada obrigatórios.
- `Wiki equipe/tarefas/INDEX.md` — visão resumida autogerada.
- `Wiki equipe/tarefas/{abertas,em-andamento,concluidas,canceladas}/.gitkeep` — marcadores para pastas vazias sobreviverem no git.
- `Equipe/<Nome> - <Cargo>/diario/` — notas tópicas duradouras por agente (uma pasta por especialista existente).
- `Equipe/<Nome> - <Cargo>/diario/_modelo.md` — arquivo inicial para novas entradas de diário.
- `.wewiki-version` — arquivo de texto simples na raiz contendo `1.10.0`.
- Novos SOPs em `Wiki equipe/SOPs/`:
  - `SOP-criar-tarefa.md`
  - `SOP-assumir-tarefa.md`
  - `SOP-fechar-tarefa.md`
  - `SOP-listar-tarefas-abertas.md`
  - `SOP-reconstruir-indice-tarefas.md`
  - `SOP-escrever-entrada-diario.md`
  - `SOP-ler-proprio-diario.md`
  - `SOP-escrever-log-de-sessao.md`

### Alterado

- (nenhum — nenhuma estrutura existente é modificada)

### Removido

- (nenhum)

### Mapeamento de caminhos (v1.x → v1.10.0)

| Caminho antigo | Caminho novo | Migração |
|---|---|---|
| _(nenhum — versão aditiva)_ | | |

Não há mapeamentos de caminhos. Os arquivos v1.x ficam onde estão. Wikilinks apontando para caminhos v1.x continuam resolvendo. Sem operações `git mv` em arquivos existentes.

### Receita de migração

Cada etapa é nomeada e numerada. Um LLM executando esta receita deve anunciar cada etapa antes de executá-la ("Etapa N/9: <nome>") para que o usuário possa auditar. Cada etapa é idempotente — executar a receita duas vezes produz o mesmo resultado que executar uma vez.

#### Etapa 1/9 — Detectar versão atual do WeWiki

Leia `<raiz>/.wewiki-version`.
- Se o arquivo existe e contém `1.10.0` ou superior, esta receita já foi aplicada. Pare.
- Se o arquivo está ausente ou contém uma versão abaixo de `1.10.0`, continue.

#### Etapa 2/9 — Verificar se a pasta é um WeWiki WeWiki

Verifique se `<raiz>/Equipe/` e `<raiz>/Wiki equipe/` existem. Se algum estiver ausente, esta não é uma pasta WeWiki — aborte e apresente a situação ao usuário.

#### Etapa 3/9 — Verificar conflitos antes da sobreposição

Se `<raiz>/Wiki equipe/tarefas/` já existe com arquivos, isso é trabalho existente do usuário. Pare e pergunte ao usuário como proceder antes de sobrescrever qualquer modelo.

O mesmo vale para qualquer pasta `<raiz>/Equipe/*/diario/` que já tenha arquivos.

Se ambas estiverem ausentes ou vazias, prossiga sem perguntar.

#### Etapa 4/9 — Criar pastas de tarefas e arquivos de modelo

```bash
ROOT="<raiz-do-WeWiki>"
mkdir -p "$ROOT/Wiki equipe/tarefas/abertas"
mkdir -p "$ROOT/Wiki equipe/tarefas/em-andamento"
mkdir -p "$ROOT/Wiki equipe/tarefas/concluidas"
mkdir -p "$ROOT/Wiki equipe/tarefas/canceladas"

touch "$ROOT/Wiki equipe/tarefas/abertas/.gitkeep"
touch "$ROOT/Wiki equipe/tarefas/em-andamento/.gitkeep"
touch "$ROOT/Wiki equipe/tarefas/concluidas/.gitkeep"
touch "$ROOT/Wiki equipe/tarefas/canceladas/.gitkeep"
```

Não há pasta `bloqueadas/`. Tarefas bloqueadas ficam em `em-andamento/` com `motivo_bloqueio` no frontmatter. (Veja `SOP-assumir-tarefa` para a convenção completa.)

Copie estes arquivos do diretório `modelos/` da versão v1.10.0:
- `modelos/tarefas/_modelo.md` → `<raiz>/Wiki equipe/tarefas/_modelo.md`
- `modelos/tarefas/INDEX.md` → `<raiz>/Wiki equipe/tarefas/INDEX.md`
- `modelos/tarefas/abertas/EXEMPLO-tsk-2026-05-10-001-bem-vindo-as-tarefas.md` → `<raiz>/Wiki equipe/tarefas/abertas/tsk-<HOJE>-001-bem-vindo-as-tarefas.md` (renomeie o prefixo de data para a data de hoje)

#### Etapa 5/9 — Criar pastas de diário por agente

Para cada subdiretório de `<raiz>/Equipe/` que segue o padrão `<Nome> - <Cargo>` E contém um `AGENTS.md`:

```bash
for AGENTE in "$ROOT/Equipe/"*/; do
  [ -f "$AGENTE/AGENTS.md" ] || continue
  mkdir -p "$AGENTE/diario"
  cp "<versao>/modelos/diario/_modelo.md" "$AGENTE/diario/_modelo.md"
done
```

NÃO crie pastas de diário para `agent-index.md` ou qualquer subdiretório que não seja de agente.

#### Etapa 6/9 — Copiar os novos SOPs

```bash
cp <versao>/sops/SOP-criar-tarefa.md               "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-assumir-tarefa.md             "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-fechar-tarefa.md              "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-listar-tarefas-abertas.md     "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-reconstruir-indice-tarefas.md "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-escrever-entrada-diario.md    "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-ler-proprio-diario.md         "$ROOT/Wiki equipe/SOPs/"
cp <versao>/sops/SOP-escrever-log-de-sessao.md     "$ROOT/Wiki equipe/SOPs/"
```

Se algum desses nomes de arquivo SOP já existir no destino, NÃO sobrescreva. Apresente o conflito ao usuário.

#### Etapa 7/9 — Escrever o arquivo de versão

```bash
echo "1.10.0" > "$ROOT/.wewiki-version"
```

#### Etapa 8/9 — Acrescentar uma entrada de log de sessão registrando a migração

Caminho: `<raiz>/Wiki equipe/logs-de-sessao/<AAAA>/<MM>/<AAAA-MM-DD-HH-MM>_<ator>_migrado-para-v1.10.0.md`

Onde `<ator>` é o agente ou LLM executando a migração (ex.: `larry`, `claude`, `gpt`).

Frontmatter:
```yaml
---
id_agente: <ator>
id_sessao: <AAAA-MM-DD>-migracao-v1.10.0
timestamp: <RFC3339-UTC>
tipo: fim-de-sessao
vinculado_sops: [SOP-criar-tarefa, SOP-escrever-entrada-diario]
vinculado_fluxos: []
vinculado_diretrizes: []
vinculado_tarefas: []
vinculado_entradas_diario: []
---
```

O corpo deve descrever: qual versão foi detectada, o que foi adicionado, quaisquer conflitos encontrados.

#### Etapa 9/9 — Executar o script de validação

A versão entrega `validation-script.sh`. Execute-o contra a pasta migrada:

```bash
bash <versao>/validation-script.sh "$ROOT"
```

Código de saída 0 significa que a migração é estruturalmente válida. Diferente de zero significa que algo está faltando ou malformado — leia a saída do script e corrija.

### Etapas de validação

Após a execução da receita, todos os seguintes devem ser verdadeiros. O script de validação (`validation-script.sh`) verifica cada um.

- [ ] `<raiz>/.wewiki-version` existe e é igual a `1.10.0` (sem espaços extras).
- [ ] `<raiz>/Wiki equipe/tarefas/{abertas,em-andamento,concluidas,canceladas}/` existem como diretórios.
- [ ] `<raiz>/Wiki equipe/tarefas/INDEX.md` existe.
- [ ] `<raiz>/Wiki equipe/tarefas/_modelo.md` existe.
- [ ] Cada `<raiz>/Equipe/<Nome> - <Cargo>/AGENTS.md` tem um diretório `diario/` irmão.
- [ ] Cada diretório de diário tem um `_modelo.md`.
- [ ] Todos os oito novos SOPs existem em `<raiz>/Wiki equipe/SOPs/`.
- [ ] Nenhum arquivo chamado `tsk-*.md` existe fora de `<raiz>/Wiki equipe/tarefas/` (detectar derramamento acidental).
- [ ] Nenhum wikilink na forma `[[tarefas/<status>/...]]` existe em lugar nenhum — links devem ser apenas pelo basename.
- [ ] Cada arquivo de tarefa tem os seis arrays `linked_*` obrigatórios no frontmatter (`vinculado_sops`, `vinculado_fluxos`, `vinculado_diretrizes`, `vinculado_minha_vida`, `vinculado_logs_sessao`, `vinculado_entradas_diario`).

### Restrições (rígidas)

- **Sem movimentos destrutivos sem confirmação explícita do usuário.** Esta receita é aditiva.
- **Todos os movimentos de arquivo preservam histórico do git.** Use `git mv`, não `cp + rm`. (Não aplicável na v1.10.0 pois nada é movido.)
- **Wikilinks devem ser corrigidos no mesmo commit que o movimento que os quebrou.** (Não aplicável na v1.10.0.)
- **Modelos nunca são sobrescritos se um arquivo com o mesmo nome já existe.** Apresente o conflito; deixe o usuário decidir.

### Rollback

O git é o rollback. Antes de executar a migração, a receita instrui o usuário a fazer um commit. Se algo der errado:

```bash
cd "$ROOT"
git status                # veja o que mudou
git restore --staged .    # se algo foi para staged
git restore .             # descartar mudanças não staged
git clean -fd             # remover os novos diretórios criados pela receita
```

Os executores de receita NÃO devem executar `git restore`/`git clean` sem confirmação do usuário. Apresente esses comandos como o caminho de rollback.

### Por que a v1.10.0 é aditiva

O briefing exigiu que as pastas v1.x continuassem funcionando sem alteração. A v1.10.0 é uma adição de capacidade (tarefas, diários, rastreamento de versão, especificação de migração) sobreposta ao WeWiki existente. Qualquer coisa que exigiria mover ou renomear conteúdo existente foi adiada para uma versão maior onde a mudança incompatível é nomeada e isolada.

Isso mantém a atualização trivialmente reversível e os wikilinks existentes do usuário intactos.

---

## Notas para LLMs lendo este arquivo

- As versões estão listadas da mais recente para a mais antiga neste arquivo. Aplique as receitas em ordem cronológica (da mais antiga para a mais nova) ao migrar de abaixo da `.wewiki-version` atual.
- Cada receita é **idempotente**. Executar novamente não tem efeito negativo. Se não tiver certeza se uma receita foi concluída, execute novamente.
- Quando uma etapa diz "se X estiver ausente, aborte", abortar significa: parar a migração, não prosseguir para a próxima etapa, apresentar a situação em linguagem simples ao usuário.
- Quando uma etapa diz "não sobrescreva", isso significa: pule a operação para esse arquivo específico; continue com o resto da receita; reporte o arquivo pulado no final.
- Nunca invente etapas que não estão na receita. Se você achar que uma etapa é necessária mas não está aqui, apresente ao usuário como pergunta antes de agir.

O arquivo `.wewiki-version` é a fonte única de verdade sobre qual migração se aplica. Leia-o primeiro. Sempre.
