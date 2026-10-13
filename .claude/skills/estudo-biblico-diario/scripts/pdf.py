"""HTML → PDF (Carta) com o Chromium, se o Playwright estiver instalado.

Sem Playwright nada quebra: o HTML já imprime direto (Ctrl+P → Salvar como PDF,
papel Carta, margens "Nenhuma", ligar "Gráficos de plano de fundo").
"""
import os
from pathlib import Path


def exportar_pdf(html, pdf, largura="8.5in", altura="11in"):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (PDF não gerado: Playwright não instalado. Abra o HTML e use Ctrl+P → Salvar como PDF.)")
        return False
    with sync_playwright() as p:
        kw = {}
        exe = os.environ.get("CHROMIUM_PATH")
        if exe:
            kw["executable_path"] = exe
        try:
            nav = p.chromium.launch(**kw)
        except Exception as e:  # navegador não encontrado
            print(f"  (PDF não gerado: {str(e).splitlines()[0]})")
            return False
        pg = nav.new_page()
        pg.goto(Path(html).resolve().as_uri())
        pg.wait_for_timeout(300)
        pg.pdf(path=str(pdf), width=largura, height=altura, print_background=True,
               margin=dict(top="0", right="0", bottom="0", left="0"), prefer_css_page_size=True)
        nav.close()
    return True
