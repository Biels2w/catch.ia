from pathlib import Path

import pygame


def carregar_personagens(imagens_lucas):
    """Reúne os personagens e carrega os sprites do Gael."""

    # Localiza a pasta de personagens a partir deste arquivo.
    # Assim, o caminho não depende da pasta aberta no terminal.
    pasta_personagens = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "imagens"
        / "personagens"
    )

    # A imagem humana está dentro da pasta "Gael".
    imagem_gael = pygame.image.load(
        pasta_personagens / "Gael" / "gael_transparente.png"
    ).convert_alpha()

    # A versão IA está em outra pasta, chamada "Gael IA".
    imagem_gael_ia = pygame.image.load(
        pasta_personagens / "Gael IA" / "gael_ia_transparente.png"
    ).convert_alpha()

    # Usa a mesma altura definida para Lucas no jogo.py.
    altura = 280

    # Calcula a largura proporcional à imagem humana.
    largura = round(
        imagem_gael.get_width()
        * altura
        / imagem_gael.get_height()
    )

    tamanho = (largura, altura)

    # Mantém as duas versões com o mesmo tamanho para que
    # o personagem não mude de posição durante a revelação.
    imagens_gael = {
        "humano": pygame.transform.scale(
            imagem_gael, tamanho
        ),
        "ia": pygame.transform.scale(
            imagem_gael_ia, tamanho
        ),
    }

    # Lucas já foi carregado no jogo.py.
    # Recebemos suas imagens para evitar carregá-las novamente.
    return {
        "lucas": {
            "nome": "Lucas",
            "imagens": imagens_lucas,
        },
        "gael": {
            "nome": "Gael",
            "imagens": imagens_gael,
        },
    }