# Responsavel: Paola

import json
import os
import random
from nlp.preprocessamento import preprocessar

TEMAS = {
    "musica": [
        "Amo música e vou a shows sempre que posso.",
        "Toco violão e adoro bandas de rock.",
        "Apaixonado por festivais de música.",
        "Ouço de tudo, mas sertanejo é minha paixão.",
        "Música eletrônica e baladas são meu mundo.",
    ],
    "esportes": [
        "Pratico futebol todo fim de semana.",
        "Adoro academia e corrida de rua.",
        "Sou apaixonado por esportes radicais.",
        "Natação e ciclismo fazem parte da minha rotina.",
        "Torço muito para o meu time de futebol.",
    ],
    "viagem": [
        "Viajo sempre que posso, adoro conhecer lugares novos.",
        "Já morei fora do país e amo culturas diferentes.",
        "Praias e montanhas são meus destinos favoritos.",
        "Mochilão pela América do Sul é meu sonho.",
        "Turismo gastronômico é minha forma favorita de viajar.",
    ],
    "gastronomia": [
        "Adoro cozinhar e experimentar receitas novas.",
        "Sou apaixonado por culinária italiana.",
        "Restaurantes e bares novos são meu programa favorito.",
        "Faço churrasco todo domingo com os amigos.",
        "Sou barista nas horas vagas e amo café especial.",
    ],
    "leitura": [
        "Leio pelo menos um livro por mês.",
        "Ficção científica e fantasia são meus gêneros favoritos.",
        "Adoro literatura brasileira e poesia.",
        "Frequento feiras de livros e livrarias antigas.",
        "Prefiro livros físicos a e-books.",
    ],
    "tecnologia": [
        "Trabalho com programação e amo tecnologia.",
        "Gamer nas horas vagas, principalmente RPG.",
        "Acompanho tendências de inteligência artificial.",
        "Construo PCs e adoro hardware.",
        "Desenvolvo aplicativos como hobbie.",
    ],
    "arte": [
        "Fotografo paisagens e retratos no tempo livre.",
        "Adoro museus e exposições de arte contemporânea.",
        "Pinto aquarelas como hobbie.",
        "Cinema independente é minha paixão.",
        "Faço esculturas em cerâmica nos fins de semana.",
    ],
    "natureza": [
        "Adoro trilhas e acampamentos na natureza.",
        "Tenho uma horta em casa e amo jardinagem.",
        "Sou apaixonado por astronomia e observação de estrelas.",
        "Mergulho e ecoturismo são meus hobbies.",
        "Cuido de animais e sou ativista ambiental.",
    ],
}

def gerar_bios_ficticias(quantidade=50, seed=42):
    random.seed(seed)
    temas = list(TEMAS.keys())
    bios = []

    for i in range(quantidade):
        temas_escolhidos = random.sample(temas, k=random.randint(2, 3))
        frases = [random.choice(TEMAS[t]) for t in temas_escolhidos]
        bio_texto = " ".join(frases)

        bios.append({
            "id": i + 1,
            "bio_original": bio_texto,
            "palavras": preprocessar(bio_texto)
        })

    return bios


def salvar_bios(bios, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(bios, f, ensure_ascii=False, indent=2)
    print(f"      Bios salvas em: {caminho}")



def carregar_bios(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        for perfil in dados:
            if "palavras" not in perfil or not perfil["palavras"]:
                perfil["palavras"] = preprocessar(perfil.get("bio_original", ""))
        return dados
    else:
        print("      bios.json nao encontrado, gerando bios ficticias pra teste...")
        bios = gerar_bios_ficticias(quantidade=50)
        salvar_bios(bios, caminho)
        return bios
