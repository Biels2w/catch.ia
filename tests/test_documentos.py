from src.documentos import carregar_documentos, entregar_documento


def test_documento_e_entregue_uma_unica_vez():
    modelos = carregar_documentos()["lucas"]
    visitante = {"documento": None}

    assert entregar_documento(visitante, modelos["humano"]) is True
    assert visitante["documento"]["codigo"] == "V-012"

    # Outra solicitação não troca o documento já entregue.
    assert entregar_documento(visitante, modelos["ia"]) is False
    assert visitante["documento"]["codigo"] == "V-012"


def test_documento_entregue_nao_modifica_o_modelo():
    modelo = carregar_documentos()["lucas"]["humano"]
    visitante = {"documento": None}

    entregar_documento(visitante, modelo)
    visitante["documento"]["nome"] = "Outro nome"

    assert modelo["nome"] == "Lucas"


def test_dados_publicos_nao_incluem_identidade_real():
    modelos = carregar_documentos()["lucas"]

    assert modelos["humano"]["codigo"] != modelos["ia"]["codigo"]

    for dados in modelos.values():
        assert "tipo" not in dados

        assert set(dados) == {
            "nome",
            "registro",
            "codigo",
            "nascimento",
            "setor",
            "validade",
        }