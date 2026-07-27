---
name: carousel-preview
description: Use quando a usuária quiser gerar uma prévia visual de um carrossel, ver todos os slides de uma vez em uma imagem só, revisar um carrossel antes de aprovar, ou compartilhar um carrossel como imagem única. Gatilhos - "me mostra o carrossel", "prévia", "preview", "quero ver os slides", "junta os slides numa imagem".
---

# Gerador de Prévia de Carrossel

Pega uma pasta de carrossel e costura todos os slides em uma única imagem horizontal larga com fundo escuro — pronta para revisão visual e para compartilhar. Se algum slide tiver versão MP4 animada, produz uma prévia em vídeo.

Esta é a **etapa de revisão visual** do sistema de conteúdo diário: a Gê aprova olhando a tira inteira, não slide a slide.

## Processo

### Passo 1: Encontrar o carrossel

A usuária fornece:
- Um caminho completo: `Entregas/2026-07-25-carrossel-bowlgreen-sustenta/`
- Ou só o nome/tema: "o carrossel da Bowl Green"

Se der só o nome, procure em `Entregas/AAAA-MM-DD-carrossel-<slug>/`. Cheque as datas mais recentes se a data exata não for especificada.

### Passo 2: Gerar a prévia

```bash
python .claude/skills/carousel-preview/scripts/carousel_preview.py "Entregas/<pasta-do-carrossel>/"
```

**Opções:**
- `--height N` — altura alvo de cada slide em pixels (padrão: 600). Use 400 para prévia menor, 800 para qualidade maior.
- `--output caminho.png` — caminho de saída customizado (padrão: `preview.png` dentro da pasta do carrossel).
- `--exclude arquivo.png` — exclui arquivos específicos da prévia.

### Passo 3: Mostrar o resultado

Leia o `preview.png` gerado com a ferramenta Read e **exiba para a usuária**. A Gê é completamente visual — nunca descreva o carrossel em texto sem mostrar a imagem.

Se algum slide tiver MP4, o script gera `preview.mp4` (vídeo) e `preview.png` (primeiro quadro estático). Sempre exiba o `.png` — nunca tente ler o `.mp4` diretamente.

Se a usuária quiser ajustes, rode de novo com opções diferentes:
- **Maior/menor:** ajuste `--height`
- **Outro local de saída:** use `--output`

## Notas desta instalação (Windows / WeWiki)

- Use `python`, não `python3` — esta máquina é Windows.
- Caminhos com espaços e acentos (`Entregas/`, `Wiki pessoal/`) **sempre** entre aspas.
- Dependências: `Pillow` (instalado ✅). Para prévia em **vídeo** também é preciso `opencv-python` (**não instalado** — rode `pip install opencv-python` se um dia usar slides animados). `ffmpeg` está disponível no PATH ✅.
- O script procura primeiro por `slide-*.png` (ordenação natural: slide-2 antes de slide-10). Se não achar, cai para qualquer `*.png` da pasta.
- `preview.png` é sempre excluído da própria prévia, então rodar de novo é seguro.

## Onde isso encaixa no sistema

Faz parte do [[FT-004-conteudo-diario]]: gerar → **prever (esta skill)** → Gê aprova → publicar.
