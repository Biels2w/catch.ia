def avaliar_decisao(tipo, decisao, vidas):
    """Retorna as vidas atualizadas e informa se houve acerto."""
    if tipo not in ("humano", "ia") or decisao not in ("liberar", "recusar"):
        raise ValueError("Tipo de visitante ou decisão inválidos.")

    acertou = (
        (tipo == "humano" and decisao == "liberar")
        or (tipo == "ia" and decisao == "recusar")
    )

    # Um erro retira uma vida; o valor nunca fica negativo.
    return max(0, vidas - (0 if acertou else 1)), acertou