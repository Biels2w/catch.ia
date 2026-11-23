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

    # Cada lista interna contém os códigos de uma página.
    paginas_codigos = [
        ["V-012", "V-014", "V-027", "V-031"],
        ["V-045", "V-052", "V-068", "V-073"],
        ["V-081", "V-096", "V-104", "V-118"],
    ]

    # Guarda a página selecionada durante a partida. (começa em 0)
    pagina_atual = 0

    # Folha aberta e áreas para trocar de página.
    ficha_documento = pygame.Rect(210, 110, 380, 410)
    botao_anterior = pygame.Rect(230, 465, 120, 36)
    botao_proximo = pygame.Rect(450, 465, 120, 36)

    fonte_codigos = pygame.font.Font(None, 32)

    # Pasta clicável sobre o balcão
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

#========================BOTÕES PERMISSÃO=========================

    # Placa abaixo da janela: a moldura termina em y=370.
    base_botoes = pygame.Rect(140, 384, 128, 62)

    # Áreas dos dois botões redondos.
    botao_liberar = pygame.Rect(154, 397, 36, 36)
    botao_recusar = pygame.Rect(218, 397, 36, 36)

    # Nenhuma decisão foi tomada ao iniciar o atendimento.
    decisao = None

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

    #=====================SPRITE PAREDE=====================
    # Parede ajustada ao tamanho da tela.
    textura_parede = pygame.image.load("assets/imagens/parede.png").convert()
    textura_parede = pygame.transform.scale(
        textura_parede, (LARGURA_TELA, ALTURA_TELA)
    )

    #=====================SPRITE MOLDURA JANELA=====================
    # A mesma imagem de metal serve para a moldura e o peitoril.
    imagem_metal = pygame.image.load("assets/imagens/moldura.png").convert()
    textura_moldura = pygame.transform.scale(imagem_metal, moldura_janela.size)
    textura_peitoril = pygame.transform.scale(imagem_metal, peitoril.size)

    #=====================SPRITE BALCÃO=====================
    # Madeira para o tampo e a frente do balcão.
    imagem_madeira = pygame.image.load("assets/imagens/balcao.png").convert()
    textura_tampo = pygame.transform.scale(imagem_madeira, tampo_balcao.size)
    textura_frente = pygame.transform.scale(imagem_madeira, frente_balcao.size)

    # Gira a madeira para deixar os veios na vertical.
    madeira_vertical = pygame.transform.rotate(imagem_madeira, 90)
    textura_frente = pygame.transform.scale(
    madeira_vertical, frente_balcao.size
)
    # Gira a madeira para deixar os veios na vertical.
    madeira_vertical = pygame.transform.rotate(imagem_madeira, 90)

    textura_frente = pygame.transform.scale(
    madeira_vertical, frente_balcao.size)

    # A frente recebe menos luz que o tampo.
    textura_frente.fill(
        (135, 135, 135), special_flags=pygame.BLEND_RGB_MULT
)

    #=====================SPRITE ARQUIVO=====================
    sprite_arquivo = pygame.image.load(
    "assets/imagens/arquivo.png"
    ).convert_alpha()

    sprite_arquivo = pygame.transform.scale(
    sprite_arquivo, (pasta.width, pasta.bottom - aba_pasta.top)
)

    #=====================SPRITE BOTÕES DECISÃO=====================
    # Carrega o painel preservando o fundo transparente.
    sprite_botoes = pygame.image.load(
        "assets/imagens/botoes.png"
    ).convert_alpha()

    sprite_botoes = pygame.transform.scale(
        sprite_botoes, base_botoes.size)

    #=====================SPRITE FOLHAS DOCUMENTO=====================
    # Ajusta a imagem ao tamanho da folha aberta.
    sprite_folha = pygame.image.load(
        "assets/imagens/folha_manual.png"
    ).convert_alpha()

    sprite_folha = pygame.transform.scale(
        sprite_folha, ficha_documento.size
)

    #=======================================================
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if documento_aberto:
                    # Enquanto o manual está aberto, os cliques controlam sua leitura.
                    if botao_anterior.collidepoint(evento.pos):
                        pagina_atual = max(0, pagina_atual - 1)

                    elif botao_proximo.collidepoint(evento.pos):
                        pagina_atual = min(
                            len(paginas_codigos) - 1,
                            pagina_atual + 1,
                        )

                    elif documento.collidepoint(evento.pos):
                        documento_aberto = False

                    elif not ficha_documento.collidepoint(evento.pos):
                        documento_aberto = False

                elif documento.collidepoint(evento.pos):
                    documento_aberto = True

                elif botao_liberar.collidepoint(evento.pos):
                    if decisao is None:
                        decisao = "liberar"

                elif botao_recusar.collidepoint(evento.pos):
                    if decisao is None:
                        decisao = "recusar"

                elif area_luminaria.collidepoint(evento.pos):
                    luminaria_acesa = not luminaria_acesa

        # Pinta a parede da cabine antes de desenhar os outros elementos.
        tela.fill(CINZA)

        # A parede cobre o fundo inteiro.
        tela.blit(textura_parede, (0, 0))

        # A vista externa cobre o centro da textura metálica,
        # deixando apenas as bordas da moldura aparentes.
        tela.blit(textura_moldura, moldura_janela)
        tela.blit(textura_ceu, ceu_externo)
        tela.blit(textura_muro, muro_externo)
        tela.blit(textura_chao, chao_externo)
        tela.blit(textura_peitoril, peitoril)

        # Balcão em primeiro plano (visto de frente).
        tela.blit(textura_tampo, tampo_balcao)
        tela.blit(textura_frente, frente_balcao)

        # Sombra projetada pela borda do tampo sobre a frente do balcão.
        pygame.draw.rect(
        tela,
        (40, 26, 18),
        (
        frente_balcao.left,
        frente_balcao.top,
        frente_balcao.width,
        8)
)

        # Sobrepõe a iluminação ao cenário quando a luminária está acesa.
        if luminaria_acesa: # Tem que desenhar antes dos items em cima da mesa
            tela.blit(iluminacao, (0, 0))

        tela.blit(sprite_arquivo, (pasta.left, aba_pasta.top))

#===========================================================================================

        # Painel com os dois botões em relevo.
        tela.blit(sprite_botoes, base_botoes)

        # Cria e desenha a mensagem somente após uma decisão.
        if decisao is not None:
            if decisao == "liberar":
                mensagem = "Entrada autorizada"
                cor_mensagem = (120, 220, 145)
            else:
                mensagem = "Entrada recusada"
                cor_mensagem = (255, 145, 145)

            texto_decisao = fonte.render(mensagem, True, cor_mensagem)
            tela.blit(texto_decisao, (285, 405))

#=======================================================================================

        if documento_aberto:
            # Sombra e folha do manual.
            pygame.draw.rect(
                tela,
                (55, 43, 31),
                ficha_documento.move(5, 5),
            )
            # Desenha o papel antes dos textos e dos botões.
            tela.blit(sprite_folha, ficha_documento)

            # Transforma o título em uma imagem e a coloca na folha.
            titulo_manual = fonte.render(
                "CÓDIGOS PERMITIDOS", True, (40, 40, 35)
            )
            tela.blit(titulo_manual, (230, 135))

            # Linha que separa o título da lista de códigos.
            pygame.draw.line(
                tela, (155, 140, 110), (230, 170), (570, 170), 2
            )

            # Seleciona a lista de códigos da página atual.
            # enumerate() fornece a posição de cada código, começando em zero.
            for indice, codigo in enumerate(paginas_codigos[pagina_atual]):
                texto_codigo = fonte_codigos.render(
                    codigo, True, (40, 40, 35)
                )
                tela.blit(texto_codigo, (250, 205 + indice * 48))

            # O botão fica mais escuro quando há uma página disponível.
            cor_anterior = (180, 166, 135)
            cor_proximo = (180, 166, 135)

            if pagina_atual == 0:
                cor_anterior = (220, 211, 190)

            if pagina_atual == len(paginas_codigos) - 1:
                cor_proximo = (220, 211, 190)

            pygame.draw.rect(
                tela, cor_anterior, botao_anterior, border_radius=4
            )
            pygame.draw.rect(
                tela, cor_proximo, botao_proximo, border_radius=4
            )

            texto_anterior = fonte.render("Anterior", True, (40, 40, 35))
            texto_proximo = fonte.render("Próxima", True, (40, 40, 35))

            # Soma um ao índice para exibir a numeração começando em 1.
            # len() informa o total de páginas do manual.
            numero_pagina = fonte.render(
                f"{pagina_atual + 1} / {len(paginas_codigos)}",
                True,
                (40, 40, 35),
            )

            # Centraliza cada texto no respectivo botão.
            tela.blit(
                texto_anterior,
                texto_anterior.get_rect(center=botao_anterior.center),
            )
            tela.blit(
                texto_proximo,
                texto_proximo.get_rect(center=botao_proximo.center),
            )

            # Centraliza o indicador de página entre os dois botões.
            tela.blit(
                numero_pagina,
                numero_pagina.get_rect(center=(400, 483)),
            )

#=======================================================================================

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