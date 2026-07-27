# SOP-002 — Converter Vault Markdown para SQLite

- **Dono padrão:** Silas (a usuária executa o procedimento com qualquer LLM capaz de código como executor; Silas é dono da auditoria de pré-voo e do relatório de migração)
- **Reutilizável por qualquer agente.** Este é uma habilidade, não uma propriedade 1:1. SOPs são procedimentos que qualquer agente pode invocar quando precisar.
- **Acionado por:** a usuária decide que sua WeWiki markdown cresceu além dos arquivos simples e quer um espelho SQLite para consultas estruturadas, análise ou desempenho do lado do LLM.
- **Referências:** [[DI-001-convencoes-de-nomeacao]], [[Wiki equipe/INDEX]]

## Propósito

Gerar um banco de dados SQLite que espelha o estado atual da sua WeWiki em markdown. O markdown permanece a fonte de verdade — SQLite é uma camada de desempenho derivada, regenerada sob demanda.

Este SOP é um **prompt como entregável**. O corpo deste arquivo (tudo abaixo do divisor) deve ser colado literalmente em um LLM capaz de código (Claude Code, Codex CLI, Cursor ou qualquer LLM de chat com execução de código). O LLM produz um script Python e o arquivo `.db` resultante. Sua WeWiki permanece somente leitura durante todo o processo.

## Quando executar este SOP

Marque pelo menos dois dos seguintes antes de se preocupar:

- Sua WeWiki ultrapassou aproximadamente 5.000 arquivos markdown e a busca por grep está ficando lenta.
- Você está executando consultas estruturadas que o LLM precisa repetir com frequência ("mostre-me todo Projeto vinculado a uma Meta sob o Pilar Saúde").
- Você quer análises da sua WeWiki (entradas por semana, frequência de menções de pessoas, cronogramas de expiração de documentos).
- Você está sincronizando entre vários dispositivos e quer um único binário para enviar em vez de milhares de arquivos.

Se nenhum desses se aplica, permaneça em markdown. SQLite é uma sobrecarga que você ainda não precisa.

## Quando NÃO executar este SOP

- Sua ferramenta principal é o Obsidian e você depende da visualização de grafo ou plugins. SQLite não interopera com esses.
- Sua WeWiki tem menos de 1.000 arquivos. O markdown lida com isso sem esforço.

---

## Prompt para o executor de código

Cole o conteúdo abaixo em qualquer LLM capaz de código. Substitua `<RAIZ>` pelo caminho absoluto da sua WeWiki.

```
Você é um engenheiro de dados. Sua tarefa é gerar um script Python que converte uma WeWiki baseada em markdown em um banco de dados SQLite, então executar esse script e entregar o arquivo .db resultante.

RAIZ DA WEWIKI: <RAIZ>

### Estrutura da WeWiki

A WeWiki tem dois ramos:

1. Wiki pessoal (conhecimento pessoal)
   - Wiki pessoal/CRM/Pessoas/         → entidade Pessoa
   - Wiki pessoal/CRM/Organizações/    → entidade Organização
   - Wiki pessoal/Minha Vida/Metas/    → entidade Meta
   - Wiki pessoal/Minha Vida/Hábitos/  → entidade Hábito
   - Wiki pessoal/Minha Vida/Projetos/ → entidade Projeto
   - Wiki pessoal/Minha Vida/Tópicos/  → entidade Tópico
   - Wiki pessoal/Minha Vida/Pilares/  → entidade Pilar
   - Wiki pessoal/Documentos/          → entidade Documento
   - Wiki pessoal/Diário/AAAA/MM/      → entidade EntradaDiario
   - Wiki pessoal/Imagens/AAAA/MM/     → entidade Imagem

2. Wiki equipe (conhecimento operacional)
   - Wiki equipe/SOPs/                    → entidade SOP
   - Wiki equipe/Fluxos de Trabalho/      → entidade FluxoTrabalho
   - Wiki equipe/Diretrizes/              → entidade Diretriz
   - Wiki equipe/logs-de-sessao/AAAA/MM/  → entidade LogSessao
   - Wiki equipe/tarefas/abertas/         → entidade Tarefa (status=aberta)
   - Wiki equipe/tarefas/em-andamento/    → entidade Tarefa (status=em-andamento)
   - Wiki equipe/tarefas/concluidas/AAAA/MM/ → entidade Tarefa (status=concluida)
   - Wiki equipe/tarefas/canceladas/AAAA/MM/ → entidade Tarefa (status=cancelada)

### O que gerar

1. Um script Python (wewiki_to_sqlite.py) que:
   - Percorre cada pasta de entidade acima
   - Analisa o frontmatter YAML de cada arquivo .md
   - Insere uma linha por arquivo nas tabelas SQLite correspondentes
   - Extrai wikilinks do corpo para uma tabela de arestas (origem_arquivo, destino_slug)
   - Gera o banco de dados em <RAIZ>/wewiki.db

2. Execute o script e confirme que wewiki.db foi criado.

### Regras

- Somente leitura na WeWiki: não modifique, não exclua, não renomeie nenhum arquivo .md
- Nomes de colunas devem corresponder exatamente às chaves de frontmatter de DI-002 (ver [[DI-002-convencoes-de-frontmatter]])
- Arrays YAML (como `tags`, `vinculado_sops`) armazenados como JSON em colunas TEXT
- Arquivos sem frontmatter são pulados com um aviso (não é um erro)
- O banco de dados é recriado do zero a cada execução (não incremental — isso é intencional)
- Stdlib Python apenas — sem pacotes de terceiros

### Entregue

- O script wewiki_to_sqlite.py completo
- Saída de amostra confirmando contagem de linhas por tabela
- Quaisquer avisos sobre arquivos pulados
```

---

## Após a execução

Silas verifica a saída e entrega um relatório de migração à Gê com:
- Contagem de linhas por tabela
- Avisos (arquivos pulados, campos ausentes)
- Hora de início e de conclusão
- Hash SHA-256 do .db para verificação de integridade
