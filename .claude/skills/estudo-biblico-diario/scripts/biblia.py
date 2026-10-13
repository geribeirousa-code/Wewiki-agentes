"""Base do plano de estudo bíblico: livros, blocos, cores, plano e progresso.

Só biblioteca padrão do Python. Tudo que a Gê edita ou imprime vive em `Bíblia/`
na raiz da pasta; esta skill só guarda o código e os dados geográficos.
"""
import json
import math
import re
import sys
from datetime import date, timedelta
from pathlib import Path

for _f in (sys.stdout, sys.stderr):   # console do Windows pode não ser UTF-8
    try:
        _f.reconfigure(encoding="utf-8")
    except Exception:
        pass

RAIZ = Path(__file__).resolve().parents[4]          # raiz da WeWiki
PASTA = RAIZ / "Bíblia"                              # dados e entregas da Gê
SKILL = Path(__file__).resolve().parents[1]
DADOS = SKILL / "dados"

# --- Blocos (a divisão que a Gê já usava) -----------------------------------
# cor = cor forte; a versão clara (tint) é calculada misturando com branco.
BLOCOS = [
    ("lei",        "Lei",               "#FF7EB6", "Torá — a aliança e os alicerces"),
    ("historicos", "Históricos",        "#F4B41A", "De Canaã ao exílio e à volta"),
    ("poeticos",   "Poéticos e Sabedoria", "#7EC8FF", "Louvor, dor e sabedoria"),
    ("profetas",   "Profetas",          "#9FD68A", "A voz de Deus em tempos de crise"),
    ("evangelhos", "Evangelhos",        "#25C2B0", "A vida de Jesus"),
    ("atos",       "Atos",              "#FFD63A", "A igreja nasce e cruza o mundo"),
    ("paulinas",   "Cartas de Paulo",   "#FFB3D1", "Cartas às igrejas e a pastores"),
    ("gerais",     "Cartas Gerais",     "#5AA9F0", "Hebreus, Tiago, Pedro, João e Judas"),
    ("apocalipse", "Apocalipse",        "#8ADBC0", "A visão final"),
]
BLOCO = {b[0]: b for b in BLOCOS}

TINTA = "#3B3350"       # texto principal (ameixa escura, boa leitura no fundo claro)
TINTA_SUAVE = "#7A6F93"


def misturar(hex_cor, f):
    """Mistura a cor com branco: f=0 → a própria cor, f=1 → branco."""
    h = hex_cor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * f) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def escurecer(hex_cor, f):
    h = hex_cor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c * (1 - f)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


# --- Livros: (sigla NVI, nome, capítulos, bloco, ritmo cap/dia, língua) -------
L = [
    ("Gn", "Gênesis", 50, "lei", 2, "hebraico"),
    ("Êx", "Êxodo", 40, "lei", 2, "hebraico"),
    ("Lv", "Levítico", 27, "lei", 2, "hebraico"),
    ("Nm", "Números", 36, "lei", 2, "hebraico"),
    ("Dt", "Deuteronômio", 34, "lei", 2, "hebraico"),
    ("Js", "Josué", 24, "historicos", 2, "hebraico"),
    ("Jz", "Juízes", 21, "historicos", 2, "hebraico"),
    ("Rt", "Rute", 4, "historicos", 4, "hebraico"),
    ("1Sm", "1 Samuel", 31, "historicos", 2, "hebraico"),
    ("2Sm", "2 Samuel", 24, "historicos", 2, "hebraico"),
    ("1Rs", "1 Reis", 22, "historicos", 2, "hebraico"),
    ("2Rs", "2 Reis", 25, "historicos", 2, "hebraico"),
    ("1Cr", "1 Crônicas", 29, "historicos", 3, "hebraico"),
    ("2Cr", "2 Crônicas", 36, "historicos", 3, "hebraico"),
    ("Ed", "Esdras", 10, "historicos", 2, "hebraico e aramaico"),
    ("Ne", "Neemias", 13, "historicos", 2, "hebraico"),
    ("Et", "Ester", 10, "historicos", 2, "hebraico"),
    ("Jó", "Jó", 42, "poeticos", 2, "hebraico"),
    ("Sl", "Salmos", 150, "poeticos", 2, "hebraico"),
    ("Pv", "Provérbios", 31, "poeticos", 2, "hebraico"),
    ("Ec", "Eclesiastes", 12, "poeticos", 2, "hebraico"),
    ("Ct", "Cântico dos Cânticos", 8, "poeticos", 4, "hebraico"),
    ("Is", "Isaías", 66, "profetas", 2, "hebraico"),
    ("Jr", "Jeremias", 52, "profetas", 2, "hebraico"),
    ("Lm", "Lamentações", 5, "profetas", 5, "hebraico"),
    ("Ez", "Ezequiel", 48, "profetas", 2, "hebraico"),
    ("Dn", "Daniel", 12, "profetas", 2, "hebraico e aramaico"),
    ("Os", "Oseias", 14, "profetas", 3, "hebraico"),
    ("Jl", "Joel", 3, "profetas", 3, "hebraico"),
    ("Am", "Amós", 9, "profetas", 3, "hebraico"),
    ("Ob", "Obadias", 1, "profetas", 1, "hebraico"),
    ("Jn", "Jonas", 4, "profetas", 4, "hebraico"),
    ("Mq", "Miqueias", 7, "profetas", 4, "hebraico"),
    ("Na", "Naum", 3, "profetas", 3, "hebraico"),
    ("Hc", "Habacuque", 3, "profetas", 3, "hebraico"),
    ("Sf", "Sofonias", 3, "profetas", 3, "hebraico"),
    ("Ag", "Ageu", 2, "profetas", 2, "hebraico"),
    ("Zc", "Zacarias", 14, "profetas", 3, "hebraico"),
    ("Ml", "Malaquias", 4, "profetas", 4, "hebraico"),
    ("Mt", "Mateus", 28, "evangelhos", 2, "grego"),
    ("Mc", "Marcos", 16, "evangelhos", 2, "grego"),
    ("Lc", "Lucas", 24, "evangelhos", 2, "grego"),
    ("Jo", "João", 21, "evangelhos", 2, "grego"),
    ("At", "Atos", 28, "atos", 2, "grego"),
    ("Rm", "Romanos", 16, "paulinas", 2, "grego"),
    ("1Co", "1 Coríntios", 16, "paulinas", 2, "grego"),
    ("2Co", "2 Coríntios", 13, "paulinas", 2, "grego"),
    ("Gl", "Gálatas", 6, "paulinas", 3, "grego"),
    ("Ef", "Efésios", 6, "paulinas", 3, "grego"),
    ("Fp", "Filipenses", 4, "paulinas", 4, "grego"),
    ("Cl", "Colossenses", 4, "paulinas", 4, "grego"),
    ("1Ts", "1 Tessalonicenses", 5, "paulinas", 5, "grego"),
    ("2Ts", "2 Tessalonicenses", 3, "paulinas", 3, "grego"),
    ("1Tm", "1 Timóteo", 6, "paulinas", 3, "grego"),
    ("2Tm", "2 Timóteo", 4, "paulinas", 4, "grego"),
    ("Tt", "Tito", 3, "paulinas", 3, "grego"),
    ("Fm", "Filemom", 1, "paulinas", 1, "grego"),
    ("Hb", "Hebreus", 13, "gerais", 2, "grego"),
    ("Tg", "Tiago", 5, "gerais", 5, "grego"),
    ("1Pe", "1 Pedro", 5, "gerais", 5, "grego"),
    ("2Pe", "2 Pedro", 3, "gerais", 3, "grego"),
    ("1Jo", "1 João", 5, "gerais", 5, "grego"),
    ("2Jo", "2 João", 1, "gerais", 1, "grego"),
    ("3Jo", "3 João", 1, "gerais", 1, "grego"),
    ("Jd", "Judas", 1, "gerais", 1, "grego"),
    ("Ap", "Apocalipse", 22, "apocalipse", 2, "grego"),
]
LIVROS = [dict(sigla=s, nome=n, caps=c, bloco=b, ritmo=r, lingua=g) for s, n, c, b, r, g in L]
LIVRO = {x["sigla"]: x for x in LIVROS}
TOTAL_CAPS = sum(x["caps"] for x in LIVROS)
assert len(LIVROS) == 66 and TOTAL_CAPS == 1189, (len(LIVROS), TOTAL_CAPS)

# --- Plano -------------------------------------------------------------------


def _passagem(l, a, b):
    return f"{l['nome']} {a}" if a == b or l["caps"] == 1 and a == 1 else f"{l['nome']} {a}–{b}"


def montar_plano(inicio, dias_por_semana=6):
    """Lista de dias: cada livro cortado em fatias de `ritmo` capítulos.

    O corte é nominal. O estudo do dia pode andar ±1 capítulo para respeitar a
    perícope; o que vale é o cursor de capítulos lidos em progresso.json.
    """
    dias = []
    n = 0
    for l in LIVROS:
        c = 1
        while c <= l["caps"]:
            d = min(c + l["ritmo"] - 1, l["caps"])
            n += 1
            dias.append(dict(dia=n, sigla=l["sigla"], livro=l["nome"], bloco=l["bloco"],
                             de=c, ate=d, passagem=_passagem(l, c, d)))
            c = d + 1
    # datas: pula domingos (6 dias/semana)
    dt = inicio
    for d in dias:
        while dt.weekday() == 6 and dias_por_semana == 6:
            dt += timedelta(days=1)
        d["data_prevista"] = dt.isoformat()
        dt += timedelta(days=1)
    return dias


# --- Progresso ---------------------------------------------------------------
ARQ_PROGRESSO = PASTA / "progresso.json"
ARQ_PLANO = PASTA / "plano.json"


def progresso_padrao():
    return {
        "inicio": "2026-10-13",
        "dias_por_semana": 6,
        "traducao": "NVI",
        "lidos": {},            # {"Gn": [1, 2, 3]} capítulos já estudados
        "dias_concluidos": [],  # números de dia do plano
    }


def ler_progresso():
    if ARQ_PROGRESSO.exists():
        return json.loads(ARQ_PROGRESSO.read_text(encoding="utf-8"))
    return progresso_padrao()


def salvar_progresso(p):
    PASTA.mkdir(parents=True, exist_ok=True)
    for k in p["lidos"]:
        p["lidos"][k] = sorted(set(p["lidos"][k]))
    ARQ_PROGRESSO.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ler_plano():
    if not ARQ_PLANO.exists():
        raise SystemExit("plano.json não existe. Rode gerar_plano.py primeiro.")
    return json.loads(ARQ_PLANO.read_text(encoding="utf-8"))


def lidos_de(p, sigla):
    return set(p["lidos"].get(sigla, []))


def proximo_capitulo(p):
    """Primeiro capítulo ainda não estudado, na ordem do plano → (sigla, cap) ou None."""
    for l in LIVROS:
        ja = lidos_de(p, l["sigla"])
        for c in range(1, l["caps"] + 1):
            if c not in ja:
                return l["sigla"], c
    return None


def totais(p):
    lidos = sum(len(lidos_de(p, l["sigla"])) for l in LIVROS)
    por_bloco = {}
    for b in BLOCOS:
        tot = sum(l["caps"] for l in LIVROS if l["bloco"] == b[0])
        ok = sum(len(lidos_de(p, l["sigla"])) for l in LIVROS if l["bloco"] == b[0])
        por_bloco[b[0]] = (ok, tot)
    return lidos, por_bloco


def sigla_de(txt):
    """Aceita sigla ('Gn'), nome ('Gênesis') ou sem acento ('genesis')."""
    def norm(s):
        import unicodedata
        s = unicodedata.normalize("NFD", s)
        return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn").lower())
    alvo = norm(txt)
    for l in LIVROS:
        if alvo in (norm(l["sigla"]), norm(l["nome"])):
            return l["sigla"]
    raise SystemExit(f"Livro não reconhecido: {txt!r}")


def slug(txt):
    import unicodedata
    s = unicodedata.normalize("NFD", txt)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
