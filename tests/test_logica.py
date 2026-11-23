from src.funcoes import avaliar_decisao
from src.dados import carregar_ocorrencias, salvar_ocorrencias


def test_quatro_decisoes_possiveis():
    casos = [
        ("humano", "liberar", (3, True)),
        ("humano", "recusar", (2, False)),
        ("ia", "liberar", (2, False)),
        ("ia", "recusar", (3, True)),
    ]

    for tipo, decisao, esperado in casos:
        assert avaliar_decisao(tipo, decisao, 3) == esperado


def test_vidas_nao_ficam_negativas():
    assert avaliar_decisao("ia", "liberar", 0) == (0, False)


def test_historico_pode_ser_salvo_e_recuperado(tmp_path):
    # O pytest fornece uma pasta temporária para este teste.
    caminho = tmp_path / "ocorrencias.json"
    registros = [{"nome": "João", "acertou": True}]

    assert carregar_ocorrencias(caminho) == []

    salvar_ocorrencias(registros, caminho)

    assert carregar_ocorrencias(caminho) == registros