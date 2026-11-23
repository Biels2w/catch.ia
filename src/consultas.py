import calendar

import pygame

from datetime import timedelta


MESES = (
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro",
)


def desenhar_calendario(tela, area, data_partida, fonte, fonte_menor):
    #Desenha o calendário sobre a folha que já está na tela.
    cor_texto = (45, 42, 36)

    titulo = fonte.render("CALENDÁRIO DO POSTO", True, cor_texto)
    tela.blit(titulo, (area.left + 20, area.top + 25))

    texto_data = fonte_menor.render(
        f"Data atual: {data_partida:%d/%m/%Y}",
        True,
        cor_texto,
    )
    tela.blit(texto_data, (area.left + 20, area.top + 62))

    # O mês é convertido de 1–12 para o índice 0–11 da tupla.
    texto_mes = fonte.render(
        f"{MESES[data_partida.month - 1]} de {data_partida.year}",
        True,
        cor_texto,
    )
    tela.blit(
        texto_mes,
        texto_mes.get_rect(center=(area.centerx, area.top + 110)),
    )

    # Cada lista representa uma semana. Zero representa uma célula vazia.
    semanas = calendar.Calendar(firstweekday=0).monthdayscalendar(
        data_partida.year, data_partida.month
    )

    largura_celula = 46
    inicio_x = area.centerx - (7 * largura_celula) // 2
    dias_semana = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")

    for coluna, nome_dia in enumerate(dias_semana):
        centro_x = inicio_x + coluna * largura_celula + largura_celula // 2
        texto = fonte_menor.render(nome_dia, True, cor_texto)
        tela.blit(
            texto,
            texto.get_rect(center=(centro_x, area.top + 150)),
        )

    for linha, semana in enumerate(semanas):
        for coluna, dia in enumerate(semana):
            if dia == 0:
                continue

            centro_x = inicio_x + coluna * largura_celula + largura_celula // 2
            centro_y = area.top + 184 + linha * 32

            # Destaca o dia atual da partida.
            if dia == data_partida.day:
                pygame.draw.circle(
                    tela, (144, 55, 48), (centro_x, centro_y), 14
                )
                cor_dia = (255, 248, 230)
            else:
                cor_dia = cor_texto

            texto = fonte_menor.render(str(dia), True, cor_dia)
            tela.blit(
                texto,
                texto.get_rect(center=(centro_x, centro_y)),
            )

    aviso = fonte_menor.render(
        "Clique fora ou Esc para fechar.", True, cor_texto
    )
    tela.blit(
        aviso,
        aviso.get_rect(center=(area.centerx, area.bottom - 25)),
    )

#==================================================================================

def desenhar_jornal(tela, area, data_partida, noticias, fonte, fonte_menor):
    #Desenha a edição semanal e seus avisos sobre a folha.
    cor_texto = (45, 42, 36)

    titulo = fonte.render("BOLETIM DO REFÚGIO", True, cor_texto)
    tela.blit(
        titulo,
        titulo.get_rect(center=(area.centerx, area.top + 38)),
    )

    # weekday() retorna 0 na segunda-feira e 6 no domingo.
    # Voltamos até a segunda para encontrar o início da edição semanal.
    inicio_semana = data_partida - timedelta(days=data_partida.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    periodo = fonte_menor.render(
        f"Semana de {inicio_semana:%d/%m} a {fim_semana:%d/%m/%Y}",
        True,
        cor_texto,
    )
    tela.blit(
        periodo,
        periodo.get_rect(center=(area.centerx, area.top + 73)),
    )

    pygame.draw.line(
        tela,
        (155, 140, 110),
        (area.left + 20, area.top + 94),
        (area.right - 20, area.top + 94),
        2,
    )

    # A posição vertical avança conforme desenhamos cada notícia.
    y = area.top + 112

    for noticia in noticias:
        manchete = fonte.render(
            noticia["titulo"], True, (116, 46, 39)
        )
        tela.blit(manchete, (area.left + 20, y))
        y += 27

        for linha in noticia["linhas"]:
            texto = fonte_menor.render(linha, True, cor_texto)
            tela.blit(texto, (area.left + 20, y))
            y += 22

        y += 13

    aviso = fonte_menor.render(
        "Clique fora ou Esc para fechar.", True, cor_texto
    )
    tela.blit(
        aviso,
        aviso.get_rect(center=(area.centerx, area.bottom - 18)),
    )

#==================================================================================

def desenhar_livro(tela, area, fonte, fonte_menor):
    #Desenha o conteúdo do livro sobre a folha já exibida pelo jogo.

    cor_texto = (45, 42, 36)

    # Render transforma o texto em uma imagem.
    titulo = fonte.render(
        "LIVRO DE OCORRÊNCIAS", True, cor_texto
    )

    # Centraliza o título usando a posição da folha recebida.
    tela.blit(
        titulo,
        titulo.get_rect(center=(area.centerx, area.top + 38)),
    )

    # Separa o cabeçalho do espaço destinado aos registros.
    pygame.draw.line(
        tela,
        (155, 140, 110),
        (area.left + 20, area.top + 72),
        (area.right - 20, area.top + 72),
        2,
    )

    # Por enquanto, o livro apresenta uma página vazia.
    mensagem = fonte_menor.render(
        "Nenhuma ocorrência registrada.", True, cor_texto
    )
    tela.blit(mensagem, (area.left + 20, area.top + 105))

    # Desenha as linhas da página, avançando 40 pixels por linha.
    for y in range(area.top + 160, area.bottom - 60, 40):
        pygame.draw.line(
            tela,
            (190, 177, 148),
            (area.left + 20, y),
            (area.right - 20, y),
            1,
        )

    aviso = fonte_menor.render(
        "Clique fora ou Esc para fechar.", True, cor_texto
    )
    tela.blit(
        aviso,
        aviso.get_rect(center=(area.centerx, area.bottom - 25)),
    )