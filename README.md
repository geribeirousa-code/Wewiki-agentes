<!-- WeWiki — © 2026 We Love Business -->

# WeWiki

**Um sistema de Assistência ao Conhecimento Pessoal com IA. Markdown puro. Qualquer LLM. Seu para sempre.**

![Version](https://img.shields.io/badge/version-2.1.0-blue)

WeWiki é uma pasta. Você a coloca na sua máquina, aponta seu LLM para ela, e tem uma equipe de IA de seis pessoas que organiza sua vida do começo ao fim. **Funciona sozinho.** Sem banco de dados para configurar, sem SaaS para fazer login, sem fornecedor para guardar seus dados.

## Começar agora

1. Clone ou baixe o repositório em uma pasta que você vai usar de verdade.
2. Abra a pasta na sua ferramenta de LLM (Claude Code, Codex CLI, Gemini CLI, Cursor ou Obsidian + plugin de chat).
3. Cole o conteúdo de `PROMPT-ATIVADOR.md` como sua primeira mensagem.
4. O LLM lê o `PROMPT-ATIVADOR.md`, escreve um arquivo de ponteiro específico da ferramenta (`CLAUDE.md`, `GEMINI.md` etc.) e reporta que o time está online.
5. Pergunte "Quem é você?" e você vai ver o Larry à sua disposição.
6. Pergunte "O que está em aberto?" e o Larry vai percorrer a pasta `Wiki equipe/tarefas/abertas/` para você.

Essa é a configuração completa. Não há etapa de instalação.

## O que você recebe

Um sistema de conhecimento funcionando, totalmente montado, que faz isso desde o primeiro dia:

- **Organiza sua vida a partir de um diário diário.** Você escreve o que aconteceu. O time arquiva as pessoas, projetos, decisões e ideias nos lugares certos. As conexões entre notas são feitas para você.
- **Lembra do trabalho inacabado por você.** Quando algo não termina em uma sessão, o time escreve como tarefa em `Wiki equipe/tarefas/`. Na próxima sessão, o Larry percorre `tarefas/abertas/` e mostra o que está esperando.
- **Carrega o aprendizado para frente.** Cada especialista mantém um diário de insights duráveis em `Equipe/<Nome>/journal/`. Quando uma tarefa referencia uma das entradas, o especialista relê seu próprio pensamento passado antes de começar o trabalho.
- **Roda em qualquer LLM que você já usa.** Claude Code, Codex CLI, Gemini CLI, Cursor, ChatGPT, Obsidian com plugin de chat. O mesmo WeWiki, o mesmo time, os mesmos arquivos. Você muda de modelo. Seu conhecimento não se move.
- **Fica em markdown puro.** Cada nota é um arquivo `.md`. Você pode ler sem IA. Pode fazer grep. Pode sincronizar com Dropbox ou git. Pode abrir no Obsidian e continuar trabalhando sem IA nenhuma.
- **Atualiza para SQLite quando você supera arquivos simples.** Cole o prompt em `Wiki equipe/SOPs/SOP-002-converter-para-sqlite.md` no seu LLM quando sua WeWiki ficar grande. Markdown continua sendo a fonte de verdade. SQLite vira uma camada de busca rápida por cima.
- **Importa de qualquer ferramenta de PKM.** Solte suas notas existentes (backup do Heptabase, export do Notion, vault do Obsidian, grafo do Roam, pasta do Logseq, export do Apple Notes, dump do Evernote) em qualquer lugar do disco, depois pergunte algo como *"importe meu export do Notion de `~/Downloads/notion.zip`"*. O WeWiki vem com [[Wiki equipe/Fluxos de Trabalho/FT-002-importar-base-de-conhecimento]] — o LLM segue o fluxo para extrair entidades, normalizar wikilinks e colocar arquivos nas pastas certas.

Não há lock-in. O sistema inteiro é texto no seu disco. Funciona no Obsidian hoje. Atualiza para SQLite quando você quiser.

## Para quem é isso

- **Trabalhadores do conhecimento** que querem uma pasta local em vez de entregar seu conhecimento para o Notion, Tana etc. e querem uma equipe de IA que realmente arquiva as coisas.
- **Fundadoras e operadores** gerenciando vários projetos que precisam de um sistema de conhecimento que pensa através de Pessoas, Tópicos, Metas, Hábitos e Pilares sem cruzamentos manuais.
- **Pais e generalistas** com entradas demais (coisas da escola, saúde, ideias, contatos) e sem estrutura para segurar tudo.
- **Entusiastas de IA** que querem uma arquitetura de referência real para um setup multi-agente.

Se você já abriu um vault vazio do Obsidian e não sabia onde colocar nada, isso é para você. (Sim — WeWiki é totalmente compatível com Obsidian. Abra a pasta como vault do Obsidian e tudo funciona.)

## Conheça o time

Seis especialistas vêm pré-carregados. **Você só fala com o Larry.** Larry roteia.

<table>
<tr>
<td width="140" align="center"><img src="github/team/larry.png" width="120" alt="Larry o Líder da Equipe e Orquestrador" /></td>
<td><b>Larry - Líder da Equipe e Orquestrador</b><br/><i>Orelhas afiadas, instintos ainda mais afiados.</i><br/><br/>Todo pedido que você faz chega primeiro ao Larry. Ele esclarece, escolhe o especialista certo, passa o brief e sintetiza a resposta para você. Ele também é o <b>Bibliotecário</b> do time (mantém a wiki limpa, corrige <code>[[wikilinks]]</code> quebrados, impõe a Regra de Ouro da SSOT), <b>Autor de Log de Sessão</b> (escreve um log diário do que o time fez e o que mudou) e o <b>Fiscalizador de Tarefas</b> do time (mostra o que está aberto no início da sessão). Larry nunca executa trabalho de especialista — essa é a regra de ferro.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/nolan.png" width="120" alt="Nolan - Aquisição de Talentos" /></td>
<td><b>Nolan - Aquisição de Talentos</b><br/><i>Leal, metódico, alérgico a contratações preguiçosas.</i><br/><br/>Quando você supera os seis especialistas que vieram, Nolan cuida da contratação de ponta a ponta: faz brief para o Pax pesquisar, rascunha o contrato do novo especialista (<code>AGENTS.md</code>), valida contra o SOP e pede sua aprovação antes de adicionar alguém ao time. Nolan é o motivo pelo qual seu time escala sem se diluir.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/pax.png" width="120" alt="Pax - Pesquisa Profunda" /></td>
<td><b>Pax - Pesquisa Profunda</b><br/><i>Paciente, com fontes citadas, alérgico a respostas de fonte única.</i><br/><br/>Quando algo importa — uma contratação, uma leitura de mercado, um "isso é verdade mesmo?" — Pax vai fundo antes de ir fundo. Retorna um brief triangulado em <code>Entregas/</code>, nunca uma opinião de uma tacada.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/penn.png" width="120" alt="Penn - Escritor de Diário" /></td>
<td><b>Penn - Escritor de Diário</b><br/><i>Quieto, observador, arquivador cuidadoso.</i><br/><br/>Penn cuida das funções de escrita do time. Solte screenshots, gravações de voz, cartões de visita ou pensamentos em rascunho em <code>Caixa de Entrada/</code>. Penn arquiva tudo no canto certo de <code>Wiki pessoal/</code> com os <code>[[wikilinks]]</code> certos.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/mack.png" width="120" alt="Mack - Especialista de Automações" /></td>
<td><b>Mack - Especialista de Automações e Integrações</b><br/><i>A camada de conexão. Quieto quando funciona, barulhento quando quebra.</i><br/><br/>Mack conecta sua WeWiki ao resto do mundo. Configuração de servidores MCP, integrações de API, receptores de webhook, fluxos OAuth e qualquer automação que precisa rodar de forma confiável em segundo plano. Quando uma importação de conhecimento externo precisa de uma busca autenticada primeiro, Mack estabelece a conexão, coloca os bytes em um caminho e passa para o Silas rodar a importação. Idempotência, tentativas, logs estruturados, credenciais em <code>.env</code> — nunca no código.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/silas.png" width="120" alt="Silas - Arquiteto de Dados" /></td>
<td><b>Silas - Arquiteto de Dados</b><br/><i>Schema é destino. Slugs são chaves primárias.</i><br/><br/>Silas guarda a integridade estrutural da sua base de conhecimento. Ele roda importações de conhecimento externo, audita frontmatter contra <code>DI-002</code>, detecta desvios de schema antes que se espalhem, e roda a conversão de markdown para SQLite (<code>SOP-002</code>) quando sua WeWiki supera arquivos simples. Markdown continua sendo a fonte de verdade; o espelho SQLite é uma camada de performance regenerável. Silas nunca inventa campos, nunca reescreve conteúdo silenciosamente.</td>
</tr>
</table>

Cada especialista tem um contrato em `Equipe/<Nome> - <Papel>/AGENTS.md` e uma pasta `journal/` para insights duráveis. Tabela de roteamento completa em `Equipe/agent-index.md`.

## O que fica onde

- `Wiki pessoal/` é o seu conhecimento. `Minha Vida/` tem os cinco conceitos de vida (Metas, Hábitos, Tópicos, Projetos, Pilares). `Documentos/`, `CRM/`, `Imagens/` e `Diário/` ficam ao lado. As notas se conectam através de `[[wikilinks]]`, não pastas aninhadas.
- `Equipe/` guarda seus especialistas. Uma pasta por agente. Cada um tem seu próprio `AGENTS.md` e sua própria pasta `journal/` para insights duráveis entre sessões.
- `Wiki equipe/` guarda o manual do time. SOPs são procedimentos atômicos. Fluxos de Trabalho orquestram fluxos multi-agente. Diretrizes são referências estáticas. `tarefas/` guarda trabalho inacabado que o time está rastreando entre sessões (`abertas/`, `em-andamento/`, `concluidas/<AAAA>/<MM>/`, `canceladas/<AAAA>/<MM>/`).
- `Entregas/` é onde o time coloca trabalho em andamento e artefatos prontos — briefs de pesquisa, análises de contratação, projetos multi-arquivo. Com timestamp, efêmero, a superfície de trabalho do time.
- `Caixa de Entrada/` é sua zona de descarte para entradas brutas. Solte screenshots, gravações de voz, cartões de visita, links ou um braindump rápido e o time arquiva em Wiki pessoal.
- `AGENTS.md` na raiz é a fonte de verdade de como o time inteiro se comporta.

## Como uma tarefa flui

Você pede ao time para fazer algo que não vai terminar em uma sessão. Larry (ou quem pegou o pedido) escreve um pequeno arquivo markdown em `Wiki equipe/tarefas/abertas/`. O frontmatter nomeia para quem é, por que importa e qual contexto já existe: qual SOP se aplica, qual fluxo de trabalho pertence, qual log de sessão o criou, qual entrada de vida ele toca, qual entrada do diário o responsável deve reler primeiro. O corpo reafirma o trabalho nas suas palavras.

Quando o responsável o pega, o arquivo se move de `abertas/` para `em-andamento/` e ele deixa uma atualização de uma linha dentro. Quando está pronto, o arquivo se move para `concluidas/<ano>/<mês>/` com o resultado escrito.

Na próxima sessão, Larry percorre `tarefas/abertas/` e `tarefas/em-andamento/` primeiro, antes de fazer qualquer outra coisa. Nada cai no chão entre sessões.

## Princípios

- **Continuidade acima de cerimônia.** O time deve conseguir continuar de onde parou, entre sessões, mesmo quando um especialista diferente assume.
- **A pasta é o banco de dados.** Markdown puro, no seu disco, legível sem IA.
- **Portabilidade é o ponto.** Você pode trocar de ferramenta de LLM sem migrar. Pode sincronizar a pasta com Dropbox, iCloud ou git.
- **Agnóstico de LLM por construção.** Qualquer coisa que o time faz, qualquer agente pode fazer com `mv`, `mkdir`, `grep`, `awk`. Nenhuma mágica específica de modelo.
- **Apenas atualizações aditivas.** Quando o WeWiki ganha uma capacidade, pastas mais antigas a ganham sem perder nada.

## Vindo de outra ferramenta?

- **Usuários do Obsidian**: abra sua pasta WeWiki como vault do Obsidian. Wikilinks, tags e Markdown funcionam como você espera.
- **Usuários do Notion**: o análogo mais próximo é "Páginas com IA dentro, mas as páginas são arquivos no seu disco." Você perde as visualizações de banco de dados do Notion. Você ganha a propriedade de cada byte.
- **Usuários do Roam/Logseq**: mesma intuição de nota diária. O time cuida da cruzamento de links que você fazia à mão.


## Aviso Legal

O WeWiki é um artefato de ensino e ponto de partida, não um sistema de produção. É fornecido como está, sem garantia de qualquer tipo. Você é responsável pelo que faz com este WeWiki. Isso inclui seus próprios backups, sua própria higiene de dados, sua escolha de LLM e ferramentas de IA.
