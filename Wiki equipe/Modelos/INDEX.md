# Modelos - Índice

Arquivos de início para copiar e editar para cada tipo de entidade na sua WeWiki. Cada modelo traz um bloco de frontmatter completo (conforme [[DI-002-convencoes-de-frontmatter]]) mais um esboço de corpo com cabeçalhos orientadores.

## Como usar um modelo

Escolha o modelo para a entidade que está criando. Copie-o para a pasta certa em `Wiki pessoal/`. Renomeie para um slug kebab-case conforme [[DI-001-convencoes-de-nomeacao]]. Preencha os campos que tiver. Deixe o resto em branco ou delete as linhas que nunca vai usar.

Exemplo, a partir da raiz da sua WeWiki:

```bash
cp "Wiki equipe/Modelos/pessoa.md" "Wiki pessoal/CRM/Pessoas/nome-sobrenome.md"
```

Depois abra o novo arquivo e edite. A aba Propriedades no Obsidian vai popular assim que você salvar o arquivo com frontmatter preenchido.

## Modelos

| Modelo | Entidade | Vai em |
|---|---|---|
| [[Modelos/pessoa]] | Pessoa | `Wiki pessoal/CRM/Pessoas/<slug>.md` |
| [[Modelos/organizacao]] | Organização | `Wiki pessoal/CRM/Organizações/<slug>.md` |
| [[Modelos/projeto]] | Projeto | `Wiki pessoal/Minha Vida/Projetos/<slug>.md` |
| [[Modelos/meta]] | Meta | `Wiki pessoal/Minha Vida/Metas/<slug>.md` |
| [[Modelos/habito]] | Hábito | `Wiki pessoal/Minha Vida/Hábitos/<slug>.md` |
| [[Modelos/topico]] | Tópico | `Wiki pessoal/Minha Vida/Tópicos/<slug>.md` |
| [[Modelos/pilar]] | Pilar | `Wiki pessoal/Minha Vida/Pilares/<slug>.md` |
| [[Modelos/documento]] | Documento | `Wiki pessoal/Documentos/<slug>.md` |

## Regras que estes modelos seguem

- Os nomes dos campos de frontmatter correspondem aos nomes de colunas SQLite em [[SOP-002-converter-para-sqlite]]. Não os renomeie.
- Os campos obrigatórios estão marcados em [[DI-002-convencoes-de-frontmatter]]. Todo o resto é opcional — delete as linhas que não precisar.
- Os cabeçalhos H2 do corpo são sugestões, não contratos. Adicione ou remova seções conforme a nota evolui.
- Campos de chave estrangeira (ex: `empresa`, `pilar`, `vinculado_*`) armazenam o **slug** do arquivo alvo, não o título. Por [[DI-002-convencoes-de-frontmatter]] regra 4.

## Em caso de dúvida

Leia [[DI-002-convencoes-de-frontmatter]]. Se um campo que você precisa não estiver lá, edite a Diretriz primeiro, depois volte e use-o.
