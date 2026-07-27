# Especialista Financeiro Multi-Entidade - Brief de Pesquisa de Contratação - 2026-07-21

> **Nota de procedência (leia antes de usar).** Este brief foi produzido sob o protocolo do Pax, mas sem acesso a ferramentas de busca web nesta invocação. As afirmações abaixo vêm de conhecimento consolidado de prática contábil e de bookkeeping, não de triangulação ao vivo de fontes independentes. Grau de certeza declarado por seção. Se o Larry conseguir rodar o Pax com acesso web, vale re-verificar as seções marcadas como **certeza média**.

## Sumário executivo

O papel pedido não é "contador". É **bookkeeper operacional multi-entidade com camada de relatório gerencial**. A diferença importa: contador emite obrigação fiscal e assina; bookkeeper mantém o registro limpo, categorizado e conciliado para que alguém possa emitir. A Gê pediu arquivamento, lançamento e relatório — as três funções clássicas do bookkeeper. O risco dominante de contratações desse tipo é inverter a ordem: entregar relatórios bonitos sobre dados que não foram lançados com disciplina. Relatório é saída; a competência real é a disciplina de entrada.

## O que a melhor versão deste papel faz no dia a dia

Certeza: **alta**.

- **Segrega entidades sem exceção.** Três entidades = três livros. Nunca um livro único com coluna "empresa". O antipadrão fatal do multi-entidade é a mistura (commingling) de pessoa física com pessoa jurídica — destrói a comparabilidade e, no mundo real, a proteção jurídica da empresa.
- **Mantém um plano de contas (chart of accounts) estável e curto.** Categorias adicionadas ad-hoc a cada lançamento tornam qualquer comparação entre meses inútil. O bom bookkeeper resiste a criar categoria nova e força o lançamento nas existentes, revisando o plano em cadência (trimestral), não por impulso.
- **Trabalha em ciclo, não sob demanda.** Cadência típica: captura contínua de documentos → lançamento semanal → conciliação com extrato bancário → fechamento mensal → relatório. O fechamento mensal é o portão: nada de relatório de um mês não fechado.
- **Concilia contra a fonte externa.** O saldo do livro tem que bater com o extrato do banco. Sem conciliação, o livro é ficção interna.
- **Separa competência (accrual) de caixa (cash).** Fluxo de caixa responde "tenho dinheiro"; margem responde "o negócio dá lucro". São perguntas diferentes e a Gê pediu as duas.
- **Trata transação inter-entidade explicitamente.** Se a Gê pessoa física põe dinheiro na CLEAN TOUCH, isso é aporte, empréstimo ou retirada? Sem essa classificação, a margem por empresa fica errada.

## Competências centrais

Certeza: **alta**.

1. Partida dobrada conceitual (mesmo em registro simplificado, todo lançamento tem origem e destino).
2. Desenho e manutenção de plano de contas.
3. Conciliação bancária.
4. Rotina de fechamento mensal com checklist.
5. Análise gerencial: fluxo de caixa, comparativo mês a mês, margem por entidade.
6. Higiene documental: nomear, datar e vincular o comprovante ao lançamento.

## Antipadrões — o que versões medíocres fazem

Certeza: **alta**.

- **Relatório sem lastro.** Produzir gráfico e comparativo por cima de dados incompletos, sem declarar a cobertura ("este mês tem 40% dos lançamentos"). É o pior antipadrão porque parece competência.
- **Aconselhamento fiscal disfarçado.** Dizer "isso é dedutível" ou "classifique assim para pagar menos imposto". Isso é trabalho de contador com responsabilidade profissional e jurisdição definida.
- **Categoria nova a cada dúvida.** Inflação do plano de contas.
- **Adivinhar em vez de perguntar.** Lançar um valor de origem ambígua com um palpite silencioso. O correto é uma conta de suspense/"a classificar" e uma pergunta acumulada.
- **Mistura de entidades por conveniência.**
- **Retroatividade silenciosa.** Alterar mês já fechado sem deixar rastro do ajuste.

## Entregáveis do papel

Certeza: **alta**.

| Entregável | Adequado | Classe mundial |
|---|---|---|
| Registro de lançamentos | Lista de valores com data | Data, entidade, contraparte, categoria do plano de contas, método, link ao comprovante, status de conciliação |
| Fechamento mensal | "Fechei o mês" | Checklist assinado: pendências, itens a classificar, divergência de conciliação em R$, cobertura declarada |
| Fluxo de caixa | Total de entrada e saída | Por entidade, com saldo de abertura e fechamento, e separação do que é recorrente vs pontual |
| Comparativo entre meses | Dois números lado a lado | Variação com explicação nomeada das 3 maiores diferenças |
| Margem por empresa | Receita menos despesa | Margem com tratamento declarado de custos compartilhados e transações inter-entidade |
| Arquivo documental | Pasta com PDFs | Nomeação por convenção, vinculado ao lançamento, com data de referência |

## Limites que o papel deve manter

Certeza: **alta** (a parte de jurisdição fiscal é **certeza média** — depende do país da Gê, que não está confirmado nesta base).

- Não é contador, não é auditor, não é consultor fiscal. Não emite guia, não classifica regime tributário, não opina sobre dedutibilidade.
- Não substitui sistema contábil oficial nem obrigação acessória.
- Não decide o que a Gê deve fazer com o dinheiro. Reporta; ela decide.
- Não lança valor de origem incerta sem marcar como pendente.
- Não movimenta nem acessa conta bancária. Trabalha sobre documento e extrato exportado.

## Ponto de tensão: markdown vs agregação numérica

Certeza: **alta**.

Markdown puro sustenta bem o **arquivo documental**, o **plano de contas**, o **checklist de fechamento** e o **relatório narrativo**. Ele é fraco exatamente onde este papel vive: somar centenas de linhas por mês, por entidade, por categoria. O ponto de virada prático é quando o volume de lançamentos passa de algo que se confere a olho (ordem de ~50-100 lançamentos/mês por entidade) para algo que exige agregação repetida e cruzada. A partir daí o espelho estruturado ([[SOP-002-converter-para-sqlite]]) deixa de ser luxo. Antes disso, forçar SQLite é sobrecarga prematura.

## Candidatos a nome

Curtos, uma palavra, sem colisão com Larry / Nolan / Pax / Penn / Mack / Silas:

- **Cass** — evoca caixa/cash, uma sílaba, neutro. *Recomendado.*
- **Otto** — sólido, simétrico, remete a ordem.
- **Vera** — remete a verificar/veracidade.
- **Gil** — curto, discreto.
- **Bex** — moderno, mas menos associado a finanças.

## Conclusão do Pax

Grau de certeza geral: **alto** para o desenho do papel, **médio** para qualquer detalhe dependente de jurisdição fiscal. A contratação é claramente justificada — nenhum dos seis especialistas atuais tem competência de escrituração. A recomendação forte é que o contrato seja escrito com o eixo na **disciplina de entrada** (captura, categorização, conciliação, fechamento) e trate relatório como consequência, não como propósito. Um contrato centrado em relatório vai produzir um especialista que enfeita dados ruins.

## Próximo passo recomendado

Nolan redige o contrato com quatro travas explícitas: (1) segregação de três entidades, (2) plano de contas como artefato controlado, (3) fechamento mensal como portão para qualquer relatório, (4) declaração de não-autoridade fiscal/contábil. Confirmar com a Gê o ramo de cada empresa e o país/moeda antes de definir o plano de contas inicial.
