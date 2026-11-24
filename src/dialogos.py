import json
from pathlib import Path

import pygame


def carregar_dialogos():
    """Lê o roteiro uma vez, antes do loop principal."""
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "roteiros_interfone.json"
    )

    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def preparar_dialogo(roteiro=None):
    """Cria uma conversa nova para cada visitante."""
    chegada = (
        roteiro["chegada"]
        if roteiro
        else "Toque a campainha para chamar alguém."
    )

    return {
        "roteiro": roteiro,

        # Guarda os índices das perguntas já feitas.
        "perguntadas": set(),

        # Texto exibido na consulta aberta.
        "fala": chegada,

        # Texto curto exibido abaixo da janela.
        "fala_cena": chegada if roteiro else "",
    }


def responder_pergunta(interfone, indice):
    """Seleciona a resposta normal ou a reação de repetição."""
    roteiro = interfone["roteiro"]

    if roteiro is None:
        return False

    if not 0 <= indice < len(roteiro["perguntas"]):
        return False

    if indice in interfone["perguntadas"]:
        interfone["fala"] = roteiro["repetir"]
    else:
        interfone["fala"] = roteiro["perguntas"][indice]["resposta"]

        # O conjunto evita guardar o mesmo índice várias vezes.
        interfone["perguntadas"].add(indice)

    return True


def quebrar_texto(texto, fonte, largura):
    """Divide o texto em linhas que cabem na largura disponível."""
    linhas = []
    linha = ""

    for palavra in texto.split():
        tentativa = f"{linha} {palavra}".strip()

        # fonte.size informa o tamanho do texto em pixels.
        if linha and fonte.size(tentativa)[0] > largura:
            linhas.append(linha)
            linha = palavra
        else:
            linha = tentativa

    if linha:
        linhas.append(linha)

    return linhas


def desenhar_interfone(
    tela, area, fonte, fonte_dialogo,
    interfone, botoes, pode_perguntar
):
    """Desenha a conversa sobre a folha já exibida pelo jogo."""
    cor = (45, 42, 36)

    titulo = fonte.render("INTERFONE - LUCAS", True, cor)
    tela.blit(
        titulo,
        titulo.get_rect(center=(area.centerx, area.top + 38)),
    )

    roteiro = interfone["roteiro"]

    if roteiro is not None:
        for indice, botao in enumerate(botoes):
            # As perguntas ficam apagadas fora do atendimento.
            cor_botao = (
                (181, 180, 156)
                if pode_perguntar
                else (214, 207, 188)
            )

            pygame.draw.rect(
                tela, cor_botao, botao, border_radius=4
            )

            pergunta = roteiro["perguntas"][indice]["pergunta"]
            texto = fonte_dialogo.render(pergunta, True, cor)

            tela.blit(
                texto,
                texto.get_rect(center=botao.center),
            )

    rotulo = fonte_dialogo.render("Resposta:", True, cor)
    tela.blit(rotulo, (area.left + 20, area.top + 224))

    # Quebra a resposta longa para caber dentro da folha.
    linhas = quebrar_texto(
        interfone["fala"], fonte_dialogo, area.width - 40
    )

    for indice, linha in enumerate(linhas):
        imagem = fonte_dialogo.render(linha, True, cor)

        tela.blit(
            imagem,
            (area.left + 20, area.top + 248 + indice * 18),
        )

    aviso = fonte_dialogo.render(
        "Esc ou clique fora para fechar.", True, cor
    )

    tela.blit(
        aviso,
        aviso.get_rect(
            center=(area.centerx, area.bottom - 18)
        ),
    )


def desenhar_fala_cena(tela, area, fonte, interfone, decisao):
    """Mostra a chegada e a reação final abaixo da janela."""
    if not interfone["fala_cena"]:
        return

    pygame.draw.rect(
        tela, (35, 39, 44), area, border_radius=4
    )

    titulo = "Lucas"
    cor = (235, 225, 202)

    if decisao is not None:
        titulo = (
            "Entrada autorizada"
            if decisao == "liberar"
            else "Entrada recusada"
        )

        cor = (
            (120, 220, 145)
            if decisao == "liberar"
            else (255, 145, 145)
        )

    tela.blit(
        fonte.render(titulo, True, cor),
        (area.left + 8, area.top + 5),
    )

    linhas = quebrar_texto(
        interfone["fala_cena"], fonte, area.width - 16
    )

    for indice, linha in enumerate(linhas):
        tela.blit(
            fonte.render(linha, True, (235, 225, 202)),
            (area.left + 8, area.top + 23 + indice * 14),
        )