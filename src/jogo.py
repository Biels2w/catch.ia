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

    # Ocupa o espaço entre o topo da abertura e o muro.
    ceu_externo = pygame.Rect(
    abertura_janela.left,
    abertura_janela.top,
    abertura_janela.width,
    muro_externo.top - abertura_janela.top,
)

#========================BALCÃO=========================
    # O balcão ocupa toda a largura da tela e vai até a borda inferior.
    tampo_balcao = pygame.Rect(0, 450, LARGURA_TELA, 90)
    frente_balcao = pygame.Rect(0, 540, LARGURA_TELA, ALTURA_TELA - 540)

#========================DOCUMENTOS=========================
    documento = pygame.Rect(40, 470, 116, 58)
    documento_aberto = False # True = aberta / False = fechada

    fonte = pygame.font.Font(None, 26) #(None = fonte padrão do pygame) e 26 é o tamanho definido

    fonte_rotulo = pygame.font.Font(None, 20)
    rotulo_documento = fonte_rotulo.render(
    "Passe de entrada", True, (30, 35, 42))

    # Transforma o "passe de entrada" em uma surface e o True suaviza a fonte
    rotulo_documento = fonte.render("Passe de entrada", True, (30, 35, 42)) 
    texto_passe = fonte.render("Passe V-014 / Setor 3", True, (30, 35, 42))
    nome_visitante = fonte.render("Portador: Alex Moraes", True, (30, 35, 42))

    # A mesma área é usada para desenhar a ficha e verificar cliques dentro dela.
    ficha_documento = pygame.Rect(210, 395, 380, 115)

    # Pasta clicável sobre o balcão
    sombra_pasta = pygame.Rect(32, 468, 140, 70)
    pasta = pygame.Rect(28, 462, 140, 70)
    aba_pasta = pygame.Rect(40, 452, 48, 18)

#========================LUMINÁRIA=========================
    # Base da luminária no canto direito do balcão.
    base_luminaria = pygame.Rect(700, 480, 78, 10)

    luminaria_acesa = False
    area_luminaria = pygame.Rect(675, 350, 110, 145)

    # Camada transparente para desenhar a iluminação (se não sobrepõe a imagem do fundo)
    iluminacao = pygame.Surface(
    (LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)

    # Feixe de luz em direção do balcão 
    pygame.draw.polygon(
        iluminacao,
        (255, 215, 130, 25),
        [(679, 386), (722, 402), (720, 525), (520, 525)],
    )

    # Manchas de luz sobre a mesa/balcão
    pygame.draw.ellipse(
        iluminacao, (255, 215, 130, 40), (520, 480, 210, 48)
    )
    pygame.draw.ellipse(
        iluminacao, (255, 215, 130, 55), (550, 487, 150, 32))

    # Define onde a iluminação pode aparecer.
    mascara_luz = pygame.Surface(
        (LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA
    )

    # Permite o feixe acima do balcão.
    pygame.draw.rect(
        mascara_luz,
        (255, 255, 255, 255),
        (0, 0, LARGURA_TELA, tampo_balcao.top),
    )

    # Sobre a mesa, permite luz somente dentro da área oval.
    pygame.draw.ellipse(
        mascara_luz,
        (255, 255, 255, 255),
        (520, 480, 210, 48),
    )

    # Recorta a iluminação conforme a máscara.
    iluminacao.blit(
        mascara_luz,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT, )

#=======================================================

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    #=====================SPRITE CHÃO=====================
    # Carrega a textura e ajusta ao tamanho do chão externo.
    textura_chao = pygame.image.load("assets/imagens/floor.png").convert()
    textura_chao = pygame.transform.scale(textura_chao, chao_externo.size)

    #=====================SPRITE MURO=====================
    # Carrega a imagem e ajusta ao tamanho do muro.
    textura_muro = pygame.image.load("assets/imagens/muro.png").convert()
    textura_muro = pygame.transform.scale(textura_muro, muro_externo.size)

    #=====================SPRITE CÉU=====================
    textura_ceu = pygame.image.load("assets/imagens/ceu.png").convert()
    textura_ceu = pygame.transform.scale(textura_ceu, ceu_externo.size)

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if area_luminaria.collidepoint(evento.pos):
                    luminaria_acesa = not luminaria_acesa

                elif documento.collidepoint(evento.pos):
                    documento_aberto = not documento_aberto

                elif not ficha_documento.collidepoint(evento.pos):
                    documento_aberto = False

        # Pinta a parede da cabine antes de desenhar os outros elementos.
        tela.fill(CINZA)

        #Moldura e abertura janela
        pygame.draw.rect(tela, (35, 40, 46), moldura_janela)
        tela.blit(textura_ceu, ceu_externo)

        # Vista externa
        # O muro e o chão cobrem a parte inferior da abertura.
        tela.blit(textura_muro, muro_externo)
        # Desenha a textura na posição do chão externo.
        tela.blit(textura_chao, chao_externo)
        pygame.draw.rect(tela, (29, 33, 39), peitoril)

        # Balcão
        # O tampo mais claro diferencia a superfície da frente do balcão.
        pygame.draw.rect(tela, (61, 66, 75), tampo_balcao)
        pygame.draw.rect(tela, (38, 42, 49), frente_balcao)

        # Sobrepõe a iluminação ao cenário quando a luminária está acesa.
        if luminaria_acesa: # Tem que desenhar antes dos items em cima da mesa
            tela.blit(iluminacao, (0, 0))

        pygame.draw.rect(tela, (225, 214, 184), documento)
        tela.blit(rotulo_documento, rotulo_documento.get_rect(center=documento.center))

        if documento_aberto:
            # O passe fica visível no balcão. Os dados só aparecem com a ficha aberta.
            pygame.draw.rect(tela, (242, 234, 211), ficha_documento)
            tela.blit(texto_passe, (230, 415))
            tela.blit(nome_visitante, (230, 450))

        # Desenha a pasta do fundo pra frente.
        pygame.draw.rect(tela, (65, 47, 30), sombra_pasta)
        pygame.draw.rect(tela, (180, 153, 100), aba_pasta)
        pygame.draw.rect(tela, (201, 176, 126), pasta)

        # Braços articulados da luminária.
        pygame.draw.line(tela, (40, 44, 50), (738, 480), (765, 410), 10)
        pygame.draw.line(tela, (40, 44, 50), (765, 410), (714, 370), 10)

        # Os trem que conectam os braços (esqueci o nome).
        pygame.draw.circle(tela, (73, 78, 85), (765, 410), 9)
        pygame.draw.circle(tela, (73, 78, 85), (714, 370), 8)

        # Cabeça da luminária, ligada por 4 pontos em sequencia
        pygame.draw.polygon(
        tela,
        (48, 53, 60),
        [(702, 360), (722, 368), (725, 403), (676, 385)])

# A lâmpada fica amarela quando acesa e cinza quando apagada.
        if luminaria_acesa:
            cor_lampada = (255, 218, 135)
        else:
            cor_lampada = (85, 85, 80)

        pygame.draw.line(
            tela,
            cor_lampada,
            (679, 386),
            (722, 402),
            6,
)

        pygame.draw.rect(tela, (40, 44, 50), base_luminaria)


        pygame.display.flip() # Exibe o quadro depois que todas as camadas foram desenhadas.
        relogio.tick(FPS)

    pygame.quit()