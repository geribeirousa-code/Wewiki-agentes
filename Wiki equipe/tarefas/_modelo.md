---
# Identidade
id: tsk-AAAA-MM-DD-NNN
titulo: "Substitua pelo título da tarefa"

# Propriedade e prioridade
atribuido_a: nao-atribuido
prioridade: 3

# Status (espelha a localização da pasta)
status: aberta
motivo_bloqueio: null
bloqueado_por: null

# Tempo
criado: AAAA-MM-DDTHH:MM:SSZ
atualizado: AAAA-MM-DDTHH:MM:SSZ
prazo: null

# Proveniência
criado_por: nao-atribuido
fonte: manual
pai: null

# Referências cruzadas — OBRIGATÓRIAS, mesmo que array vazio. O ato de preenchê-las é o ponto central.
vinculado_sops: []
vinculado_fluxos: []
vinculado_diretrizes: []
vinculado_minha_vida: []
vinculado_logs_sessao: []
vinculado_entradas_diario: []

# Etiquetas
tags: []
---

# Substitua pelo título da tarefa

## O que é isto
Um parágrafo: qual é o trabalho, qual é o resultado visível pela usuária, passos para reproduzir se for um bug. Seja concisa — quem retomar isto precisa poder ler esta seção e saber o que está pegando.

## Contexto a um clique
- Procedimento: [[<nome-do-sop>]]
- Fluxo de Trabalho: [[<nome-do-fluxo>]]
- Diretriz: [[<nome-da-diretriz>]]
- Contexto pessoal: [[<nome-de-entrada-minha-vida>]]
- Originado em: [[<nome-do-log-de-sessao>]]
- Aprendizado anterior: [[<nome-da-entrada-de-diario>]]

(Delete os pontos que não se aplicam. Mantenha o que importa para a retomada. Os arrays `linked_*` do frontmatter precisam estar em sincronia com estes.)

## Critérios de sucesso
- Um resultado específico e observável
- Outro resultado específico

## Atualizações
- AAAA-MM-DD HH:MM (nome-do-criador) — criado

## Resultado
_(preenchido quando o status muda para concluída — veja SOP-fechar-tarefa)_
