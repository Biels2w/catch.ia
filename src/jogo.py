import pygame

from src.config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO, CINZA


def executar_jogo():
    # Abre a janela e executa o loop principal do Catch.IA.
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Catch.IA")

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(CINZA)
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()