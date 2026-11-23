import calendar

import pygame


MESES = (
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro",
)


def desenhar_calendario(tela, area, data_partida, fonte, fonte_menor):
    """Desenha o calendário sobre a folha que já está na tela."""
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