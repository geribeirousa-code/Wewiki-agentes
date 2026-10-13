"""Marca capítulos como estudados em Bíblia/progresso.json.

Uso:
  python marcar.py Gn 1-2          # capítulos 1 e 2 de Gênesis
  python marcar.py Gênesis 3       # um capítulo
  python marcar.py --desmarcar Gn 2
  python marcar.py --status        # mostra onde você está
"""
import argparse

import biblia as B

ap = argparse.ArgumentParser()
ap.add_argument("livro", nargs="?")
ap.add_argument("caps", nargs="?", help="ex.: 3 ou 1-2")
ap.add_argument("--desmarcar", action="store_true")
ap.add_argument("--status", action="store_true")
a = ap.parse_args()

p = B.ler_progresso()
if not a.status:
    if not (a.livro and a.caps):
        raise SystemExit("Informe livro e capítulos, ex.: marcar.py Gn 1-2")
    s = B.sigla_de(a.livro)
    ini, _, fim = a.caps.partition("-")
    ini, fim = int(ini), int(fim or ini)
    maxc = B.LIVRO[s]["caps"]
    if not (1 <= ini <= fim <= maxc):
        raise SystemExit(f"{B.LIVRO[s]['nome']} tem {maxc} capítulos.")
    cur = set(p["lidos"].get(s, []))
    for c in range(ini, fim + 1):
        (cur.discard if a.desmarcar else cur.add)(c)
    p["lidos"][s] = sorted(cur)
    B.salvar_progresso(p)

lidos, por_bloco = B.totais(p)
print(f"{lidos}/{B.TOTAL_CAPS} capítulos ({lidos / B.TOTAL_CAPS:.1%})")
for b in B.BLOCOS:
    ok, tot = por_bloco[b[0]]
    print(f"  {b[1]:<22} {ok:>3}/{tot:<3}")
prox = B.proximo_capitulo(p)
if prox:
    print(f"Próximo: {B.LIVRO[prox[0]]['nome']} {prox[1]}")
