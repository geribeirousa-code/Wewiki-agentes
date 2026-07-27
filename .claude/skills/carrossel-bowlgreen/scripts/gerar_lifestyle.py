#!/usr/bin/env python3
"""
Fotos de pessoas reais — Bowl Green.

O feed estava só com prato em fundo branco. Isso gera a outra metade: gente
comendo, mão segurando, mesa com amigo, suco na mão. Sai em Fotos/geradas/.

Usa /v1/images/edits com a foto REAL do prato como referência — a embalagem
de papel com estampa tropical é ativo de marca, não pode virar outra tigela.

Uso:
    python gerar_lifestyle.py            # todas as cenas pendentes
    python gerar_lifestyle.py mesa-dupla # uma cena
"""

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

RAIZ_MARCA = Path(r"c:/Users/gerib/OneDrive/Desktop/GE NEGOCIOS/BOWL GREEN")
SAIDA = RAIZ_MARCA / "Fotos" / "geradas"
PRATOS = RAIZ_MARCA / "Fotos" / "pratos"

# PÚBLICO A e B. NUNCA C. Ticket médio de R$ 50 — quem aparece na peça precisa
# ser alguém que paga isso num almoço sem pensar.
#
# Duas rodadas foram recusadas antes desta. A primeira dizia "gente simples do
# subúrbio, roupa do dia a dia" → "ficou com cara de pobre". A segunda acertou o
# padrão social mas errou o elenco: virou editorial de carro importado e cashmere,
# e o negócio é um restaurante de bairro. O elenco certo é o profissional do
# bairro QUE TEM DINHEIRO — quem sai da academia, secretária, dona de salão, dona
# de estabelecimento, médico de clínica, gente de loja.
#
# "Não pode fazer a galera pobre e ferrada, feia." Casting bonito e bem cuidado
# é requisito da peça, não detalhe: pele boa, cabelo tratado, corpo cuidado,
# sorriso bonito, roupa impecável dentro do papel de cada um.
BASE = (
    "Fotografia publicitária de alto padrão, qualidade de campanha de marca, "
    "luz natural suave e direcional, tom quente e limpo, profundidade de campo "
    "rasa com fundo desfocado, textura sutil de filme, cor rica e saturada na medida. "
    "Modelo brasileiro entre 26 e 42 anos, muito bonito e fotogênico, traços "
    "harmoniosos, pele saudável e bem cuidada, cabelo tratado com corte atual, "
    "corpo em forma, sorriso bonito e natural, unhas feitas. Aparência de classe "
    "A ou B — alguém que paga R$ 50 num almoço sem pensar duas vezes. "
    "Roupa impecável e bem passada, tecido de qualidade, caimento certo. "
    "Ambiente moderno, claro e bem cuidado, com acabamento de bom gosto. "
    "Nada de cenário pobre, bagunçado ou malcuidado. Nada de plástico barato. "
    "Nada com cara de banco de imagens genérico. "
    # Reproduzir a embalagem é o ponto mais frágil da geração. Quando a instrução
    # era só "como na referência", saiu bowl de papel kraft marrom com a logo
    # redesenhada. Descrever o objeto explicitamente é o que segura.
    "REGRA ABSOLUTA DA EMBALAGEM: copie o bowl da imagem de referência pixel a "
    "pixel. É um bowl de papel BRANCO ou creme muito claro, com estampa de "
    "folhagem tropical desenhada em traço fino verde-claro, e a marca BOWL GREEN "
    "impressa em verde escuro, com a palavra BOWL grande e GREEN menor embaixo. "
    "NÃO use papel kraft marrom. NÃO redesenhe nem reposicione a logo. "
    "NÃO troque a fonte da marca. NÃO mude a estampa. "
    "O conteúdo do bowl também deve ser o mesmo da referência — os mesmos "
    "ingredientes, nas mesmas posições. Não invente ingrediente novo. "
    "Nenhum outro texto, nenhuma marca d'água, nenhum logotipo inventado. "
)

# O elenco que a Gê pediu, um prato diferente em cada cena. Ela apontou nas duas
# rodadas anteriores que era sempre o mesmo poke.
#
# ENQUADRAMENTO NUNCA SE REPETE. A primeira leva deste elenco saiu com as três
# pessoas na mesma pose — de frente, sorrindo para a câmera, bowl erguido com as
# duas mãos. Vira catálogo. Cada cena aqui declara ângulo e ação próprios, e a
# maioria não olha para a câmera.
CENAS = {
    "academia-mulher": {
        "ref": ["SUN SALMÃO"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Mulher muito bonita e em ótima forma saindo pela porta de vidro de uma "
            "academia moderna, conjunto de treino preto de tecido nobre, cabelo "
            "preso, bolsa esportiva no ombro. Ela caminha em direção à rua com o "
            "bowl fechado numa das mãos, olhando para frente, no meio do passo. "
            "Perfil de três quartos, corpo inteiro cortado no joelho, câmera na "
            "altura do peito. Ela NÃO olha para a câmera. Fim de tarde."
        ),
    },
    "academia-homem": {
        "ref": ["GUACAFITGRILL"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Homem bonito e atlético em camiseta dry-fit cinza, sentado num banco "
            "de madeira da área de convivência de uma academia premium depois do "
            "treino. Câmera baixa, olhando levemente para cima. Ele está no meio de "
            "uma garfada, com o bowl apoiado na coxa e os olhos na comida, toalha "
            "no ombro. Corte na altura da cintura. NÃO olha para a câmera."
        ),
    },
    "secretaria": {
        "ref": ["POKE YUKI"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Secretária executiva elegante e bonita atrás do balcão de recepção de "
            "uma empresa de bom padrão, blazer bem cortado e blusa de seda. Vista "
            "de lado, por cima do ombro dela: o bowl aberto sobre o balcão em "
            "primeiro plano nítido, a mão pegando um pedaço com o hashi, o rosto "
            "dela desfocado ao fundo em foco suave. Arranjo de flores e monitor "
            "atrás. Luz de escritório clara."
        ),
    },
    "salao": {
        "ref": ["POKE PHILADELFIA"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Dona de um salão de beleza sofisticado, mulher bonita de uns 35 anos, "
            "cabelo perfeito, avental preto elegante sobre roupa clara. Ela está "
            "encostada na bancada de mármore do salão, rindo de algo que alguém "
            "fora do quadro disse, com o bowl apoiado na bancada e o garfo na mão. "
            "Enquadramento horizontal amplo, ela deslocada para a direita do quadro. "
            "Espelhos de moldura dourada e cadeiras de couro desfocados."
        ),
    },
    "clinica": {
        "ref": ["POKE FRUTOS DO MAR"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Vista de cima, direto para baixo, sobre a mesa de um consultório "
            "médico moderno de madeira clara. O bowl aberto no centro do quadro, "
            "nítido. Ao redor: as mangas do jaleco branco e as mãos de uma médica "
            "segurando o hashi, estetoscópio pousado na mesa, caneta, prontuário "
            "e um copo de água. SEM rosto no quadro. Luz de janela grande."
        ),
    },
    "loja": {
        "ref": ["WRAP DE CAMARAO"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Dona de uma loja de roupas de bom padrão, mulher bonita e muito bem "
            "vestida, de pé no meio das araras comendo o wrap na hora do almoço, "
            "apoiada de leve numa arara. Corpo inteiro cortado na canela, câmera "
            "afastada, ela olhando para o lado, descontraída. Iluminação quente de "
            "loja, espelho grande e balcão desfocados atrás."
        ),
    },
    "balcao": {
        "ref": ["POKE SORA"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Casal jovem e bonito almoçando no balcão alto de um restaurante de "
            "bowls moderno, banquetas de madeira, azulejo verde e plantas. Vista "
            "lateral, os dois de perfil lado a lado, cada um com seu bowl aberto "
            "no balcão, conversando no meio da refeição. Ninguém olha para a "
            "câmera. Luz quente de fim de tarde entrando pela vitrine, contraluz."
        ),
    },
    "hashi-drizzle": {
        "ref": ["POKE TROPICAL"],
        "size": "1024x1536",
        "prompt": BASE + (
            "Macro editorial: um par de hashis de madeira clara ergue um cubo de "
            "salmão acima do bowl, com um fio fino de molho escorrendo e uma gota "
            "suspensa no ar, congelada. Foco rasíssimo no cubo, o bowl abaixo em "
            "desfoque cremoso. Superfície de pedra clara, copo de suco desfocado no "
            "canto. Sem pessoas no quadro além da mão, de manicure impecável."
        ),
    },
}


def ref(nome):
    for p in PRATOS.iterdir():
        if p.stem.lower() == nome.strip().lower():
            return p
    raise SystemExit(f"ERRO: referência '{nome}' não achada em {PRATOS}")


def env_openai():
    for linha in (RAIZ_MARCA / ".env").read_text(encoding="utf-8").splitlines():
        if linha.startswith("OPENAI_API_KEY="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit("ERRO: OPENAI_API_KEY não está no .env da marca")


def multipart(campos, arquivos):
    """multipart/form-data na mão — o endpoint /edits não aceita JSON."""
    limite = "----bowlgreen" + base64.b16encode(os.urandom(8)).decode()
    corpo = b""
    for k, v in campos:
        corpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, caminho in arquivos:
        corpo += (f"--{limite}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                  f"filename=\"{caminho.name}\"\r\nContent-Type: image/png\r\n\r\n").encode()
        corpo += caminho.read_bytes() + b"\r\n"
    corpo += f"--{limite}--\r\n".encode()
    return corpo, f"multipart/form-data; boundary={limite}"


def gerar(slug, cena, chave):
    destino = SAIDA / f"{slug}.png"
    campos = [("model", "gpt-image-1"), ("prompt", cena["prompt"]),
              ("size", cena["size"]), ("quality", "high"), ("n", "1")]
    arquivos = [("image[]", ref(n)) for n in cena["ref"]]
    corpo, tipo = multipart(campos, arquivos)

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits", data=corpo,
        headers={"Authorization": f"Bearer {chave}", "Content-Type": tipo})
    with urllib.request.urlopen(req, timeout=600) as r:
        dados = json.loads(r.read())

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(base64.b64decode(dados["data"][0]["b64_json"]))
    print(f"OK  {destino.name}")


if __name__ == "__main__":
    chave = env_openai()
    alvos = sys.argv[1:] or list(CENAS)
    for slug in alvos:
        if slug not in CENAS:
            raise SystemExit(f"ERRO: cena '{slug}' não existe. Tem: {', '.join(CENAS)}")
        try:
            gerar(slug, CENAS[slug], chave)
        except Exception as e:
            print(f"FALHOU  {slug}: {e}")
