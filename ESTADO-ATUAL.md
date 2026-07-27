# Estado atual — ponte PC ↔ celular

Última atualização: 2026-07-27

Este arquivo existe para que uma sessão nova (celular, web, outra máquina) abra já sabendo
onde o trabalho parou. Larry: leia junto com `AGENTS.md` no início de toda sessão remota.

## Onde o trabalho parou

- Frente ativa: conteúdo diário das duas marcas — **Bowl Green** (PT, @bowlgreenxerem) e
  **Clean Touch Cabinets** (EN).
- Entregas mais recentes em `Entregas/`: `2026-07-27-bowlgreen-componentes`,
  `2026-07-27-bowlgreen-editorial`, `2026-07-27-bowlgreen-pecas`.
- Arquivo em edição no PC quando a ponte foi montada:
  `.claude/skills/carrossel-bowlgreen/scripts/gerar_componentes.py`.

## Preferências da Gê que valem em qualquer sessão

1. **Entrega é visual.** Toda tarefa termina em imagem mostrada, nunca em descrição de texto.
2. **Duas marcas apenas:** Bowl Green (PT) e Clean Touch Cabinets (EN). O time gera, a Gê aprova.
3. **Peças:** display nunca abaixo de 120px, silhueta diferente em cada peça, pessoa real na capa.

## O que NÃO está neste repositório

Ficou de fora por privacidade ou por peso — veja `.gitignore`:

- `Wiki pessoal/` (Diário, CRM, Minha Vida) — decisão de privacidade, não subiu pra nuvem.
- `Caixa de Entrada/` — mesma razão.
- PNGs de `Entregas/` — 130MB de peças renderizadas ficam só no PC.

Consequência prática no celular: **Penn não consegue escrever no Diário** e as peças antigas
não aparecem. Geração nova de peça funciona, mas a imagem sai por download, não vai direto
pro Desktop.

## Como reverter a exclusão do conteúdo pessoal

Se a Gê decidir que quer o Diário disponível no celular, apague as linhas
`Wiki pessoal/` e `Caixa de Entrada/` do `.gitignore` e rode:

```
git add "Wiki pessoal" "Caixa de Entrada" && git commit -m "inclui conteudo pessoal"
```
