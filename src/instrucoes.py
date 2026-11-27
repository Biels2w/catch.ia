import pygame

from src.audio import tocar_som
from src.config import FPS, META_ATENDIMENTOS
from src.dialogos import quebrar_texto


# Cada dicionário representa uma página do guia inicial.
PAGINAS = [
    {
        "titulo": "Sua missão",
        "textos": [
            "Você fiscaliza a entrada de um refúgio humano. Compare as pistas antes de decidir.",
            "Toque a campainha e espere o visitante chegar ao centro da janela.",
            "O botão verde autoriza e o vermelho recusa. Autorizar uma IA ou recusar um humano custa uma vida.",
            f"Você começa com 3 vidas. Conclua {META_ATENDIMENTOS} atendimentos com pelo menos uma vida para vencer.",
            "O scanner pode errar. Compare documentos, respostas, cadastro e datas.",
            "Alguns humanos chegam sem documento. Reúna pistas antes de decidir.",
        ],
    },
    {
        "titulo": "Itens sobre a mesa",
        "textos": [
            "Pasta: abre o manual de códigos permitidos. Use os botões para trocar de página.",
            "Campainha: chama o próximo visitante quando o posto está livre.",
            "Documento: aparece após pedir os documentos no interfone. Clique no passe para ampliar.",
            "Livro: registra decisões, acertos e erros; possui botões de navegação.",
            "Scanner: inicie a leitura e aguarde. Uma leitura inconclusiva pode ser repetida.",
            "Luminária: clique para acender ou apagar a iluminação da mesa.",
        ],
    },
    {
        "titulo": "Parede, visitas e controles",
        "textos": [
            "Interfone: faça perguntas, peça documentos e observe as respostas repetidas.",
            "Moradores: confira nome, código, nascimento e setor. Alguns moradores só recebem visitas.",
            "Visitas: o setor de quem recebe a visita pode ser diferente do setor do visitante.",
            "Calendário e relógio: mostram a data e o horário fictícios do expediente.",
            "Jornal: apresenta avisos sobre os riscos e as limitações dos equipamentos.",
            "Use o mouse. Esc fecha consultas. No resultado, R reinicia e B abre o livro.",
        ],
    },
]


def mostrar_instrucoes(tela, sons):
    """Retorna True para iniciar a partida ou False para encerrar."""
    pagina = 0
    relogio = pygame.time.Clock()

    titulo = pygame.font.Font(None, 42)
    subtitulo = pygame.font.Font(None, 28)
    fonte = pygame.font.Font(None, 22)
    pequena = pygame.font.Font(None, 18)

    anterior = pygame.Rect(70, 510, 140, 40)
    proximo = pygame.Rect(590, 510, 140, 40)

    # Este loop termina antes de começar o loop da partida.
    while True:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            voltar = False
            avancar = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False

                voltar = evento.key == pygame.K_LEFT
                avancar = evento.key in (
                    pygame.K_RIGHT,
                    pygame.K_RETURN,
                )

            elif (
                evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):
                voltar = anterior.collidepoint(evento.pos)
                avancar = proximo.collidepoint(evento.pos)

            if voltar and pagina > 0:
                pagina -= 1
                tocar_som(sons, "botao")

            if avancar:
                tocar_som(sons, "botao")

                # A última página inicia o jogo.
                if pagina == len(PAGINAS) - 1:
                    return True

                pagina += 1

        tela.fill((35, 40, 46))

        pygame.draw.rect(
            tela,
            (48, 55, 63),
            (40, 30, 720, 540),
            border_radius=12,
        )

        for texto, fonte_usada, y in [
            ("Catch.IA - Instruções", titulo, 75),
            (PAGINAS[pagina]["titulo"], subtitulo, 125),
        ]:
            imagem = fonte_usada.render(
                texto, True, (242, 234, 211)
            )
            tela.blit(
                imagem,
                imagem.get_rect(center=(400, y)),
            )

        # Quebra os parágrafos para caberem no painel.
        y = 165

        for texto in PAGINAS[pagina]["textos"]:
            for linha in quebrar_texto(texto, fonte, 640):
                tela.blit(
                    fonte.render(linha, True, (235, 235, 230)),
                    (80, y),
                )
                y += 22

            y += 12

        ultima = pagina == len(PAGINAS) - 1

        for area, rotulo, cor in [
            (
                anterior,
                "Anterior",
                (85, 94, 104) if pagina > 0 else (57, 64, 72),
            ),
            (
                proximo,
                "Iniciar" if ultima else "Próxima",
                (55, 115, 80),
            ),
        ]:
            pygame.draw.rect(
                tela, cor, area, border_radius=6
            )

            texto = fonte.render(
                rotulo, True, (245, 240, 225)
            )

            tela.blit(
                texto,
                texto.get_rect(center=area.center),
            )

        numero = fonte.render(
            f"{pagina + 1} / {len(PAGINAS)}",
            True,
            (242, 234, 211),
        )
        tela.blit(
            numero,
            numero.get_rect(center=(400, 530)),
        )

        aviso = pequena.render(
            "Setas ou clique: navegar | Enter: avançar | Esc: sair",
            True,
            (210, 210, 205),
        )
        tela.blit(
            aviso,
            aviso.get_rect(center=(400, 480)),
        )

        pygame.display.flip()