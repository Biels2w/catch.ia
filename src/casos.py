import json
from copy import deepcopy
from pathlib import Path


def carregar_casos():
    """Lê as variações uma vez, antes do loop."""
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "casos.json"
    )

    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def montar_caso(caso, modelos, roteiro_base, tipo):
    """Prepara documento e roteiro sem alterar os originais."""
    base = caso.get("base_documento", tipo)

    documento = deepcopy(modelos[base])

    # Alguns visitantes, como Gael, chegam sem documento.
    # Só aplicamos alterações quando existe um documento.
    if documento is not None:
        documento.update(caso.get("documento", {}))

    roteiro = deepcopy(roteiro_base)
    substituicoes = caso.get("respostas", {})

    acoes = {
        pergunta.get("acao")
        for pergunta in roteiro["perguntas"]
    }

    if not set(substituicoes).issubset(acoes):
        raise ValueError(
            "Marque as ações das perguntas no roteiro antes de usar o caso."
        )

    for pergunta in roteiro["perguntas"]:
        acao = pergunta.get("acao")

        if acao in substituicoes:
            pergunta["resposta"] = substituicoes[acao]

    for campo in ("chegada", "repetir"):
        if campo in caso:
            roteiro[campo] = caso[campo]

    return documento, roteiro