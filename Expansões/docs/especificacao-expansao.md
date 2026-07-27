# Especificação de Expansão WeWiki — v1.1

Este documento é o contrato público e **bloqueado** para criar uma Expansão WeWiki. Se você está escrevendo uma, é isto que você segue. Se está se perguntando o que uma Expansão tem permissão de fazer, é isto que define.

## O que é uma Expansão

Uma Expansão é uma única pasta que **amplia a equipe pré-contratada da usuária ou conecta a equipe a um sistema externo**. Coloque a pasta em `Expansões/`. O Larry a detecta na próxima inicialização da sessão, percorre o fluxo de instalação ([[FT-003-instalar-uma-expansao]]), e a equipe cresce.

Dois pontos importantes:

1. **Expansões são como a equipe cresce.** Esta é a tese para a usuária: "instale um pacote, contrate mais especialistas, continue sem bloqueios."
2. **Expansões são desinstalaváveis.** Execute a desinstalação e o WeWiki volta ao estado anterior.

## Os quatro formatos (`tipo_expansao`)

| Formato | Adiciona | Exemplos |
|---|---|---|
| `pacote_de_agentes` | Novos especialistas, seus SOPs, opcionalmente Diretrizes/Modelos | Pacote Designer (Des + Aul + Pub) |
| `conector` | OAuth/API/webhook, variáveis de ambiente, registros de servidor MCP | Notion, Readwise, Linear |
| `runtime` | Processo em segundo plano de longa duração (`start.command` / plist launchd) | Slack Expansion |
| `hibrido` | Combina dois dos acima. Raro. Permitido apenas quando dividir em duas Expansões produziria pior experiência. | Pacote de agente que também inclui um listener de runtime |

## `expansion.yaml` — esquema v1 (BLOQUEADO)

Toda pasta de Expansão DEVE conter um `expansion.yaml` em sua raiz.

### Campos obrigatórios (todos os tipos de expansão)

| Campo | Tipo | Notas |
|---|---|---|
| `nome` | string | Nome legível por humanos. |
| `slug` | string | kebab-case. DEVE corresponder ao nome da pasta. |
| `versao` | semver | `MAJOR.MINOR.PATCH`. |
| `descricao` | string | Uma frase. Vai para `Expansões/INDEX.md`. |
| `categoria` | string | Etiqueta de texto livre (ex: `agentes`, `conector`, `produtividade`). |
| `tipo_expansao` | enum | `pacote_de_agentes` | `conector` | `runtime` | `hibrido` |
| `requer_versao_WeWiki` | semver range | ex: `">=1.7.0 <2.0.0"`. |
| `requer_agentes` | lista | Agentes pré-contratados que esta Expansão usa. O Larry bloqueia a instalação se algum estiver faltando. |
| `licenca` | string | Identificador SPDX ou string curta. |
| `autor` | string | Quem publicou esta Expansão. |

### Campos condicionais / opcionais

| Campo | Quando | Formato |
|---|---|---|
| `adiciona_agentes` | `pacote_de_agentes` ou `hibrido` | Lista de `{ nome, papel, pasta }`. |
| `adiciona_sops` | opcional, qualquer tipo | Lista de `{ dono_padrao, arquivo }`. O fluxo de instalação numera automaticamente. |
| `adiciona_diretrizes` | raro | Lista de `{ slug, arquivo }`. |
| `adiciona_fluxos` | raro | Lista de `{ slug, arquivo }`. |
| `adiciona_modelos` | opcional | Lista de caminhos relativos para copiar em `Wiki equipe/Modelos/`. |
| `adds_skills` | opcional, qualquer tipo | Lista de `{ dir }` — diretórios de skill (cada um com seu `SKILL.md`) instalados no destino de skills do host, `~/.claude/skills/<nome>/`. Adicionado em v1.1. |
| `adds_docs` | opcional, qualquer tipo | Lista de `{ file }` — docs auxiliares persistentes copiados para `Wiki equipe/docs-expansoes/<slug>/`. O instalador reescreve as referências relativas para o destino final, de modo que sobrevivam ao arquivamento da pasta da Expansão (ver [[FT-003-instalar-uma-expansao]] §7). Adicionado em v1.1. |
| `variaveis_ambiente` | `conector`, `runtime`, `hibrido` | Lista de `{ chave, descricao, obrigatorio, sensivel }`. |
| `passos_pos_instalacao` | opcional | Lista legível por humanos. |
| `validacao_pos_instalacao` | opcional | Verificável por máquina. |
| `servidores_mcp` | opcional, qualquer tipo | Lista de configurações de servidor MCP. |

## Estrutura canônica de pasta de Expansão

```
Expansões/
  <slug>/
    expansion.yaml          # manifesto (obrigatório)
    README.md               # descrição legível por humanos (obrigatório)
    LICENSE                 # licença (opcional, definida pelo autor da Expansão)
    agents/
      <Pasta do Agente>/
        AGENTS.md
    sops/
      SOP-<slug>.md
    diretrizes/
      DI-<slug>.md
    modelos/
      <tipo>.md
    scripts/
      install.sh
      uninstall.sh
      start.command          # se runtime/hibrido
    .env.example             # se variaveis_ambiente
```

## Regras que toda Expansão deve seguir

1. **Sem escrita de estado silenciosa fora de `residual_paths`.** Qualquer arquivo que a Expansão escreve fora da sua pasta própria (dentro de `Equipe/`, `Wiki equipe/`, etc.) deve ser declarado no manifesto.
2. **Credenciais apenas em `.env`.** Nunca commits de tokens reais no manifesto ou em qualquer arquivo rastreado por git. `.env.example` lista apenas as chaves.
3. **Sem lançamento automático.** Runtimes anunciam; a usuária inicia. Regra rígida.
4. **Manifesto honesto.** O que o `expansion.yaml` declara é o que a Expansão faz. A revisão de segurança do Vex busca divergências.
5. **Sem números SOP embutidos.** O fluxo de instalação atribui `SOP-NNN` automaticamente para evitar colisões entre Expansões.

## Histórico de versões do esquema

- **v1.1** — Adicionados os campos opcionais `adds_skills` e `adds_docs` (ver tabela de campos condicionais/opcionais). Aditivo e retrocompatível: Expansões v1 sem esses campos continuam válidas e instalam exatamente como antes. Skills vão para `~/.claude/skills/<nome>/` (destino de descoberta de skills do host); docs auxiliares vão para `Wiki equipe/docs-expansoes/<slug>/` (destino persistente), com referências relativas reescritas pelo instalador.
- **v1** — Esquema inicial bloqueado.
