# Estado atual — ponte PC ↔ celular

Última atualização: 2026-10-09

Este arquivo existe para que uma sessão nova (celular, web, outra máquina) abra já sabendo
onde o trabalho parou. Larry: leia junto com `AGENTS.md` no início de toda sessão e **atualize
no `/fechar-sessao`** (passo 3). Se algo aqui contradiz o que a Gê disser agora, vale o que
ela disser, e você corrige este arquivo.

## Onde o trabalho parou

- Frente de conteúdo: peças diárias das duas marcas — **Bowl Green** (PT, @bowlgreenxerem) e
  **Clean Touch Cabinets** (EN). Últimas entregas registradas em `Entregas/`:
  `2026-07-27-bowlgreen-componentes`, `-editorial`, `-pecas`.
- Frente de ferramentas (2026-10-09): skill `/arena` instalada e no `main`.
- **A confirmar com a Gê:** se há entregas ou fios mais recentes que julho. Veja também
  `Wiki equipe/tarefas/abertas/` e o último log em `Wiki equipe/logs-de-sessao/`.

## Decisões vigentes (valem até a Gê mudar)

| Tema | Decisão | Desde |
|---|---|---|
| Bowl Green | Fora das prioridades estratégicas. Manter funcionando até dez/2026: simplificar, controlar custo, preservar caixa, reduzir o dia a dia dela. Sem expansão nem investimento alto. Não presumir fechar ou vender em dez/2026. | pref. da Gê |
| Canais dark (YouTube) | Meta: R$ 50 mil/mês. Tratar como hipótese a validar; separar faturamento, custo e lucro. | pref. da Gê |
| `/arena` | Instalada. Usar só em decisão importante, sempre com `--quick` (16 agentes, 91 chamadas). Modo "aceitar edições" ligado. Colocar `.arena/` no `.gitignore` antes do primeiro uso. | 2026-10-09 |
| `omniroute` | **Rejeitado por ora.** Não roda no celular/nuvem; risco de bloqueio da assinatura (TLS stealth, reuso de login); seus textos iriam a provedores gratuitos. Reavaliar só se o limite de uso virar gargalo, e testar no PC. | 2026-10-09 |
| `claude-mem` | **Rejeitado.** Acrescenta gasto de tokens, é redundante com este sistema de memória, só roda no PC, captura dados pessoais. | 2026-10-09 |

Não reavalie as ferramentas rejeitadas sem fato novo.

## Preferências da Gê que valem em qualquer sessão

1. **Português do Brasil**, direto. Comece pela recomendação.
2. **Fim de toda avaliação de ferramenta, skill ou ideia = bloco Resumo:** Veredito (vale /
   não vale) · O que faz · Devemos? · Próximo passo.
3. **Entrega de conteúdo é visual.** Termina em imagem mostrada, não em descrição.
4. **Duas marcas apenas:** Bowl Green (PT) e Clean Touch Cabinets (EN). O time gera, a Gê aprova.
5. **Peças:** display nunca abaixo de 120px, silhueta diferente em cada peça, pessoa real na capa.
6. Pouco tempo e orçamento: validação pequena antes de investimento, com limite de gasto,
   prazo e critério de continuar ou abandonar.
7. Não misturar os negócios.

## O que NÃO está neste repositório

Ficou de fora por privacidade ou por peso — veja `.gitignore`:

- `Wiki pessoal/` (Diário, CRM, Minha Vida) — decisão de privacidade, não subiu pra nuvem.
- `Caixa de Entrada/` — mesma razão.
- PNGs de `Entregas/` — 130MB de peças renderizadas ficam só no PC.

Consequência prática no celular: **Penn não consegue escrever no Diário** e as peças antigas
não aparecem. Geração nova de peça funciona, mas a imagem sai por download, não vai direto
pro Desktop. Nesse caso, registre o que seria do Diário como fio aberto no log da sessão
(sem dados sensíveis) para o Penn capturar no PC.

## Como reverter a exclusão do conteúdo pessoal

Se a Gê decidir que quer o Diário disponível no celular, apague as linhas
`Wiki pessoal/` e `Caixa de Entrada/` do `.gitignore` e rode:

```
git add "Wiki pessoal" "Caixa de Entrada" && git commit -m "inclui conteudo pessoal"
```
