#!/usr/bin/env python3
"""
Extrai a ficha técnica dos pratos do Painel de Precificação da Bowl Green.

O painel é a fonte de verdade do que vai dentro de cada prato — quantidade
por ingrediente, em quilo. Este script tira o objeto FICHAS de lá e grava
`dados/fichas.json`, que o gerador de posts e as legendas consultam.

Nenhum ingrediente é inventado. Se um prato não está no painel, ele não tem
ficha, e a legenda dele não pode afirmar composição.

Uso:
    python extrair_fichas.py
"""

import json
import re
import sys
from pathlib import Path

# O console do Windows abre em cp1252 e quebra em qualquer acento ou seta.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAINEL = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN/Painel-Precificacao-BowlGreen.html")
DESTINO = Path(__file__).resolve().parents[1] / "dados" / "fichas.json"

# Embalagem e descartável não são ingrediente — nunca entram em legenda.
NAO_COMESTIVEL = {"bowl", "kit_talher", "pote_molho", "saco", "garrafinha",
                  "papel_embrulho", "copo_fruta", "etiqueta", "guardanapo"}

# O que conta como proteína para a soma que aparece nos posts.
PROTEINAS = {"salmao", "camarao", "frango", "carne", "peixe_branco", "atum", "tilapia"}


def bloco(texto, nome, abre, fecha):
    i = texto.find(f"{nome} =")
    if i < 0:
        raise SystemExit(f"ERRO: não achei '{nome}' em {PAINEL.name}")
    j = texto.find(abre, i)
    prof = 0
    for k in range(j, len(texto)):
        if texto[k] == abre:
            prof += 1
        elif texto[k] == fecha:
            prof -= 1
            if prof == 0:
                return texto[j:k + 1]
    raise SystemExit(f"ERRO: bloco '{nome}' não fecha")


def main():
    if not PAINEL.exists():
        raise SystemExit(f"ERRO: painel não encontrado em {PAINEL}")
    texto = PAINEL.read_text(encoding="utf-8", errors="replace")

    nomes = dict(re.findall(r"id:\s*'([^']+)'\s*,\s*n:\s*'([^']+)'",
                            bloco(texto, "INGREDIENTES", "[", "]")))

    fichas = {}
    for m in re.finditer(r'"([^"]+)"\s*:\s*\{([^}]*)\}', bloco(texto, "FICHAS", "{", "}")):
        prato = m.group(1)
        bruto = dict((k, float(v)) for k, v in re.findall(r'(\w+)\s*:\s*([\d.]+)', m.group(2)))

        ingredientes, proteina = [], 0
        for chave, qtd in bruto.items():
            if chave in NAO_COMESTIVEL:
                continue
            gramas = round(qtd * 1000)
            ingredientes.append({"id": chave, "nome": nomes.get(chave, chave), "gramas": gramas})
            if chave in PROTEINAS:
                proteina += gramas

        ingredientes.sort(key=lambda x: -x["gramas"])
        fichas[prato] = {"ingredientes": ingredientes, "proteina_g": proteina}

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(fichas, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(fichas)} fichas → {DESTINO}\n")
    for prato, f in sorted(fichas.items()):
        if f["proteina_g"]:
            comp = " + ".join(f'{i["nome"]} {i["gramas"]}g' for i in f["ingredientes"] if i["id"] in PROTEINAS)
            print(f"  {prato:24} {f['proteina_g']:>4}g de proteína   ({comp})")


if __name__ == "__main__":
    main()
