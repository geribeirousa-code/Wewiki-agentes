---
name: pauta-diaria
description: Monta o painel visual de aprovação do dia — todas as peças de todas as marcas lado a lado, legenda copiável e botão aprovar/refazer num único HTML autocontido. Use quando a usuária pedir a pauta do dia, quiser revisar/aprovar o conteúdo, disser "me mostra o que tem pra hoje", "monta a pauta", "quero aprovar", ou ao final de qualquer geração de conteúdo diário.
---

# Pauta Diária — painel de aprovação

A etapa de revisão do [[FT-004-conteudo-diario]]. A Gê é completamente visual: ela aprova olhando, não lendo. Esta skill entrega uma página onde o dia inteiro cabe numa tela.

## Processo

### Passo 1: Gerar as peças primeiro

A pauta **não gera conteúdo** — ela apresenta o que já existe. Antes de rodar, cada peça já deve estar numa pasta própria em `Entregas/`:

```
Entregas/AAAA-MM-DD-carrossel-<marca>-<slug>/
├── config.json
├── slide-01.png … slide-NN.png
└── preview.png        (opcional, ignorado pela pauta)
```

### Passo 2: Escrever o pauta.json

Crie `Entregas/AAAA-MM-DD-pauta/pauta.json`:

```json
{
  "data": "2026-07-25",
  "pecas": [
    {
      "marca": "Bowl Green",
      "handle": "@bowlgreenxerem",
      "plataforma": "Instagram · Carrossel",
      "pasta": "2026-07-25-carrossel-bowlgreen-sustenta",
      "angulo": "A tese da peça em uma linha.",
      "legenda": "Texto da legenda com \\n\\n entre parágrafos.",
      "hashtags": "#uma #linha #só",
      "observacao": "Nota do time para a Gê — decisão tomada, limitação conhecida.",
      "atencao": "Aviso destacado em amarelo. Use só quando algo bloqueia a publicação.",
      "excluir": ["slide-99.png"]
    }
  ]
}
```

`marca` e `plataforma` são obrigatórios. `pasta` é relativa a `Entregas/`. O resto é opcional.

**`marca` deve bater exatamente** com o `nome` do frontmatter em `Wiki pessoal/CRM/Organizações/` — é o que aplica a paleta certa. Marca desconhecida cai num cinza neutro.

### Passo 3: Rodar

```bash
python .claude/skills/pauta-diaria/scripts/gerar_pauta.py "Entregas/AAAA-MM-DD-pauta/pauta.json"
```

Gera `pauta.html` ao lado do JSON. Autocontido: imagens em base64, nada de caminho externo. Abre offline, pode ser movido, mandado por WhatsApp.

### Passo 4: Mostrar

Diga o caminho **e mostre**. Nunca só o caminho — a Gê é visual. Se precisar exibir aqui na conversa, tire um print:

```bash
python - <<'EOF'
from playwright.sync_api import sync_playwright
from pathlib import Path
alvo = Path(r"...\pauta.html").as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1320, "height": 1100}, device_scale_factor=2)
    pg.goto(alvo); pg.wait_for_timeout(1000)
    pg.screenshot(path="pauta.png", full_page=True)
    b.close()
EOF
```

## O que o painel faz

| Recurso | Comportamento |
|---|---|
| Tira de slides | Todos visíveis de uma vez, sem rolagem lateral. Carrossel longo cai para uma segunda linha. Clique amplia. |
| Legenda | Bloco copiável no fundo da marca. Botão `copiar` leva legenda + hashtags juntas. |
| Aprovar / Refazer | Pinta a borda (verde/vermelho), marca o selo. Clicar de novo desmarca. |
| Comentário | Campo livre por peça: "o que mudar". |
| Estado | Salvo no `localStorage` do navegador, por dia. Fechar e reabrir não perde. |
| Veredito | Botão no rodapé monta o resumo de todas as decisões **e já copia** para colar aqui na conversa. |
| Tema | Segue claro/escuro do sistema. Imprime limpo (botões somem). |

## Como a Gê devolve a decisão

Ela clica em `Fechar a pauta e copiar o veredito` e cola aqui. Chega assim:

```
Pauta de 2026-07-25

• Bowl Green — Instagram · Carrossel: aprovada
• Clean Touch Cabinets — Instagram · Carrossel: refazer
    ajuste: trocar o slide 1 por foto de obra real
```

Aí é só reprocessar o que voltou como `refazer` e regerar a pauta.

## Notas desta instalação

- `python`, não `python3` — Windows.
- Caminhos com espaço e acento sempre entre aspas.
- Sem dependência externa: só biblioteca padrão. O print opcional usa `playwright` (instalado ✅).
- Cores de marca ficam em `CORES_MARCA` no topo do script. Marca nova entra ali **e** em `Wiki pessoal/CRM/Organizações/`.
