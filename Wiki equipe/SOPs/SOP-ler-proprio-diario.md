# SOP — Ler o Próprio Diário

- **Dono:** qualquer agente especialista no início da sessão ou ao pegar uma tarefa
- **Acionado por:** início da sessão, antes de começar trabalho em uma nova tarefa
- **Saída:** aprendizados anteriores carregados e nomeados explicitamente no log de atualização da tarefa
- **Referências:** [[SOP-escrever-entrada-diario]]

## Propósito

Continuidade para o responsável. Seu diário é o que você já aprendeu e que o você-do-futuro vai querer reutilizar. Lê-lo antes de começar o trabalho é como você evita reaprender lições que já pagou. O custo é 30 segundos. O custo de pular é repetir erros que o você-anterior escreveu.

## Quando acionar

- Todo início de sessão, após o Larry passar uma tarefa e antes de você começar.
- Quando você está prestes a fazer algo que combina com uma situação anterior, mesmo que já tenha iniciado sessão antes.

## Passos

### 1. Ler o que o criador da tarefa já pré-carregou para você

Abra a tarefa que você vai assumir. Leia o array `vinculado_entradas_diario` no frontmatter. O criador da tarefa já identificou as entradas que considera relevantes. Leia-as na íntegra — `## O que aprendi`, `## Quando se aplica` e especialmente `## Quando NÃO se aplica`.

Este é o passo de maior valor. Pular é ignorar registros anteriores selecionados.

### 2. Listar suas entradas mais recentes

```bash
EU="<Seu Nome> - <Seu Papel>"
ls -t "Equipe/${EU}/diario/" 2>/dev/null | grep -v '^_modelo' | head -10
```

Leia os títulos (linha `# ...`) e a seção `## O que aprendi` de cada uma. Leitura rápida de 30 segundos.

### 3. Combinar por etiqueta com sua tarefa atual

Veja as `tags` da tarefa:

```bash
TAGS_TAREFA="<tag1> <tag2> <tag3>"
for tag in $TAGS_TAREFA; do
  grep -lE "tags:.*\b${tag}\b" "Equipe/${EU}/diario/"*.md 2>/dev/null
done
```

Para cada correspondência não coberta pelo passo 1: leia a entrada na íntegra.

### 4. Combinar por tópico

Se o título da tarefa contiver uma palavra-chave que corresponda ao campo `topico:` de uma entrada de diário existente, leia essa entrada.

### 5. Anotar o que está faltando

Se a tarefa for em um domínio onde você NÃO tem entradas de diário ainda, isso é sinal — você está prestes a fazer algo pela primeira vez (ou pela primeira vez que está registrando). Faça uma anotação mental: escreva uma entrada de diário no fechamento da sessão se aprender algo durável.

### 6. Levar os registros anteriores para o trabalho — visivelmente

Antes de iniciar a tarefa, nomeie os registros que está carregando. Acrescente às `## Atualizações` da tarefa:

```
- 2026-05-10 09:18 (mack) — registros carregados: [[2026-05-09-exemplo]] se aplica; [[2026-04-12-outro-exemplo]] também se aplica
```

Isso torna a superfície de retomada auditável. Se você esqueceu um registro relevante e cometeu um erro, a ausência é visível no log de atualização.

## Anti-padrão: ler-tudo-toda-vez

Se seu diário crescer para mais de 50 entradas, não leia cada entrada toda vez. Os passos 1 (tarefa `vinculado_entradas_diario`) + 2 (10 mais recentes) + 3 (combinação por tag) + 4 (combinação por tópico) reduzem isso. O arquivo completo é pesquisável quando você precisar.

## Erros comuns

- Pular esta etapa porque "quero logo começar." 30 segundos economizam 30 minutos.
- Ler apenas por recência, não por tag/tópico/`vinculado_entradas_diario`. A entrada relevante pode ter três meses e ter sido pré-carregada pelo criador da tarefa.
- Ler entradas antigas e usá-las silenciosamente sem nomear os registros. Se você vai seguir o conselho de uma entrada de diário, nomeie-a no log de atualização da tarefa.
- Esquecer de escrever novos aprendizados no final da sessão. O diário é um ciclo de feedback. Leia E escreva.
