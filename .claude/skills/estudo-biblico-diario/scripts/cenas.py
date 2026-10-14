"""Catálogo das páginas de pausa: Jesus e a mulher ocupada, cansada ou culpada.

As pinturas NÃO são desenhadas por código (o vetor ficou feio e foi descartado pela Gê). Elas
são geradas por IA no estilo ilustração fofa desenhada à mão e salvas em
`Bíblia/planner/imagens/<chave>.jpg|png`. Este arquivo guarda só os textos de cada cena.
Os `canva` são os ids das mídias geradas no Canva da Gê (alta resolução fica lá).
"""

CENAS = {
    "banco": dict(frase="Senta aqui um pouquinho.", ref="Mateus 11:28–30", canva="MAHX81jYVzk",
                  titulo="Ele guardou um lugar para você",
                  texto="Jesus disse a quem estava cansado e sobrecarregado: venham a mim, e eu darei descanso. Ele não pede que você termine a lista antes. Hoje o convite é só este: sentar um pouquinho ao lado dele, do jeito que você chegou.",
                  oracao="“Senhor, hoje eu me sento. Do jeito que estou.”"),
    "carrega": dict(frase="Eu te carrego.", ref="Isaías 46:4", canva="MAHX87PE6I0",
                    titulo="Há dias em que você não precisa andar sozinha",
                    texto="Deus prometeu carregar o seu povo, não só guiar de longe. Há dias em que você não consegue mais andar sozinha. Descansar nos braços dele não é fraqueza nem preguiça: é exatamente o que ele ofereceu.",
                    oracao="“Senhor, hoje eu deixo que Tu me carregues.”"),
    "porta": dict(frase="Eu bato bem baixinho.", ref="Apocalipse 3:20", canva="MAHX8-eEREQ",
                  titulo="Ele bate com delicadeza",
                  texto="Jesus não arromba a porta: ele bate e espera. Você não precisa arrumar a casa antes de abrir. Pode abrir um pouquinho, no meio da bagunça e da correria mesmo.",
                  oracao="“Senhor, a porta está aberta. Entra.”"),
    "marta": dict(frase="Marta, Marta…", ref="Lucas 10:38–42", canva="MAHX89PMCck",
                  titulo="Ele a chamou pelo nome",
                  texto="Marta recebeu Jesus em casa e ficou ocupada com muitas coisas. Ele não a repreendeu por servir: chamou-a pelo nome, duas vezes, com carinho, e disse que uma só coisa é necessária. Se você vive correndo, este convite também é para você.",
                  oracao="“Senhor, ensina-me a parar um minuto sem culpa.”"),
    "buque": dict(frase="Eu guardei o buquê pra você.", ref="Lucas 12:27", canva="MAHX8-ehJi8",
                  titulo="Ele guarda o buquê inteiro",
                  texto="Jesus disse para olharmos os lírios do campo: ninguém os força a crescer. Há dias em que você colhe uma florzinha de cada vez, cansada, enquanto Ele já guarda o buquê inteiro para você.",
                  oracao="“Senhor, eu aceito o que Tu preparaste.”"),
}
