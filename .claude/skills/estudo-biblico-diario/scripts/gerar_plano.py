"""Gera Bíblia/plano.json (e progresso.json, se ainda não existir).

Uso: python gerar_plano.py [--inicio AAAA-MM-DD] [--dias-por-semana 6]
"""
import argparse
import json
from datetime import date

import biblia as B

ap = argparse.ArgumentParser()
ap.add_argument("--inicio")
ap.add_argument("--dias-por-semana", type=int)
a = ap.parse_args()

p = B.ler_progresso()
if a.inicio:
    p["inicio"] = a.inicio
if a.dias_por_semana:
    p["dias_por_semana"] = a.dias_por_semana
B.salvar_progresso(p)

plano = B.montar_plano(date.fromisoformat(p["inicio"]), p["dias_por_semana"])
B.PASTA.mkdir(parents=True, exist_ok=True)
B.ARQ_PLANO.write_text(json.dumps(plano, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

print(f"{len(plano)} dias de estudo · {B.TOTAL_CAPS} capítulos · início {p['inicio']} · "
      f"término previsto {plano[-1]['data_prevista']}")
for b in B.BLOCOS:
    ds = [d for d in plano if d["bloco"] == b[0]]
    print(f"  {b[1]:<22} dias {ds[0]['dia']:>3}–{ds[-1]['dia']:<3} ({len(ds)} dias)")
