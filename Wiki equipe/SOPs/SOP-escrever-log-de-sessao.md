# SOP — Escrever um Log de Sessão

- **Dono:** Larry (padrão), qualquer agente especialista (quando operando de forma independente)
- **Acionado por:** fim de uma sessão de trabalho, ponto de verificação intermediário, fim do dia
- **Saída:** um novo arquivo em `Wiki equipe/logs-de-sessao/<AAAA>/<MM>/`
- **Referências:** [[SOP-escrever-entrada-diario]] (para aprendizados entre sessões), [[SOP-criar-tarefa]] (para trabalho de acompanhamento enfileirado)

## Propósito

Os logs de sessão são a superfície de retomada cronológica da equipe. Quando a sessão de amanhã precisa saber o que a sessão de ontem fez e decidiu, o log de sessão é onde isso vive. São o tecido conjuntivo entre as tarefas (que apontam para logs de sessão via `vinculado_logs_sessao`) e as entradas de diário (que frequentemente têm referência de volta à sessão que as originou).

## O que um log de sessão É

Um registro cronológico de uma sessão de trabalho. Append-only por design (escrito uma vez no encerramento da sessão). Voz em primeira pessoa do agente que conduziu a sessão. Captura: o que aconteceu, o que foi entregue, o que travou, o que está enfileirado para depois.

## O que um log de sessão NÃO É

- Uma entrada de diário (temática, durável; fica em `Equipe/<Nome> - <Papel>/diario/`).
- Uma tarefa (trabalho a fazer; fica em `Wiki equipe/tarefas/`).
- Uma transcrição palavra por palavra. O log de sessão é curado — o que importou, não cada passo.

## Quando escrever

- **Fim de toda sessão coordenada pelo Larry.** O Larry escreve um como Autor de Log de Sessão (um dos seus três deveres).
- **Fim de uma sessão independente de especialista.** Quando um especialista executa uma tarefa longa sem o Larry no loop, ele escreve seu próprio log de sessão.
- **Ponto de verificação intermediário** se a sessão atravessa uma fronteira importante.

## Convenção de nome de arquivo

```
Wiki equipe/logs-de-sessao/<AAAA>/<MM>/AAAA-MM-DD-HH-MM_<agente>_<slug-curto>.md
```

- `AAAA-MM-DD-HH-MM` é o timestamp de FIM da sessão (UTC), não o início.
- `<agente>` é o nome do agente em minúsculas: `larry`, `mack`, `silas`.
- `<slug-curto>` é kebab-case, ~30-60 caracteres, captura o título da sessão.

Se a pasta do ano ou mês não existir, o agente a cria (Regra Rígida 5 no AGENTS.md raiz).

## Frontmatter

```yaml
---
id_agente: <slug-do-agente>
id_sessao: <identificador estável da sessão — data+agente+tópico>
timestamp: <RFC3339 UTC, fim da sessão>
tipo: encerramento-sessao
vinculado_sops: []
vinculado_fluxos: []
vinculado_diretrizes: []
vinculado_tarefas: []
vinculado_entradas_diario: []
---
```

Notas de campos:

- `id_sessao` é legível por humanos e estável entre pontos de verificação intermediários. Ex: `2026-05-09-mack-webhook-firefighting` cobre múltiplas entregas mesmo que sejam logs de sessão separados.
- `tipo` padrão é `encerramento-sessao`. Outros valores: `ponto-verificacao-intermediario`, `recuo`.
- `vinculado_tarefas` lista tarefas que esta sessão criou, assumiu, bloqueou, desbloqueou ou fechou.
- `vinculado_entradas_diario` lista entradas de diário originadas nesta sessão.

## Estrutura do corpo (seções recomendadas, não obrigatórias)

```markdown
# {Título da sessão — o que foi entregue ou o que mudou}

## Contexto
{Por que esta sessão aconteceu. No máximo dois parágrafos.}

## O que entreguei
{Artefatos concretos, versões, commits, decisões. Lista de pontos ou prosa curta.}

## Tarefas tocadas
{Wikilinks para tarefas criadas, assumidas, bloqueadas, desbloqueadas ou fechadas nesta sessão.}

## Causa raiz / decisões que valem registrar
{Se houve um problema difícil, qual foi a causa real? Se uma decisão foi tomada, por que esta opção vs as alternativas?}

## O que NÃO toquei
{Espaço negativo — importante para o próximo agente no fio.}

## O que está enfileirado para depois
{Específico. Como wikilinks para tarefas existentes ([[tsk-...]]) ou pontos de trabalho futuro concretos.}

## Notas de voz para o próximo agente neste fio
{Tom, armadilhas, "se você ver X, não faça Y." Ouro de voz pessoal.}
```

## Referências cruzadas (a fiação bidirecional)

Os logs de sessão participam da rede de referências cruzadas:

- **Do log para as tarefas:** toda tarefa tocada nesta sessão vai em `vinculado_tarefas` do frontmatter e recebe um wikilink no corpo. Simétrico: essas tarefas listam esta sessão em seus `vinculado_logs_sessao`.
- **Do log para entradas de diário:** toda entrada de diário originada nesta sessão vai em `vinculado_entradas_diario` e recebe uma linha `Diário: [[nomebase]]` no final do corpo.
- **Da tarefa para o log:** o array `vinculado_logs_sessao` da tarefa carrega o nome base desta sessão.

A fiação é simétrica para que um leitor percorrendo qualquer direção (tarefa → sessão, sessão → tarefa) chegue ao outro lado em um clique.

## Voz e estilo

- Primeira pessoa. A voz do agente. Seja específico.
- Sem travessões (regra anti-escrita-IA do DI-001).
- Sem rodeios. Se você não tiver certeza, diga "incerto porque X." Se estiver confiante, diga.
- Concreto > abstrato. Hashes de commit, números de versão, medições de tempo.
- A seção "notas de voz para o próximo agente" é onde a personalidade vive.

## Erros comuns

- Escrever um log de sessão em vez de uma entrada de diário para um aprendizado durável. O aprendizado fica soterrado na cronologia; extraia-o.
- Pular `## O que NÃO toquei`. O próximo agente assume que você pode ter tocado em tudo.
- "O que está enfileirado para depois" vago sem wikilinks. O você-do-futuro não sabe o que esses pontos significavam.
- Escrever na voz passiva ("o webhook foi corrigido"). Primeira pessoa ativa. "Rotacionei o segredo."
- Travessões. Use vírgulas ou frases. A equipe tem uma convenção sem travessões.
- Esquecer de preencher `vinculado_tarefas` no frontmatter. Os wikilinks no corpo não são suficientes — a análise legível por máquina precisa do array.
