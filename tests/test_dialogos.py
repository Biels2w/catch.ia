from src.dialogos import (
    carregar_dialogos,
    preparar_dialogo,
    responder_pergunta,
)


def test_pergunta_repetida_e_nova_pergunta():
    roteiro = carregar_dialogos()["lucas"]["humano"]
    interfone = preparar_dialogo(roteiro)

    # A primeira pergunta recebe a resposta normal.
    responder_pergunta(interfone, 0)
    assert interfone["fala"] == roteiro["perguntas"][0]["resposta"]

    # Repetir a mesma pergunta aciona a reação do roteiro.
    responder_pergunta(interfone, 0)
    assert interfone["fala"] == roteiro["repetir"]

    # Uma pergunta diferente ainda recebe sua resposta normal.
    responder_pergunta(interfone, 1)
    assert interfone["fala"] == roteiro["perguntas"][1]["resposta"]
    assert interfone["perguntadas"] == {0, 1}


def test_novo_visitante_comeca_com_outra_conversa():
    roteiros = carregar_dialogos()["lucas"]

    anterior = preparar_dialogo(roteiros["humano"])
    responder_pergunta(anterior, 0)

    novo = preparar_dialogo(roteiros["ia"])

    assert novo["perguntadas"] == set()
    assert novo["fala"] == roteiros["ia"]["chegada"]

    # Preparar outra conversa não modifica a anterior.
    assert anterior["perguntadas"] == {0}


def test_interfone_sem_visitante():
    interfone = preparar_dialogo()

    assert responder_pergunta(interfone, 0) is False
    assert interfone["perguntadas"] == set()