# Logs de Sessão — a memória automática da equipe

Esta pasta é a memória estruturada da equipe de IA entre sessões. É escrita
pelos agentes, não por você. Você pode lê-la. Deve ocasionalmente dar uma
olhada. Não precisa mantê-la.

## O que vive aqui

`Wiki equipe/logs-de-sessao/AAAA/MM/AAAA-MM-DD-HH-MM_<id-sessao>.md`

Um arquivo por entrada de sessão. Sessões podem escrever múltiplas entradas —
veja "Quando os agentes escrevem" abaixo. As pastas se aninham por ano e mês.
O agente cria a subpasta `AAAA/` e `MM/` se ainda não existir.

## Quando os agentes escrevem aqui

1. **No encerramento da sessão** (`/encerrar-sessao`). O Larry executa o
   protocolo de encerramento da sessão, varre as tarefas abertas, escreve uma
   entrada de `encerramento-sessao` resumindo o que chegou, o que foi adiado
   e o que mudou.
2. **No meio da sessão, quando algo durável acontece.** Os agentes podem
   proativamente acrescentar uma entrada durante uma sessão se um realinhamento
   com você produz um novo aprendizado, uma nova regra, uma nova decisão que
   vale lembrar.

Os quatro tipos de entrada:

| `tipo:` | Quando escrever |
|---|---|
| `encerramento-sessao` | Resumo de fim de sessão, escrito pelo Larry no `/encerrar-sessao`. |
| `aprendizado-intermediario` | Algo que a equipe aprendeu no meio da sessão que a próxima sessão precisa saber. |
| `realinhamento` | Você contestou um plano ou corrigiu uma leitura errada. Capture a correção literalmente. |
| `proativo` | Um agente sinalizou um problema, oportunidade ou padrão que vale a pena trazer à tona sem ser solicitado. |

## O que se forma aqui

Os logs de sessão são memória de trabalho com acréscimo contínuo. Quando algo
escrito aqui se torna **consolidado** — repetível, aplicável além do momento
— ele é promovido ao lar certo em `Wiki equipe/`:

- Um procedimento repetível → um SOP (`Wiki equipe/SOPs/SOP-NNN-<slug>.md`).
- Uma orquestração multi-agente recorrente → um Fluxo de Trabalho
  (`Wiki equipe/Fluxos de Trabalho/FT-NNN-<slug>.md`).
- Uma regra de referência estática (nomenclatura, tom, padrões) → uma Diretriz
  (`Wiki equipe/Diretrizes/DI-NNN-<slug>.md`).

O Larry cuida da promoção como Bibliotecário. A entrada do log de sessão
permanece onde está (acréscimo contínuo), e o novo SOP/Fluxo/Diretriz faz
referência de volta via `[[wikilinks]]`.

## Como usar isso como humana

Você geralmente não precisa. A equipe usa esta pasta para se lembrar. Se
você quiser saber o que a equipe tem feito, o arquivo mais recente na
subpasta `AAAA/MM/` mais profunda é a leitura certa.

## Nomenclatura e estrutura

- Nome do arquivo: `AAAA-MM-DD-HH-MM_<id-sessao>.md`. Prefixo de data ISO
  até o minuto, depois um sublinhado, depois um id de sessão curto em kebab-case
  derivado do tema principal da sessão.
- Pasta: aninhado por ano e mês — `AAAA/MM/`.
- Frontmatter: cada entrada usa o esquema de frontmatter em `_modelo.md`.

Veja `_modelo.md` nesta pasta para o esboço da entrada.
