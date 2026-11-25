from src.documentos import carregar_documentos
from src.moradores import carregar_moradores, obter_pagina_moradores


def test_cadastro_de_lucas_confere_com_passe_humano():
    moradores = carregar_moradores()

    lucas = next(
        morador
        for morador in moradores
        if morador["nome"] == "Lucas"
    )

    documentos = carregar_documentos()["lucas"]

    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert lucas[campo] == documentos["humano"][campo]

    assert lucas["codigo"] != documentos["ia"]["codigo"]


def test_pagina_incompleta_e_limites():
    moradores = [
        {"nome": str(indice)}
        for indice in range(5)
    ]

    assert obter_pagina_moradores(
        moradores, 0
    ) == (moradores[:2], 3)

    # A última página contém somente o quinto registro.
    assert obter_pagina_moradores(
        moradores, 2
    ) == (moradores[4:], 3)

    # Valores fora dos limites são ajustados.
    assert obter_pagina_moradores(
        moradores, -1
    ) == (moradores[:2], 3)

    assert obter_pagina_moradores(
        moradores, 99
    ) == (moradores[4:], 3)


def test_cadastro_vazio():
    assert obter_pagina_moradores([], 0) == ([], 1)