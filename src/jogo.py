import pygame

from random import choice
from datetime import date, datetime
from src.consultas import MESES, desenhar_calendario, desenhar_jornal, desenhar_livro
from src.sprites import carregar_sprites_interface

from src.audio import carregar_audio, tocar_som
from src.funcoes import desenhar_relogio, avaliar_decisao, desenhar_vidas
from src.dados import salvar_ocorrencias

from src.config import META_ATENDIMENTOS
from src.relatorio import verificar_fim_partida, montar_relatorio, desenhar_relatorio

from src.efeitos import criar_efeito_dano, aplicar_efeito_dano

from src.dialogos import (
    carregar_dialogos,
    preparar_dialogo,
    responder_pergunta,
    desenhar_interfone,
    desenhar_fala_cena,
)

from src.documentos import (
    carregar_documentos,
    entregar_documento,
    desenhar_documento,
    preparar_passe
)

from src.moradores import (
    carregar_moradores,
    obter_pagina_moradores,
    desenhar_moradores,
)

from src.scanner import (
    criar_scanner,
    iniciar_leitura,
    atualizar_scanner,
    desenhar_scanner,
)

from src.casos import carregar_casos, montar_caso
from src.personagens import carregar_personagens

from src.config import LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO, CINZA, PRETO

#======================================================================

def executar_jogo():
    # Abre a janela e executa o loop principal do Catch.IA.
    pygame.init()

    # Carrega os efeitos uma única vez e inicia a trilha em repetição.
    sons = carregar_audio()

#==================SISTEMA DE VIDAS==================
    vidas = 3

    # Estes contadores pertencem somente à partida atual.
    acertos = 0
    erros = 0
    atendimentos = 0

    # None indica que a partida ainda não terminou.
    relatorio_final = None

    # Cada partida começa com um livro vazio na primeira página.
    ocorrencias = []
    pagina_livro = 0

    # Atualiza também o arquivo para remover os registros da partida anterior.
    salvar_ocorrencias(ocorrencias)

    # Camada transparente usada no efeito de captura.
    camada_efeitos = pygame.Surface(
        (LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA
    )

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

    # Prepara a camada de rachaduras uma única vez.
    efeito_dano = criar_efeito_dano(tela.get_size())

    # A janela precisa existir antes de carregar imagens com convert_alpha.
    sprites_interface = carregar_sprites_interface()

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
    
    #=====================SPRITE RELÓGIO PAREDE=====================
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

    #=====================SPRITE CAMPAINHA=====================

    # Posição sobre o balcão, à direita da pasta.
    area_campainha = pygame.Rect(204, 460, 80, 70)

    sprite_campainha = pygame.image.load(
        "assets/imagens/campainha.png"
    ).convert_alpha()

    sprite_campainha = pygame.transform.scale(
        sprite_campainha, area_campainha.size
    )

    # Usa o toque armazenado na pasta assets/sons.
    som_campainha = sons.get("campainha")

    # Guardam até quando cada efeito deve permanecer ativo.
    campainha_pressionada_ate = 0
    aviso_campainha_ate = 0

    # Impede vários toques seguidos em um intervalo muito curto.
    proximo_toque = 0

    fonte_campainha = pygame.font.Font(None, 24)
    texto_campainha = fonte_campainha.render(
        "Próximo, por favor!", True, (242, 229, 197)
    )

    #=====================SPRITE LIVRO=====================

    # Define a posição e o tamanho do livro sobre o balcão.
    # Rect recebe: x, y, largura e altura.
    area_livro = pygame.Rect(330, 466, 132, 64)

    # Carrega o sprite preservando a transparência ao redor do livro.
    # Este carregamento vem depois da criação da janela.
    sprite_livro = pygame.image.load(
        "assets/imagens/livro_ocorrencias.png"
    ).convert_alpha()

    # Ajusta a imagem às dimensões do retângulo.
    # O carregamento e o redimensionamento acontecem uma única vez.
    sprite_livro = pygame.transform.scale(
        sprite_livro, area_livro.size
    )

    #=====================SPRITE LISTA DE MORADORES=====================

    # Espaço da parede abaixo do relógio.
    area_moradores = pygame.Rect(30, 215, 90, 135)

    sprite_moradores = pygame.image.load(
        "assets/imagens/lista_moradores.png"
    ).convert_alpha()

    sprite_moradores = pygame.transform.scale(
        sprite_moradores, area_moradores.size
    )

    rotulo_moradores = fonte_parede.render(
        "Moradores", True, (235, 225, 202)
    )

    # O arquivo é lido uma única vez, antes do loop.
    moradores = carregar_moradores()

    # Mantém a página selecionada ao fechar e reabrir a consulta.
    pagina_moradores = 0

    #=====================SPRITE SCANNER=====================

    area_scanner = pygame.Rect(610, 482, 88, 50)

    sprite_scanner = pygame.image.load(
        "assets/imagens/scanner.png"
    ).convert_alpha()

    sprite_scanner = pygame.transform.scale(
        sprite_scanner, area_scanner.size
    )

    # Botão dentro do painel ampliado.
    botao_scanner = pygame.Rect(
        ficha_documento.left + 85,
        ficha_documento.bottom - 80,
        210,
        36,
    )

    scanner = criar_scanner()



    #=====================SPRITE DOCUMENTO DO VISITANTE=====================

    # Espaço livre sobre o balcão, à direita do livro.
    area_passe = pygame.Rect(490, 470, 110, 62)

    # Sprite próprio do passe sobre a mesa.
    sprite_passe = pygame.image.load(
        "assets/imagens/passe_documento.png"
    ).convert_alpha()

    sprite_passe = pygame.transform.scale(
        sprite_passe, area_passe.size
    )

    # O rótulo continua sendo escrito pelo código.
    fonte_passe = pygame.font.Font(None, 14)

    sprite_passe.blit(
        fonte_passe.render("PASSE", True, (48, 43, 35)),
        (47, 6),
    )

    # Fundo exclusivo da ficha aberta.
    sprite_documento = pygame.image.load(
        "assets/imagens/fundo_documento.png"
    ).convert_alpha()

    sprite_documento = pygame.transform.scale(
        sprite_documento, ficha_documento.size
    )

    # Os modelos são lidos uma única vez.
    modelos_documentos = carregar_documentos()
    casos = carregar_casos()


    #=====================SPRITE INTERFONE=====================

    # Aparelho à direita dos botões, abaixo da janela.
    area_interfone = pygame.Rect(548, 382, 114, 64)

    # Espaço entre os botões e o aparelho para as falas curtas.
    area_fala = pygame.Rect(278, 382, 260, 64)

    sprite_interfone = pygame.image.load(
        "assets/imagens/interfone.png"
    ).convert_alpha()

    sprite_interfone = pygame.transform.scale(
        sprite_interfone, area_interfone.size
    )

    fonte_dialogo = pygame.font.Font(None, 20)
    fonte_fala = pygame.font.Font(None, 16)

    # O arquivo é lido uma única vez.
    roteiros = carregar_dialogos()

    # Começa sem visitante e sem perguntas realizadas.
    interfone = preparar_dialogo()

    # Três botões dentro da mesma folha usada pelas consultas.
    botoes_perguntas = [
        pygame.Rect(
            ficha_documento.left + 20,
            ficha_documento.top + 82 + indice * 44,
            ficha_documento.width - 40,
            36,
        )
        for indice in range(3)
    ]


    #=====================SPRITES VISITANTES=====================

    #=====================PRIMEIRO VISITANTE=====================

    imagem_lucas = pygame.image.load(
        "assets/imagens/personagens/Lucas/lucas_transparente.png"
    ).convert_alpha()

    # Define a altura e calcula a largura mantendo a proporção.
    altura_visitante = 280
    largura_visitante = round(
        imagem_lucas.get_width() * altura_visitante
        / imagem_lucas.get_height()
    )

    imagem_lucas = pygame.transform.scale(
        imagem_lucas, (largura_visitante, altura_visitante)
    )

    # Foto antiga de Lucas com cabelo mais curto.
    foto_documento = pygame.image.load(
        "assets/imagens/lucas_documento.png"
    ).convert_alpha()

    # Desconsidera as margens transparentes para aproveitar melhor
    # o espaço da foto dentro do documento.
    foto_documento = foto_documento.subsurface(
        foto_documento.get_bounding_rect()
    ).copy()

    # Mantém a proporção ao ajustar a altura.
    altura_foto = 106
    largura_foto = round(
        foto_documento.get_width()
        * altura_foto
        / foto_documento.get_height()
    )

    foto_documento = pygame.transform.scale(
        foto_documento, (largura_foto, altura_foto)
    )

    # A foto será colocada na miniatura quando o visitante entregar o passe.

    # A forma revelada usa o mesmo tamanho da aparência humana.
    imagem_lucas_ia = pygame.image.load(
        "assets/imagens/personagens/Lucas_ia/lucas_ia_transparente.png"
    ).convert_alpha()

    imagem_lucas_ia = pygame.transform.scale(
        imagem_lucas_ia, (largura_visitante, altura_visitante)
    )

    # Permite selecionar a imagem pelo tipo do visitante.
    imagens_visitante = {
        "humano": imagem_lucas,
        "ia": imagem_lucas_ia,
    }

    # Carrega todos os personagens disponíveis antes do loop.
    personagens = carregar_personagens(
        imagens_visitante, foto_documento
    )

    # Começa totalmente à esquerda da abertura.
    rect_visitante = imagem_lucas.get_rect()
    rect_visitante.right = abertura_janela.left

    # O corpo continua abaixo do peitoril, como alguém do lado de fora.
    rect_visitante.bottom = abertura_janela.bottom + 20

    # O dicionário reúne a imagem, a posição e o estado do visitante.
    visitante = {
        "nome": "Lucas",
        "imagem": imagem_lucas,
        "rect": rect_visitante,
        "x": float(rect_visitante.x),
        "destino_x": abertura_janela.centerx - rect_visitante.width // 2,
        "velocidade": 220,  # Pixels percorridos por segundo.
        "estado": "ausente",
        "documento": None,  # Será preenchido quando o jogador solicitar.
        "caso": None,
        "modelo_documento": None,
        "tipo": None, # Será sorteado na chegada.
        "revelado": False, # Controla a exibição da identidade.
        "revelacao_ate": 0, # Momento em que poderá começar a sair.
        "registrado": False,
        "desfecho": "saindo",
        "efeito_inicio": 0,
    }
    #=======================================================
    # Começa depois do carregamento das imagens e sons.
    inicio_partida = pygame.time.get_ticks()
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        # tick retorna milissegundos; dividimos por 1000 para obter segundos.
        tempo_frame = relogio.tick(FPS) / 1000
        # Tempo atual em milissegundos.
        # Controla os efeitos sem interromper o jogo.
        agora = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and relatorio_final is not None:
                # Reinicia o turno e limpa o histórico do livro.
                vidas = 3
                acertos = 0
                erros = 0
                atendimentos = 0
                # Limpa os registros e volta à primeira página.
                relatorio_final = None
                # Cancela qualquer efeito que ainda estivesse ativo.
                efeito_dano["inicio"] = None
                # Reinicia também a conversa e as perguntas realizadas.
                interfone = preparar_dialogo()
                ocorrencias = []
                pagina_livro = 0

                # Reinicia a consulta pela primeira página do cadastro.
                pagina_moradores = 0
                scanner = criar_scanner()

                # Sobrescreve o arquivo com a lista vazia.
                salvar_ocorrencias(ocorrencias)

                decisao = None
                visitante["estado"] = "ausente"
                visitante["caso"] = None
                visitante["modelo_documento"] = None
                documento_aberto = False
                consulta_aberta = None

                inicio_partida = agora
                inicio_turno = agora
                proximo_toque = 0
                aviso_campainha_ate = 0

            elif (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_b
                and relatorio_final is not None
            ):
                # Permite consultar as ocorrências após o resultado.
                # O ESC existente fecha o livro e volta ao relatório.
                consulta_aberta = "livro"
                tocar_som(sons, "abrir")

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                # Só toca o fechamento se alguma consulta estava aberta.
                if documento_aberto or consulta_aberta is not None:
                    # O interfone usa um clique; os papéis usam o som de folha.
                    som_fechamento = (
                        "botao"
                        if consulta_aberta in ("interfone", "scanner")
                        else "fechar"
                    )

                    tocar_som(sons, som_fechamento)

                consulta_aberta = None
                documento_aberto = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Não permite acionar o cenário atrás do relatório.
                # Quando o livro está aberto, seus cliques continuam funcionando.
                if relatorio_final is not None and consulta_aberta is None:
                    continue
                if consulta_aberta is not None:
                    # Clicar fora fecha a consulta e toca o efeito.
                    if consulta_aberta == "scanner":
                        if not ficha_documento.collidepoint(evento.pos):
                            consulta_aberta = None
                            tocar_som(sons, "botao")

                        elif (
                            botao_scanner.collidepoint(evento.pos)
                            and visitante["estado"] == "aguardando"
                            and decisao is None
                        ):
                            if iniciar_leitura(
                                scanner, agora, visitante["nome"]
                            ):
                                tocar_som(sons, "scanner_ler")

                    elif consulta_aberta == "interfone":
                        if not ficha_documento.collidepoint(evento.pos):
                            consulta_aberta = None
                            tocar_som(sons, "botao")

                        elif visitante["estado"] == "aguardando":
                            # Descobre qual pergunta foi clicada.
                            for indice, botao in enumerate(botoes_perguntas):
                                if botao.collidepoint(evento.pos):
                                    responder_pergunta(interfone, indice)
                                    tocar_som(sons, "interfone_resposta")

                                    # Consulta a ação configurada nessa pergunta.
                                    pergunta = (
                                        interfone["roteiro"]["perguntas"][indice]
                                    )

                                    if pergunta.get("acao") == "entregar_documento":
                                        # Entrega o documento da variação sorteada.
                                        modelo = visitante["modelo_documento"]

                                        # Repetir a pergunta mantém o mesmo passe.
                                        if entregar_documento(visitante, modelo):
                                            # Cria o passe com a foto deste visitante.
                                            visitante["sprite_passe"] = preparar_passe(
                                                sprite_passe, visitante["foto"]
                                            )

                                            tocar_som(sons, "abrir")

                                    # Um clique responde somente uma pergunta.
                                    break

                    elif consulta_aberta == "moradores":
                        if botao_anterior.collidepoint(evento.pos):
                            if pagina_moradores > 0:
                                pagina_moradores -= 1
                                tocar_som(sons, "pagina")

                        elif botao_proximo.collidepoint(evento.pos):
                            # Aqui precisamos apenas da quantidade de páginas.
                            _, total_paginas = obter_pagina_moradores(
                                moradores, pagina_moradores
                            )

                            if pagina_moradores < total_paginas - 1:
                                pagina_moradores += 1
                                tocar_som(sons, "pagina")

                        elif not ficha_documento.collidepoint(evento.pos):
                            consulta_aberta = None
                            tocar_som(sons, "fechar")


                    elif consulta_aberta == "livro" and botao_anterior.collidepoint(evento.pos):
                        if pagina_livro > 0:
                            pagina_livro -= 1
                            tocar_som(sons, "pagina")

                    elif consulta_aberta == "livro" and botao_proximo.collidepoint(evento.pos):
                        ultima = max(
                            0, (len(ocorrencias) - 1) // 3
                        )

                        if pagina_livro < ultima:
                            pagina_livro += 1
                            tocar_som(sons, "pagina")

                    elif not ficha_documento.collidepoint(evento.pos):
                        consulta_aberta = None
                        tocar_som(sons, "fechar")

                elif documento_aberto:
                    if botao_anterior.collidepoint(evento.pos):
                        # Só toca quando existe uma página anterior.
                        if pagina_atual > 0:
                            pagina_atual -= 1
                            tocar_som(sons, "pagina")

                    elif botao_proximo.collidepoint(evento.pos):
                        # Evita som ao tentar ultrapassar a última página.
                        if pagina_atual < len(paginas_codigos) - 1:
                            pagina_atual += 1
                            tocar_som(sons, "pagina")

                    elif not ficha_documento.collidepoint(evento.pos):
                        documento_aberto = False
                        tocar_som(sons, "fechar")

                elif (
                    visitante["documento"] is not None
                    and area_passe.collidepoint(evento.pos)
                ):
                    consulta_aberta = "passe"
                    tocar_som(sons, "abrir")

                elif area_moradores.collidepoint(evento.pos):
                    consulta_aberta = "moradores"
                    tocar_som(sons, "lista_abrir")

                elif area_scanner.collidepoint(evento.pos):
                    consulta_aberta = "scanner"
                    tocar_som(sons, "botao")


                elif area_interfone.collidepoint(evento.pos):
                    consulta_aberta = "interfone"
                    tocar_som(sons, "interfone_chamar")


                elif area_livro.collidepoint(evento.pos):
                    # Guarda qual consulta precisa aparecer na tela.
                    consulta_aberta = "livro"

                    # Reutiliza o efeito de papel já carregado.
                    tocar_som(sons, "abrir")

                elif area_calendario.collidepoint(evento.pos):
                    consulta_aberta = "calendario"
                    tocar_som(sons, "abrir")

                elif area_jornal.collidepoint(evento.pos):
                    consulta_aberta = "jornal"
                    tocar_som(sons, "abrir")

                elif documento.collidepoint(evento.pos):
                    documento_aberto = True
                    tocar_som(sons, "abrir")

                elif botao_liberar.collidepoint(evento.pos):
                    if vidas > 0 and decisao is None and visitante["estado"] == "aguardando":
                        decisao = "liberar"
                        tocar_som(sons, "botao")

                elif botao_recusar.collidepoint(evento.pos):
                    if vidas > 0 and decisao is None and visitante["estado"] == "aguardando":
                        decisao = "recusar"
                        tocar_som(sons, "botao")

                elif area_campainha.collidepoint(evento.pos):
                    if (
                        agora >= proximo_toque
                        and vidas > 0
                        and atendimentos < META_ATENDIMENTOS
                    ):
                        tocar_som(sons, "campainha")
                        # Inicia a chegada somente se ainda não houver visitante.
                        # Tocar novamente não reinicia o movimento.
                        if visitante["estado"] == "ausente":
                            # Sorteia primeiro o personagem e depois sua identidade.
                            personagem_id = choice(list(personagens))
                            personagem = personagens[personagem_id]

                            visitante["nome"] = personagem["nome"]

                            # Guarda as formas humana e IA deste personagem.
                            visitante["imagens"] = personagem["imagens"]

                            # Guarda a foto apresentada no documento.
                            visitante["foto"] = personagem["foto"]

                            visitante["tipo"] = choice(("humano", "ia"))

                            # Sorteia o caso uma única vez.
                            # Abrir consultas não muda os dados deste atendimento.
                            caso_sorteado = choice(
                                casos[personagem_id][visitante["tipo"]]
                            )

                            # Usa documento e roteiro do personagem sorteado.
                            documento_caso, roteiro_caso = montar_caso(
                                caso_sorteado,
                                modelos_documentos[personagem_id],
                                roteiros[personagem_id][visitante["tipo"]],
                                visitante["tipo"],
                            )

                            visitante["caso"] = caso_sorteado["id"]
                            visitante["modelo_documento"] = documento_caso

                            interfone = preparar_dialogo(
                                roteiro_caso, visitante["nome"]
                            )

                            # Todos chegam com aparência humana.
                            visitante["imagem"] = (
                                visitante["imagens"]["humano"].copy()
                            )

                            visitante["revelado"] = False
                            visitante["revelacao_ate"] = 0
                            visitante["registrado"] = False
                            visitante["documento"] = None

                            # A leitura anterior não pertence ao novo visitante.
                            scanner = criar_scanner()

                            # Recria o retângulo porque os personagens
                            # podem ter larguras diferentes.
                            visitante["rect"] = (
                                visitante["imagem"].get_rect()
                            )

                            # Posiciona o visitante fora da janela, à esquerda.
                            visitante["rect"].right = abertura_janela.left
                            visitante["rect"].bottom = (
                                abertura_janela.bottom + 20
                            )

                            visitante["x"] = float(visitante["rect"].x)

                            # Calcula o destino com a largura do novo sprite.
                            visitante["destino_x"] = (
                                abertura_janela.centerx
                                - visitante["rect"].width // 2
                            )

                            visitante["estado"] = "entrando"
                            decisao = None

                        campainha_pressionada_ate = agora + 150
                        aviso_campainha_ate = agora + 2500
                        proximo_toque = agora + 800

                elif area_luminaria.collidepoint(evento.pos):
                    luminaria_acesa = not luminaria_acesa

                    # Cada posição do interruptor possui seu efeito.
                    if luminaria_acesa:
                        tocar_som(sons, "luz_ligar")
                    else:
                        tocar_som(sons, "luz_desligar")

        # A leitura continua mesmo com outra consulta aberta.
        if scanner["estado"] == "lendo":
            if (
                visitante["estado"] != "aguardando"
                or decisao is not None
            ):
                # Cancela se o jogador decidir antes do término.
                scanner = criar_scanner()

            elif atualizar_scanner(
                scanner, agora, visitante["tipo"]
            ):
                # A função retorna True somente no quadro da conclusão.
                som = (
                    "scanner_falha"
                    if scanner["resultado"] == "inconclusivo"
                    else "scanner_ok"
                )
                tocar_som(sons, som)


        # Este bloco fica fora do for de eventos, mas dentro do while.
        if decisao is not None and not visitante["registrado"]:
            # Guarda as vidas para descobrir se houve perda.
            vidas_antes = vidas

            vidas, acertou = avaliar_decisao(
                visitante["tipo"], decisao, vidas
            )

            if vidas < vidas_antes:
                # Guarda o instante do impacto.
                # "registrado" impede repetir isso nos próximos quadros.
                efeito_dano["inicio"] = agora

            # Cada atendimento continua sendo contado uma única vez.
            atendimentos += 1

            if acertou:
                acertos += 1
            else:
                erros += 1

#=========================================================================================

            # Usa o horário fictício do expediente.
            segundos = horario_inicial + (agora - inicio_turno) // 1000
            hora = (
                f"{(segundos // 3600) % 24:02d}:"
                f"{(segundos // 60) % 60:02d}"
            )

            ocorrencias.append({
                "nome": visitante["nome"],
                "caso": visitante["caso"],
                "tipo": visitante["tipo"],
                "decisao": decisao,
                "acertou": acertou,
                "vidas": vidas,
                "data": data_partida.strftime("%d/%m/%Y"),
                "hora": hora,
            })

            salvar_ocorrencias(ocorrencias)

            # Abre a página que contém o registro mais recente.
            pagina_livro = (len(ocorrencias) - 1) // 3

            # Seleciona a reação correspondente à decisão.
            interfone["fala"] = interfone["roteiro"][decisao]
            interfone["fala_cena"] = interfone["fala"]

            tocar_som(sons, "interfone_resposta")

            # Impede novo desconto e novo registro nos próximos quadros.
            visitante["registrado"] = True

            visitante["revelado"] = True
            # Revela a forma do personagem deste atendimento.
            visitante["imagem"] = visitante["imagens"][
                visitante["tipo"]
            ].copy()

            # Escolhe a consequência da decisão.
            if decisao == "liberar":
                visitante["desfecho"] = "saindo"
            elif visitante["tipo"] == "ia":
                visitante["desfecho"] = "desativando"
            else:
                visitante["desfecho"] = "capturado"

            visitante["estado"] = "revelando"
            visitante["revelacao_ate"] = agora + 1200

        if visitante["estado"] == "entrando":
            # Atualiza a posição e move o retângulo usado no desenho.
            visitante["x"] = min(
                visitante["x"] + visitante["velocidade"] * tempo_frame,
                visitante["destino_x"],
            )
            visitante["rect"].x = round(visitante["x"])

            # A entrada termina quando ele chega ao centro.
            if visitante["x"] >= visitante["destino_x"]:
                visitante["estado"] = "aguardando"

        elif visitante["estado"] == "revelando":
            if agora >= visitante["revelacao_ate"]:
                visitante["estado"] = visitante["desfecho"]
                visitante["efeito_inicio"] = agora

                # Guarda a altura de onde o personagem começará a subir.
                visitante["captura_y"] = visitante["rect"].y

                # Localiza a borda inferior visível do sprite.
                fundo_corpo = (
                    visitante["rect"].top
                    + visitante["imagem"].get_bounding_rect().bottom
                )
                # Define quanto ele pode subir sem mostrar o corte do corpo.
                # O resultado fica entre 0 e 16 pixels.
                visitante["subida_maxima"] = min(
                    16,
                    max(0, fundo_corpo - abertura_janela.bottom - 4),
                )

        elif visitante["estado"] == "saindo":
            visitante["x"] += visitante["velocidade"] * tempo_frame
            visitante["rect"].x = round(visitante["x"])

            # A saída termina quando ele ultrapassa a abertura.
            if visitante["rect"].left >= abertura_janela.right:
                visitante["estado"] = "ausente"

        elif visitante["estado"] == "desativando":
            # A IA perde a opacidade durante 900 milissegundos.
            progresso = min(
                1, (agora - visitante["efeito_inicio"]) / 900
            )
            visitante["imagem"].set_alpha(
                round(255 * (1 - progresso))
            )

            if progresso >= 1:
                visitante["estado"] = "ausente"

        elif visitante["estado"] == "capturado":
            # O humano é puxado para a direita enquanto desaparece.
            tempo_captura = agora - visitante["efeito_inicio"]

            # Em 180 milissegundos, o corpo desaparece completamente.
            progresso = min(1, tempo_captura / 180)
            # A posição parte da altura original, evitando acumular movimento.
            visitante["rect"].y = round(
                visitante["captura_y"]
                - visitante["subida_maxima"] * progresso)
            # Alpha 255 = visível; alpha 0 = transparente.
            visitante["imagem"].set_alpha(
                round(255 * (1 - progresso))
            )
            # O feixe continua um pouco depois do desaparecimento.
            if tempo_captura >= 650:
                visitante["estado"] = "ausente"
#=========================================================================================
        # Recolhe o passe quando o visitante termina de sair.
        # Isso também cobre o reinício, que deixa o estado como ausente.
        if visitante["estado"] == "ausente":
            visitante["documento"] = None

            # Fecha a ficha caso ela ainda estivesse aberta.
            if consulta_aberta == "passe":
                consulta_aberta = None

        # Relátorio sobrepondo tudo que tem na tela
        resultado = verificar_fim_partida(
            vidas, atendimentos, META_ATENDIMENTOS
        )

        if (
            relatorio_final is None
            and resultado is not None
            and visitante["estado"] == "ausente"
        ):
            # Espera a última animação terminar.
            # Como deixa de ser None, o relatório não será recriado.
            relatorio_final = montar_relatorio(
                resultado,
                acertos,
                erros,
                inicio_partida,
                agora,
                datetime.now(),
                META_ATENDIMENTOS,
            )

            documento_aberto = False
            consulta_aberta = None


        # Pinta a parede da cabine antes de desenhar os outros elementos.
        tela.fill(CINZA)

        # A parede cobre o fundo inteiro.
        tela.blit(textura_parede, (0, 0))

        # Prancheta abaixo do relógio.
        tela.blit(sprite_moradores, area_moradores)

        tela.blit(
            rotulo_moradores,
            rotulo_moradores.get_rect(
                center=(
                    area_moradores.centerx,
                    area_moradores.bottom + 10,
                )
            ),
        )

        desenhar_vidas(tela, vidas, sprites_interface) # desenha os corações de vida

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

        # === Cria Jornal ===
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

        if visitante["estado"] != "ausente":
            # Guarda o recorte atual da tela.
            recorte_anterior = tela.get_clip()

            # Permite desenhar somente dentro da abertura.
            # Assim, o personagem passa por trás da parede.
            tela.set_clip(abertura_janela)
            if visitante["estado"] == "capturado":
                # Limpa o efeito desenhado no quadro anterior.
                camada_efeitos.fill((0, 0, 0, 0))
                centro_x = visitante["rect"].centerx

                # O feixe se estreita em direção ao alto da janela.
                pygame.draw.polygon(
                    camada_efeitos,
                    (110, 210, 255, 55),
                    [
                        (centro_x - 40, abertura_janela.top),
                        (centro_x + 40, abertura_janela.top),
                        (visitante["rect"].right, abertura_janela.bottom),
                        (visitante["rect"].left, abertura_janela.bottom),
                    ],
                )

                # Três traços subindo reforçam a direção da captura.
                for indice, deslocamento in enumerate((-25, 0, 25)):
                    y = abertura_janela.bottom - int(
                        (
                            (agora - visitante["efeito_inicio"]) * 0.5
                            + indice * 60
                        )
                        % abertura_janela.height
                    )

                    pygame.draw.line(
                        camada_efeitos,
                        (170, 235, 255, 150),
                        (centro_x + deslocamento, y),
                        (centro_x + deslocamento, y - 20),
                        2,
                    )

                tela.blit(camada_efeitos, (0, 0))

            tela.blit(visitante["imagem"], visitante["rect"])

            # Evita deixar o rótulo flutuando depois do desaparecimento.
            if visitante["revelado"] and visitante["estado"] != "capturado":
                tipo_real = visitante["tipo"].upper()

                if tipo_real == "IA":
                    cor_tipo = (190, 130, 255)
                else:
                    cor_tipo = (140, 240, 150)

                rotulo_tipo = fonte_consulta.render(
                    tipo_real, True, cor_tipo
                )

                # O rótulo acompanha o personagem durante a saída.
                tela.blit(
                    rotulo_tipo,
                    rotulo_tipo.get_rect(
                        midtop=(
                            visitante["rect"].centerx,
                            abertura_janela.top + 6,
                        )
                    ),
                )

            # Linhas piscando simulam o curto-circuito da IA.
            if visitante["estado"] == "desativando" and (agora // 80) % 2 == 0:
                for deslocamento in (60, 120, 180):
                    y = visitante["rect"].top + deslocamento

                    pygame.draw.line(
                        tela,
                        (210, 140, 255),
                        (visitante["rect"].left, y),
                        (visitante["rect"].right, y + 8),
                        3,
                    )
            # Restaura o desenho normal para o restante do cenário.
            tela.set_clip(recorte_anterior)

        # O peitoril aparece na frente do visitante.
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

        
        # === Pasta em cima da mesa ===
        tela.blit(sprite_arquivo, (pasta.left, aba_pasta.top))

        # ==== Desenha o livro sobre o balcão ====
        # A posição vem do retângulo criado antes do loop.
        tela.blit(sprite_livro, area_livro)


        # O passe aparece somente depois de ser solicitado.
        if visitante["documento"] is not None:
            tela.blit(visitante["sprite_passe"], area_passe)

        # Scanner ao lado do passe.
        tela.blit(sprite_scanner, area_scanner)

        # === Campainha em cima da mesa ===
        # Durante o toque, desloca o sprite um pouco para baixo.
        deslocamento = 0


        # Sombra de contato sobre a madeira.
        pygame.draw.ellipse(
            tela,
            (45, 30, 20),
            (
                area_campainha.left + 6,
                area_campainha.bottom - 8,
                area_campainha.width - 12,
                8,
            ),
        )

        if agora < campainha_pressionada_ate:
            deslocamento = 3

        tela.blit(
            sprite_campainha,
            area_campainha.move(0, deslocamento),
        )

        # O aviso desaparece automaticamente quando o prazo termina.
        if agora < aviso_campainha_ate:
            # Coloca o aviso na frente do balcão, abaixo dos objetos.
            fundo_aviso = pygame.Rect(300, 558, 240, 30)

            pygame.draw.rect(
                tela,
                (45, 39, 32),
                fundo_aviso,
                border_radius=4,
            )

            tela.blit(
                texto_campainha,
                texto_campainha.get_rect(center=fundo_aviso.center),
            )

#===========================================================================================

        # Aparelho fixado abaixo da janela.
        tela.blit(sprite_interfone, area_interfone)
        # Desenha o painel com os botões de autorizar e recusar.
        tela.blit(sprite_botoes, base_botoes)

        # Mostra a chegada ou a reação à decisão tomada.
        desenhar_fala_cena(
            tela, area_fala, fonte_fala, interfone, decisao
        )

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

        if (
            relatorio_final is not None
            and consulta_aberta is None
            and not documento_aberto
        ):
            desenhar_relatorio(
                tela,
                relatorio_final,
                sprites_interface,
                fonte,
                fonte_consulta,
            )

        # A consulta ampliada aparece sobre o cenário.
        if consulta_aberta is not None:
            pygame.draw.rect(
                tela, (55, 43, 31), ficha_documento.move(5, 5)
            )
            # O passe possui um fundo próprio.
            if consulta_aberta == "passe":
                tela.blit(sprite_documento, ficha_documento)
            else:
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

            elif consulta_aberta == "livro":
                # A folha e sua sombra já foram desenhadas acima.
                # Esta função acrescenta apenas o conteúdo do livro.
                desenhar_livro(
                    tela,
                    ficha_documento,
                    fonte,
                    fonte_consulta,
                    ocorrencias,
                    pagina_livro,
                    botao_anterior,
                    botao_proximo,
                )

            elif consulta_aberta == "interfone":
                desenhar_interfone(
                    tela,
                    ficha_documento,
                    fonte,
                    fonte_dialogo,
                    interfone,
                    botoes_perguntas,
                    visitante["estado"] == "aguardando",
                    visitante["documento"] is not None
                )

            elif consulta_aberta == "passe":
                desenhar_documento(
                    tela,
                    ficha_documento,
                    fonte,
                    fonte_consulta,
                    visitante["documento"],
                    visitante["foto"],
                )

            elif consulta_aberta == "moradores":
                desenhar_moradores(
                    tela,
                    ficha_documento,
                    fonte,
                    fonte_consulta,
                    moradores,
                    pagina_moradores,
                    botao_anterior,
                    botao_proximo,
                )

            elif consulta_aberta == "scanner":
                desenhar_scanner(
                    tela,
                    ficha_documento,
                    fonte,
                    fonte_consulta,
                    scanner,
                    agora,
                    visitante["estado"] == "aguardando"
                    and decisao is None,
                    botao_scanner,
                )

        # Aplica o impacto depois de desenhar todas as camadas.
        aplicar_efeito_dano(tela, efeito_dano, agora)

        pygame.display.flip() # Exibe o quadro depois que todas as camadas foram desenhadas.

    pygame.quit()