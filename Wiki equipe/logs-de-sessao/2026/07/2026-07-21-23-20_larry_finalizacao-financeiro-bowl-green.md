---
id_agente: larry
id_sessao: 954421d6-be8d-48a4-b35f-a133350729b4
timestamp: 2026-07-21T23:20:00Z
tipo: encerramento-sessao
vinculado_sops: []
vinculado_fluxos: []
vinculado_diretrizes: []
vinculado_tarefas: []
vinculado_entradas_diario: []
---

# Finalização e Alinhamento Financeiro da Bowl Green

## Contexto

A usuária Gê solicitou o fechamento e a consolidação do assunto financeiro referente à Bowl Green, após o time ter realizado uma auditoria profunda dos extratos e proposto a nova arquitetura financeira multi-entidade e a contratação de suporte operacional.

## O que fizemos

- O **Silas** (Arquiteto de Dados) deduplicou e auditou 16 planilhas e extratos da 99Food e Brendi entre 06/01/2026 e 21/07/2026, consolidando as perdas reais e identificando onde o dinheiro vaza em [[Entregas/2026-07-21-bowl-green-auditoria-extratos]].
- O **Silas** elaborou em [[Entregas/2026-07-21-proposta-arquitetura-financeira]] a estrutura lógica de pastas e metadados para separar três entidades financeiras: Clean Touch, Bowl Green e Gê PF.
- O **Pax** (Pesquisador) estruturou em [[Entregas/2026-07-21-financeiro-multi-entidade-pesquisa-contratacao]] o perfil do papel e a pesquisa para contratação de um especialista em escrituração (bookkeeper), sugerindo o nome **Cass**.
- O time gerou os painéis interativos visuais em [[Entregas/2026-07-21-bowl-green-painel.html]] e [[Entregas/2026-07-21-painel-financeiro-visual.html]] para visualização limpa dos dados e metas de precificação.

## Decisões tomadas

- **Pergunta:** Como segregar as informações financeiras de CLEAN TOUCH, BOWL GREEN e Gê PF na WeWiki?
  **Decisão:** Utilizar a nova pasta `Empresas/` dividida em subpastas por entidade, com um plano de contas compartilhado em `Empresas/_Compartilhado/` e lançamentos divididos por competência (não caixa) em subpastas anuais/mensais, mantendo `Wiki pessoal/` livre de dados comerciais.
- **Pergunta:** Qual o papel ideal para executar a manutenção e conciliação diária dos livros financeiros?
  **Decisão:** Contratar um bookkeeper multi-entidade gerencial (Cass) focado na disciplina de entrada de dados, conciliação mensal e arquivo documental, em vez de um consultor de relatórios de topo.
- **Pergunta:** Quais são as principais ações de redução de danos na Bowl Green?
  **Decisão:** 
  1. Limitar/zerar descontos de ofertas na 99Food bancados 100% pela loja.
  2. Avaliar retorno da entrega própria (evitando o acréscimo de R$ 10,16/pedido cobrado pela plataforma).
  3. Cortar custos fixos supérfluos (ciclovia, iFood inativo, segunda linha).

## Aprendizados

- O Pix no 99Food não é mais barato que os cartões (taxa fixa de 3,21% de processamento para todos os pagamentos online pela plataforma).
- A perda da Bowl Green não é por falta de margem de contribuição (que é positiva nos dois canais), mas sim por gargalo de volume (MC total não cobre os custos fixos estruturais).
- O pró-labore de R$ 5.000 é o maior peso nos custos fixos; sem ele como despesa operacional, o breakeven cai para 363 pedidos/mês.

## Realinhamentos

- _(nenhum nesta sessão)_

## Fios abertos

- [ ] Nolan redigir o contrato e iniciar processo de contratação da **Cass** conforme aprovação da Gê.
- [ ] Gê decidir sobre a criação física da estrutura de pastas de `Empresas/` proposta pelo Silas.
- [ ] Gê validar a implementação das ações de corte de custos na operação da Bowl Green.

## Próximos passos

- Nolan redigir o modelo de contrato de Cass com as travas gerenciais e limites fiscais acordados.
- Criar a diretriz financeira em [[Wiki equipe/Diretrizes/DI-002-convencoes-de-frontmatter]] com os novos campos de empresa, lançamento e documento.

## Referências cruzadas

- _(primeiro log desta iniciativa)_
