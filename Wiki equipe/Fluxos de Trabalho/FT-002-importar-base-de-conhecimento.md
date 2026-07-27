# FT-002 — Importar Base de Conhecimento Externa

- **Status:** Ativo (desde v1.4.0)
- **Tipo:** Fluxo de Trabalho — uma composição multi-agente. Os agentes abaixo colaboram para entregar o resultado. Novos Fluxos de Trabalho surgem quando padrões se repetem nos logs de sessão; este vem já estabelecido porque o fluxo de importação precisa da metade de conexão (Mack) e da formatação de conteúdo (Silas) funcionando desde o primeiro dia.
- **Donos:** **Silas (pré-contratado)** é o executor principal — executa §2 em diante (perguntas de esclarecimento, inventário, plano, criação de entidades, normalização de wikilinks, entrada de log de sessão). **Mack (pré-contratado)** executa a camada de conexão §1 quando a fonte só é acessível via OAuth/API/MCP. **Pax** para formatos de fonte desconhecidos que precisam de pesquisa antes de elaborar o plano de importação.
- **Referências:** [[DI-001-convencoes-de-nomeacao]], [[DI-002-convencoes-de-frontmatter]], [[SOP-002-converter-para-sqlite]], [[FT-001-diario-diario]], [[Wiki equipe/Modelos/INDEX]]
- **Acionado por:** qualquer frase da usuária que sinalize "trazer minhas notas antigas de outra ferramenta para esta WeWiki."

## Propósito

Pegar a base de conhecimento existente da usuária — exportada de qualquer ferramenta de PKM, em uma pasta, um zip, uma API, um servidor MCP ou um arquivo SQLite — e colocá-la dentro desta pasta WeWiki como um conjunto de notas corretamente formatadas: pasta correta, frontmatter correto por [[DI-002-convencoes-de-frontmatter]], slug correto por [[DI-001-convencoes-de-nomeacao]], wikilinks normalizados, anexos roteados para `Wiki pessoal/Imagens/AAAA/...`, e uma entrada de log de sessão capturando o que chegou.

O Fluxo de Trabalho é **somente procedimento**. Não executa nenhuma importação por conta própria. O LLM que executa este procedimento é o executor; a usuária é a fonte de verdade sobre a intenção das entidades.

## O que este Fluxo de Trabalho NÃO faz

- Não migra o **formato WeWiki** (markdown ↔ SQLite). Isso é [[SOP-002-converter-para-sqlite]].
- Não escreve novos modelos ou novos campos de frontmatter.
- Não exclui nem modifica a fonte. A fonte é somente leitura durante todo o processo.
- Não executa escrita em massa sem supervisão. Todo plano passa pela aprovação da usuária antes de qualquer arquivo ser criado.

## Passo a passo

### Passo 1 — Detecção da fonte

O LLM percorre esta árvore de decisão com base no que a usuária fornece:

1. **A usuária colou um caminho?**
   - Caminho termina em `.zip` ou `.tar.gz` → arquivo comprimido. Pergunte se deve extrair no lugar ou em um diretório temporário.
   - Caminho é um diretório → exportação baseada em arquivos.
   - Caminho termina em `.db` ou `.sqlite` → fonte SQLite. Pule para §5.
   - Caminho termina em `.json` ou `.edn` → dump estruturado.
2. **A usuária mencionou token de API / endpoint?** → API ao vivo.
3. **A usuária disse "tenho o MCP [ferramenta] rodando"?** → Fonte MCP.
4. **A usuária apenas nomeou uma ferramenta sem caminho?** → Pergunte: "Você tem uma exportação para eu ler, um token de API, ou o servidor MCP de [ferramenta] já está rodando?"

### Passo 2 — Perguntas de esclarecimento obrigatórias

Antes de qualquer inventário, antes de qualquer escrita, o LLM faz este conjunto de perguntas. Não são opcionais.

1. **Onde está a fonte?** Caminho absoluto / endpoint de API + token / nome do servidor MCP.
2. **Intenção de entidade.** Há entidades (pessoas, organizações, projetos, metas, hábitos, tópicos, pilares) na fonte que você quer extrair para Wiki pessoal/CRM e Minha Vida — ou você quer tudo arquivado como notas-de-notas em `Wiki pessoal/Documentos/`?
3. **Frontmatter existente na fonte.** A fonte já tem frontmatter YAML?
   - **Preservar como está?** Mantém cada chave que a usuária já escreveu.
   - **Normalizar para DI-002?** Mapeia chaves conhecidas para o esquema, descarta chaves desconhecidas para o corpo.
   - **Sobrescrever?** Substitui o frontmatter da fonte pelo frontmatter derivado do modelo.
   Padrão se a usuária não tiver certeza: **normalizar**.
4. **Mapeamento de campo de data.** Qual campo de data se torna o `date:` por [[DI-002-convencoes-de-frontmatter]]? Padrão: `created_at`.
5. **Branch de fonte SQLite.** Se a fonte for SQLite: "Quer fazer a WeWiki migrar para SQLite primeiro via [[SOP-002-converter-para-sqlite]], ou transcrever tudo para markdown?"
6. **Política de conflito.** Se um arquivo de destino já existir: pular, sobrescrever ou renomear? Padrão: **renomear**.
7. **Tratamento de anexos.** Imagens copiadas para `Wiki pessoal/Imagens/AAAA/MM/` (padrão) ou referenciadas por caminho absoluto?
8. **Política de etiquetas.** Se a fonte tiver etiquetas: nivelar no array `tags:` (padrão) ou remodelar etiquetas recorrentes em notas de Tópico?

### Passo 3 — Inventário

Com as respostas do Passo 2, o LLM varre a fonte e produz um inventário **sem escrever nada na WeWiki ainda**. A saída é um resumo de contagem para a usuária verificar.

### Passo 4 — Plano + aprovação da usuária

O LLM propõe um plano de migração para a usuária. O plano é texto, não ação. A usuária deve aprovar antes de qualquer escrita.

O plano contém:
1. Tabela de contagem de entidades
2. Amostra de mapeamento por tipo
3. Plano de normalização de wikilinks
4. Relatório de conflitos
5. Lista de anomalias
6. Contagem estimada de escritas

### Passo 5 — Criar entidades (por tipo)

Para cada entidade descoberta, o LLM:

1. Carrega o modelo correspondente de `Wiki equipe/Modelos/<tipo>.md`.
2. Preenche o frontmatter por [[DI-002-convencoes-de-frontmatter]].
3. Gera o slug por [[DI-001-convencoes-de-nomeacao]].
4. Escreve no destino. Cria pastas `AAAA/MM/` automaticamente conforme necessário.
5. Atualiza o `INDEX.md` da seção com o novo arquivo.

### Passo 6 — Normalizar wikilinks

Após todos os arquivos estarem em disco, percorra cada nota importada e reescreva as referências cruzadas para slugs kebab-case.

### Passo 7 — Entrada de log de sessão

Escreva uma entrada de log de sessão do tipo `proativo` em `Wiki equipe/logs-de-sessao/AAAA/MM/`. O corpo deve capturar: fonte, decisões, contagens, wikilinks órfãos, o que não foi importado.

### Passo 8 — Passe de graduação opcional

O LLM pode ter encontrado procedimentos que parecem candidatos a SOP / Fluxo de Trabalho. Eles são listados no final do log de sessão sob `## Candidatos a graduação`. Não os crie automaticamente.

## Tabela de mapeamento — conceito de fonte → destino WeWiki

| Conceito de fonte | Destino WeWiki | Notas |
|---|---|---|
| nota diária / entrada de diário | `Wiki pessoal/Diário/AAAA/MM/AAAA-MM-DD.md` | Aplicar o formato de notas diárias usado por [[FT-001-diario-diario]]. |
| pessoa / contato | `Wiki pessoal/CRM/Pessoas/<slug>.md` | Usar `Wiki equipe/Modelos/pessoa.md`. |
| empresa / instituição / local | `Wiki pessoal/CRM/Organizações/<slug>.md` | Usar `Wiki equipe/Modelos/organizacao.md`. |
| projeto / esforço com prazo | `Wiki pessoal/Minha Vida/Projetos/<slug>.md` | Usar `Wiki equipe/Modelos/projeto.md`. |
| meta / objetivo com horizonte | `Wiki pessoal/Minha Vida/Metas/<slug>.md` | Usar `Wiki equipe/Modelos/meta.md`. |
| hábito / rotina com cadência | `Wiki pessoal/Minha Vida/Hábitos/<slug>.md` | Usar `Wiki equipe/Modelos/habito.md`. |
| tópico / área / interesse | `Wiki pessoal/Minha Vida/Tópicos/<slug>.md` | Usar `Wiki equipe/Modelos/topico.md`. |
| MOC / índice / hub / dimensão de vida | `Wiki pessoal/Minha Vida/Pilares/<slug>.md` | Usar `Wiki equipe/Modelos/pilar.md`. |
| documento / arquivo / passaporte / contrato | `Wiki pessoal/Documentos/<slug>.md` | Usar `Wiki equipe/Modelos/documento.md`. |
| nota que não se encaixa nos tipos acima | `Wiki pessoal/Documentos/<slug>.md` | Documento é o destino curinga. Sinalizar para a usuária. |

## Definição de pronto

O Fluxo de Trabalho está completo quando **tudo** o seguinte for verdadeiro:

1. As contagens de entidades aprovadas pela usuária no Passo 4 correspondem às contagens reais de arquivos em disco por destino.
2. Cada novo arquivo nas oito pastas de entidade valida contra [[DI-002-convencoes-de-frontmatter]].
3. Slugs correspondem a [[DI-001-convencoes-de-nomeacao]].
4. O passe de reescrita de wikilinks produziu zero links quebrados, exceto a lista de órfãos explicitamente registrados.
5. Cada `INDEX.md` relevante lista as novas entradas.
6. O log de sessão de importação existe e contém todas as seções do Passo 7.
7. O passe de Bibliotecário do Larry no encerramento da sessão não encontra novas violações de SSOT.
