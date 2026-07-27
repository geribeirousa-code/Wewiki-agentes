# SOPs - Índice

**SOPs são habilidades dos agentes.** Cada SOP é um procedimento canônico — uma receita passo a passo para um trabalho. São agnósticos de LLM e reutilizáveis entre agentes: um SOP tem um **dono padrão** (o especialista que o executa com mais frequência), mas qualquer agente pode invocar um SOP quando precisar do seu procedimento.

Padrão de nome de arquivo: `SOP-NNN-<título>.md`. Veja [[DI-001-convencoes-de-nomeacao]] para regras de slug.

## SOPs ativos

| SOP | Título | Dono padrão | Descrição |
|---|---|---|---|
| SOP-001 | [[SOP-001-como-adicionar-novo-especialista]] | Nolan | Procedimento passo a passo para redigir e integrar um novo especialista ao time. Referencia [[DI-001-convencoes-de-nomeacao]]. |
| SOP-002 | [[SOP-002-converter-para-sqlite]] | Silas (executado pelo usuário via prompt colado no LLM) | Gerar um espelho SQLite da sua WeWiki sob demanda. Markdown continua sendo a fonte de verdade; SQLite é uma camada de performance derivada. |
| — | [[SOP-assumir-tarefa]] | qualquer agente | Como um agente reivindica uma tarefa aberta. |
| — | [[SOP-fechar-tarefa]] | qualquer agente | Como um agente fecha uma tarefa concluída. |
| — | [[SOP-criar-tarefa]] | qualquer agente | Como criar uma nova tarefa. |
| — | [[SOP-listar-tarefas-abertas]] | Larry | Como Larry percorre tarefas abertas no boot de sessão. |
| — | [[SOP-ler-proprio-diario]] | qualquer agente | Como um agente lê suas próprias entradas de journal antes de começar o trabalho. |
| — | [[SOP-reconstruir-indice-tarefas]] | qualquer agente | Como reconstruir `tarefas/INDEX.md` quando está desatualizado. |
| — | [[SOP-escrever-entrada-diario]] | Penn | Como Penn escreve uma entrada de Diário. |
| — | [[SOP-escrever-log-de-sessao]] | Larry | Como Larry escreve um log de sessão no fechamento. |

## Como adicionar um novo SOP

1. Escolha o próximo número não usado (`SOP-NNN`) — por ordem de autoria, não por tópico.
2. Nome do arquivo: `SOP-NNN-<título-kebab-case>.md`.
3. Cabeçalho inclui o dono padrão, status, gatilhos, referências e uma nota explícita "Reutilizável por qualquer agente".
4. Referencie [[DI-001-convencoes-de-nomeacao]] e qualquer outra Diretriz em vez de duplicar seu conteúdo.
5. Adicione uma linha a este índice.
