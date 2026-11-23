from pathlib import Path

import pygame


def carregar_audio():
    """Carrega os efeitos e inicia a trilha ambiente em repetição."""
    if pygame.mixer.get_init() is None:
        return {}

    # Encontra a pasta de sons a partir da localização deste módulo.
    pasta = Path(__file__).resolve().parent.parent / "assets" / "sons"

    arquivos = {
        "abrir": ("abrir_arquivo.wav", 0.45),
        "fechar": ("fechar_arquivo.wav", 0.40),
        "pagina": ("virar_pagina.wav", 0.35),
        "luz_ligar": ("luz_ligar.wav", 0.40),
        "luz_desligar": ("luz_desligar.wav", 0.40),
        "campainha": ("campainha.wav", 0.50),
    }

    sons = {}

    # Os arquivos são carregados apenas uma vez, antes do loop.
    for nome, (arquivo, volume) in arquivos.items():
        som = pygame.mixer.Sound(str(pasta / arquivo))
        som.set_volume(volume)
        sons[nome] = som

    # A música usa um canal separado dos efeitos sonoros.
    pygame.mixer.music.load(str(pasta / "trilha_refugio.wav"))
    pygame.mixer.music.set_volume(0.22)
    pygame.mixer.music.play(-1, fade_ms=1500)

    return sons


def tocar_som(sons, nome):
    """Toca um efeito sem interromper o loop principal."""
    som = sons.get(nome)

    if som is not None:
        som.play()

