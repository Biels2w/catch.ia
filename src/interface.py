from math import sin, cos, radians

import pygame


def desenhar_relogio(tela, sprite, area, segundos_turno):
    """Desenha a base do relógio e seus três ponteiros."""
    tela.blit(sprite, area)
    centro = area.center

    # Converte o tempo do expediente em horas, minutos e segundos.
    horas = (segundos_turno // 3600) % 24
    minutos = (segundos_turno // 60) % 60
    segundos = segundos_turno % 60

    def ponta_ponteiro(angulo, comprimento):
        """Calcula onde termina cada ponteiro."""
        # Faz o ângulo zero apontar para o número 12.
        angulo = radians(angulo - 90)

        return (
            round(centro[0] + cos(angulo) * comprimento),
            round(centro[1] + sin(angulo) * comprimento),
        )

    # Cada tupla contém: ângulo, comprimento, cor e espessura.
    ponteiros = [
        (
            (horas % 12) * 30 + minutos * 0.5,
            area.width * 0.18,
            (45, 40, 35),
            4,
        ),
        (
            minutos * 6 + segundos * 0.1,
            area.width * 0.27,
            (45, 40, 35),
            3,
        ),
        (
            segundos * 6,
            area.width * 0.33,
            (160, 50, 40),
            1,
        ),
    ]

    for angulo, comprimento, cor, espessura in ponteiros:
        pygame.draw.line(
            tela,
            cor,
            centro,
            ponta_ponteiro(angulo, comprimento),
            espessura,
        )

    # Acabamento no encontro dos ponteiros.
    pygame.draw.circle(tela, (55, 48, 40), centro, 4)


def desenhar_vidas(tela, vidas, sprites):
    """Desenha três corações, preenchidos conforme as vidas restantes."""
    for indice in range(3):
        nome = "coracao_cheio" if indice < vidas else "coracao_vazio"

        # Posiciona os corações lado a lado.
        tela.blit(sprites[nome], (24 + indice * 34, 24))