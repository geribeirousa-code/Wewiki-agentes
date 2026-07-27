# -*- coding: utf-8 -*-
"""Painel Financeiro — Gê | gerador do .xlsx (vira Google Sheets na subida)"""
import openpyxl, os, base64
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule

VERDE, DOURADO = "0F2A24", "C9A961"
CREME, CREME2, BRANCO = "F5F1E8", "FBF9F4", "FFFFFF"
GRAFITE, POS, NEG, CINZA = "2B2B2B", "1E7A55", "B23A3A", "8A8A8A"
MOEDA = '"$"#,##0.00'
MOEDA_NEG = '"$"#,##0.00;[Red]-"$"#,##0.00'
PCT, DATA = '0%', 'DD/MM/YYYY'
thin = Side(style="thin", color="DDD6C7")
BORDA = Border(left=thin, right=thin, top=thin, bottom=thin)

FRENTES = ["Pessoal", "Clean Touch", "Internet"]
ANO = 2026
NL = 400            # linhas prontas em Lançamentos
wb = openpyxl.Workbook()


def titulo(ws, texto, sub, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=texto)
    c.font = Font(size=20, bold=True, color=BRANCO)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    for i in range(1, ncols + 1):
        ws.cell(row=1, column=i).fill = PatternFill("solid", fgColor=VERDE)
    ws.row_dimensions[1].height = 42
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    s = ws.cell(row=2, column=1, value=sub)
    s.font = Font(size=10, italic=True, color=CINZA)
    s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 22


def cabecalho(ws, linha, headers, larguras=None, freeze=True):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=linha, column=i, value=h)
        c.font = Font(size=10, bold=True, color=BRANCO)
        c.fill = PatternFill("solid", fgColor=VERDE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDA
    ws.row_dimensions[linha].height = 34
    if larguras:
        for i, w in enumerate(larguras, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    if freeze:
        ws.freeze_panes = ws.cell(row=linha + 1, column=1)


def secao(ws, linha, texto, ncols):
    ws.merge_cells(start_row=linha, start_column=1, end_row=linha, end_column=ncols)
    c = ws.cell(row=linha, column=1, value=texto)
    c.font = Font(size=12, bold=True, color=VERDE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    for i in range(1, ncols + 1):
        ws.cell(row=linha, column=i).fill = PatternFill("solid", fgColor=CREME)
    ws.row_dimensions[linha].height = 28


def zebra(ws, r0, r1, ncols):
    for r in range(r0, r1 + 1):
        f = PatternFill("solid", fgColor=CREME2 if (r - r0) % 2 else BRANCO)
        for c in range(1, ncols + 1):
            cel = ws.cell(row=r, column=c)
            cel.fill = f
            cel.border = BORDA
            cel.font = Font(size=10, color=GRAFITE)


def dv(fonte, ws, aplica):
    d = DataValidation(type="list", formula1="=" + fonte, allow_blank=True, showDropDown=False)
    ws.add_data_validation(d)
    d.add(aplica)


def dvl(itens, ws, aplica):
    d = DataValidation(type="list", formula1='"%s"' % ",".join(itens), allow_blank=True, showDropDown=False)
    ws.add_data_validation(d)
    d.add(aplica)


# intervalo de datas a partir de uma célula texto "AAAA-MM"
def ini_mes(cel):
    return '">="&DATE(VALUE(LEFT(%s,4)),VALUE(RIGHT(%s,2)),1)' % (cel, cel)


def fim_mes(cel):
    return '"<"&DATE(VALUE(LEFT(%s,4)),VALUE(RIGHT(%s,2))+1,1)' % (cel, cel)


# =====================================================================
# LISTAS
# =====================================================================
lst = wb.active
lst.title = "Listas"
titulo(lst, "LISTAS  ·  as opções dos menus suspensos",
       "Edite aqui e os menus de todas as abas mudam junto. Não apague nem reordene as colunas.", 8)
cabecalho(lst, 4, ["Frente", "Tipo", "Categoria", "Forma de pagamento",
                   "Tipo de patrimônio", "Frequência", "Status", "Tipo de estratégia"],
          [18, 14, 28, 22, 22, 14, 16, 24])
L = {
 1: FRENTES,
 2: ["Entrada", "Saída"],
 3: ["Moradia", "Alimentação", "Transporte", "Saúde", "Educação", "Lazer",
     "Assinaturas", "Impostos e taxas", "Marketing", "Fornecedores",
     "Ferramentas e software", "Equipamentos", "Salários e pró-labore",
     "Serviços profissionais", "Viagem", "Tarifas bancárias",
     "Cartão - pagamento de fatura", "Empréstimo / parcelamento",
     "Aporte investimento", "Resgate investimento", "Transferência entre contas",
     "Vendas / serviços", "Renda de internet", "Outras entradas", "Outras saídas"],
 4: ["Dinheiro", "Débito", "Crédito", "Pix / Transferência", "Boleto",
     "Zelle", "PayPal", "Stripe", "Cheque", "Débito automático"],
 5: ["Conta corrente", "Poupança", "Reserva de emergência", "Investimento",
     "Cripto", "Imóvel", "Veículo", "Equipamento", "Recebível", "Outro"],
 6: ["Mensal", "Trimestral", "Semestral", "Anual"],
 7: ["Ativo", "Pausado", "Encerrado", "Planejado", "Em teste"],
 8: ["Renda ativa", "Renda passiva", "Fazer render (investir)",
     "Cortar custo", "Escalar o que já existe"],
}
for col, vals in L.items():
    for i, v in enumerate(vals, start=5):
        c = lst.cell(row=i, column=col, value=v)
        c.font = Font(size=10, color=GRAFITE)
        c.border = BORDA
R_FRENTE, R_TIPO = "Listas!$A$5:$A$7", "Listas!$B$5:$B$6"
R_CAT, R_PAG = "Listas!$C$5:$C$29", "Listas!$D$5:$D$14"
R_PATR, R_FREQ = "Listas!$E$5:$E$14", "Listas!$F$5:$F$8"
R_STATUS, R_ESTR = "Listas!$G$5:$G$9", "Listas!$H$5:$H$9"

# =====================================================================
# LANÇAMENTOS   A Data | B Frente | C Tipo | D Categoria | E Descrição
#               F Valor | G Forma | H Cartão | I Parcela | J Status
# =====================================================================
lan = wb.create_sheet("Lançamentos")
titulo(lan, "LANÇAMENTOS  ·  tudo que entra e tudo que sai",
       "Uma linha por movimento. É a única aba onde você digita todo dia. Todo o resto se calcula a partir daqui.", 10)
cabecalho(lan, 4, ["Data", "Frente", "Tipo", "Categoria", "Descrição", "Valor",
                   "Forma de pagamento", "Cartão", "Parcela", "Status"],
          [12, 15, 11, 26, 38, 14, 20, 18, 11, 13])
FIM = 4 + NL
# formato aplicado na coluna inteira (o Google Sheets herda isso na importacao)
lan.column_dimensions["A"].number_format = DATA
lan.column_dimensions["F"].number_format = MOEDA
zebra(lan, 5, 60, 10)          # zebra so nas primeiras linhas: mantem o arquivo leve
for r in range(5, FIM + 1):
    lan.cell(row=r, column=1).number_format = DATA
    c = lan.cell(row=r, column=6)
    c.number_format = MOEDA
    c.font = Font(size=10, bold=True, color=GRAFITE)
dv(R_FRENTE, lan, "B5:B%d" % FIM)
dv(R_TIPO,   lan, "C5:C%d" % FIM)
dv(R_CAT,    lan, "D5:D%d" % FIM)
dv(R_PAG,    lan, "G5:G%d" % FIM)
dvl(["Pago", "Pendente", "Agendado"], lan, "J5:J%d" % FIM)
lan.conditional_formatting.add("C5:C%d" % FIM,
    CellIsRule(operator="equal", formula=['"Entrada"'], font=Font(color=POS, bold=True)))
lan.conditional_formatting.add("C5:C%d" % FIM,
    CellIsRule(operator="equal", formula=['"Saída"'], font=Font(color=NEG, bold=True)))
lan.conditional_formatting.add("J5:J%d" % FIM,
    CellIsRule(operator="equal", formula=['"Pendente"'],
               fill=PatternFill("solid", bgColor="FFF3CD"), font=Font(color="8A6D1B", bold=True)))

Q = "'Lançamentos'!"
DT, VL, FR, TP, CR = Q+"$A:$A", Q+"$F:$F", Q+"$B:$B", Q+"$C:$C", Q+"$H:$H"


def soma(cel_mes, frente=None, tipo=None):
    """SUMIFS do mês apontado por cel_mes, opcionalmente filtrando frente/tipo."""
    p = [VL, DT, ini_mes(cel_mes), DT, fim_mes(cel_mes)]
    if frente:
        p += [FR, '"%s"' % frente]
    if tipo:
        p += [TP, '"%s"' % tipo]
    return "=SUMIFS(%s)" % ",".join(p)


# =====================================================================
# RESUMO MENSAL
# =====================================================================
res = wb.create_sheet("Resumo Mensal")
titulo(res, "RESUMO MENSAL  ·  %d" % ANO,
       "Não digite nada aqui. Tudo vem dos Lançamentos. Se um número parece errado, o erro está lá.", 14)
cabecalho(res, 4, ["Mês", "Pessoal entra", "Pessoal sai", "Pessoal saldo",
                   "Clean Touch entra", "Clean Touch sai", "Clean Touch saldo",
                   "Internet entra", "Internet sai", "Internet saldo",
                   "TOTAL entra", "TOTAL sai", "SALDO DO MÊS", "ACUMULADO"],
          [11] + [15] * 9 + [15, 15, 17, 17])
for i in range(12):
    r = 5 + i
    res.cell(row=r, column=1, value="%d-%02d" % (ANO, i + 1))
    for j, f in enumerate(FRENTES):
        b = 2 + j * 3
        res.cell(row=r, column=b,     value=soma("$A%d" % r, f, "Entrada"))
        res.cell(row=r, column=b + 1, value=soma("$A%d" % r, f, "Saída"))
        res.cell(row=r, column=b + 2, value="=%s%d-%s%d" % (get_column_letter(b), r, get_column_letter(b + 1), r))
    res.cell(row=r, column=11, value="=B%d+E%d+H%d" % (r, r, r))
    res.cell(row=r, column=12, value="=C%d+F%d+I%d" % (r, r, r))
    res.cell(row=r, column=13, value="=K%d-L%d" % (r, r))
    res.cell(row=r, column=14, value="=M5" if i == 0 else "=N%d+M%d" % (r - 1, r))
zebra(res, 5, 16, 14)
TOT = 17
res.cell(row=TOT, column=1, value="TOTAL %d" % ANO)
for col in range(2, 14):
    l = get_column_letter(col)
    res.cell(row=TOT, column=col, value="=SUM(%s5:%s16)" % (l, l))
res.cell(row=TOT, column=14, value="=N16")
for col in range(1, 15):
    c = res.cell(row=TOT, column=col)
    c.fill = PatternFill("solid", fgColor=DOURADO)
    c.font = Font(size=11, bold=True, color=VERDE)
    c.border = BORDA
for r in range(5, TOT + 1):
    for col in range(2, 15):
        res.cell(row=r, column=col).number_format = MOEDA_NEG
for col in (4, 7, 10, 13, 14):
    l = get_column_letter(col)
    rng = "%s5:%s%d" % (l, l, TOT)
    res.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["0"], font=Font(color=NEG, bold=True)))
    res.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0"], font=Font(color=POS, bold=True)))

# =====================================================================
# CARTÕES E DÍVIDAS
# =====================================================================
cd = wb.create_sheet("Cartões e Dívidas")
titulo(cd, "CARTÕES E DÍVIDAS  ·  quanto você deve e até quando",
       "Preencha as colunas claras. Fatura do mês, saldo devedor e data de quitação se calculam sozinhos.", 11)
secao(cd, 4, "CARTÕES", 11)
cabecalho(cd, 5, ["Cartão", "Bandeira", "Frente", "Limite", "Fecha dia", "Vence dia",
                  "Fatura do mês", "Limite usado", "Anuidade", "Ativo?", "Observação"],
          [20, 14, 15, 14, 11, 11, 15, 13, 13, 10, 32], freeze=False)
zebra(cd, 6, 13, 11)
HOJE = '">="&DATE(YEAR(TODAY()),MONTH(TODAY()),1),%s,"<"&DATE(YEAR(TODAY()),MONTH(TODAY())+1,1)' % DT
for r in range(6, 14):
    cd.cell(row=r, column=7, value='=IF($A%d="","",SUMIFS(%s,%s,$A%d,%s,%s,%s,"Saída"))'
            % (r, VL, CR, r, DT, HOJE, TP))
    cd.cell(row=r, column=8, value='=IF(N($D%d)=0,"",$G%d/$D%d)' % (r, r, r))
    for col in (4, 7, 9):
        cd.cell(row=r, column=col).number_format = MOEDA
    cd.cell(row=r, column=8).number_format = PCT
dv(R_FRENTE, cd, "C6:C13")
dvl(["Sim", "Não"], cd, "J6:J13")
cd.conditional_formatting.add("H6:H13",
    CellIsRule(operator="greaterThan", formula=["0.7"],
               fill=PatternFill("solid", bgColor="F8D7DA"), font=Font(color=NEG, bold=True)))

secao(cd, 15, "DÍVIDAS, PARCELAMENTOS E FINANCIAMENTOS", 11)
cabecalho(cd, 16, ["Descrição", "Credor", "Frente", "Valor total", "Parcela mensal",
                   "Parcelas pagas", "Total de parcelas", "Saldo devedor",
                   "1ª parcela", "Quitação prevista", "Status"],
          None, freeze=False)
zebra(cd, 17, 31, 11)
for r in range(17, 32):
    cd.cell(row=r, column=8, value='=IF($E%d="","",MAX(0,($G%d-$F%d)*$E%d))' % (r, r, r, r))
    cd.cell(row=r, column=10, value='=IF(OR($I%d="",$G%d=""),"",EDATE($I%d,$G%d-1))' % (r, r, r, r))
    for col in (4, 5, 8):
        cd.cell(row=r, column=col).number_format = MOEDA
    cd.cell(row=r, column=9).number_format = DATA
    cd.cell(row=r, column=10).number_format = DATA
dv(R_FRENTE, cd, "C17:C31")
dv(R_STATUS, cd, "K17:K31")
for r, rot, form, cor in ((33, "TOTAL QUE VOCÊ DEVE HOJE", "=SUM(H17:H31)", NEG),
                          (34, "COMPROMETIDO POR MÊS (parcelas ativas)", '=SUMIFS(E17:E31,K17:K31,"Ativo")', NEG)):
    cd.cell(row=r, column=1, value=rot).font = Font(size=12, bold=True, color=VERDE)
    c = cd.cell(row=r, column=8, value=form)
    c.number_format = MOEDA
    c.font = Font(size=13, bold=True, color=cor)
    c.fill = PatternFill("solid", fgColor=CREME)

# =====================================================================
# PATRIMÔNIO
# =====================================================================
pt = wb.create_sheet("Patrimônio")
titulo(pt, "PATRIMÔNIO  ·  o que é seu de verdade",
       "Ativos menos dívidas. Atualize os valores uma vez por mês e registre a linha do Snapshot.", 8)
secao(pt, 4, "O QUE VOCÊ TEM", 8)
cabecalho(pt, 5, ["Item", "Tipo", "Instituição", "Frente", "Valor atual",
                  "Rende?", "Rendimento a.a.", "Observação"],
          [30, 22, 22, 15, 16, 11, 16, 36], freeze=False)
zebra(pt, 6, 25, 8)
for r in range(6, 26):
    pt.cell(row=r, column=5).number_format = MOEDA
    pt.cell(row=r, column=7).number_format = PCT
dv(R_PATR, pt, "B6:B25")
dv(R_FRENTE, pt, "D6:D25")
dvl(["Sim", "Não"], pt, "F6:F25")
for r, rot, form, cor, tam in ((27, "TOTAL DE ATIVOS", "=SUM(E6:E25)", GRAFITE, 12),
                               (28, "TOTAL DE DÍVIDAS", "='Cartões e Dívidas'!H33", NEG, 12),
                               (29, "PATRIMÔNIO LÍQUIDO", "=E27-E28", POS, 15)):
    pt.cell(row=r, column=1, value=rot).font = Font(size=12 if tam == 12 else 14, bold=True, color=VERDE)
    c = pt.cell(row=r, column=5, value=form)
    c.number_format = MOEDA_NEG
    c.font = Font(size=tam, bold=True, color=cor)
    c.fill = PatternFill("solid", fgColor=CREME)

secao(pt, 31, "SNAPSHOT MENSAL  ·  registre no dia 1 de cada mês", 8)
cabecalho(pt, 32, ["Mês", "Ativos", "Dívidas", "Patrimônio líquido",
                   "Variação", "Variação %", "", "O que mudou"],
          None, freeze=False)
zebra(pt, 33, 56, 8)
for i, r in enumerate(range(33, 57)):
    pt.cell(row=r, column=4, value='=IF($B%d="","",$B%d-$C%d)' % (r, r, r))
    if i:
        pt.cell(row=r, column=5, value='=IF(OR($D%d="",$D%d=""),"",$D%d-$D%d)' % (r, r - 1, r, r - 1))
        pt.cell(row=r, column=6, value='=IF(N($D%d)=0,"",$E%d/ABS($D%d))' % (r - 1, r, r - 1))
    for col in (2, 3, 4, 5):
        pt.cell(row=r, column=col).number_format = MOEDA_NEG
    pt.cell(row=r, column=6).number_format = PCT
for rng in ("E33:E56", "F33:F56"):
    pt.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["0"], font=Font(color=NEG, bold=True)))
    pt.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0"], font=Font(color=POS, bold=True)))

# =====================================================================
# METAS
# =====================================================================
mt = wb.create_sheet("Metas")
titulo(mt, "METAS  ·  pra onde o dinheiro está indo de propósito",
       "Coloque o alvo e o prazo. A planilha te diz quanto precisa guardar por mês pra chegar lá.", 10)
cabecalho(mt, 4, ["Meta", "Frente", "Por que importa", "Valor alvo", "Já guardado",
                  "Falta", "% concluído", "Prazo", "Meses restantes", "Guardar por mês"],
          [30, 15, 36, 15, 15, 15, 13, 13, 15, 17])
zebra(mt, 5, 24, 10)
for r in range(5, 25):
    mt.cell(row=r, column=6, value='=IF($D%d="","",MAX(0,$D%d-$E%d))' % (r, r, r))
    mt.cell(row=r, column=7, value='=IF(N($D%d)=0,"",MIN(1,$E%d/$D%d))' % (r, r, r))
    mt.cell(row=r, column=9, value='=IF($H%d="","",MAX(0,DATEDIF(TODAY(),$H%d,"M")))' % (r, r))
    mt.cell(row=r, column=10, value='=IF(N($I%d)=0,"",$F%d/$I%d)' % (r, r, r))
    for col in (4, 5, 6, 10):
        mt.cell(row=r, column=col).number_format = MOEDA
    mt.cell(row=r, column=7).number_format = PCT
    mt.cell(row=r, column=8).number_format = DATA
dv(R_FRENTE, mt, "B5:B24")
mt.conditional_formatting.add("G5:G24", DataBarRule(start_type="num", start_value=0,
                                                    end_type="num", end_value=1, color=DOURADO))

# =====================================================================
# ASSINATURAS
# =====================================================================
asn = wb.create_sheet("Assinaturas")
titulo(asn, "ASSINATURAS  ·  o dinheiro que sai sozinho",
       "Tudo que debita sem você aprovar. A coluna 'Custo no ano' costuma doer — é pra doer mesmo.", 10)
cabecalho(asn, 4, ["Serviço", "Frente", "Pra que serve", "Valor cobrado", "Frequência",
                   "Dia da cobrança", "Custo no mês", "Custo no ano", "Cartão", "Ativa?"],
          [26, 15, 32, 15, 14, 15, 15, 15, 18, 11])
zebra(asn, 5, 34, 10)
for r in range(5, 35):
    asn.cell(row=r, column=7, value='=IF($D%d="","",$D%d/IFS($E%d="Mensal",1,$E%d="Trimestral",3,'
             '$E%d="Semestral",6,$E%d="Anual",12))' % (r, r, r, r, r, r))
    asn.cell(row=r, column=8, value='=IF($G%d="","",$G%d*12)' % (r, r))
    for col in (4, 7, 8):
        asn.cell(row=r, column=col).number_format = MOEDA
dv(R_FRENTE, asn, "B5:B34")
dv(R_FREQ, asn, "E5:E34")
dvl(["Sim", "Não"], asn, "J5:J34")
asn.cell(row=36, column=1, value="SANGRIA (só as assinaturas ativas)").font = Font(size=12, bold=True, color=VERDE)
for col, form in ((7, '=SUMIFS(G5:G34,J5:J34,"Sim")'), (8, '=SUMIFS(H5:H34,J5:J34,"Sim")')):
    c = asn.cell(row=36, column=col, value=form)
    c.number_format = MOEDA
    c.font = Font(size=13, bold=True, color=NEG)
    c.fill = PatternFill("solid", fgColor=CREME)

# =====================================================================
# ESTRATÉGIAS
# =====================================================================
est = wb.create_sheet("Estratégias")
titulo(est, "ESTRATÉGIAS  ·  fazer dinheiro e fazer o dinheiro render",
       "Cada linha é uma aposta. Payback diz em quantos meses ela se paga. Revise no dia 1 do mês.", 12)
cabecalho(est, 4, ["Estratégia", "Frente", "Tipo", "O que precisa acontecer",
                   "Investimento inicial", "Custo por mês", "Retorno esperado / mês",
                   "Lucro líquido / mês", "Payback (meses)", "Esforço", "Status", "Próxima ação"],
          [30, 15, 22, 38, 18, 15, 20, 18, 16, 12, 14, 36])
zebra(est, 5, 29, 12)
for r in range(5, 30):
    est.cell(row=r, column=8, value='=IF($G%d="","",$G%d-$F%d)' % (r, r, r))
    est.cell(row=r, column=9, value='=IF(N($H%d)<=0,"",$E%d/$H%d)' % (r, r, r))
    for col in (5, 6, 7, 8):
        est.cell(row=r, column=col).number_format = MOEDA_NEG
    est.cell(row=r, column=9).number_format = '0.0'
dv(R_FRENTE, est, "B5:B29")
dv(R_ESTR, est, "C5:C29")
dv(R_STATUS, est, "K5:K29")
dvl(["Baixo", "Médio", "Alto"], est, "J5:J29")
est.conditional_formatting.add("I5:I29",
    ColorScaleRule(start_type="num", start_value=0, start_color="C6EFCE",
                   mid_type="num", mid_value=12, mid_color="FFEB9C",
                   end_type="num", end_value=36, end_color="F8CBAD"))
est.conditional_formatting.add("H5:H29",
    CellIsRule(operator="lessThan", formula=["0"], font=Font(color=NEG, bold=True)))
for r, rot, form, cor in ((31, "RETORNO LÍQUIDO / MÊS  (só as estratégias ativas)", '=SUMIFS(H5:H29,K5:K29,"Ativo")', POS),
                          (32, "RETORNO LÍQUIDO / MÊS  (se tudo que está planejado rodar)", "=SUM(H5:H29)", DOURADO)):
    est.cell(row=r, column=1, value=rot).font = Font(size=12, bold=True, color=VERDE)
    c = est.cell(row=r, column=8, value=form)
    c.number_format = MOEDA
    c.font = Font(size=13, bold=True, color=cor)
    c.fill = PatternFill("solid", fgColor=CREME)

# =====================================================================
# INÍCIO
# =====================================================================
ini = wb.create_sheet("Início")
titulo(ini, "PAINEL FINANCEIRO  ·  Gê",
       "Tudo que você tem, deve, ganha e planeja — num lugar só. Se atualiza sozinho a partir dos Lançamentos.", 9)
for col, w in zip("ABCDEFGHI", [3, 21, 21, 3, 21, 21, 3, 21, 21]):
    ini.column_dimensions[col].width = w
ini.cell(row=4, column=2, value="Mês de referência").font = Font(size=10, bold=True, color=CINZA)
m = ini.cell(row=4, column=3, value='=TEXT(TODAY(),"YYYY-MM")')
m.font = Font(size=12, bold=True, color=VERDE)
m.fill = PatternFill("solid", fgColor=DOURADO)
m.alignment = Alignment(horizontal="center")
ini.merge_cells(start_row=4, start_column=5, end_row=4, end_column=9)
ini.cell(row=4, column=5, value="↑ troque essa célula pra ver outro mês (ex: 2026-03)").font = Font(size=9, italic=True, color=CINZA)

M = "$C$4"
CARDS = [
    ("ENTROU NO MÊS",        soma(M, None, "Entrada"), POS),
    ("SAIU NO MÊS",          soma(M, None, "Saída"), NEG),
    ("SALDO DO MÊS",         "=B7-E7", VERDE),
    ("PESSOAL · saldo",      "=%s-%s" % (soma(M, "Pessoal", "Entrada")[1:], soma(M, "Pessoal", "Saída")[1:]), VERDE),
    ("CLEAN TOUCH · saldo",  "=%s-%s" % (soma(M, "Clean Touch", "Entrada")[1:], soma(M, "Clean Touch", "Saída")[1:]), VERDE),
    ("INTERNET · saldo",     "=%s-%s" % (soma(M, "Internet", "Entrada")[1:], soma(M, "Internet", "Saída")[1:]), VERDE),
    ("PATRIMÔNIO LÍQUIDO",   "='Patrimônio'!E29", POS),
    ("VOCÊ DEVE HOJE",       "='Cartões e Dívidas'!H33", NEG),
    ("PARCELAS POR MÊS",     "='Cartões e Dívidas'!H34", NEG),
    ("ASSINATURAS / MÊS",    "=Assinaturas!G36", NEG),
    ("ASSINATURAS / ANO",    "=Assinaturas!H36", NEG),
    ("ESTRATÉGIAS ATIVAS",   "=Estratégias!H31", DOURADO),
]
pos = [(r, c) for r in (6, 10, 14, 18) for c in (2, 5, 8)]
for (rot, form, cor), (r, c) in zip(CARDS, pos):
    ini.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
    ini.merge_cells(start_row=r + 1, start_column=c, end_row=r + 1, end_column=c + 1)
    lb = ini.cell(row=r, column=c, value=rot)
    lb.font = Font(size=9, bold=True, color=CINZA)
    lb.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    vl = ini.cell(row=r + 1, column=c, value=form)
    vl.font = Font(size=18, bold=True, color=cor)
    vl.number_format = MOEDA_NEG
    vl.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ini.row_dimensions[r].height = 20
    ini.row_dimensions[r + 1].height = 36
    for rr in (r, r + 1):
        for cc in (c, c + 1):
            cel = ini.cell(row=rr, column=cc)
            cel.fill = PatternFill("solid", fgColor=CREME)
            cel.border = BORDA

secao(ini, 21, "COMO USAR  ·  leia uma vez, depois nunca mais", 9)
COMO = [
 "1.  Todo dia (2 min): abra a aba Lançamentos e registre o que entrou e o que saiu. Só isso.",
 "2.  Toda semana: olhe a coluna Status — o que está 'Pendente' e já venceu vira problema.",
 "3.  Dia 1 do mês: atualize os valores da aba Patrimônio e preencha uma linha do Snapshot.",
 "4.  Dia 1 do mês: revise Estratégias — o que avançou, o que morreu, qual é a próxima ação.",
 "5.  A cada 3 meses: abra Assinaturas e cancele o que não usou. Olhe a coluna 'Custo no ano'.",
 "",
 "As abas Início, Resumo Mensal, Cartões e Dívidas se calculam sozinhas — não digite nelas.",
 "As três frentes são Pessoal, Clean Touch e Internet. Sempre preencha a coluna Frente: é ela que separa tudo.",
]
for i, txt in enumerate(COMO):
    ini.merge_cells(start_row=22 + i, start_column=2, end_row=22 + i, end_column=9)
    c = ini.cell(row=22 + i, column=2, value=txt)
    c.font = Font(size=10, bold=i >= 6, color=VERDE if i >= 6 else GRAFITE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ini.row_dimensions[22 + i].height = 20

wb._sheets = [wb[n] for n in ["Início", "Lançamentos", "Resumo Mensal", "Cartões e Dívidas",
                              "Patrimônio", "Metas", "Assinaturas", "Estratégias", "Listas"]]
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = VERDE
wb["Listas"].sheet_properties.tabColor = CINZA
wb["Início"].sheet_properties.tabColor = DOURADO

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Painel-Financeiro-Ge.xlsx")
wb.save(OUT)
b = base64.b64encode(open(OUT, "rb").read()).decode()
open(os.path.join(HERE, "b64.txt"), "w").write(b)
print("xlsx bytes:", os.path.getsize(OUT), "| base64 chars:", len(b))
