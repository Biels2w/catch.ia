import pygame
from math import sin, cos, radians, pi
from array import array

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

#====================================================================================

#FAZ A CAMPAINHA FUNCIONAR
def criar_som_campainha():
    #Gera um toque metálico e devolve um som do Pygame.

    configuracao = pygame.mixer.get_init()

    # Permite continuar o jogo caso o áudio não tenha iniciado.
    if configuracao is None:
        return None

    frequencia, formato, canais = configuracao

    if formato != -16:
        return None

    duracao = 0.7
    amostras = array("h")

    for indice in range(int(frequencia * duracao)):
        instante = indice / frequencia

        # O toque começa rapidamente e perde volume aos poucos.
        volume = (
            min(1, instante / 0.005)
            * (1 - instante / duracao) ** 3
        )

        # Combina duas frequências para produzir um toque metálico.
        onda = sin(2 * pi * 1046.5 * instante)
        onda += 0.35 * sin(2 * pi * 2888 * instante)

        valor = int(11000 * volume * onda)

        # Repete a amostra conforme a quantidade de canais de áudio.
        amostras.extend([valor] * canais)

    return pygame.mixer.Sound(buffer=amostras.tobytes())