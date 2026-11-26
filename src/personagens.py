from pathlib import Path

import pygame


def carregar_par(pasta, caminho_humano, caminho_ia, altura=280):
    """Carrega as duas formas de um personagem com o mesmo tamanho."""
    humano = pygame.image.load(
        pasta / caminho_humano
    ).convert_alpha()

    ia = pygame.image.load(
        pasta / caminho_ia
    ).convert_alpha()

    # Remove margens transparentes e pixels quase invisíveis.
    # Assim, o busto alcança o peitoril após o redimensionamento.
    humano = humano.subsurface(
        humano.get_bounding_rect(min_alpha=128)
    ).copy()

    ia = ia.subsurface(
        ia.get_bounding_rect(min_alpha=128)
    ).copy()

    # Mantém a proporção da imagem humana.
    largura = round(
        humano.get_width() * altura / humano.get_height()
    )
    tamanho = (largura, altura)

    # A revelação não altera o tamanho do retângulo.
    return {
        "humano": pygame.transform.scale(humano, tamanho),
        "ia": pygame.transform.scale(ia, tamanho),
    }


def preparar_foto(imagem):
    """Ajusta uma imagem humana ao espaço disponível no documento."""

    # Desconsidera as margens transparentes.
    recorte = imagem.subsurface(
        imagem.get_bounding_rect()
    ).copy()

    # A foto precisa caber tanto na largura quanto na altura.
    escala = min(
        90 / recorte.get_width(),
        106 / recorte.get_height(),
    )

    tamanho = (
        max(1, round(recorte.get_width() * escala)),
        max(1, round(recorte.get_height() * escala)),
    )

    return pygame.transform.scale(recorte, tamanho)


def carregar_personagens(imagens_lucas, foto_lucas):
    """Carrega os personagens uma única vez, depois de criar a janela."""
    pasta = (
        Path(__file__).resolve().parent.parent
        / "assets" / "imagens" / "personagens"
    )

    imagens_gael = carregar_par(
        pasta,
        "Gael/gael_transparente.png",
        "Gael IA/gael_ia_transparente.png",
    )

    imagens_estefanny = carregar_par(
        pasta,
        "estefanny/estefanny_transparente.png",
        "estefanny/estefanny_ia_transparente.png",
    )

    # Carrega as duas formas com o mesmo tamanho.
    imagens_nayra = carregar_par(
        pasta,
        "Nayra/nayra_transparente.png",
        "Nayra/nayra_ia_transparente.png",
    )

    # Foto antiga com cabelo preto e franja, conforme o roteiro.
    foto_nayra = pygame.image.load(
        pasta / "Nayra" / "nayra_documento.png"
    ).convert_alpha()

    # Carrega a aparência de chegada e a forma revelada.
    imagens_amanda = carregar_par(
        pasta,
        "amanda/amanda_transparente.png",
        "amanda/amanda_ia_transparente.png",
    )

    # Carrega as duas formas do Nero antes do loop principal.
    imagens_nero = carregar_par(
        pasta,
        "Nero/nero_transparente.png",
        "Nero/nero_ia_transparente.png",
    )

    return {
        "lucas": {
            "nome": "Lucas",
            "imagens": imagens_lucas,

            # Preserva a foto antiga do Lucas com cabelo curto.
            "foto": foto_lucas,
        },
        "gael": {
            "nome": "Gael",
            "imagens": imagens_gael,

            # Gael não apresenta documento.
            "foto": None,
        },
        "estefanny": {
            "nome": "Estefanny",
            "imagens": imagens_estefanny,

            # A foto apresentada não revela a identidade sorteada.
            "foto": preparar_foto(imagens_estefanny["humano"]),
        },
        "nayra": {
            "nome": "Nayra",
            "imagens": imagens_nayra,

            # A foto antiga é apresentada pelas duas identidades.
            "foto": preparar_foto(foto_nayra),
        },
            "amanda": {
            "nome": "Amanda",
            "imagens": imagens_amanda,

            # As duas identidades apresentam a mesma foto humana.
            "foto": preparar_foto(imagens_amanda["humano"]),
        },
            "nero": {
            "nome": "Nero",
            "imagens": imagens_nero,

            # O documento usa a foto humana nas duas identidades.
            "foto": preparar_foto(imagens_nero["humano"]),
        },
    }
