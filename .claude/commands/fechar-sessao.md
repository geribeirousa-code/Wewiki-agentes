---
description: Fecha a sessão como Larry — varredura de Bibliotecário + log de sessão + estado atual
---

Você é o Larry. Execute o fechamento de sessão nos passos abaixo, nesta ordem.

## 0. Data e hora reais

Rode `date +%F` e `date +%H-%M` e use esses valores em nomes de arquivo e no
`timestamp`. Nunca deduza a data de memória.

## 1. Bibliotecário

Varra o trabalho desta sessão em busca de:

- Violações da Regra de Ouro da SSOT (o mesmo fato escrito em mais de um arquivo).
- `[[wikilinks]]` quebrados ou apontando para arquivos inexistentes.
- Arquivos órfãos (sem nenhum link de entrada) criados durante a sessão.
- Notas nas oito pastas de entidade cujo frontmatter não bate com `[[DI-002-convencoes-de-frontmatter]]`.

Corrija o que for mecânico. Reporte o que precisar de decisão da usuária.

## 2. Autor de Log de Sessão

Escreva o log em:

`Wiki equipe/logs-de-sessao/<AAAA>/<MM>/<AAAA-MM-DD-HH-MM>_larry_<slug-topico>.md`

Crie as pastas de ano e mês se não existirem. Siga exatamente o esquema de
`Wiki equipe/logs-de-sessao/_modelo.md`, incluindo o frontmatter e todas as seções.
Use `tipo: encerramento-sessao`.

Na seção **Decisões tomadas**, registre também o que foi **avaliado e rejeitado**
(ferramenta, skill, ideia), com o motivo em uma linha, para a próxima sessão não
reavaliar do zero. Capture em **Realinhamentos** qualquer correção da usuária,
literalmente.

Preencha as referências cruzadas: SOPs, Fluxos de Trabalho, Diretrizes, tarefas e
entradas de diário que a sessão tocou, mais um link para o log de sessão anterior
mais relacionado.

## 3. Estado atual

Abra `ESTADO-ATUAL.md` na raiz e atualize só o que mudou:

- A data de "Última atualização".
- **Onde o trabalho parou**: frente ativa, últimas entregas, o que ficou em edição.
- **Decisões vigentes**: adicione linha para cada decisão nova (inclusive rejeições) e
  corrija as que a usuária mudou. Um fato por linha; detalhes ficam no log, não aqui.
- **Preferências**: só se a usuária declarou uma nova.

Não copie o log inteiro para este arquivo. Ele deve caber em uma leitura rápida no celular.

## 4. Tarefas

Qualquer fio aberto que não vá fechar nesta sessão vira arquivo de tarefa em
`Wiki equipe/tarefas/abertas/` conforme `[[SOP-criar-tarefa]]`. Nada cai no chão
entre sessões.

Se a sessão estava sem acesso à `Wiki pessoal/` (celular ou nuvem), registre aqui o que o
Penn precisa capturar no Diário quando estiver no PC, sem dados sensíveis.

## 5. Salvar

Se a pasta for um repositório git com remoto, faça commit dos arquivos tocados na
sessão (log, tarefas, `ESTADO-ATUAL.md`) e envie. Em sessão na nuvem, o que não for
enviado se perde quando o contêiner é descartado. Em branch protegida ou `main`, use
uma branch e avise a usuária; não abra pull request sem ela pedir.

## 6. Síntese

Sintetize para a usuária como Larry, em português, curto:

- O que foi registrado e onde.
- O que a varredura de Bibliotecário encontrou.
- O que ficou aberto.
- Se salvou no GitHub: em qual branch.
