import pygame


def verificar_fim_partida(vidas, atendimentos, meta):
    """Verifica se a partida terminou e devolve o resultado."""

    # Perder a última vida também causa derrota no décimo atendimento.
    if vidas <= 0:
        return "derrota"

    if atendimentos >= meta:
        return "vitoria"

    return None


def montar_relatorio(
    resultado, acertos, erros, inicio_ms, fim_ms, data_real, meta
):
    """Guarda os resultados; o tempo não muda depois disso."""

    segundos = max(0, fim_ms - inicio_ms) // 1000

    # divmod devolve o resultado da divisão inteira e o resto.
    horas, restante = divmod(segundos, 3600)
    minutos, segundos = divmod(restante, 60)

    return {
        "resultado": resultado,
        "data": data_real.strftime("%d/%m/%Y"),
        "duracao": f"{horas:02d}:{minutos:02d}:{segundos:02d}",
        "acertos": acertos,
        "erros": erros,
        "atendimentos": acertos + erros,
        "meta": meta,
    }


def desenhar_relatorio(
    tela, relatorio, sprites, fonte, fonte_menor
):
    """Desenha os dados sobre a folha do relatório."""

    # Escurece o cenário para destacar o resultado.
    sombra = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 175))
    tela.blit(sombra, (0, 0))

    tela.blit(sprites["fundo_relatorio"], (180, 65))

    # Função auxiliar usada somente dentro deste desenho.
    def centralizar(texto, y, fonte_usada, cor=(50, 43, 35)):
        imagem = fonte_usada.render(texto, True, cor)
        tela.blit(imagem, imagem.get_rect(center=(400, y)))

    centralizar("RELATÓRIO DO TURNO", 115, fonte)

    venceu = relatorio["resultado"] == "vitoria"
    nome_icone = "icone_vitoria" if venceu else "icone_derrota"
    icone = sprites[nome_icone]

    tela.blit(icone, icone.get_rect(center=(400, 180)))

    centralizar(
        "VITÓRIA" if venceu else "DERROTA",
        235,
        fonte,
        (45, 105, 75) if venceu else (155, 50, 50),
    )

    # Cada tupla contém um rótulo e o valor correspondente.
    linhas = [
        ("Data:", relatorio["data"]),
        ("Duração:", relatorio["duracao"]),
        (
            "Atendimentos:",
            f'{relatorio["atendimentos"]} / {relatorio["meta"]}',
        ),
        ("Acertos:", str(relatorio["acertos"])),
        ("Erros:", str(relatorio["erros"])),
    ]

    for indice, (rotulo, valor) in enumerate(linhas):
        y = 278 + indice * 34

        imagem_rotulo = fonte_menor.render(
            rotulo, True, (50, 43, 35)
        )
        imagem_valor = fonte_menor.render(
            valor, True, (50, 43, 35)
        )

        tela.blit(imagem_rotulo, (225, y))

        # Alinha os valores pela margem direita.
        tela.blit(
            imagem_valor,
            imagem_valor.get_rect(topright=(575, y)),
        )

    centralizar(
        "R: novo turno | B: ocorrências",
        495,
        fonte_menor,
    )