from src.scanner import (
    criar_scanner,
    iniciar_leitura,
    sortear_resultado,
    atualizar_scanner,
)


def test_scanner_pode_falhar_ou_inverter_o_indicio():
    assert sortear_resultado("humano", 0.10) == "inconclusivo"
    assert sortear_resultado("ia", 0.10) == "inconclusivo"

    assert sortear_resultado("humano", 0.30) == "irregular"
    assert sortear_resultado("ia", 0.30) == "regular"

    assert sortear_resultado("humano", 0.80) == "regular"
    assert sortear_resultado("ia", 0.80) == "irregular"


def test_leitura_respeita_prazo_e_conclui_uma_vez():
    scanner = criar_scanner()
    iniciar_leitura(scanner, 100, "Lucas")

    assert atualizar_scanner(
        scanner, 2299, "humano", 0.80
    ) is False

    assert atualizar_scanner(
        scanner, 2300, "humano", 0.80
    ) is True

    # Atualizar novamente não sorteia outro resultado.
    assert atualizar_scanner(
        scanner, 2301, "humano", 0.10
    ) is False

    assert scanner["resultado"] == "regular"


def test_clique_repetido_nao_reinicia_leitura():
    scanner = criar_scanner()

    assert iniciar_leitura(scanner, 100, "Lucas") is True
    assert iniciar_leitura(scanner, 500, "Outro") is False

    assert scanner["inicio"] == 100
    assert scanner["nome"] == "Lucas"


def test_so_leitura_inconclusiva_permite_nova_tentativa():
    scanner = criar_scanner()

    iniciar_leitura(scanner, 0, "Lucas")
    atualizar_scanner(scanner, 2200, "humano", 0.10)

    assert iniciar_leitura(scanner, 2300, "Lucas") is True

    atualizar_scanner(scanner, 4500, "humano", 0.80)

    assert iniciar_leitura(scanner, 4600, "Lucas") is False