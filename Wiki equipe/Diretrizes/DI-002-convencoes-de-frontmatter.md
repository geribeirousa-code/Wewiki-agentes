# DI-002 - Convenções de Frontmatter

> **Esta Diretriz é a fonte de verdade para todos os campos YAML frontmatter em arquivos de entidade da WeWiki.** Silas audita contra isso. O código de conversão SQLite lê isso. Se um campo que você precisa não está aqui, edite esta Diretriz primeiro, depois use o campo.

## Regras gerais

1. **Frontmatter fica no topo.** Bloco YAML delimitado por `---` no início de todo arquivo de entidade.
2. **Dados estruturados no frontmatter; narrativa no corpo.** Não repita fatos do frontmatter em texto simples no corpo. O corpo é para prosa, contexto e wikilinks.
3. **Nenhum campo ad-hoc.** Se um campo não está nesta Diretriz, não use. Proponha adicioná-lo e aguarde aprovação.
4. **Campos obrigatórios vs opcionais.** Campos marcados com `(obrigatório)` devem estar presentes. Campos opcionais podem ser omitidos se desconhecidos — não invente valores.
5. **Chaves estrangeiras via slug.** Referências a outras entidades usam o slug do arquivo (sem extensão), não o nome para exibição.

## Por tipo de entidade

### Pessoa (`Wiki pessoal/CRM/Pessoas/<slug>.md`)

```yaml
---
tipo: pessoa
nome: Fulano de Tal                   # (obrigatório)
email: fulano@exemplo.com             # (opcional)
telefone: "+55 11 99999-9999"         # (opcional)
empresa: slug-da-empresa              # chave estrangeira → Organizações/ (opcional)
papel: Cargo ou título                # (opcional)
primeira_menção: AAAA-MM-DD           # data da entrada de Diário onde apareceu pela primeira vez (opcional)
tags: [tag1, tag2]                    # (opcional)
---
```

### Organização (`Wiki pessoal/CRM/Organizações/<slug>.md`)

```yaml
---
tipo: organizacao
nome: Nome da Empresa                 # (obrigatório)
setor: tecnologia                     # (opcional)
website: https://exemplo.com          # (opcional)
instagram: "@handle"                  # handle sem barra e sem URL, com @ (opcional)
primeira_menção: AAAA-MM-DD           # (opcional)
tags: [tag1, tag2]                    # (opcional)
---
```

> Campo `instagram` adicionado em 2026-07-25 para sustentar [[FT-004-conteudo-diario]]. O handle no frontmatter é a **fonte de verdade única** do @ da marca — os geradores de carrossel leem daqui. Nunca digite o handle direto num `config.json`.

### Projeto (`Wiki pessoal/Minha Vida/Projetos/<slug>.md`)

```yaml
---
tipo: projeto
titulo: Nome do Projeto               # (obrigatório)
status: ativo | pausado | concluido | cancelado  # (obrigatório)
data_inicio: AAAA-MM-DD               # (opcional)
data_alvo: AAAA-MM-DD                 # (opcional)
metas_relacionadas: [slug-meta]       # chaves estrangeiras → Metas/ (opcional)
---
```

### Meta (`Wiki pessoal/Minha Vida/Metas/<slug>.md`)

```yaml
---
tipo: meta
titulo: Título da Meta                # (obrigatório)
status: ativa | concluida | abandonada  # (obrigatório)
prazo: AAAA-MM-DD                     # (opcional)
pilares_relacionados: [slug-pilar]    # chaves estrangeiras → Pilares/ (opcional)
---
```

### Hábito (`Wiki pessoal/Minha Vida/Hábitos/<slug>.md`)

```yaml
---
tipo: habito
titulo: Título do Hábito              # (obrigatório)
frequencia: diario | semanal | mensal  # (obrigatório)
status: ativo | pausado | abandonado  # (obrigatório)
inicio: AAAA-MM-DD                    # (opcional)
---
```

### Tópico (`Wiki pessoal/Minha Vida/Tópicos/<slug>.md`)

```yaml
---
tipo: topico
titulo: Título do Tópico              # (obrigatório)
tags: [tag1, tag2]                    # (opcional)
---
```

### Pilar (`Wiki pessoal/Minha Vida/Pilares/<slug>.md`)

```yaml
---
tipo: pilar
titulo: Título do Pilar               # (obrigatório)
---
```

### Documento (`Wiki pessoal/Documentos/<slug>.md`)

```yaml
---
tipo: documento
titulo: Título do Documento           # (obrigatório)
numero: ABC123                        # número do documento se aplicável (opcional)
valido_ate: AAAA-MM-DD               # (opcional)
arquivo_real: ~/Documentos/nome-do-arquivo.pdf  # caminho para o arquivo real (opcional)
---
```

## Convenções de wikilink

- Referências dentro do frontmatter usam slugs simples (sem colchetes duplos).
- Referências no corpo do arquivo usam `[[wikilinks]]` normais.
- Para referências de frontmatter a listas: `[slug1, slug2]` em YAML.
