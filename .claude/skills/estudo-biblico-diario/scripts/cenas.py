"""Catálogo das páginas de pausa em QUADRINHO: Jesus e a mulher de hoje, com humor leve e carinho.

Decisão da Gê (2026-10-14): estilo Pixar (3D animado, olhos grandes, luz quente) misturado ao traço
suave da ilustração de gratidão que ela mostrou, com sátiras no contexto feminino (mãe, trabalha fora,
empresária, sozinha, culpada). O texto dos balões NÃO fica na imagem (IA erra português): o planner
escreve os balões por cima. Por isso toda imagem deve deixar o terço de cima limpo, a mulher à esquerda
e Jesus à direita.

Regras de tom: o humor é ENTRE Jesus e ela, nunca contra Jesus nem contra a Bíblia. Jesus é manso,
bem-humorado e paciente; a graça vem da vida real da mulher. Cada cena aponta um texto bíblico.

bolhas: lista de (quem, texto) em ordem; quem = "ela" (balão à esquerda) ou "jesus" (balão à direita).
"""

PERSONAGENS = (
    "Pixar-style 3D animated movie character illustration, warm cinematic golden lighting, big expressive brown eyes, soft painterly background. "
    "THE WOMAN (same character in every scene): Brazilian woman in her early 30s, tan skin, big brown eyes, dark brown hair in a messy bun, beige knit cardigan over a cream t-shirt, small gold necklace. "
    "JESUS (same character in every scene): kind smiling eyes, shoulder-length wavy brown hair, short beard, cream linen tunic with a rust-red sash across one shoulder, brown sandals, very soft golden halo, gentle humorous expression. "
    "Composition: the woman on the LEFT, Jesus on the RIGHT, the top third of the image is plain soft cream wall or sky with nothing on it (reserved for speech bubbles). No text, no letters, no watermark."
)

CENAS = {
    "banheiro": dict(
        ref="Mateus 6:6", legenda="A mãe só consegue orar trancada no banheiro…",
        bolhas=[("ela", "Senhor, só 5 minutinhos de silêncio!"), ("jesus", "Pode falar. Eu espero. Eu não tenho pressa.")],
        texto="Jesus disse que, para orar, a gente pode entrar no quarto e fechar a porta. Para muita mãe, o “quarto” é o banheiro. Ele não se incomoda: onde houver uma porta fechada e um coração aberto, ele está.",
        oracao="“Senhor, até aqui, no meio da bagunça, eu falo contigo.”",
        cena="inside a small home bathroom with the door closed, she stands with eyes shut and hands clasped in prayer, a laundry basket and a rubber duck nearby, toys on the floor; Jesus leans casually against the sink with arms crossed, smiling patiently."),
    "agenda": dict(
        ref="Lucas 10:41–42", legenda="Oração: entre “tirar o lixo” e “pagar o boleto”.",
        bolhas=[("ela", "Eu vou te encaixar na agenda, **prometo**!"), ("jesus", "Eu não quero ser um item da lista. Eu quero **você**.")],
        texto="Marta estava ocupada com muitas coisas e Jesus a chamou pelo nome, com carinho: uma só coisa é necessária. Ele não quer ser mais uma tarefa riscada. Quer a sua companhia.",
        oracao="“Senhor, ensina-me a parar um minuto sem culpa.”",
        cena="she holds a huge overflowing planner full of colorful sticky notes, a phone and a coffee, looking frazzled; Jesus holds up a tiny sticky note that says nothing (blank), smiling warmly at her."),
    "presenca": dict(
        ref="Romanos 8:1", legenda="A culpa de não ter orado “como deveria”.",
        bolhas=[("ela", "Faz três dias que eu não leio a Bíblia… de novo."), ("jesus", "Eu não tenho **lista de presença**, filha.")],
        texto="Para quem está em Cristo, diz a Bíblia, não há condenação. Ele não cobra caderneta de presença. Cada vez que você volta, ele já está esperando, sem sermão.",
        oracao="“Senhor, eu volto. Obrigada por não me cobrar.”",
        cena="she sits on the sofa late at night hugging a pillow, looking guilty, with a closed Bible on the table; Jesus sits beside her holding a blank attendance clipboard upside down and smiling gently."),
    "controle": dict(
        ref="1 Pedro 5:7", legenda="Eu dou conta de tudo sozinha!",
        bolhas=[("ela", "Eu dou conta de **tudo** sozinha! (as pernas tremendo)"), ("jesus", "Posso segurar alguma coisa pra você?")],
        texto="Pedro escreveu: lancem sobre ele toda a ansiedade, porque ele cuida de vocês. Segurar tudo sozinha não prova que você é forte. Entregar é que é.",
        oracao="“Senhor, pega esta parte. Eu estou cansada.”",
        cena="she is balancing an absurd tower of things in her arms (laundry basket, laptop, a pot, a child's backpack, a calendar), her knees trembling but forcing a big smile; Jesus offers his open hands to take something, smiling."),
    "descanso": dict(
        ref="Salmo 127:2", legenda="Empresária pedindo bênção… às 2 da manhã.",
        bolhas=[("ela", "Senhor, abençoa o meu negócio!"), ("jesus", "Posso abençoar o seu sono também?")],
        texto="O Salmo 127 diz que não adianta madrugar e trabalhar sem parar: Deus dá o sono a quem ele ama. Descansar também é confiar que ele cuida do que você não alcança.",
        oracao="“Senhor, hoje eu durmo. Tu cuidas do resto.”",
        cena="she works at a laptop at a home desk at night, surrounded by papers, empty coffee cups and a glowing screen, dark circles under her eyes; Jesus stands beside her holding a fluffy pillow and a blanket, smiling kindly."),
    "bagunca": dict(
        ref="Lucas 10:38–42", legenda="A casa tá uma bagunça. E ele veio assim mesmo.",
        bolhas=[("ela", "Desculpa a bagunça, eu não esperava visita!"), ("jesus", "Eu não vim pela casa. Eu vim por você.")],
        texto="Jesus foi à casa de Marta e Maria. A Bíblia não conta que ele reparou na louça: conta que ele quis conversar. Você não precisa da casa pronta para receber o Senhor.",
        oracao="“Senhor, entra. Do jeito que está.”",
        cena="a messy living room with toys, laundry and dishes everywhere, she stands embarrassed at the door with messy hair, Jesus has just entered, sitting happily on the cluttered sofa moving a toy aside, smiling."),
    "comparacao": dict(
        ref="Salmo 139:14", legenda="Comparando os seus bastidores com o palco dos outros.",
        bolhas=[("ela", "Todo mundo parece dar conta, menos eu."), ("jesus", "Você está vendo o palco. Eu vejo os bastidores de todo mundo.")],
        texto="O salmista louva a Deus porque foi feito de modo especial e admirável. Ninguém tem a vida perfeita que aparece no feed. Você não precisa competir; precisa ser a que ele fez.",
        oracao="“Senhor, tira de mim a pressa de me comparar.”",
        cena="she scrolls on her phone with a sad face, the phone screen glowing with tiny perfect pictures (no readable text), sitting on a couch; Jesus sits behind her over the couch shoulder looking at the phone with a gentle smile and a raised eyebrow."),
    "cozinha": dict(
        ref="1 Tessalonicenses 5:17", legenda="Dá para orar cortando cenoura.",
        bolhas=[("ela", "Eu não tenho tempo de orar direito…"), ("jesus", "Pode orar assim mesmo. Eu escuto até o barulho da faca.")],
        texto="Paulo pediu que orássemos sem cessar. Isso não é ficar parada de olhos fechados: é conversar com Deus enquanto se vive. Cozinhar, dirigir e dobrar roupa também podem virar oração.",
        oracao="“Senhor, esta cozinha é o meu altar de hoje.”",
        cena="a warm home kitchen, she chops carrots with an apron and a headscarf, smiling; Jesus stands beside her wearing a small apron over his tunic, holding a wooden spoon and tasting the soup, smiling."),
    "gratidao": dict(
        ref="Salmo 136:1", legenda="Até aqui, obrigada.",
        bolhas=[("ela", "Até aqui, e por tudo o que há de vir, obrigada, Jesus.")],
        texto="O Salmo 136 repete uma frase em todos os versos: o amor dele dura para sempre. Antes de qualquer pedido, um minuto de “obrigada” muda o jeito de olhar o dia.",
        oracao="“Obrigada, Senhor. Até aqui e por tudo o que vem.”",
        cena="calm and serene, she sits cross-legged on a sunny harbor quay at golden hour, eyes closed, smiling peacefully, oversized cream sweater and mustard pants, sneakers; Jesus is a soft gentle presence sitting a little behind her, smiling kindly. Soft anime-like painted sky and sea with distant city (this one is the quiet gratitude scene)."),
}


def prompt(chave):
    return f"{PERSONAGENS} SCENE: {CENAS[chave]['cena']}"
