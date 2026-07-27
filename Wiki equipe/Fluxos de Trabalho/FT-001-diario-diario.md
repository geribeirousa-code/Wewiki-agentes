# FT-001 — Diário Diário

- **Tipo:** Fluxo de Trabalho — uma composição multi-agente. Os agentes abaixo colaboram para entregar o resultado. Novos Fluxos de Trabalho surgem quando padrões se repetem nos logs de sessão; este vem já estabelecido porque o diário diário é um fluxo do primeiro dia.
- **Donos:** Penn (captura e escrita), Larry (roteamento e passe de Bibliotecário)
- **Referências:** [[SOP-001-como-adicionar-novo-especialista]], [[DI-001-convencoes-de-nomeacao]], [[Equipe/Penn - Escritor de Diário/AGENTS]], [[Equipe/Larry - Orquestrador/AGENTS]]
- **Gatilho:** qualquer entrada da usuária que contenha um pensamento, observação, encontro, screenshot, foto ou nota de voz.

## Propósito

Transformar entradas diárias brutas em registros estruturados na Wiki pessoal. O Diário é a caixa de entrada. Pessoas, organizações e tópicos referenciados nas entradas do Diário recebem referências cruzadas no CRM e em Minha Vida.

## Entradas

- **Texto** — a usuária digita ou cola um pensamento.
- **Imagem** — a usuária envia um screenshot, foto ou cartão de visita.
- **Áudio** — a usuária compartilha uma nota de voz (transcrita pelo LLM se possível; caso contrário, armazenada e sinalizada).

## Coreografia

### Passo 1 — Larry recebe a entrada

Larry verifica a tabela de roteamento em seu AGENTS.md. Gatilhos de diário diário são roteados para o Penn.

### Passo 2 — Penn escreve a entrada do Diário

- **Caminho:** `Wiki pessoal/Diário/AAAA/MM/AAAA-MM-DD-<slug>.md`.
- **Criar pastas automaticamente:** se `AAAA/` ou `AAAA/MM/` não existir, Penn as cria.
- **Nome do arquivo:** prefixo de data ISO mais um slug kebab-case derivado do tema principal do dia. Veja [[DI-001-convencoes-de-nomeacao]].
- **Formato:** markdown simples. Uma entrada por dia. Se o dia já tiver uma entrada, Penn acrescenta uma nova seção ao arquivo existente.

### Passo 3 — Penn cuida das imagens

- **Caminho:** `Wiki pessoal/Imagens/AAAA/MM/AAAA-MM-DD-<slug>.<ext>`.
- **Criar pastas automaticamente:** mesma regra do Diário.
- **Incorporar no Diário:** Penn incorpora a imagem na entrada do Diário com `![[Imagens/AAAA/MM/AAAA-MM-DD-<slug>.<ext>]]`. A imagem fica em `Wiki pessoal/Imagens/`. A entrada do Diário a referencia. A imagem nunca é duplicada na pasta do Diário.

### Passo 4 — Penn cria referências cruzadas na Wiki pessoal

Para cada entidade mencionada na entrada, Penn roteia por tipo. Use a tabela abaixo como mapa de roteamento:

| Tipo de menção | Pasta de destino | Padrão de nome | Notas |
|---|---|---|---|
| Pessoa | `Wiki pessoal/CRM/Pessoas/` | `nome-sobrenome.md` | Cria esboço se não existir. Incorpora cartão de visita ou foto via `![[Imagens/...]]`. |
| Organização, empresa, local | `Wiki pessoal/CRM/Organizações/` | `<slug-org>.md` | Cria esboço se não existir. Referência cruzada com Pessoas que trabalham lá. |
| Área de interesse ou assunto recorrente | `Wiki pessoal/Minha Vida/Tópicos/` | `<slug-topico>.md` | Cria esboço se não existir. Tópicos são categorias estáveis de atenção, não projetos. |
| Hábito, ritmo contínuo, rotina | `Wiki pessoal/Minha Vida/Hábitos/` | `<slug-habito>.md` | Cria esboço se não existir. Hábitos têm cadência e definição de pronto. |
| Esforço concreto com prazo | `Wiki pessoal/Minha Vida/Projetos/` | `<slug-projeto>.md` | Cria esboço se não existir. Projetos têm uma linha de chegada. |
| Resultado ou aspiração com horizonte | `Wiki pessoal/Minha Vida/Metas/` | `<slug-meta>.md` | Cria esboço se não existir. Metas se vinculam ao Pilar a que pertencem. |
| Dimensão estável da vida (Saúde, Família, Carreira, etc.) | `Wiki pessoal/Minha Vida/Pilares/` | `<slug-pilar>.md` | Cria esboço se não existir. Pilares são dimensões, não metas. |
| Documento real (passaporte, contrato, certificado, identidade) | `Wiki pessoal/Documentos/` | `<slug-doc>.md` | Cria esboço se não existir. O arquivo real (se digitalizado) vai em `Wiki pessoal/Imagens/` e é incorporado. |

Para cada entidade roteada:

- Se um arquivo já existir no destino, Penn faz `[[wikilinks]]` para ele a partir da entrada do Diário. Sem repetir detalhes biográficos ou contextuais que já vivem no arquivo.
- Se nenhum arquivo existir, Penn cria um esboço no caminho correto com o conteúdo mínimo necessário para o link resolver, depois faz `[[wikilinks]]` para ele a partir da entrada do Diário.

É assim que o Diário se torna o tecido conjuntivo da sua WeWiki.

### Passo 4a — Regra de decisão: esboço vs menção inline

Crie um esboço quando a entidade tiver qualquer um dos seguintes:

- Um nome ao qual a usuária provavelmente se referirá novamente (pessoas, organizações, tópicos recorrentes).
- Uma propriedade que a usuária vai querer recuperar depois (data de expiração do passaporte, prazo do projeto, horizonte da meta).
- Relevância transversal (uma pessoa que aparece em vários contextos, um tópico que se repete).

Mencione inline apenas (sem esboço) quando:

- A referência é pontual e claramente não vai retornar (um nome passageiro, uma anedota de única vez).
- A usuária disse explicitamente "não arquive isso" ou similar.

Na dúvida, crie o esboço. Um esboço não custa nada. Uma referência ausente custa a conectividade da wiki.

### Passo 5 — Passe de Bibliotecário do Larry no encerramento da sessão

No encerramento da sessão, Larry varre a nova entrada do Diário, a nova imagem (se houver) e quaisquer novos esboços do CRM ou Minha Vida:

- Confirma que `[[wikilinks]]` resolvem.
- Confirma que imagens estão em `Wiki pessoal/Imagens/AAAA/MM/`, não duplicadas em outro lugar.
- Confirma que cada novo esboço está listado no `INDEX.md` da sua seção.
- Sinaliza violações de SSOT para a usuária.

## O que este Fluxo de Trabalho NÃO faz

- Não escreve fluxos de trabalho de negócios. Esses são tratados por especialistas futuros contratados pelo Nolan via [[SOP-001-como-adicionar-novo-especialista]].
- Não produz relatórios de pesquisa. O Pax cuida disso.
- Não edita entradas existentes do CRM da usuária. Penn acrescenta, nunca sobrescreve, a menos que a usuária peça.

## Regras de nomenclatura e imagens

Todas as dúvidas de nomenclatura se resolvem em [[DI-001-convencoes-de-nomeacao]]. Se precisar saber como nomear um slug, qual formato de data usar, ou como lidar com colisões de nome de arquivo, consulte lá. Não repita as regras de nomenclatura dentro deste Fluxo de Trabalho.
