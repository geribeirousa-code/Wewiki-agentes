# Wiki equipe / scripts

Scripts utilitários de uso único que vêm com o WeWiki da WeWiki.

Estes **não** fazem parte do dia a dia da WeWiki — são ferramentas que você executa uma vez
(ou poucas vezes) para migrar ou reparar conteúdo, e depois esquece.

---

## `migrate-inline-fields-to-frontmatter.py`

**Status:** incluído desde v1.3.0. Opcional. Pode ser deletado após a migração.

### O que faz

Nas versões anteriores à v1.3.0, você pode ter escrito notas de entidade com metadados como
texto inline no corpo:

```markdown
# Dra. Ana Lima

**Nome completo:** Dra. Ana Lima
**Cargo:** médica
**Organização:** [[clinica-dra-ana]]
```

A v1.3.0 faz o **frontmatter YAML** a fonte de verdade (conforme
`Wiki equipe/Diretrizes/DI-002-convencoes-de-frontmatter.md` e os modelos de entidade em
`Wiki equipe/Modelos/`). Os campos inline no corpo resultam em **nada** — perda silenciosa
de dados.

Este script varre sua WeWiki, detecta o padrão antigo `**Campo:** valor`, e reescreve suas
notas com um bloco de frontmatter YAML no topo.

### O que ele toca

Olha apenas dentro das oito pastas de entidade:

```
Wiki pessoal/CRM/Pessoas/
Wiki pessoal/CRM/Organizações/
Wiki pessoal/Minha Vida/Projetos/
Wiki pessoal/Minha Vida/Metas/
Wiki pessoal/Minha Vida/Hábitos/
Wiki pessoal/Minha Vida/Tópicos/
Wiki pessoal/Minha Vida/Pilares/
Wiki pessoal/Documentos/
```

**Pula:**

- arquivos que já têm frontmatter YAML (sem dupla escrita)
- arquivos `INDEX.md`, `README.md`, `_modelo.md`
- pastas fora das oito pastas de entidade acima

### Como executar

O script é **em modo de simulação por padrão** — imprime diffs unificados e não toca seus arquivos
até você passar `--aplicar`.

```bash
# 1. Pré-visualizar o que mudaria (seguro; somente leitura)
python3 "Wiki equipe/scripts/migrate-inline-fields-to-frontmatter.py" .

# 2. Aplicar as reescritas (os originais são salvos como `<arquivo>.bak`)
python3 "Wiki equipe/scripts/migrate-inline-fields-to-frontmatter.py" . --aplicar

# 3. (opcional) Limitar a uma pasta de entidade
python3 "Wiki equipe/scripts/migrate-inline-fields-to-frontmatter.py" . \
    --somente "Wiki pessoal/CRM/Pessoas"

# 4. (opcional) Pré-visualização mais silenciosa (somente resumo, sem diffs)
python3 "Wiki equipe/scripts/migrate-inline-fields-to-frontmatter.py" . --silencioso
```

O primeiro argumento posicional é a **raiz da sua WeWiki** — a pasta que contém
`Wiki pessoal/`, `Wiki equipe/`, etc.

### Requisitos

- Python 3.9 ou mais recente
- **Sem pacotes de terceiros.** Apenas biblioteca padrão.

### Segurança

- O modo padrão é `--simulacao`. Você não vai sobrescrever nada acidentalmente.
- `--aplicar` salva um arquivo `.bak` ao lado de cada arquivo modificado antes de reescrevê-lo.
- Arquivos com frontmatter YAML existente são pulados completamente. O script é idempotente.
- Rótulos inline desconhecidos são **deixados no corpo intocados** e relatados no resumo por arquivo.

### Quando deletar este script

Uma vez que você o tiver executado na sua WeWiki e estiver satisfeita com o resultado, pode
deletar com segurança `Wiki equipe/scripts/migrate-inline-fields-to-frontmatter.py`
e este README. Eles não têm propósito no dia a dia.
