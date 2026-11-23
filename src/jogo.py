import pygame

from datetime import date
from src.consultas import MESES, desenhar_calendario, desenhar_jornal

from math import sin, cos, radians

from src.config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO, CINZA, PRETO

#======================================================================

def desenhar_relogio(tela, sprite, area, segundos_turno):
    # Desenha o sprite do relógio com os ponteiros animados.
    # O sprite já contém a moldura, os números e as marcações.
    tela.blit(sprite, area)

    centro = area.center

    # Separa o horário em horas, minutos e segundos.
    horas = (segundos_turno // 3600) % 24
    minutos = (segundos_turno // 60) % 60
    segundos = segundos_turno % 60

    def ponta_ponteiro(angulo, comprimento):
        # O ângulo zero aponta para o número 12.
        angulo = radians(angulo - 90)

        return (
            round(centro[0] + cos(angulo) * comprimento),
            round(centro[1] + sin(angulo) * comprimento),
        )

    # Inclui os minutos e segundos para os ponteiros avançarem
    # aos poucos entre as marcações do mostrador.
    angulo_horas = (horas % 12) * 30 + minutos * 0.5
    angulo_minutos = minutos * 6 + segundos * 0.1
    angulo_segundos = segundos * 6

    # Os comprimentos acompanham a largura do sprite.
    pygame.draw.line(
        tela,
        (45, 40, 35),
        centro,
        ponta_ponteiro(angulo_horas, area.width * 0.18),
        4,
    )

    pygame.draw.line(
        tela,
        (45, 40, 35),
        centro,
        ponta_ponteiro(angulo_minutos, area.width * 0.27),
        3,
    )

    pygame.draw.line(
        tela,
        (160, 50, 40),
        centro,
        ponta_ponteiro(angulo_segundos, area.width * 0.33),
        1,
    )

    # Acabamento que cobre a junção dos três ponteiros.
    pygame.draw.circle(tela, (55, 48, 40), centro, 4)
#======================================================================

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

#========================CALÊNDARIO PAREDE=========================
    # Consultas fixadas na parede, acima da luminária.
    area_calendario = pygame.Rect(680, 75, 100, 110)
    area_jornal = pygame.Rect(680, 210, 100, 120)

    # Data fictícia usada pelos documentos e pelas consultas da partida.
    data_partida = date(2042, 11, 22)

    # None significa que nenhuma consulta está aberta.
    consulta_aberta = None

    fonte_consulta = pygame.font.Font(None, 22)
    fonte_parede = pygame.font.Font(None, 16)

#========================INFORMAÇÕES JORNAL PAREDE=========================
    # Conteúdo fictício da primeira edição do jornal.
    # Cada notícia tem uma manchete e uma lista de linhas.
    noticias_semana = [
        {
            "titulo": "FALHA NO SCANNER",
            "linhas": [
                "O scanner apresentou falhas.",
                "Confira também os documentos.",
            ],
        },
        {
            "titulo": "PASSES COPIADOS",
            "linhas": [
                "Cópias de credenciais da série V",
                "foram encontradas nesta semana.",
                "Compare os dados apresentados.",
            ],
        },
        {
            "titulo": "AVISO AOS FISCAIS",
            "linhas": [
                "Divergências exigem conferência.",
                "Consulte as fontes disponíveis.",
            ],
        },
]

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

    #=====================SPRITE CALENDÁRIO=====================

    sprite_calendario = pygame.image.load(
    "assets/imagens/calendario.png"
).convert_alpha()

    sprite_calendario = pygame.transform.scale(
        sprite_calendario, area_calendario.size
    )

    # Os números são desenhados pelo jogo sobre o sprite.
    texto_mes_calendario = fonte_parede.render(
        f"{MESES[data_partida.month - 1][:3].upper()} {data_partida.year}",
        True,
        (255, 241, 218),
    )

    texto_dia_calendario = fonte_codigos.render(
        str(data_partida.day), True, (55, 48, 39)
    )

    texto_data_calendario = fonte_parede.render(
        f"{data_partida:%d/%m/%Y}", True, (55, 48, 39)
)

    #=====================SPRITE JORNAL=====================
    sprite_jornal = pygame.image.load(
        "assets/imagens/jornal.png"
    ).convert_alpha()

    sprite_jornal = pygame.transform.scale(
        sprite_jornal, area_jornal.size
    )

    fonte_titulo_jornal = pygame.font.Font(None, 14)

    texto_boletim = fonte_titulo_jornal.render(
        "BOLETIM", True, (55, 48, 39)
    )
    texto_refugio = fonte_titulo_jornal.render(
        "DO REFÚGIO", True, (55, 48, 39)
)

    #=====================RELÓGIO DE PAREDE=====================

    # Posição e tamanho: x, y, largura e altura.
    # Cabe na parede à esquerda da janela, que começa em x=140.
    area_relogio = pygame.Rect(17, 87, 106, 106)

    # convert_alpha() preserva a transparência ao redor do relógio.
    sprite_relogio = pygame.image.load(
        "assets/imagens/relogio.png"
    ).convert_alpha()

    sprite_relogio = pygame.transform.scale(
        sprite_relogio, area_relogio.size
    )

    # O expediente começa às 08:00.
    horario_inicial = 8 * 60 * 60

    # Guarda o instante inicial uma única vez, fora do while.
    inicio_turno = pygame.time.get_ticks()

    # Horário fictício de início do expediente: 08:00.
    horario_inicial = 8 * 60 * 60

    # Guarda o instante inicial uma única vez.
    # get_ticks() informa quantos milissegundos passaram desde pygame.init().
    inicio_turno = pygame.time.get_ticks()

    fonte_relogio = pygame.font.Font(None, 18)

    #=======================================================
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                # Fecha a leitura sem reiniciar a página do manual.
                consulta_aberta = None
                documento_aberto = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if consulta_aberta is not None:
                    # Durante a consulta, clicar fora fecha a folha.
                    if not ficha_documento.collidepoint(evento.pos):
                        consulta_aberta = None

                elif documento_aberto:
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

                elif area_calendario.collidepoint(evento.pos):
                    consulta_aberta = "calendario"

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

                elif area_calendario.collidepoint(evento.pos):
                    consulta_aberta = "calendario"

                elif area_jornal.collidepoint(evento.pos):
                    consulta_aberta = "jornal"

                elif documento.collidepoint(evento.pos):
                    documento_aberto = True

        # Pinta a parede da cabine antes de desenhar os outros elementos.
        tela.fill(CINZA)

        # A parede cobre o fundo inteiro.
        tela.blit(textura_parede, (0, 0))

        #=== Aciona o relógio na parede ===
        # Converte os milissegundos transcorridos em segundos.
        segundos_passados = (
            pygame.time.get_ticks() - inicio_turno
        ) // 1000

        segundos_turno = horario_inicial + segundos_passados

        # Desenha sobre a parede, antes das consultas abertas.
        desenhar_relogio(
            tela,
            sprite_relogio,
            area_relogio,
            segundos_turno,
        )

        # === Desenha o caléndario acima da parede ===
        tela.blit(sprite_calendario, area_calendario)

        tela.blit(
            texto_mes_calendario,
            texto_mes_calendario.get_rect(
                center=(area_calendario.centerx, area_calendario.top + 24)
            ),
        )
        tela.blit(
            texto_dia_calendario,
            texto_dia_calendario.get_rect(
                center=(area_calendario.centerx, area_calendario.top + 65)
            ),
        )
        tela.blit(
            texto_data_calendario,
            texto_data_calendario.get_rect(
                center=(area_calendario.centerx, area_calendario.top + 92)
            ),
        )

        tela.blit(sprite_jornal, area_jornal)

        tela.blit(
            texto_boletim,
            texto_boletim.get_rect(
                center=(area_jornal.centerx, area_jornal.top + 21)
            ),
        )
        tela.blit(
            texto_refugio,
            texto_refugio.get_rect(
                center=(area_jornal.centerx, area_jornal.top + 32)
            ))
#==========================================================================

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


        # A consulta ampliada aparece sobre o cenário.
        if consulta_aberta is not None:
            pygame.draw.rect(
                tela, (55, 43, 31), ficha_documento.move(5, 5)
            )
            tela.blit(sprite_folha, ficha_documento)

            if consulta_aberta == "calendario":
                desenhar_calendario(
                    tela,
                    ficha_documento,
                    data_partida,
                    fonte,
                    fonte_consulta,
                )

            elif consulta_aberta == "jornal":
                desenhar_jornal(
                    tela,
                    ficha_documento,
                    data_partida,
                    noticias_semana,
                    fonte,
                    fonte_consulta,
                )

            


        pygame.display.flip() # Exibe o quadro depois que todas as camadas foram desenhadas.
        relogio.tick(FPS)

    pygame.quit()