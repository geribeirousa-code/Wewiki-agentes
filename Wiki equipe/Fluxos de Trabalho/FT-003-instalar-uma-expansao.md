---
tipo: fluxo_trabalho
id: FT-003
titulo: "Instalar uma Expansão"
dono: larry
agentes_envolvidos: [larry, vex, nolan, mack, silas]
acionado_por: "qualquer frase da usuária que sinalize instalar ou desinstalar uma Expansão"
referencias: [DI-001-convencoes-de-nomeacao, DI-002-convencoes-de-frontmatter, SOP-001-como-adicionar-novo-especialista]
tags: []
---

# FT-003 — Instalar uma Expansão

- **Status:** Ativo (desde v1.7.0)
- **Tipo:** Fluxo de Trabalho — uma composição multi-agente. Vem já estabelecido porque Expansões são um fluxo de instalar/desinstalar do primeiro dia que precisa da coreografia multi-agente (Larry → Vex → Nolan → Mack → Silas → Larry) corretamente configurada desde o início.
- **Donos:** **Larry** (orquestrador, pré-voo, validação pós-instalação, arquivo, anúncio). **Vex** (revisão de segurança — portão). **Nolan** (mesclagem de equipe — copia agentes, SOPs, diretrizes, modelos para a sua WeWiki). **Mack** (conexão de conector — variáveis de ambiente, servidores MCP, anúncio de runtime). **Silas** (verificação de integridade pós-mesclagem).
- **Referências:** `Expansões/docs/especificacao-expansao.md` (esquema de manifesto), [[DI-001-convencoes-de-nomeacao]], [[DI-002-convencoes-de-frontmatter]], [[SOP-001-como-adicionar-novo-especialista]], [[Equipe/agent-index]].
- **Acionado por:** qualquer frase da usuária que sinalize "instalar ou desinstalar uma Expansão." O Larry também detecta novas pastas em `Expansões/` na inicialização da sessão e oferece executar este fluxo.

## Propósito

Pegar uma pasta colocada em `Expansões/`, validá-la, revisá-la em termos de segurança, mesclar seu conteúdo na sua WeWiki (agentes, SOPs, diretrizes, modelos), conectar quaisquer conectores ou runtimes, validar o resultado e anunciar a nova capacidade — sem deixar a sua WeWiki em estado inconsistente em caso de falha. O fluxo de desinstalação simétrico retorna a sua WeWiki ao estado anterior.

## Contrato de gatilho

| A usuária diz (ou implica) | Ação |
|---|---|
| "instalar a Expansão [X]" / "instalar Slack" | Executar este fluxo a partir do §1 |
| "derrubei o pacote [X] em Expansões/" | Detectar → confirmar → executar §1 |
| "desinstalar [X]" / "remover a Expansão [X]" | Executar **§Desinstalar** |
| (Larry detectou na inicialização — nova pasta em `Expansões/` com `expansion.yaml` válido e ainda não em `Expansões/INDEX.md`) | Anunciar + oferecer executar §1 |

## Pré-voo

Larry confirma que a pasta de Expansão existe em `Expansões/<slug>/` e contém um `expansion.yaml` em sua raiz. Se não, o Larry informa à usuária o que está faltando e para.

## Passo 1 — Larry: detectar, analisar, apresentar visualização prévia

Larry lê `Expansões/<slug>/expansion.yaml` e valida contra o esquema em `Expansões/docs/especificacao-expansao.md`:

1. Campos obrigatórios presentes? (`name`, `slug`, `version`, `description`, `category`, `expansion_type`, `requires_wewiki_version`, `requires_agents`, `license`, `author`)
2. `requires_wewiki_version` corresponde à `VERSION`?
3. `requires_agents` presentes no `Equipe/agent-index.md`?
4. Nome da pasta = `slug`?

Os campos `adds_skills` e `adds_docs` (esquema v1.1) são **opcionais**: se ausentes, a instalação prossegue como antes. Se presentes, devem ser listas bem-formadas (`adds_skills`: itens com `dir`; `adds_docs`: itens com `file`) — caso contrário Larry sinaliza e para. A maioria das Expansões não os usa.

Se todas as verificações passarem, Larry apresenta a **visualização prévia de instalação** para a usuária e pergunta: Prosseguir? [s/n/inspecionar]

## Passo 2 — Vex: revisão de segurança (o portão)

O Vex audita a pasta de Expansão antes de qualquer mesclagem. Este é um portão rígido.

Verificações do Vex:
1. **Verificação de nível de confiança.** Se `author: We Love Business` (ou We Love Business), verifica hash. Correspondência → verde. Sem correspondência → vermelho.
2. **Varredura de tratamento de token.** Grep por qualquer string com formato de token comprometido.
3. **Revisão do `.env.example`.** Confirma somente chaves de variáveis de ambiente, sem valores.
4. **Revisão da superfície de permissões.** Para tipos `connector` e `runtime`.
5. **Padrões de rede de saída.** Para Expansões tipo Slack.
6. **Revisão de scripts.** `install.sh`, `uninstall.sh`, scripts de inicialização — verificar injeção de shell.

Vex retorna: **VERDE** → §3. **AMARELO** → Larry apresenta à usuária. **VERMELHO** → instalação bloqueada.

## Passo 3 — Nolan: mesclar agentes, SOPs, diretrizes, modelos, fluxos de trabalho, skills, docs

Nolan executa a mesclagem no nível de arquivo. Confirme cada operação antes de escrever.

> **Cópia robusta (iCloud-safe).** Para toda cópia de diretório/arquivo deste passo, use `ditto <origem> <destino>` (macOS) ou `rsync -a <origem>/ <destino>/` em vez de `cp -R`. Em pastas sincronizadas pelo iCloud Drive — onde muitas WeWikis vivem — arquivos podem estar *evicted* (placeholders ainda não baixados); o `cp -R` simples copia parcial **em silêncio**. `ditto`/`rsync` materializam o conteúdo e falham alto se algo não vier. Após copiar, confirme a contagem de arquivos origem × destino antes de prosseguir.

### 3.1 Agentes
Para cada entrada `{ name, role, folder }`: verificar se `Equipe/<folder>/` não existe; copiar diretório; atualizar `Equipe/agent-index.md`; atualizar `AGENTS.md` raiz.

### 3.2 SOPs — preservar números embarcados; renumerar só em colisão
Para cada SOP da Expansão:
1. **Preservar por padrão.** Pacotes vêm com números fixos (ex.: `SOP-060`…`SOP-070`) referenciados em dezenas de wikilinks `[[SOP-NNN-...]]` cruzados entre os próprios artefatos do pacote. Se o número embarcado está **livre** na WeWiki de destino, copie preservando-o — **não renumere**. Renumerar à toa quebra as cross-references internas do pacote.
2. **Renumerar só em colisão.** Se o número embarcado já está ocupado por um SOP existente, atribua o próximo `SOP-NNN` livre **e, na mesma operação, reescreva**: (a) o campo `id:` no frontmatter do SOP copiado; (b) todos os wikilinks `[[SOP-<antigo>-...]]` → `[[SOP-<novo>-...]]` nos demais artefatos **deste pacote** (SOPs, fluxos, diretrizes, skills) que referenciam o SOP renumerado. Registre o remapeamento (antigo → novo) no `.manifest.json` para reversão.
3. Copiar para `Wiki equipe/SOPs/SOP-NNN-<slug>.md`; atualizar `Wiki equipe/SOPs/INDEX.md`.

### 3.3 Diretrizes
Mesma regra que SOPs (§3.2: preservar número embarcado; renumerar + reescrever `id`/wikilinks só em colisão), com prefixo `DI-NNN-`. Atualizar `Wiki equipe/Diretrizes/INDEX.md`.

### 3.4 Fluxos de Trabalho
Mesma regra que SOPs (§3.2), com prefixo `FT-NNN-`. Atualizar `Wiki equipe/Fluxos de Trabalho/INDEX.md`.

### 3.5 Modelos
Copiar para `Wiki equipe/Modelos/`. Atualizar `Wiki equipe/Modelos/INDEX.md`.

### 3.7 Skills (esquema v1.1 — opcional)
Pular se `adds_skills` ausente. Para cada entrada `{ dir }`:
1. Resolver o diretório de origem dentro da pasta da Expansão (`Expansões/<slug>/<dir>/`) e confirmar que contém um `SKILL.md`.
2. Destino: `~/.claude/skills/<nome>/`, onde `<nome>` é o nome base do diretório de skill. Este é o local de descoberta de skills do host — fora da árvore markdown da WeWiki, que não executa código. Uma skill copiada para dentro da WeWiki nunca seria carregada pelo Claude Code.
3. Verificar que `~/.claude/skills/<nome>/` ainda **não** existe; se existir, sinalizar colisão e parar (sem sobrescrever skills do host).
4. Copiar o diretório inteiro da skill para o destino.
5. Registrar cada skill instalada (origem → destino) no `.manifest.json` da instalação, para desinstalação reversível.

### 3.8 Docs auxiliares persistentes (esquema v1.1 — opcional)
Pular se `adds_docs` ausente. Para cada entrada `{ file }`:
1. Destino persistente: `Wiki equipe/docs-expansoes/<slug>/`. Criar a pasta se não existir. Razão: o §7 arquiva a pasta original da Expansão em `Expansões/_instaladas/`, deixando mortos os caminhos relativos `docs/...` que a skill usa em runtime. Este destino vive na árvore ativa da WeWiki e sobrevive ao arquivamento.
2. Copiar o `file` (preservando subcaminho relativo, ex. `docs/guia.md` → `Wiki equipe/docs-expansoes/<slug>/docs/guia.md`) para o destino.
3. **Reescrita de referências:** após copiar, o instalador atualiza as referências relativas a esses docs nos artefatos que as usam (skills instaladas no §3.7 e quaisquer SOPs/diretrizes/fluxos da Expansão) para apontar ao caminho final em `Wiki equipe/docs-expansoes/<slug>/`. Isso garante que as referências resolvam após o arquivamento do §7.
4. Registrar cada doc copiado (origem → destino) e cada referência reescrita no `.manifest.json`, para desinstalação reversível.

### 3.9 Reversão em caso de falha
Se qualquer passo em §3 (incluindo 3.7 e 3.8) falhar após escritas terem começado, Nolan reverte tudo para o estado pré-instalação: remove diretórios de skill copiados de `~/.claude/skills/`, remove docs copiados de `Wiki equipe/docs-expansoes/<slug>/`, e desfaz reescritas de referências, além das reversões de agentes/SOPs/diretrizes/modelos/fluxos.

## Passo 4 — Silas: verificação de integridade pós-mesclagem

Silas valida o estado da sua WeWiki após a mesclagem do Nolan:

1. Conformidade do frontmatter com [[DI-002-convencoes-de-frontmatter]].
2. Consistência do `agent-index.md`.
3. Resolução de wikilinks.
4. Consistência dos arquivos INDEX.md.
5. Sem violações de SSOT introduzidas.

Silas retorna: **PASSOU** → §5. **FALHOU** → Larry apresenta; usuária escolhe reverter ou aceitar.

## Passo 5 — Mack: conexão de conector (somente se `connector` / `runtime` / `hybrid`)

Pule este passo para Expansões puras de `pacote_de_agentes`.

### 5.1 Variáveis de ambiente
Para cada `env_vars` obrigatória: solicitar à usuária; escrever em `Expansões/<slug>/.env`; `chmod 600`.

### 5.2 Servidores MCP
Para cada `mcp_servers`: detectar a ferramenta LLM da usuária; escrever o bloco de registro; verificar se o servidor inicia.

### 5.3 Anúncio de runtime
Para `expansion_type: runtime` ou `hybrid`: **Não iniciar automaticamente.** Regra rígida. Informar à usuária como iniciar manualmente.

## Passo 6 — Larry: validação pós-instalação

Larry executa `post_install_validation` do manifesto:
- Cada `{ type: "file_exists" }` → verificar.
- Cada `{ type: "shell" }` → executar e verificar código de saída.
- Cada `{ type: "http" }` → curl e verificar status.

## Passo 7 — Larry: arquivamento + anúncio

1. Escrever entrada de log de sessão.
2. Arquivar a pasta de Expansão em `Expansões/_instaladas/<slug>-<version>/`. **Nota:** skills (§3.7) já vivem em `~/.claude/skills/` e docs persistentes (§3.8) já vivem em `Wiki equipe/docs-expansoes/<slug>/`, com referências reescritas para esses destinos — portanto o arquivamento aqui não invalida nenhuma skill ou doc instalado.
3. Atualizar `Expansões/INDEX.md`.
4. Anunciar os novos especialistas / capacidades para a usuária.
5. Percorrer `post_install_steps`.

## Desinstalar

Simétrico. Acionado por "desinstalar Expansão [X]", "remover [X]".

### D1 — Larry: confirmar + apresentar visualização prévia de desinstalação
Larry lê `Expansões/_instaladas/<slug>-<version>/.manifest.json`. Apresenta o que será removido.

### D2 — Mack: parar runtime + desmontar conector
Para Expansões de runtime: descarregar o plist; encerrar processos; cancelar registro de servidores MCP; limpar `.env`.

### D3 — Nolan: reverter a mesclagem
Remover agentes de `Equipe/`, remover linhas de `agent-index.md`, remover SOPs/Diretrizes/Fluxos/Modelos. Não renumerar SOPs existentes — a lacuna é aceitável.

Simetricamente para os artefatos do esquema v1.1, consultando o `.manifest.json`:
- **Skills:** para cada skill registrada em `adds_skills`, remover seu diretório de `~/.claude/skills/<nome>/`. Remover apenas os diretórios que esta Expansão instalou (registrados no manifesto); nunca tocar skills do host não rastreadas.
- **Docs:** remover os arquivos copiados para `Wiki equipe/docs-expansoes/<slug>/` e, se a pasta ficar vazia, removê-la. As reescritas de referência do §3.8 vão embora junto com os artefatos da Expansão que as continham (skills/SOPs/diretrizes/fluxos removidos), então não há referências órfãs.

### D4 — Silas: verificação de integridade pós-desinstalação
Verificar se arquivos removidos não deixaram wikilinks quebrados, linhas de INDEX ou linhas de `agent-index` pendentes. Para Expansões com `adds_skills`/`adds_docs`: confirmar que os diretórios de skill saíram de `~/.claude/skills/` e que `Wiki equipe/docs-expansoes/<slug>/` foi limpo, sem referências pendentes a docs removidos.

### D5 — Larry: arquivamento + log de sessão
Mover para `Expansões/_desinstaladas/`. Escrever entrada de log de sessão.
