# -*- coding: utf-8 -*-
"""
Extrato bancário -> linhas prontas pra colar na aba Lançamentos do Painel Financeiro.

Uso:
    python extrato_para_lancamentos.py "caminho/do/extrato.csv" --frente Pessoal
    python extrato_para_lancamentos.py "Caixa de Entrada/Extratos"  --frente "Clean Touch"

Aceita .csv, .xlsx/.xls e .ofx/.qfx. Detecta as colunas sozinho.
Sai um .tsv com exatamente as 10 colunas da aba Lançamentos, na ordem certa,
e um relatório do que não foi categorizado automaticamente.

As regras de categorização ficam em regras.csv (mesma pasta). Formato:
    padrao;frente;tipo;categoria;forma
`padrao` é buscado como substring, sem acento e sem caixa, dentro da descrição.
Campo vazio = não sobrescreve o que já foi deduzido.
"""
import argparse, csv, os, re, sys, unicodedata
from datetime import datetime, date

COLUNAS = ["Data", "Frente", "Tipo", "Categoria", "Descrição", "Valor",
           "Forma de pagamento", "Cartão", "Parcela", "Status"]

AQUI = os.path.dirname(os.path.abspath(__file__))
REGRAS = os.path.join(AQUI, "regras.csv")


# ---------------------------------------------------------------- utilidades
def normalizar(s):
    s = unicodedata.normalize("NFKD", str(s or ""))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def parse_data(v, dia_primeiro=True):
    """dia_primeiro=True -> 01/03 é 1 de março (BR). False -> 3 de janeiro (US)."""
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v or "").strip()
    if not s:
        return None
    s = s.split("T")[0].split(" ")[0]
    ambiguos = (("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y")
                if dia_primeiro else
                ("%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y", "%m/%d/%y"))
    for f in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d") + ambiguos:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def detectar_ordem_data(valores):
    """Olha o arquivo inteiro e decide se é DD/MM ou MM/DD. Devolve (dia_primeiro, motivo)."""
    primeiro_alto = segundo_alto = 0
    for v in valores:
        if isinstance(v, (datetime, date)):
            continue
        m = re.match(r"^\s*(\d{1,2})[/.\-](\d{1,2})[/.\-]\d{2,4}", str(v or ""))
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            primeiro_alto += 1
        if b > 12:
            segundo_alto += 1
    if primeiro_alto and not segundo_alto:
        return True, "DD/MM (achei dia > 12 na 1ª posição, %dx)" % primeiro_alto
    if segundo_alto and not primeiro_alto:
        return False, "MM/DD (achei dia > 12 na 2ª posição, %dx)" % segundo_alto
    if primeiro_alto and segundo_alto:
        raise SystemExit(
            "Datas inconsistentes neste extrato: achei valores > 12 nas duas posições "
            "(%dx na 1ª, %dx na 2ª). Não dá pra adivinhar o formato — rode de novo com "
            "--data br ou --data us." % (primeiro_alto, segundo_alto))
    return None, "ambíguo (nenhuma data com dia > 12)"


def parse_valor(v):
    """Aceita 1.234,56 / 1,234.56 / (123.45) / R$ -12,00 / $12.00"""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    neg = s.startswith("(") and s.endswith(")")
    s = re.sub(r"[^\d,.\-]", "", s)
    if not s or s in ("-", ".", ","):
        return None
    if "," in s and "." in s:
        # o separador decimal é o que aparece por último
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        inteiro, _, dec = s.rpartition(",")
        s = (inteiro.replace(",", "") + "." + dec) if len(dec) in (1, 2) else s.replace(",", "")
    try:
        n = float(s)
    except ValueError:
        return None
    return -n if neg else n


# ------------------------------------------------------------------ leitura
def ler_csv(caminho):
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(caminho, encoding=enc, newline="") as fh:
                amostra = fh.read(8192)
                fh.seek(0)
                try:
                    dial = csv.Sniffer().sniff(amostra, delimiters=";,\t|")
                except csv.Error:
                    dial = csv.excel
                    dial.delimiter = ";" if amostra.count(";") > amostra.count(",") else ","
                return [r for r in csv.reader(fh, dial) if any(str(c).strip() for c in r)]
        except UnicodeDecodeError:
            continue
    raise SystemExit("Não consegui ler o CSV em nenhuma codificação conhecida: %s" % caminho)


def ler_xlsx(caminho):
    import openpyxl
    wb = openpyxl.load_workbook(caminho, data_only=True)
    linhas = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            if any(c is not None and str(c).strip() for c in row):
                linhas.append(list(row))
    return linhas


def ler_ofx(caminho):
    txt = open(caminho, encoding="latin-1", errors="ignore").read()
    linhas = [["DTPOSTED", "TRNAMT", "NAME", "MEMO", "CHECKNUM"]]
    for bloco in re.findall(r"<STMTTRN>(.*?)</STMTTRN>", txt, re.S | re.I):
        def tag(t):
            m = re.search(r"<%s>([^<\r\n]*)" % t, bloco, re.I)
            return m.group(1).strip() if m else ""
        linhas.append([tag("DTPOSTED")[:8], tag("TRNAMT"), tag("NAME"), tag("MEMO"), tag("CHECKNUM")])
    return linhas


def ler(caminho):
    ext = os.path.splitext(caminho)[1].lower()
    if ext in (".csv", ".txt"):
        return ler_csv(caminho)
    if ext in (".xlsx", ".xlsm", ".xls"):
        return ler_xlsx(caminho)
    if ext in (".ofx", ".qfx"):
        return ler_ofx(caminho)
    raise SystemExit("Extensão não suportada: %s" % ext)


# ------------------------------------------------------- detecção de colunas
PISTAS = {
    "data":    ["data", "date", "dtposted", "data lancamento", "data da compra",
                "posting date", "transaction date", "data movimento", "dt"],
    "desc":    ["descricao", "description", "historico", "memo", "name", "detalhe",
                "lancamento", "estabelecimento", "merchant", "payee", "titulo"],
    "valor":   ["valor", "amount", "trnamt", "value", "montante", "valor (r$)", "valor r$"],
    "debito":  ["debito", "debit", "saida", "withdrawal", "pagamento", "despesa"],
    "credito": ["credito", "credit", "entrada", "deposit", "recebimento", "receita"],
    "saldo":   ["saldo", "balance"],
    "doc":     ["documento", "checknum", "doc", "numero"],
}


def achar_cabecalho(linhas):
    """Devolve (indice_da_linha_de_cabecalho, mapa {papel: indice_coluna})."""
    melhor, melhor_mapa, melhor_nota = None, None, 0
    for i, linha in enumerate(linhas[:40]):
        celulas = [normalizar(c) for c in linha]
        mapa, nota = {}, 0
        for papel, pistas in PISTAS.items():
            for j, c in enumerate(celulas):
                if not c or j in mapa.values():
                    continue
                if any(c == p for p in pistas) or any(p in c for p in pistas):
                    mapa[papel] = j
                    nota += 2 if c in pistas else 1
                    break
        tem_valor = "valor" in mapa or ("debito" in mapa or "credito" in mapa)
        if "data" in mapa and "desc" in mapa and tem_valor and nota > melhor_nota:
            melhor, melhor_mapa, melhor_nota = i, mapa, nota
    if melhor is None:
        raise SystemExit(
            "Não achei o cabeçalho do extrato. Preciso de pelo menos uma coluna de data, "
            "uma de descrição e uma de valor.\nPrimeiras linhas lidas:\n  " +
            "\n  ".join(" | ".join(str(c) for c in l) for l in linhas[:6]))
    return melhor, melhor_mapa


# ------------------------------------------------------------------- regras
REGRAS_PADRAO = """# padrao;frente;tipo;categoria;forma
# 'padrao' e procurado como pedaco do texto da descricao, sem acento e sem caixa.
# Campo vazio = nao mexe. Adicione linhas aqui conforme o Larry for te mostrando o que sobrou.
pix recebido;;Entrada;Vendas / serviços;Pix / Transferência
pix enviado;;Saída;Outras saídas;Pix / Transferência
transferencia recebida;;Entrada;Outras entradas;Pix / Transferência
transferencia enviada;;Saída;Outras saídas;Pix / Transferência
zelle;;;;Zelle
paypal;;;;PayPal
stripe;;Entrada;Vendas / serviços;Stripe
tarifa;;Saída;Tarifas bancárias;Débito automático
taxa;;Saída;Tarifas bancárias;Débito automático
juros;;Saída;Tarifas bancárias;Débito automático
iof;;Saída;Impostos e taxas;Débito automático
pagamento de fatura;;Saída;Cartão - pagamento de fatura;
aluguel;;Saída;Moradia;
rent;;Saída;Moradia;
mortgage;;Saída;Moradia;
energia;;Saída;Moradia;
luz;;Saída;Moradia;
agua;;Saída;Moradia;
internet;;Saída;Moradia;
uber;;Saída;Transporte;
lyft;;Saída;Transporte;
shell;;Saída;Transporte;
gas station;;Saída;Transporte;
posto;;Saída;Transporte;
supermercado;;Saída;Alimentação;
market;;Saída;Alimentação;
walmart;;Saída;Alimentação;
costco;;Saída;Alimentação;
restaurante;;Saída;Alimentação;
ifood;;Saída;Alimentação;
farmacia;;Saída;Saúde;
pharmacy;;Saída;Saúde;
seguro;;Saída;Saúde;
insurance;;Saída;Saúde;
netflix;;Saída;Assinaturas;
spotify;;Saída;Assinaturas;
google;;Saída;Ferramentas e software;
adobe;;Saída;Ferramentas e software;
canva;;Saída;Ferramentas e software;
openai;;Saída;Ferramentas e software;
anthropic;;Saída;Ferramentas e software;
meta pl;;Saída;Marketing;
facebk;;Saída;Marketing;
home depot;Clean Touch;Saída;Fornecedores;
lowes;Clean Touch;Saída;Fornecedores;
"""


def carregar_regras():
    if not os.path.exists(REGRAS):
        open(REGRAS, "w", encoding="utf-8").write(REGRAS_PADRAO)
        print("  regras.csv não existia — criei um inicial em %s" % REGRAS)
    regras = []
    for linha in open(REGRAS, encoding="utf-8"):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        p = (linha.split(";") + ["", "", "", "", ""])[:5]
        if p[0].strip():
            regras.append([normalizar(p[0])] + [x.strip() for x in p[1:]])
    return regras


# ---------------------------------------------------------------- conversão
def converter(caminho, frente_padrao, regras, forcar_data=None):
    linhas = ler(caminho)
    i_cab, mapa = achar_cabecalho(linhas)
    saida, sem_regra, ignoradas = [], {}, 0

    j_data = mapa["data"]
    brutas = [l[j_data] for l in linhas[i_cab + 1:] if j_data < len(l)]
    if forcar_data is None:
        dia_primeiro, motivo = detectar_ordem_data(brutas)
        if dia_primeiro is None:          # nenhuma data desempata: assume BR e avisa
            dia_primeiro = True
            motivo += " — assumi DD/MM. Se estiver errado, rode com --data us"
    else:
        dia_primeiro = (forcar_data == "br")
        motivo = "forçado por --data %s" % forcar_data
    print("   formato de data: %s" % motivo)

    for linha in linhas[i_cab + 1:]:
        def col(papel):
            j = mapa.get(papel)
            return linha[j] if j is not None and j < len(linha) else None

        d = parse_data(col("data"), dia_primeiro)
        if d is None:
            ignoradas += 1
            continue

        if "valor" in mapa:
            valor = parse_valor(col("valor"))
        else:
            deb = parse_valor(col("debito")) or 0.0
            cre = parse_valor(col("credito")) or 0.0
            valor = cre - abs(deb)
        if valor is None or valor == 0:
            ignoradas += 1
            continue

        partes = [str(col(k)).strip() for k in ("desc", "doc")
                  if col(k) not in (None, "") and str(col(k)).strip().lower() != "none"]
        descricao = " · ".join(dict.fromkeys(partes)) or "(sem descrição no extrato)"

        tipo = "Entrada" if valor > 0 else "Saída"
        frente, categoria, forma = frente_padrao, "", ""
        alvo = normalizar(descricao)
        casou = False
        for padrao, r_frente, r_tipo, r_cat, r_forma in regras:
            if padrao in alvo:
                casou = True
                frente = r_frente or frente
                tipo = r_tipo or tipo
                categoria = r_cat or categoria
                forma = r_forma or forma
                break
        if not categoria:
            categoria = "Outras entradas" if tipo == "Entrada" else "Outras saídas"
        if not casou:
            sem_regra[descricao[:60]] = sem_regra.get(descricao[:60], 0) + 1

        saida.append([d.strftime("%d/%m/%Y"), frente, tipo, categoria, descricao,
                      "%.2f" % abs(valor), forma, "", "", "Pago"])

    saida.sort(key=lambda r: datetime.strptime(r[0], "%d/%m/%Y"))
    return saida, sem_regra, ignoradas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", help="arquivo de extrato ou pasta com vários")
    ap.add_argument("--frente", default="Pessoal", help="Pessoal | Clean Touch | Internet")
    ap.add_argument("--saida", default=None, help="caminho do .tsv de saída")
    ap.add_argument("--data", choices=["br", "us"], default=None,
                    help="força DD/MM (br) ou MM/DD (us). Sem isso, detecta por arquivo.")
    a = ap.parse_args()

    alvos = []
    if os.path.isdir(a.entrada):
        for nome in sorted(os.listdir(a.entrada)):
            if os.path.splitext(nome)[1].lower() in (".csv", ".txt", ".xlsx", ".xlsm", ".xls", ".ofx", ".qfx"):
                alvos.append(os.path.join(a.entrada, nome))
    else:
        alvos = [a.entrada]
    if not alvos:
        raise SystemExit("Nenhum extrato encontrado em %s" % a.entrada)

    regras = carregar_regras()
    todas, sem_regra_total, ignoradas_total = [], {}, 0
    for caminho in alvos:
        print("\n>> %s" % os.path.basename(caminho))
        try:
            linhas, sem_regra, ignoradas = converter(caminho, a.frente, regras, a.data)
        except SystemExit as e:
            print("   ERRO: %s" % e)
            continue
        print("   %d lançamentos · %d linhas ignoradas" % (len(linhas), ignoradas))
        todas += linhas
        ignoradas_total += ignoradas
        for k, v in sem_regra.items():
            sem_regra_total[k] = sem_regra_total.get(k, 0) + v

    if not todas:
        raise SystemExit("Nada convertido.")
    todas.sort(key=lambda r: datetime.strptime(r[0], "%d/%m/%Y"))

    destino = a.saida or os.path.join(
        os.path.dirname(alvos[0]) or ".",
        "lancamentos-%s.tsv" % normalizar(a.frente).replace(" ", "-"))
    with open(destino, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(COLUNAS)
        w.writerows(todas)

    entradas = sum(float(r[5]) for r in todas if r[2] == "Entrada")
    saidas = sum(float(r[5]) for r in todas if r[2] == "Saída")
    print("\n" + "=" * 62)
    print("ARQUIVO PRONTO: %s" % destino)
    print("%d lançamentos · %s a %s" % (len(todas), todas[0][0], todas[-1][0]))
    print("Entradas %.2f  ·  Saídas %.2f  ·  Saldo %.2f" % (entradas, saidas, entradas - saidas))
    print("=" * 62)
    print("\nCole assim: abra a aba Lançamentos, clique na célula A5 (ou na")
    print("primeira linha vazia), e cole. As colunas já estão na ordem certa.")

    if sem_regra_total:
        print("\nSEM REGRA — %d descrições diferentes caíram em 'Outras'." % len(sem_regra_total))
        print("As mais frequentes (adicione ao regras.csv o que se repetir):")
        for desc, n in sorted(sem_regra_total.items(), key=lambda x: -x[1])[:25]:
            print("   %3dx  %s" % (n, desc))


if __name__ == "__main__":
    main()
