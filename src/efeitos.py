from math import sin, cos

import pygame

# efeito feito pelo CHATGPT

def criar_efeito_dano(tamanho):
    """Prepara as rachaduras uma única vez, antes do loop."""
    largura, altura = tamanho

    # Superfície transparente que ficará sobre o jogo.
    camada = pygame.Surface(tamanho, pygame.SRCALPHA)

    # Tom avermelhado discreto durante o impacto.
    camada.fill((140, 15, 25, 30))

    # Coordenadas proporcionais: 0 representa o começo da tela e 1, o final.
    # Cada lista representa uma rachadura com pequenas curvas.
    caminhos = [
        [(0.54, 0.43), (0.43, 0.36), (0.38, 0.22), (0.24, 0.13), (0.18, 0.00)],
        [(0.54, 0.43), (0.60, 0.28), (0.58, 0.15), (0.70, 0.00)],
        [(0.54, 0.43), (0.69, 0.39), (0.78, 0.25), (1.00, 0.16)],
        [(0.54, 0.43), (0.71, 0.53), (0.83, 0.51), (1.00, 0.65)],
        [(0.54, 0.43), (0.56, 0.62), (0.68, 0.76), (0.64, 1.00)],
        [(0.54, 0.43), (0.40, 0.54), (0.32, 0.73), (0.15, 1.00)],
        [(0.54, 0.43), (0.34, 0.44), (0.20, 0.52), (0.00, 0.40)],

        # Ramificações menores das rachaduras principais.
        [(0.38, 0.22), (0.24, 0.28), (0.12, 0.21)],
        [(0.78, 0.25), (0.82, 0.13), (0.94, 0.07)],
        [(0.83, 0.51), (0.89, 0.42), (1.00, 0.43)],
        [(0.68, 0.76), (0.83, 0.81), (0.90, 0.96)],
        [(0.32, 0.73), (0.19, 0.70), (0.07, 0.81)],
        [(0.20, 0.52), (0.15, 0.63), (0.00, 0.66)],
    ]

    for caminho in caminhos:
        # Converte as proporções em posições de pixels.
        pontos = [
            (round(x * largura), round(y * altura))
            for x, y in caminho
        ]

        # A linha escura forma a borda da rachadura.
        pygame.draw.lines(
            camada, (15, 20, 25, 170), False, pontos, 3
        )

        # A linha clara e fina dá aparência de vidro rachado.
        pygame.draw.lines(
            camada, (210, 225, 230, 210), False, pontos, 1
        )

    return {
        "camada": camada,
        "inicio": None,  # None significa que o efeito está desligado.
        "duracao": 650,  # Duração em milissegundos.
        "forca": 6,      # Deslocamento máximo em pixels.
    }


def aplicar_efeito_dano(tela, efeito, agora):
    """Aplica o efeito sobre o quadro completo antes de exibi-lo."""

    # Sem perda de vida recente, não precisa desenhar o efeito.
    if efeito["inicio"] is None:
        return

    tempo = agora - efeito["inicio"]

    # Desliga o efeito quando sua duração termina.
    if tempo >= efeito["duracao"]:
        efeito["inicio"] = None
        return

    # Começa em 1 e diminui até chegar próximo de 0.
    intensidade = 1 - tempo / efeito["duracao"]

    # As rachaduras e o vermelho desaparecem gradualmente.
    efeito["camada"].set_alpha(round(255 * intensidade))
    tela.blit(efeito["camada"], (0, 0))

    # Copia tudo que já foi desenhado: cenário, personagem e consultas.
    quadro = tela.copy()

    # O tremor também diminui conforme o efeito termina.
    forca = efeito["forca"] * intensidade

    # Seno e cosseno alternam o movimento em direções diferentes.
    deslocamento_x = round(sin(tempo * 0.08) * forca)
    deslocamento_y = round(cos(tempo * 0.11) * forca)

    # Preenche as pequenas bordas expostas pelo deslocamento.
    tela.fill((15, 18, 22))

    # Desenha o quadro inteiro levemente deslocado.
    tela.blit(quadro, (deslocamento_x, deslocamento_y))