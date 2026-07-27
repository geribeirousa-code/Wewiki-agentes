# Fluxos de Trabalho - Índice

**Fluxos de Trabalho são composições multi-agente.** Um Fluxo de Trabalho descreve como mais de um especialista (frequentemente mais o usuário) colabora para entregar um resultado recorrente. Onde um SOP é uma habilidade de agente único, um Fluxo de Trabalho é a coreografia que encadeia habilidades.

Fluxos de Trabalho são **emergentes**. O WeWiki fornece apenas os fluxos canônicos que precisam funcionar no primeiro dia. Novos Fluxos de Trabalho são criados pelo time quando um padrão multi-agente se repete.

Fluxos de Trabalho referenciam SOPs e Diretrizes via `[[wikilinks]]`. Nunca duplicam os passos ou regras que esses arquivos contêm.

Padrão de nome de arquivo: `FT-NNN-<título>.md`. Veja [[DI-001-convencoes-de-nomeacao]] para regras de slug.

## Fluxos de Trabalho ativos

| FT | Título | Donos | Descrição |
|---|---|---|---|
| FT-001 | [[FT-001-diario-diario]] | Penn + Larry | Como entradas diárias (texto, imagem, áudio) fluem para Diário, Imagens e CRM. |
| FT-002 | [[FT-002-importar-base-de-conhecimento]] | Silas (executor principal) + Mack (metade de conexão quando a fonte precisa de OAuth/API/MCP) + Pax (pesquisa para formatos desconhecidos) | Como uma base de conhecimento existente (Heptabase, Notion, Obsidian, Roam, Logseq, etc.) é importada para sua WeWiki. |
| FT-003 | [[FT-003-instalar-uma-expansao]] | Larry (orquestrador) + Nolan (fusão do time) + Mack (fiação do conector) + Silas (verificação de integridade) | Como uma pasta de Expansão colocada em `Expansões/` é validada, mesclada ao time do usuário, conectada, validada e anunciada. |
| FT-004 | [[FT-004-conteudo-diario]] | Larry (orquestrador) | Como o conteúdo diário das duas marcas ([[bowl-green]], [[clean-touch-cabinets]]) é gerado, conferido visualmente e entregue à Gê como painel de aprovação. |

## Quando escrever um novo Fluxo de Trabalho

- Mais de um especialista está envolvido.
- A atividade se repete em um agendamento ou em um gatilho recorrente.
- A coreografia (quem passa para quem) importa tanto quanto os passos.

Se apenas um especialista estiver envolvido, escreva um SOP — procedimentos de agente único são habilidades, não fluxos de trabalho.
Se a regra for estática e nunca executada, escreva uma Diretriz.
