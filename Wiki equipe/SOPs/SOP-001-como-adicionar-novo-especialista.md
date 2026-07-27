# SOP-001 - Como Adicionar um Novo Especialista

- **Dono padrão:** Nolan
- **Reutilizável por qualquer agente.** Esta é uma habilidade, não uma propriedade 1:1. SOPs são procedimentos que qualquer agente pode invocar quando precisar.
- **Co-dono para a etapa de pesquisa:** Pax
- **Acionado por:** pedido do usuário para contratar, ou Larry detectando uma lacuna
- **Referências:** [[DI-001-convencoes-de-nomeacao]], [[Equipe/agent-index]]

## Time pré-contratado

**Larry, Nolan, Pax, Penn, Mack e Silas vêm pré-contratados com o WeWiki.** SOP-001 governa a contratação de todos além desses seis. Não rode SOP-001 para "criar" nenhum dos seis — eles já existem. SOP-001 é para a sétima contratação em diante.

## Propósito

Adicionar um novo especialista ao time de forma que mantém a tabela de roteamento limpa, os contratos AGENTS.md consistentes e a Regra de Ouro da SSOT intacta.

## Passos

### 1. Capturar a necessidade (Larry → Nolan)

Larry roteia o pedido de contratação para o Nolan com um brief de uma frase: o que o novo especialista vai fazer que nenhum especialista atual consegue. Se o Nolan não conseguir terminar essa frase com o usuário, o papel não está pronto.

### 2. Fazer brief do Pax para a etapa de pesquisa (Nolan → Pax)

Nolan escreve um brief de pesquisa para o Pax. Perguntas obrigatórias:

- O que a melhor versão do mundo deste especialista realmente faz, no dia a dia?
- Quais são as competências centrais e os antipadrões (coisas que versões medíocres deste papel fazem que o time deve evitar explicitamente)?
- Quais entregáveis este papel produz? Como é o output de classe mundial vs output adequado?
- Quais limites este papel deve manter? Que pedidos devem ser recusados ou devolvidos?
- Candidatos a nome sugeridos (curto, distinto, uma palavra).

Pax retorna um brief proporcional ao papel — geralmente 400 a 800 palavras. O brief vai em `Entregas/AAAA-MM-DD-<slug-papel>-pesquisa-contratacao.md`.

### 3. Escolher nome e papel (Nolan)

Usando o brief do Pax, escolha:

- **Nome:** curto, distinto, uma palavra. Dos candidatos do Pax ou uma variante. Evite colisões com nomes existentes.
- **Papel:** uma frase curta. Exemplo: "Desenvolvedor Frontend" ou "Especialista em Email Marketing."
- **Pasta:** `Equipe/<Nome> - <Papel>/` (espaço, hífen, espaço). Corresponde ao padrão dos seis especialistas pré-contratados.

### 4. Redigir o AGENTS.md (Nolan)

Crie `Equipe/<Nome> - <Papel>/AGENTS.md`. Traduza o brief de pesquisa do Pax em um contrato com estas seções:

- **Identidade** — nome, papel, a quem reporta, princípio operacional.
- **Quando Larry roteia para eles** — padrões de sugestão.
- **Método ou protocolo** — como trabalham, em passos.
- **Estrutura de entregável** — como é o output.
- **Onde escrevem** — caminhos e nomenclatura. Referencie [[DI-001-convencoes-de-nomeacao]].
- **Referências cruzadas** — Diretrizes e Fluxos de Trabalho que tocam.
- **Limites de escopo** — o que não fazem.

Mantenha curto. Os seis pré-contratados são o template. Não cole o brief de pesquisa do Pax no AGENTS.md.

### 5. Redigir o(s) shim(s) de subagente do host (Nolan)

**Obrigatório para toda contratação, em todo host que o usuário ativou.** Sem o shim, Larry só pode fazer role-play do novo especialista dentro do contexto principal.

Para Claude Code: `.claude/agents/<slug>.md` com frontmatter YAML `name`, `description` e `tools`.

**Regra de idempotência:** verifique se o shim já existe. Se sim, pule — nunca sobrescreva.

### 6. Atualizar o agent-index (Nolan)

Adicione uma linha a `Equipe/agent-index.md` com: especialista, papel, pasta, condição de roteamento.

### 7. Obter aprovação do usuário (Nolan)

Apresente ao usuário:
- Nome e papel do novo especialista
- Princípio operacional de uma frase
- Qualquer lacuna de escopo que precisará de outra contratação

Aguarde aprovação explícita. Não faça commit da contratação antes.

### 8. Fazer commit da contratação (Nolan)

1. Mover o rascunho para `Equipe/<Nome> - <Papel>/AGENTS.md` (provavelmente já no lugar).
2. Registrar a contratação no log de sessão atual.
3. Reportar ao Larry: "Contratação de [Nome] concluída. Adicionado ao agent-index."
