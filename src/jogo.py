import pygame

from src.config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO, CINZA, PRETO


def executar_jogo():
    # Abre a janela e executa o loop principal do Catch.IA.
    pygame.init()

#========================JANELA=========================
    # retângulo recebe (x, y, largura, altura).
    # A abertura fica 12 pixels para dentro da moldura em todos os lados.
    moldura_janela = pygame.Rect(140, 70, 520, 300)
    abertura_janela = pygame.Rect(152, 82, 496, 276)

#=====================CENÁRIO PÁTIO=====================
    # O muro e o chão têm a mesma largura da abertura.
    # O chão começa onde o muro termina: 235 + 55 = 290.
    muro_externo = pygame.Rect(152, 235, 496, 55)
    chao_externo = pygame.Rect(152, 290, 496, 68)
    peitoril = pygame.Rect(132, 358, 536, 16)

#========================BALCÃO=========================
    # O balcão ocupa toda a largura da tela e vai até a borda inferior.
    tampo_balcao = pygame.Rect(0, 450, LARGURA_TELA, 90)
    frente_balcao = pygame.Rect(0, 540, LARGURA_TELA, ALTURA_TELA - 540)

#========================DOCUMENTO=========================
    documento = pygame.Rect(40, 470, 150, 48)
    documento_aberto = False # True = aberta / False = fechada

    fonte = pygame.font.Font(None, 26) #(None = fonte padrão do pygame) e 26 é o tamanho definido

    # Transforma o "passe de entrada" em uma surface e o True suaviza a fonte
    rotulo_documento = fonte.render("Passe de entrada", True, (30, 35, 42)) 
    texto_passe = fonte.render("Passe V-014 / Setor 3", True, (30, 35, 42))
    nome_visitante = fonte.render("Portador: Alex Moraes", True, (30, 35, 42))

    # A mesma área é usada para desenhar a ficha e verificar cliques dentro dela.
    ficha_documento = pygame.Rect(210, 395, 380, 115)

#=======================================================

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # O passe alterna o estado da ficha. Clicar fora dela fecha a leitura.
                if documento.collidepoint(evento.pos):
                    documento_aberto = not documento_aberto
                elif not ficha_documento.collidepoint(evento.pos):
                    documento_aberto = False

        # Pinta a parede da cabine antes de desenhar os outros elementos.
        tela.fill(CINZA)

        #Moldura e abertura janela
        pygame.draw.rect(tela, (35, 40, 46), moldura_janela)
        pygame.draw.rect(tela, (77, 93, 155), abertura_janela)

        # Vista externa
        # O muro e o chão cobrem a parte inferior da abertura.
        # A faixa azulada que sobra acima deles representa o céu.
        pygame.draw.rect(tela, (60, 68, 80), muro_externo)
        pygame.draw.rect(tela, (47, 56, 68), chao_externo)
        pygame.draw.rect(tela, (29, 33, 39), peitoril)

        # Balcão
        # O tampo mais claro diferencia a superfície da frente do balcão.
        pygame.draw.rect(tela, (61, 66, 75), tampo_balcao)
        pygame.draw.rect(tela, (38, 42, 49), frente_balcao)

        pygame.draw.rect(tela, (225, 214, 184), documento)
        tela.blit(rotulo_documento, rotulo_documento.get_rect(center=documento.center))

        if documento_aberto:
            # O passe fica visível no balcão. Os dados só aparecem com a ficha aberta.
            pygame.draw.rect(tela, (242, 234, 211), ficha_documento)
            tela.blit(texto_passe, (230, 415))
            tela.blit(nome_visitante, (230, 450))

        pygame.display.flip() # Exibe o quadro depois que todas as camadas foram desenhadas.
        relogio.tick(FPS)

    pygame.quit()