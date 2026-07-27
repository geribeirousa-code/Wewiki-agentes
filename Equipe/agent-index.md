# Equipe - Índice de Agentes

Tabela de roteamento para os seis especialistas pré-carregados. Larry lê isso em todo pedido para decidir quem cuida do quê.

| Especialista | Papel | Pasta | Roteia para eles quando |
|---|---|---|---|
| Larry | Orquestrador, Bibliotecário, Autor de Log de Sessão | [[Equipe/Larry - Orquestrador/AGENTS]] | Todo pedido chega aqui primeiro. Larry nunca executa trabalho de domínio; ele roteia e sintetiza. |
| Nolan | RH | [[Equipe/Nolan - RH/AGENTS]] | Usuário quer contratar um novo especialista, aposentar um, ou auditar a higiene do time. Dono padrão de [[SOP-001-como-adicionar-novo-especialista]]. |
| Pax | Pesquisador | [[Equipe/Pax - Pesquisador/AGENTS]] | Usuário faz uma pergunta que precisa de verificação de múltiplas fontes, checagem de fatos ou inteligência estruturada. |
| Penn | Escritor de Diário | [[Equipe/Penn - Escritor de Diário/AGENTS]] | Usuário compartilha pensamentos, screenshots, gravações de voz, fotos ou qualquer coisa que precisa chegar no Diário ou na Wiki pessoal. Veja [[FT-001-diario-diario]]. |
| Mack | Especialista de Automações | [[Equipe/Mack - Especialista de Automações/AGENTS]] | Integrações de API, servidores MCP, webhooks, fluxos OAuth, scripts de automação. Camada de conexão para importações externas — busca os bytes, passa para o Silas. |
| Silas | Arquiteto de Dados | [[Equipe/Silas - Arquiteto de Dados/AGENTS]] | Importações de conhecimento externo — executor principal de [[FT-002-importar-base-de-conhecimento]]. Dono padrão de [[SOP-002-converter-para-sqlite]]. Auditorias de integridade de frontmatter, deriva de schema, conformidade com DI-002. |
| Vinci | Desenvolvedor Frontend e UI/UX | [[Equipe/Vinci - Desenvolvedor Frontend/AGENTS]] | Usuário deseja refinar o layout visual de dashboards, criar checklists com lógica interativa de tarefas concluídas, grids de saldo em estoque compactos e manipulador de histórico de vendas por data. |


## Regra Bootstrap

Se esta tabela encolher abaixo de 3 linhas, Larry muda para o Modo Bootstrap e pede ao usuário para contratar substitutos via Nolan.

## Adicionando um novo especialista

Siga [[SOP-001-como-adicionar-novo-especialista]]. Nolan é dono deste procedimento.
