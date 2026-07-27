# Wiki equipe - Hub Central

Este é o lado operacional da sua WeWiki. Guarda os procedimentos do time, orquestrações, material de referência e histórico de sessões. O conhecimento pessoal do usuário fica em [[Wiki pessoal/INDEX]].

## Seções

- **[[Wiki equipe/SOPs/INDEX|SOPs]]** — habilidades dos agentes. Procedimentos canônicos passo a passo, um trabalho por arquivo, agnósticos de LLM e reutilizáveis entre agentes. Cada SOP tem um dono padrão, mas qualquer agente pode invocá-lo. Nomes de arquivo: `SOP-NNN-<título>.md`.
- **[[Wiki equipe/Fluxos de Trabalho/INDEX|Fluxos de Trabalho]]** — composições multi-agente. Orquestrações recorrentes onde mais de um especialista colabora. Fluxos de Trabalho encadeiam SOPs. Apenas fluxos canônicos do primeiro dia vêm no WeWiki; novos Fluxos de Trabalho são criados quando um padrão se repete. Nomes de arquivo: `FT-NNN-<título>.md`.
- **[[Wiki equipe/Diretrizes/INDEX|Diretrizes]]** — regras gerais que todo agente lê. Restrições estáticas (nomenclatura, frontmatter, design system) para as quais SOPs e Fluxos de Trabalho apontam via `[[wikilink]]` em vez de duplicar. Nomes de arquivo: `DI-NNN-<título>.md`.
- **logs-de-sessao/** — registro append-only de toda sessão de trabalho, escrito pelo Larry. Caminho: `logs-de-sessao/AAAA/MM/AAAA-MM-DD-<slug>.md`.

## Taxonomia em linguagem simples

- Um **SOP** é uma habilidade do agente. Responde "como faço X?" em passos claros. Dono padrão roda com mais frequência; qualquer agente pode invocar.
- Um **Fluxo de Trabalho** é uma composição multi-agente. Responde "como entregamos X juntos, recorrentemente?" Só é criado quando o padrão é canônico; novos emergem de padrões repetidos nos logs de sessão.
- Uma **Diretriz** é uma regra geral. Responde "qual é a regra para X?" Referência estática que todo agente relevante lê. Nunca um procedimento.

Na dúvida: escreva uma Diretriz primeiro se a regra é estática. Escreva um SOP se o procedimento tem passos e um dono padrão. Escreva um Fluxo de Trabalho apenas quando mais de um especialista estiver envolvido E o padrão se repetir.

## SSOT se aplica aqui também

Se as regras de nomenclatura pertencem à [[DI-001-convencoes-de-nomeacao]], não as reescreva dentro de um SOP ou Fluxo de Trabalho. Aponte para a Diretriz.

## Aprendizados entre sessões

Quando o time aprende algo durável entre sessões, Larry acrescenta a uma seção "Aprendizados entre sessões" ao final deste arquivo. Notas específicas de sessão ficam no log de sessão em `logs-de-sessao/AAAA/MM/`.

### Aprendizados entre sessões

(vazio no primeiro dia — Larry preenche conforme o time opera)

## Log de sessão ativo

O log de sessão atual fica em `logs-de-sessao/AAAA/MM/`. Larry escreve um por sessão no fechamento.
