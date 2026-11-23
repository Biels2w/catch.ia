from datetime import datetime

from src.relatorio import verificar_fim_partida, montar_relatorio


def test_condicoes_de_encerramento():
    assert verificar_fim_partida(3, 9, 10) is None
    assert verificar_fim_partida(1, 10, 10) == "vitoria"

    # A terceira falha no último atendimento ainda significa derrota.
    assert verificar_fim_partida(0, 10, 10) == "derrota"


def test_relatorio_da_partida():
    relatorio = montar_relatorio(
        "vitoria",
        8,
        2,
        5000,
        3728000,
        datetime(2026, 11, 23),
        10,
    )

    assert relatorio["duracao"] == "01:02:03"
    assert relatorio["data"] == "23/11/2026"
    assert relatorio["atendimentos"] == 10
    assert relatorio["acertos"] == 8
    assert relatorio["erros"] == 2