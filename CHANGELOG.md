# Changelog

Todas as mudanças relevantes no WeWiki são registradas aqui. As versões seguem semver: MAIOR para mudanças estruturais incompatíveis, MENOR para adições, PATCH para correções.

## [2.1.2] - 2026-05-20

**Repositório movido para a organização We Love Business para propriedade corporativa; continua público e gratuito.** A camada SaaS em we-love-business.com continua sendo o produto pago. Sem alterações de código ou conteúdo em relação à 2.1.0 — esta versão existe apenas para publicar o artefato sob propriedade corporativa. (AUTO-175)

### Arquivos de versão

- `VERSION` → `2.1.2`
- `.wewiki-version` → `2.1.2`

## [2.1.0] - 2026-05-19

**Slash commands passam a ser gerados pelo ativador.** O comando `/close-session` não é mais pré-configurado no WeWiki como arquivo exclusivo do Claude. O ativador agora o gera na configuração inicial a partir do protocolo de encerramento de sessão em `AGENTS.md`, de modo que o WeWiki é agnóstico de host. Adição sem quebra de compatibilidade — usuários do Claude Code têm o comando regenerado de forma idempotente na próxima ativação. (COU-272)

### Adicionado

- **PROMPT-ATIVADOR §7-bis "Vincular slash commands nativos do host."** Nova etapa idempotente de configuração: se o host suporta slash commands nativos (Claude Code → `.claude/commands/close-session.md`), o ativador gera `close-session.md` a partir do protocolo em `AGENTS.md`. Hosts sem slash commands (Codex CLI, Gemini CLI, Cursor, somente chat) pulam a geração. Pula se já existe — nunca sobrescreve um arquivo de comando personalizado pelo usuário.
- **Campo `SLASH COMMANDS BOUND:` no relatório do PROMPT-ATIVADOR** — o ativador agora reporta se o comando de encerramento de sessão foi escrito, pulado (já existe) ou não aplicável ao host.

### Removido

- **`.claude/commands/close-session.md` não é mais rastreado no repositório.** Era um arquivo pré-configurado exclusivo do Claude Code; agora é gerado pelo ativador via §7-bis. Removê-lo do WeWiki torna o repositório agnóstico de host.

### Alterado

- `AGENTS.md` (raiz) — a linha de gatilho de encerramento de sessão ganha as frases `fechar esta sessão`, `encerrar`, `registrar esta sessão`. A linha de opcionalidade do slash command é ajustada: `/close-session` é explicitamente uma conveniência exclusiva do Claude Code gerada na configuração (PROMPT-ATIVADOR §7-bis), não obrigatória e não incluída no WeWiki; os gatilhos em linguagem natural são o caminho universal.
- `validation-script.sh` — verificação de `.wewiki-version` ampliada da linha `2.0.x` para a linha completa `2.x`.

### Arquivos de versão

- `VERSION` → `2.1.0`
- `.wewiki-version` → `2.1.0`

## [2.0.0] - 2026-05-18

**Mudança estrutural incompatível.** O time base passa de **nove especialistas para seis**. Os três especialistas criativos — Iris (Arquiteta de Sistema de Design), Charta (Designer de Infográficos), Pixel (Especialista Visual) — e tudo o que gerenciam saem do WeWiki base e entram no opcional **Pack de Designer** da Biblioteca de IA. A base agora inclui Larry, Nolan, Pax, Penn, Mack e Silas. Um usuário atualizando da 1.10.x para a 2.0.0 perde os três agentes criativos do time base — instale o Pack de Designer para mantê-los. (COU-261)

### Removido

- **Três especialistas criativos.** `Equipe/Iris - Arquiteta de Design/`, `Equipe/Charta - Designer de Infográficos/`, `Equipe/Pixel - Especialista Visual/` — pastas de agentes, contratos e templates de `diario/` por agente.
- **Três arquivos de boot de subagente Claude.** `.claude/agents/iris.md`, `.claude/agents/charta.md`, `.claude/agents/pixel.md`.
- **Quatro SOPs de design.** `SOP-007-construir-infografico`, `SOP-008-gerar-imagem-estilizada`, `SOP-009-criar-sistema-design`, `SOP-010-auditar-conformidade-design`. Os slots SOP-007–SOP-010 estão agora vagos e reservados; por regra de não-renumeração, a lacuna é intencional. Uma nova instalação do Pack de Designer usa os slots livres mais baixos a partir de SOP-003.
- **`DI-003-sistema-design`.** A Diretriz de sistema de design (a SSOT de identidade visual) vai para o Pack de Designer. Não faz mais parte do conjunto base de Diretrizes.
- **Três imagens de retratos do time.** `github/team/iris.png`, `github/team/charta.png`, `github/team/pixel.png`.

### Alterado

- `Equipe/agent-index.md` — tabela de roteamento reduzida para seis linhas; referências a "nove especialistas" → "seis especialistas".
- `Equipe/Larry - Orquestrador/AGENTS.md` — tabela de roteamento rápido perde as quatro linhas de design; seção "O que Larry não faz" perde as linhas de design/DI-003.
- `AGENTS.md` (raiz) — "O time (9 especialistas)" → "O time (6 especialistas)"; tabela do time reduzida para seis linhas.
- `LEIA-ME.md` — referências a "nove"/"9" no time → "seis"/"6" (×5 incluindo badge de versão); três blocos de cartão do time criativo removidos; nota sobre o Pack de Designer adicionada.
- `WAY-FORWARD.md` — linhas do time e seção "Quando… especialistas não é suficiente" atualizadas para seis.
- `Wiki equipe/SOPs/INDEX.md` — quatro linhas de SOP de design removidas; linha Reservado ampliada para "SOP-003 em diante".
- `Wiki equipe/Diretrizes/INDEX.md` — linha `DI-003` removida; substituída por nota Reservado apontando para o Pack de Designer.
- `validation-script.sh` — verificação de versão estrutural movida da linha `1.10.x` para `2.0.x`.

### Migração

Atualizar da 1.10.x para a 2.0.0 é **incompatível** — o time base encolhe em três. Se você faz trabalho de marca ou visual, instale o **Pack de Designer** (Iris, Charta, Pixel + os quatro SOPs de design + `DI-003-sistema-design`) da Biblioteca de IA; ele restaura a capacidade criativa completa como um pack opcional. Usuários que fazem apenas PKM, journaling, pesquisa, automação ou banco de dados não precisam de nenhuma ação — o base de seis especialistas os atende. Logs de sessão existentes que referenciam os agentes removidos ou SOP-007–010 são mantidos intactos como registro histórico.

### Arquivos de versão

- `VERSION` → `2.0.0`
- `.wewiki-version` → `2.0.0`

## [1.10.2] - 2026-05-15

Restaura o conteúdo de exemplo semeado que o curso WeAgency percorre. As versões v1.10.x entregaram as pastas `Wiki pessoal/Minha Vida/`, `Wiki pessoal/CRM/`, `Wiki pessoal/Documentos/`, `Wiki pessoal/Diário/` e `Wiki pessoal/Imagens/` vazias (marcadores `.gitkeep`), mas o currículo do curso referencia arquivos concretos dentro delas pelo nome — `sessao-construcao-matinal.md`, `lancar-mvp-ate-q3.md`, entre outros. Alunos que acompanhavam o curso não encontravam os arquivos e achavam que o download estava quebrado. Esta versão fecha essa lacuna. Sem alterações de estrutura de pasta, schema ou SOP — apenas conteúdo, portanto a validação v1.10.x não é afetada.

### Adicionado

- **Exemplos de conceito em `Wiki pessoal/Minha Vida/`** — um arquivo semeado por subseção: `Tópicos/ferramentas-ia.md`, `Hábitos/sessao-construcao-matinal.md`, `Metas/lancar-mvp-ate-q3.md`, `Projetos/mvp-projeto-paralelo.md`, `Pilares/saude.md`. Cada um segue a forma que seu conceito adota e é interligado com os outros via `[[wikilinks]]`.
- **`INDEX.md` por subpasta** para cada uma das cinco subseções de `Minha Vida` (`Tópicos/`, `Hábitos/`, `Metas/`, `Projetos/`, `Pilares/`). O curso (lição "Hábitos — Os Ritmos que o Time Apoia") os referencia diretamente.
- **Exemplos de `Wiki pessoal/CRM/`** — `Pessoas/dra-ana.md` e `Organizações/clinica-dra-ana.md`, o par de demonstração de SSOT que o curso percorre.
- **`Wiki pessoal/Documentos/passaporte.md`** — exemplo de rascunho de documento semeado.
- **`Wiki pessoal/Diário/2026/05/2026-05-04-primeiro-dia.md`** — entrada de diário semeada, a referenciada na demonstração da Dra. Ana.
- **`Wiki pessoal/Imagens/2026/05/`** — duas imagens de exemplo semeadas, incorporadas pelo CRM e pelos exemplos de Diário.
- **Banner de exemplo do curso** — cada arquivo semeado abre com um callout Obsidian `[!example]` marcando-o como exemplo trabalhado para adaptar ou substituir.

### Alterado

- `Wiki pessoal/Minha Vida/INDEX.md`, `Wiki pessoal/Minha Vida/README.md` — texto de marcador "entregue vazio" substituído pela listagem real dos exemplos semeados.
- `Wiki pessoal/Documentos/INDEX.md`, `Wiki pessoal/CRM/INDEX.md`, `Wiki pessoal/Diário/INDEX.md`, `Wiki pessoal/Imagens/INDEX.md` — seções "Arquivos ativos" agora listam os exemplos semeados.

### Registro de confiança

- `Expansões/.trusted-sources` — `slack@1.0.3` fixado. A v1.0.3 do Slack Expansion é uma versão apenas de empacotamento/documentação; `runtime/index.js` é byte-idêntico à v1.0.2, então a auditoria VERDE se mantém. (AUTO-26)
- Marcadores `.gitkeep` removidos das pastas que agora têm conteúdo semeado.

### Arquivos de versão

- `VERSION` → `1.10.2`
- `.wewiki-version` → `1.10.2`

## [1.10.1] - 2026-05-10

Conecta o sistema de tarefas e os SOPs de diário da v1.10.0 aos contratos de agentes. A v1.10.0 entregou a estrutura de pastas, modelos, script de validação e 8 SOPs — mas os arquivos `AGENTS.md` não foram atualizados, o que significava que o boot e a leitura do diário só aconteciam se o LLM descobrisse os SOPs por conta própria. A v1.10.1 fecha essa lacuna. Sem novos SOPs, sem novas pastas, sem novos comportamentos — apenas a fiação no nível do contrato do que a v1.10.0 já entregou.

### Alterado

- `Equipe/Larry - Orquestrador/AGENTS.md` — adiciona `## Boot de sessão — varredura de tarefas primeiro` antes de `## Três deveres`. Larry agora varre `Wiki equipe/tarefas/abertas/` + `tarefas/em-andamento/` via [[SOP-listar-tarefas-abertas]] a cada boot de sessão e apresenta os itens abertos de prioridade 1 / em andamento / bloqueados / obsoletos na saudação.
- `Equipe/Larry - Orquestrador/AGENTS.md` — Dever 1 etapa 4 (Briefar) agora exige que Larry crie uma tarefa via [[SOP-criar-tarefa]] antes de delegar qualquer trabalho que não termine dentro do turno.
- Todos os 8 AGENTS.md de especialistas (Nolan, Pax, Penn, Mack, Silas) — adiciona uma seção compartilhada `## Disciplina de tarefas (v1.10.1)`.
- `validation-script.sh` — verificação de versão flexibilizada de um literal `1.10.0` para um glob `1.10.x`.

### Migração

Nenhuma. A v1.10.1 é apenas contrato — sem alterações de estrutura de pasta, schemas ou SOPs.

### Arquivos de versão

- `VERSION` → `1.10.1`
- `.wewiki-version` → `1.10.1`

## [1.10.0] - 2026-05-10

Adiciona gerenciamento de tarefas, diários por agente e um changelog de migração legível por LLM. Aditivo — sem mudanças incompatíveis em relação à v1.9.x. As pastas v1.9.x ganham novos diretórios e modelos; nada existente é movido, renomeado ou modificado.

### Adicionado

- `Wiki equipe/tarefas/` — gerenciamento de tarefas em markdown para trabalho inacabado que o time carrega entre sessões. A pasta codifica o status (`abertas/`, `em-andamento/`, `concluidas/<AAAA>/<MM>/`, `canceladas/<AAAA>/<MM>/`). Um arquivo `.md` por tarefa. O frontmatter contém seis arrays de referência cruzada obrigatórios (`vinculado_sops`, `vinculado_fluxos`, `vinculado_diretrizes`, `vinculado_minha_vida`, `vinculado_logs_sessao`, `vinculado_entradas_diario`) para que qualquer agente ou humano que reabra a tarefa esteja a um wikilink do contexto completo de trabalho.
- `Wiki equipe/tarefas/_modelo.md` — arquivo inicial para novas tarefas.
- `Wiki equipe/tarefas/INDEX.md` — visão resumida autogerada.
- `Wiki equipe/tarefas/{abertas,em-andamento,concluidas,canceladas}/.gitkeep` — marcadores para pastas vazias sobreviverem no git.
- Esquema de ID de tarefa: `tsk-AAAA-MM-DD-NNN`.
- `Equipe/<Nome> - <Cargo>/diario/` — notas de insight duradouras por agente.
- `Equipe/<Nome> - <Cargo>/diario/_modelo.md` — arquivo inicial para entradas de diário.
- `.wewiki-version` — arquivo de texto simples na raiz contendo `1.10.0`.
- `CHANGELOG-MIGRATION.md` — especificação de atualização acionável por máquina.
- `validation-script.sh` — script bash na raiz que verifica conformidade estrutural v1.10.0.
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

- `VERSION` incrementado de `1.9.0` para `1.10.0`.
- Expansões direcionadas à v1.10.0+ devem declarar `wewiki_compat: ">=1.10.0 <2.0.0"`.

### Notas

- Continuidade é o princípio desta versão. O time deve conseguir retomar de onde parou entre sessões, mesmo quando um especialista diferente assume. Tarefas e diários servem a isso.
- Localização da pasta, frontmatter e corpo são redundantes de propósito. Um agente lendo qualquer um dos três consegue reconstruir o suficiente para agir.
- Não há pasta `bloqueadas/`. Tarefas bloqueadas ficam em `em-andamento/` com `motivo_bloqueio:` e `bloqueado_por:` no frontmatter.
- Os wikilinks usam apenas basenames, nunca caminhos. Arquivos podem mover-se entre pastas sem quebrar links.
- Um espelho SQLite para tarefas está esboçado mas deliberadamente não entregue na v1.10.0. O markdown continua canônico.
- Compatível com versões anteriores: Expansões e SOPs v1.9.x continuam funcionando sem alteração.

## [1.9.0] - 2026-05-09

**Vinculação de subagente de host entregue por padrão.** A primeira ativação agora gera shims de subagente específicos de host para que os deputies (Penn, Pax, Nolan, Mack, Silas) possam despachar em paralelo via runtime de agentes do host — não simulado em contexto único. Larry é excluído (ele é a identidade da sessão principal, não um subagente despachado).

O contrato: **duas camadas, nunca três.** O contrato wiki em `Equipe/<Nome>/AGENTS.md` é canônico e agnóstico de host. O shim de host (`.claude/agents/<slug>.md` para Claude Code) é um ponteiro fino que o runtime do host lê para despachar o especialista.

### Adicionado

- `.claude/agents/{mack,nolan,pax,penn,silas}.md` — shims de subagente Claude Code para os deputies. Larry é intencionalmente excluído.
- **PROMPT-ATIVADOR Etapa 7 (nova)** — procedimento agnóstico de host para percorrer `Equipe/`, derivar cada slug e gerar shims específicos de host na primeira inicialização.

### Alterado

- `Equipe/Nolan - RH/AGENTS.md` — cada contratação agora entrega dois artefatos: o contrato wiki E o(s) shim(s) de host.
- `Wiki equipe/SOPs/SOP-001-como-adicionar-novo-especialista.md` §5 — princípio agnóstico de host + matriz de caminho de shim por host.
- `VERSION` 1.8.2 → 1.9.0.

## [1.8.2] - 2026-05-09

**Personalização + limpeza de representante de usuário.** As menções a representantes de usuário no WeWiki são substituídas por tokens de marcador `{{NOME_USUARIO}}`. O `PROMPT-ATIVADOR.md` agora captura o primeiro nome do usuário na primeira ativação e substitui o marcador em todo o WeWiki. Créditos de autoria formais mantidos com nome completo.

### Alterado

- `Equipe/Larry - Orquestrador/AGENTS.md` — referências de exemplo ao representante de usuário substituídas por `{{NOME_USUARIO}}`.
- `Wiki equipe/logs-de-sessao/_modelo.md` — itens de exemplo substituídos por `{{NOME_USUARIO}}`.
- `Wiki equipe/Fluxos de Trabalho/FT-003-instalar-uma-expansao.md` — referência ao representante substituída por texto genérico.
- `PROMPT-ATIVADOR.md` — nova etapa 4: detectar marcadores `{{NOME_USUARIO}}`, pedir nome ao usuário, substituir no WeWiki, salvar em `Wiki pessoal/.user.yaml`.
- `AGENTS.md` — nova seção "Personalização" codifica a regra de substituição.
- `VERSION` 1.8.1 → 1.8.2.

## [1.8.1] - 2026-05-09

**Primeira versão pública.** A WeWiki vem com um time de IA pré-contratado de 6 pessoas (Larry, Nolan, Pax, Penn, Mack, Silas), estrutura completa de pastas de Arquitetura de Conhecimento Pessoal (`Wiki pessoal/Minha Vida`, `Wiki pessoal/CRM`, `Wiki pessoal/Documentos`, `Wiki pessoal/Diário`, `Wiki pessoal/Imagens`), camada `Wiki equipe` (SOPs, Fluxos de Trabalho, Diretrizes, Modelos, logs-de-sessao) e a arquitetura de Expansões para packs de agentes e conectores baixáveis.

### Destaques

- **Markdown puro.** Toda nota é um arquivo `.md`. Funciona no Claude Code, Codex CLI, Gemini CLI, Cursor, ChatGPT, Obsidian + plugin de chat, ou qualquer LLM que leia `AGENTS.md`.
- **Gatilhos de log de sessão (agnósticos de LLM).** Frases em linguagem natural como `fechar sessão`, `guarde isso`, `vamos realinhar` roteiam a auto-memória do time em qualquer LLM — não exclusivo do Claude.
- **Importação de conhecimento externo.** [[FT-002-importar-base-de-conhecimento]] deixa o time importar de Heptabase, Notion, Obsidian, Roam, Logseq, Mem, Capacities, Apple Notes, Evernote, Tana via MCP, ou qualquer ferramenta PKM com SQLite.
- **Arquitetura de Expansões.** Packs do dia 1 disponíveis via Biblioteca de IA em [we-love-business.com](https://we-love-business.com). [[FT-003-instalar-uma-expansao]] codifica o fluxo de instalação multi-agente.
- **Disciplina de frontmatter.** `DI-002` define schemas de campo para todos os oito tipos de entidade (Pessoa, Organização, Projeto, Meta, Hábito, Tópico, Pilar, Documento); `Wiki equipe/Modelos/` entrega os modelos correspondentes.
- **Caminho de upgrade para SQLite.** [[SOP-002-converter-para-sqlite]] gera um espelho SQLite derivado quando a camada markdown superar arquivos simples. Markdown continua sendo a fonte de verdade.
