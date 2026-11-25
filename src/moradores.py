import json
from pathlib import Path

import pygame


def carregar_moradores():
    """Lê o cadastro uma vez e organiza os nomes."""
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "moradores.json"
    )

    with caminho.open(encoding="utf-8") as arquivo:
        moradores = json.load(arquivo)

    # Organiza os registros pelo nome, em ordem alfabética.
    return sorted(
        moradores,
        key=lambda morador: morador["nome"].lower(),
    )


def obter_pagina_moradores(moradores, pagina):
    """Devolve os dois registros da página e o total de páginas."""

    # Soma 1 antes da divisão para contar uma última página incompleta.
    # Mesmo um cadastro vazio apresenta a página 1 de 1.
    total_paginas = max(1, (len(moradores) + 1) // 2)

    # Impede acessar páginas anteriores à primeira ou posteriores à última.
    pagina = max(0, min(pagina, total_paginas - 1))

    inicio = pagina * 2
    return moradores[inicio:inicio + 2], total_paginas

#================================================================================

def desenhar_moradores(
    tela, area, fonte, fonte_menor,
    moradores, pagina, anterior, proximo
):
    """Desenha o cadastro sobre a folha já exibida pelo jogo."""
    cor = (45, 42, 36)

    registros, total_paginas = obter_pagina_moradores(
        moradores, pagina
    )

    pagina = max(0, min(pagina, total_paginas - 1))

    titulo = fonte.render("LISTA DE MORADORES", True, cor)
    tela.blit(
        titulo,
        titulo.get_rect(center=(area.centerx, area.top + 38)),
    )

    subtitulo = fonte_menor.render(
        "Cadastro de referência", True, cor
    )
    tela.blit(
        subtitulo,
        subtitulo.get_rect(
            center=(area.centerx, area.top + 62)
        ),
    )

    if not registros:
        aviso = fonte_menor.render(
            "Nenhum morador cadastrado.", True, cor
        )
        tela.blit(aviso, (area.left + 20, area.top + 100))

    for indice, morador in enumerate(registros):
        # Cada cadastro ocupa um espaço vertical de 116 pixels.
        y = area.top + 92 + indice * 116

        tela.blit(
            fonte.render(morador["nome"], True, cor),
            (area.left + 20, y),
        )

        for rotulo, campo, deslocamento in [
            ("Código", "codigo", 28),
            ("Nascimento", "nascimento", 50),
            ("Setor", "setor", 72),
        ]:
            texto = f"{rotulo}: {morador[campo]}"

            tela.blit(
                fonte_menor.render(texto, True, cor),
                (area.left + 20, y + deslocamento),
            )

        pygame.draw.line(
            tela,
            (175, 158, 126),
            (area.left + 20, y + 100),
            (area.right - 20, y + 100),
            1,
        )

    # Reutiliza os botões de navegação das outras consultas.
    for botao, rotulo, ativo in [
        (anterior, "Anterior", pagina > 0),
        (proximo, "Próxima", pagina < total_paginas - 1),
    ]:
        cor_botao = (
            (180, 166, 135) if ativo else (220, 211, 190)
        )

        pygame.draw.rect(
            tela, cor_botao, botao, border_radius=4
        )

        texto = fonte.render(rotulo, True, cor)
        tela.blit(texto, texto.get_rect(center=botao.center))

    numero = fonte.render(
        f"{pagina + 1} / {total_paginas}", True, cor
    )
    tela.blit(
        numero,
        numero.get_rect(
            center=(area.centerx, anterior.centery)
        ),
    )