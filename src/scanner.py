from random import random

import pygame


def criar_scanner():
    """Cria um scanner sem leitura associada ao visitante."""
    return {
        "estado": "pronto",
        "inicio": 0,
        "duracao": 2200,
        "resultado": None,
        "nome": None,
    }


def iniciar_leitura(scanner, agora, nome):
    """Inicia a primeira leitura ou repete uma leitura inconclusiva."""
    if scanner["estado"] == "lendo":
        return False

    # Um resultado concluído fica guardado até o próximo visitante.
    if scanner["resultado"] in ("regular", "irregular"):
        return False

    scanner.update(
        estado="lendo",
        inicio=agora,
        resultado=None,
        nome=nome,
    )
    return True


def sortear_resultado(tipo, sorteio=None):
    """Simula limitações do equipamento sem mudar a identidade real."""
    if tipo not in ("humano", "ia"):
        raise ValueError("Tipo de visitante inválido.")

    # O parâmetro sorteio permite testar resultados específicos.
    valor = random() if sorteio is None else sorteio

    # 25% das tentativas não conseguem concluir a leitura.
    if valor < 0.25:
        return "inconclusivo"

    resultado = "regular" if tipo == "humano" else "irregular"

    # Outros 15% produzem um indício incorreto.
    if valor < 0.40:
        resultado = (
            "irregular" if resultado == "regular" else "regular"
        )

    return resultado


def atualizar_scanner(scanner, agora, tipo, sorteio=None):
    """Conclui a leitura uma única vez, depois do prazo."""
    if scanner["estado"] != "lendo":
        return False

    if agora - scanner["inicio"] < scanner["duracao"]:
        return False

    scanner["resultado"] = sortear_resultado(tipo, sorteio)
    scanner["estado"] = "finalizado"
    return True


def desenhar_scanner(
    tela, area, fonte, fonte_menor,
    scanner, agora, pode_ler, botao
):
    """Desenha o painel, o progresso e o indício da última leitura."""
    pygame.draw.rect(tela, (28, 39, 43), area)
    pygame.draw.rect(tela, (75, 130, 132), area, 2)

    # Função auxiliar para centralizar os textos do painel.
    def centralizar(
        texto, y, cor=(220, 232, 222), fonte_usada=fonte_menor
    ):
        imagem = fonte_usada.render(texto, True, cor)
        tela.blit(
            imagem,
            imagem.get_rect(center=(area.centerx, y)),
        )

    centralizar(
        "SCANNER", area.top + 38, (120, 225, 205), fonte
    )
    centralizar(
        "Leitura biométrica simulada", area.top + 70
    )

    nome = scanner["nome"] or "Nenhum"
    centralizar(f"Última leitura: {nome}", area.top + 100)

    progresso = 0

    if scanner["estado"] == "lendo":
        progresso = min(
            1,
            max(
                0,
                (agora - scanner["inicio"]) / scanner["duracao"],
            ),
        )
    elif scanner["estado"] == "finalizado":
        progresso = 1

    barra = pygame.Rect(
        area.left + 30,
        area.top + 135,
        area.width - 60,
        18,
    )
    pygame.draw.rect(tela, (13, 24, 28), barra)

    preenchimento = barra.copy()
    preenchimento.width = round(barra.width * progresso)
    pygame.draw.rect(tela, (85, 195, 170), preenchimento)

    mensagens = {
        None: (
            "Pronto para iniciar" if pode_ler else "Chame um visitante",
            (220, 232, 222),
        ),
        "regular": (
            "Padrão biológico aparente",
            (120, 220, 170),
        ),
        "irregular": (
            "Padrão atípico detectado",
            (245, 190, 100),
        ),
        "inconclusivo": (
            "Leitura inconclusiva",
            (245, 190, 100),
        ),
    }

    mensagem, cor = mensagens[scanner["resultado"]]

    if scanner["estado"] == "lendo":
        mensagem = "Analisando..."
        cor = (120, 225, 205)

    centralizar(mensagem, area.top + 195, cor)
    centralizar(
        "Leitura auxiliar: pode falhar.", area.top + 235
    )
    centralizar(
        "Compare o passe, a lista e as respostas.",
        area.top + 260,
    )

    habilitado = (
        pode_ler
        and scanner["estado"] != "lendo"
        and scanner["resultado"] not in ("regular", "irregular")
    )

    pygame.draw.rect(
        tela,
        (65, 130, 120) if habilitado else (60, 75, 77),
        botao,
        border_radius=4,
    )

    rotulo = "Iniciar leitura"

    if scanner["estado"] == "lendo":
        rotulo = "Lendo..."
    elif scanner["resultado"] == "inconclusivo":
        rotulo = "Tentar novamente"
    elif scanner["resultado"] is not None:
        rotulo = "Leitura registrada"

    centralizar(
        rotulo, botao.centery, fonte_usada=fonte
    )
    centralizar(
        "Esc ou clique fora para fechar.",
        area.bottom - 18,
    )