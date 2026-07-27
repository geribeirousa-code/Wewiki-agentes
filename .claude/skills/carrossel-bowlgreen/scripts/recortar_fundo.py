#!/usr/bin/env python3
"""
Recorta o fundo branco das fotos de prato, gerando PNG com transparência.

As fotos vêm em fundo branco de estúdio. Coladas direto sobre o creme da marca,
o quadrado branco aparece e estraga a peça. Aqui o branco vira alpha.

O recorte parte das BORDAS para dentro (flood fill), nunca por limiar global —
senão o cream cheese, a maionese e o arroz branco de dentro do bowl sumiriam junto.

Uso:
    python recortar_fundo.py            # processa a pasta inteira
    python recortar_fundo.py "POKE SORA"
"""

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ORIGEM = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN/Fotos/pratos")
DESTINO = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN/Fotos/recortados")

LIMIAR = 232      # acima disso é candidato a fundo
SUAVIZA = 1.6     # desfoque da máscara, para a borda não ficar serrilhada


def recortar(caminho):
    im = Image.open(caminho).convert("RGB")
    arr = np.asarray(im).astype(np.int16)
    alt, larg = arr.shape[:2]

    # Candidato a fundo: claro e sem cor (o branco do estúdio, incluindo a sombra suave)
    claro = arr.min(axis=2) >= LIMIAR - 40
    neutro = (arr.max(axis=2) - arr.min(axis=2)) <= 18
    candidato = claro & neutro

    # Flood fill a partir das bordas — só o que encosta na moldura é fundo
    fundo = np.zeros((alt, larg), dtype=bool)
    fila = deque()
    for x in range(larg):
        for y in (0, alt - 1):
            if candidato[y, x] and not fundo[y, x]:
                fundo[y, x] = True; fila.append((y, x))
    for y in range(alt):
        for x in (0, larg - 1):
            if candidato[y, x] and not fundo[y, x]:
                fundo[y, x] = True; fila.append((y, x))

    while fila:
        y, x = fila.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < alt and 0 <= nx < larg and candidato[ny, nx] and not fundo[ny, nx]:
                fundo[ny, nx] = True; fila.append((ny, nx))

    alpha = np.where(fundo, 0, 255).astype(np.uint8)
    mascara = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(SUAVIZA))

    saida = im.convert("RGBA")
    saida.putalpha(mascara)
    return saida.crop(saida.getbbox())  # apara a margem vazia que sobrou


def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    alvos = [p for p in sorted(ORIGEM.iterdir())
             if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}]
    if len(sys.argv) > 1:
        filtro = sys.argv[1].lower()
        alvos = [p for p in alvos if p.stem.lower() == filtro]
        if not alvos:
            raise SystemExit(f"não achei '{sys.argv[1]}' em {ORIGEM}")

    for p in alvos:
        rec = recortar(p)
        destino = DESTINO / f"{p.stem}.png"
        rec.save(destino)
        print(f"  {p.stem:26} {rec.size[0]}x{rec.size[1]}")

    print(f"\n{len(alvos)} recortadas em {DESTINO}/")


if __name__ == "__main__":
    main()
