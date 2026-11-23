import pygame

def carregar_sprites_interface():
    """Carrega os PNGs uma única vez, depois da criação da janela."""
    from pathlib import Path

    # Calcula o caminho a partir do projeto.
    pasta = Path(__file__).resolve().parent.parent / "assets" / "imagens"

    # Cada imagem será ajustada ao tamanho usado na interface.
    tamanhos = {
        "coracao_cheio": (28, 28),
        "coracao_vazio": (28, 28),
        "icone_derrota": (72, 72),
        "icone_vitoria": (72, 72),
        "fundo_relatorio": (440, 480),
    }

    sprites = {}

    for nome, tamanho in tamanhos.items():
        # convert_alpha preserva a transparência dos PNGs.
        imagem = pygame.image.load(
            str(pasta / f"{nome}.png")
        ).convert_alpha()

        sprites[nome] = pygame.transform.scale(imagem, tamanho)

    return sprites