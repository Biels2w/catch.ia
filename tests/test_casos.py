from copy import deepcopy
from datetime import date, datetime

from src.casos import carregar_casos, montar_caso
from src.dialogos import carregar_dialogos
from src.documentos import carregar_documentos
from src.moradores import carregar_moradores


def montar_lucas(caso, tipo):
    """Auxiliar usado pelos testes."""
    return montar_caso(
        caso,
        carregar_documentos()["lucas"],
        carregar_dialogos()["lucas"][tipo],
        tipo,
    )


def test_caso_nao_modifica_modelos_e_roteiro_original():
    modelos = carregar_documentos()["lucas"]
    roteiro_base = carregar_dialogos()["lucas"]["ia"]

    copia_modelos = deepcopy(modelos)
    copia_roteiro = deepcopy(roteiro_base)

    caso = carregar_casos()["lucas"]["ia"][-1]

    documento, roteiro = montar_caso(
        caso, modelos, roteiro_base, "ia"
    )

    documento["nome"] = "Outro nome"
    roteiro["perguntas"][0]["resposta"] = "Outra resposta"

    assert modelos == copia_modelos
    assert roteiro_base == copia_roteiro


def test_cadastro_clonado_exige_conferir_a_resposta():
    caso = carregar_casos()["lucas"]["ia"][-1]
    documento, roteiro = montar_lucas(caso, "ia")

    assert documento == carregar_documentos()["lucas"]["humano"]

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "B-02" in motivo["resposta"]

    # A pista continua acessível quando a pergunta é repetida.
    assert "B-02" in roteiro["repetir"]


def test_cada_caso_ia_tem_uma_contradicao_verificavel():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Lucas"
    )

    for caso in carregar_casos()["lucas"]["ia"]:
        documento, roteiro = montar_lucas(caso, "ia")

        dados_divergem = any(
            documento[campo] != cadastro[campo]
            for campo in ("nome", "codigo", "nascimento", "setor")
        )

        vencido = (
            datetime.strptime(
                documento["validade"], "%d/%m/%Y"
            ).date()
            < date(2042, 11, 22)
        )

        fala_diverge = any(
            pergunta.get("acao") == "informar_motivo"
            and "B-02" in pergunta["resposta"]
            for pergunta in roteiro["perguntas"]
        )

        assert dados_divergem or vencido or fala_diverge, caso["id"]


def test_humano_preserva_documento_e_roteiro():
    caso = carregar_casos()["lucas"]["humano"][0]
    documento, roteiro = montar_lucas(caso, "humano")

    assert documento == carregar_documentos()["lucas"]["humano"]
    assert roteiro == carregar_dialogos()["lucas"]["humano"]