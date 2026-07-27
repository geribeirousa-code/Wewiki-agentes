#!/usr/bin/env python3
import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Define a paleta de cores oficial da Bowl Green
COLORS = {
    "verde": "#24573A",
    "coral": "#E8684A",
    "coral_ink": "#B14A2F",
    "coral_soft": "#F6D9D0",
    "dourado": "#C9A24B",
    "dourado_ink": "#8A6314",
    "dourado_soft": "#FFF3D6",
    "salvia": "#E4EBDD",
    "salvia_soft": "#EDF2E6",
    "creme": "#F2EFE4",
    "branco": "#ffffff",
    "navy": "#1C3527",
    "texto": "#1C3527",
    "texto2": "#24573A",
    "texto3": "#8A6314"
}

# Caminhos das fontes
fonts_dir = "c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/AGENTES/.agents/skills/carrossel-opiniao/fonts"
baloo_path = os.path.join(fonts_dir, "Baloo2-VariableFont.ttf")
nunito_path = os.path.join(fonts_dir, "Nunito-VariableFont.ttf")

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        print(f"Erro ao carregar fonte {path}. Usando fonte padrão.")
        return ImageFont.load_default()

# Carrega fontes com tamanhos diferentes
font_title_large = get_font(baloo_path, 72)
font_title_medium = get_font(baloo_path, 54)
font_title_small = get_font(baloo_path, 36)
font_body = get_font(nunito_path, 28)
font_body_bold = get_font(nunito_path, 30)
font_caption = get_font(nunito_path, 20)

def draw_mosaico(draw, y_offset, width):
    # Desenha a faixa de mosaico geométrico descrita no design system
    colors_mosaico = [COLORS["coral"], COLORS["salvia"], COLORS["navy"], COLORS["creme"], COLORS["dourado"]]
    block_width = width // len(colors_mosaico)
    for i, color in enumerate(colors_mosaico):
        draw.rectangle([i * block_width, y_offset, (i + 1) * block_width, y_offset + 30], fill=color)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        # Test line width
        line_str = " ".join(current_line)
        w = font.getbbox(line_str)[2]
        if w > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def create_slide_1(output_path):
    # Slide 1 (Capa) - Mitos x Verdades
    img = Image.new("RGB", (1080, 1350), COLORS["creme"])
    draw = ImageDraw.Draw(img)
    
    # Desenha faixas de mosaico no topo e no rodapé
    draw_mosaico(draw, 0, 1080)
    draw_mosaico(draw, 1320, 1080)
    
    # Desenha etiqueta superior
    draw.rectangle([440, 120, 640, 155], fill=COLORS["coral"])
    draw.text((540, 137), "MITO × VERDADE", font=font_caption, fill=COLORS["branco"], anchor="mm")
    
    # Título Principal
    title_1 = "SALADA NÃO"
    title_2 = "SUSTENTA?"
    draw.text((540, 320), title_1, font=font_title_large, fill=COLORS["verde"], anchor="mm")
    
    # Desenha risco coral sobre o "SUSTENTA" (como no design system)
    t2_w = font_title_large.getbbox(title_2)[2]
    draw.text((540, 420), title_2, font=font_title_large, fill=COLORS["verde"], anchor="mm")
    draw.line([540 - t2_w//2 - 10, 420, 540 + t2_w//2 + 10, 420], fill=COLORS["coral"], width=15)
    
    # Elemento Central (Emoji de salada grande)
    draw.ellipse([440, 550, 640, 750], fill=COLORS["salvia"])
    draw.text((540, 650), "🥗", font=get_font(nunito_path, 110), anchor="mm")
    
    # Descrição do Mito
    desc_lines = [
        "O maior mito de Xerém desmistificado em 1 minuto.",
        "Comida que vicia, mas sem culpa nenhuma. 💚"
    ]
    y_pos = 920
    for line in desc_lines:
        draw.text((540, y_pos), line, font=font_body, fill=COLORS["texto"], anchor="mm")
        y_pos += 45
        
    # Salva slide
    img.save(output_path)

def create_slide_2(output_path):
    # Slide 2 - A Base
    img = Image.new("RGB", (1080, 1350), COLORS["salvia_soft"])
    draw = ImageDraw.Draw(img)
    
    draw_mosaico(draw, 0, 1080)
    draw_mosaico(draw, 1320, 1080)
    
    # Etiqueta
    draw.rectangle([460, 120, 620, 155], fill=COLORS["verde"])
    draw.text((540, 137), "1. A BASE", font=font_caption, fill=COLORS["branco"], anchor="mm")
    
    # Título do slide
    draw.text((540, 300), "BOWL NÃO É SÓ ALFACE", font=font_title_medium, fill=COLORS["verde"], anchor="mm")
    
    # Ilustração de Arroz / Folhas
    draw.ellipse([440, 480, 640, 680], fill=COLORS["branco"])
    draw.text((540, 580), "🍙", font=get_font(nunito_path, 100), anchor="mm")
    
    # Corpo de texto
    text = "Nossos bowls não são apenas alface e tomate. Eles têm uma base firme de arroz shari japonês ou arroz integral.\n\nA base perfeita para te dar energia de verdade e sustentar a tarde inteira."
    lines = wrap_text(text, font_body, 800)
    
    y_pos = 850
    for line in lines:
        draw.text((540, y_pos), line, font=font_body, fill=COLORS["texto"], anchor="mm")
        y_pos += 42
        
    img.save(output_path)

def create_slide_3(output_path):
    # Slide 3 - Proteína (Fundo Navy para Contraste Premium)
    img = Image.new("RGB", (1080, 1350), COLORS["navy"])
    draw = ImageDraw.Draw(img)
    
    draw_mosaico(draw, 0, 1080)
    draw_mosaico(draw, 1320, 1080)
    
    # Estrelas douradas premium
    draw.text((540, 120), "✦ ✦ ✦ ✦ ✦", font=font_title_small, fill=COLORS["dourado"], anchor="mm")
    
    # Título do slide
    draw.text((540, 300), "2. PROTEÍNA GENEROSA", font=font_title_medium, fill=COLORS["dourado"], anchor="mm")
    
    # Círculo com Emoji de Peixe
    draw.ellipse([440, 480, 640, 680], fill=COLORS["salvia"])
    draw.text((540, 580), "🐟", font=get_font(nunito_path, 100), anchor="mm")
    
    # Corpo de texto
    text = "Salmão fresco, peixe branco ou frango grelhado.\n\nSão mais de 120g de proteína de verdade pesada na balança para segurar a sua fome por horas, sem dar aquele peso no estômago."
    lines = wrap_text(text, font_body, 800)
    
    y_pos = 820
    for line in lines:
        draw.text((540, y_pos), line, font=font_body, fill=COLORS["branco"], anchor="mm")
        y_pos += 42
        
    # Selo no rodapé
    draw.rectangle([340, 1150, 740, 1195], fill=COLORS["dourado"])
    draw.text((540, 1172), "DADO REAL PESADO NA BALANÇA ✦", font=font_caption, fill=COLORS["navy"], anchor="mm")
    
    img.save(output_path)

def create_slide_4(output_path):
    # Slide 4 - Toppings e Molho
    img = Image.new("RGB", (1080, 1350), COLORS["creme"])
    draw = ImageDraw.Draw(img)
    
    draw_mosaico(draw, 0, 1080)
    draw_mosaico(draw, 1320, 1080)
    
    # Etiqueta
    draw.rectangle([420, 120, 660, 155], fill=COLORS["coral"])
    draw.text((540, 137), "3. TOppings & molho", font=font_caption, fill=COLORS["branco"], anchor="mm")
    
    # Título
    draw.text((540, 300), "CROCÂNCIA DA CASA", font=font_title_medium, fill=COLORS["verde"], anchor="mm")
    
    # Círculo com Emoji de cebola crispy / molho
    draw.ellipse([440, 480, 640, 680], fill=COLORS["coral_soft"])
    draw.text((540, 580), "🥣", font=get_font(nunito_path, 100), anchor="mm")
    
    # Corpo de texto
    text = "E para finalizar, a crocância da nossa cebola crispy combinada com os molhos artesanais secretos feitos aqui todos os dias.\n\nÉ comida que vicia, mas sem culpa nenhuma. 💚"
    lines = wrap_text(text, font_body, 800)
    
    y_pos = 850
    for line in lines:
        draw.text((540, y_pos), line, font=font_body, fill=COLORS["texto"], anchor="mm")
        y_pos += 42
        
    img.save(output_path)

def create_slide_5(output_path):
    # Slide 5 - CTA Ticket
    img = Image.new("RGB", (1080, 1350), COLORS["salvia_soft"])
    draw = ImageDraw.Draw(img)
    
    draw_mosaico(draw, 0, 1080)
    draw_mosaico(draw, 1320, 1080)
    
    # Título
    draw.text((540, 250), "QUER PROVAR O ALMOÇO", font=font_title_medium, fill=COLORS["verde"], anchor="mm")
    draw.text((540, 320), "QUE XERÉM PEDIU?", font=font_title_medium, fill=COLORS["verde"], anchor="mm")
    
    # Desenha o Cupom / Ticket físico simulado (Scrapbook do design system)
    # Fundo do ticket
    draw.rectangle([280, 460, 800, 920], fill=COLORS["branco"], outline="#EDEADB", width=3)
    
    # Linha tracejada divisória
    for y in range(480, 900, 15):
        draw.line([660, y, 660, y + 8], fill=COLORS["texto3"], width=2)
        
    # Círculos de picote no topo e rodapé da linha tracejada
    draw.ellipse([648, 448, 672, 472], fill=COLORS["salvia_soft"])
    draw.ellipse([648, 908, 672, 932], fill=COLORS["salvia_soft"])
    
    # Conteúdo da esquerda (Cupom)
    draw.text((470, 520), "BOWL GREEN", font=font_title_small, fill=COLORS["verde"], anchor="mm")
    draw.text((470, 580), "VALE UM ALMOÇO GOSTOSO", font=font_caption, fill=COLORS["texto2"], anchor="mm")
    draw.text((470, 680), "BOWLOVER10", font=font_title_small, fill=COLORS["coral"], anchor="mm")
    draw.text((470, 740), "Use no WhatsApp ou Balcão", font=font_caption, fill=COLORS["texto3"], anchor="mm")
    
    # Conteúdo da direita (Destaque do cupom)
    # Vira o texto de lado escrevendo em uma imagem menor e colando rotacionada
    txt_img = Image.new("RGBA", (400, 100), (0,0,0,0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((200, 50), "10% OFF NO SEU BOWL ✦", font=font_caption, fill=COLORS["branco"], anchor="mm")
    rot_img = txt_img.rotate(270, expand=1)
    
    # Desenha o cupom coral
    draw.rectangle([680, 480, 780, 900], fill=COLORS["coral"])
    img.paste(rot_img, (670, 490), rot_img)
    
    # Instrução final
    draw.text((540, 1080), "Clique no link da bio e faça seu pedido", font=font_body_bold, fill=COLORS["verde"], anchor="mm")
    draw.text((540, 1130), "no WhatsApp dos bowlovers.", font=font_body, fill=COLORS["texto"], anchor="mm")
    
    img.save(output_path)

if __name__ == "__main__":
    output_dir = "c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/AGENTES/Entregas/2026-07-25-carrossel-bowlgreen-sustenta"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Gerando Slide 1...")
    create_slide_1(os.path.join(output_dir, "slide-01.png"))
    
    print("Gerando Slide 2...")
    create_slide_2(os.path.join(output_dir, "slide-02.png"))
    
    print("Gerando Slide 3...")
    create_slide_3(os.path.join(output_dir, "slide-03.png"))
    
    print("Gerando Slide 4...")
    create_slide_4(os.path.join(output_dir, "slide-04.png"))
    
    print("Gerando Slide 5...")
    create_slide_5(os.path.join(output_dir, "slide-05.png"))
    
    print("Carrossel gerado com sucesso no design system oficial da Bowl Green!")
