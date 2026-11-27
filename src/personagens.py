from pathlib import Path
from random import shuffle

import pygame


# Os caminhos partem de assets/imagens/personagens.
#
# foto:
# - caminho de um PNG: utiliza uma fotografia específica;
# - "humano": utiliza a imagem humana preparada como fotografia;
# - None: o personagem não apresenta fotografia.
ARQUIVOS = {
    "lucas": {
        "nome": "Lucas",
        "humano": "Lucas/Lucas_transparente.png",
        "ia": "Lucas/lucas_ia_transparente.png",
        "foto": "Lucas/lucas_documento.png",
    },
    "gael": {
        "nome": "Gael",
        "humano": "Gael/gael_transparente.png",
        "ia": "Gael/gael_ia_transparente.png",
        "foto": None,
    },
    "estefanny": {
        "nome": "Estefanny",
        "humano": "estefanny/estefanny_transparente.png",
        "ia": "estefanny/estefanny_ia_transparente.png",
        "foto": "humano",
    },
    "nayra": {
        "nome": "Nayra",
        "humano": "Nayra/nayra_transparente.png",
        "ia": "Nayra/nayra_ia_transparente.png",
        "foto": "Nayra/nayra_documento.png",
    },
    "amanda": {
        "nome": "Amanda",
        "humano": "Amanda/amanda_transparente.png",
        "ia": "Amanda/amanda_ia_transparente.png",
        "foto": "humano",
    },
    "nero": {
        "nome": "Nero",
        "humano": "Nero/nero_transparente.png",
        "ia": "Nero/nero_ia_transparente.png",
        "foto": "humano",
    },
    "sarah": {
        "nome": "Sarah",
        "humano": "Sarah/sarah_transparente.png",
        "ia": "Sarah/sarah_ia_transparente.png",
        "foto": "Sarah/sarah_documento.png",
    },
    "matheus": {
        "nome": "Matheus",
        "humano": "Matheus/matheus_transparente.png",
        "ia": "Matheus/matheus_ia_transparente.png",
        "foto": "humano",
    },
    "lia": {
        "nome": "Lia",
        "humano": "Lia/lia_transparente.png",
        "ia": "Lia/lia_ia_transparente.png",
        "foto": "humano",
    },
    "otavio": {
        "nome": "Otávio",
        "humano": "Otavio/otavio_transparente.png",
        "ia": "Otavio/otavio_ia_transparente.png",
        "foto": "humano",
    },
}


def carregar_par(pasta, caminho_humano, caminho_ia, altura=280):
    """Prepara as duas formas de um personagem com o mesmo tamanho."""
    humano = pygame.image.load(
        pasta / caminho_humano
    ).convert_alpha()

    ia = pygame.image.load(
        pasta / caminho_ia
    ).convert_alpha()

    # Remove as margens transparentes antes do redimensionamento.
    humano = humano.subsurface(
        humano.get_bounding_rect(min_alpha=128)
    ).copy()

    ia = ia.subsurface(
        ia.get_bounding_rect(min_alpha=128)
    ).copy()

    # Calcula a largura mantendo a proporção da imagem humana.
    largura = round(
        humano.get_width() * altura / humano.get_height()
    )
    tamanho = (largura, altura)

    # As duas formas usam o mesmo tamanho durante a revelação.
    return {
        "humano": pygame.transform.scale(humano, tamanho),
        "ia": pygame.transform.scale(ia, tamanho),
    }


def preparar_foto(imagem):
    """Ajusta a fotografia aos limites da identificação."""
    recorte = imagem.subsurface(
        imagem.get_bounding_rect()
    ).copy()

    # Escolhe uma escala que respeita largura e altura disponíveis.
    escala = min(
        90 / recorte.get_width(),
        106 / recorte.get_height(),
    )

    tamanho = (
        max(1, round(recorte.get_width() * escala)),
        max(1, round(recorte.get_height() * escala)),
    )

    return pygame.transform.scale(recorte, tamanho)


def carregar_personagens():
    """Carrega todos os personagens e fotos após criar a janela."""
    pasta = (
        Path(__file__).resolve().parent.parent
        / "assets" / "imagens" / "personagens"
    )

    personagens = {}

    # Percorre o catálogo para preparar cada personagem.
    for identificador, dados in ARQUIVOS.items():
        imagens = carregar_par(
            pasta,
            dados["humano"],
            dados["ia"],
        )

        if dados["foto"] is None:
            foto = None

        elif dados["foto"] == "humano":
            foto = preparar_foto(imagens["humano"])

        else:
            original = pygame.image.load(
                pasta / dados["foto"]
            ).convert_alpha()

            foto = preparar_foto(original)

        # As mesmas chaves são utilizadas por jogo.py.
        personagens[identificador] = {
            "nome": dados["nome"],
            "imagens": imagens,
            "foto": foto,
        }

    return personagens


def criar_fila_personagens(personagens):
    """Cria uma fila aleatória sem alterar o banco de personagens."""
    fila = list(personagens)

    # Embaralha os identificadores uma vez por partida.
    shuffle(fila)

    return fila