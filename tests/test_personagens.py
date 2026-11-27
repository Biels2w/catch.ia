from copy import deepcopy
from datetime import date, datetime

from src.casos import carregar_casos, montar_caso
from src.dialogos import (
    carregar_dialogos,
    preparar_dialogo,
    responder_pergunta,
)
from src.documentos import carregar_documentos, entregar_documento
from src.moradores import carregar_moradores


# ==================== AUXILIAR ====================

def montar_lucas(caso, tipo):
    """Prepara um atendimento do Lucas para os testes."""
    return montar_caso(
        caso,
        carregar_documentos()["lucas"],
        carregar_dialogos()["lucas"][tipo],
        tipo,
    )


# ==================== LUCAS ====================

def test_lucas_caso_nao_modifica_dados_originais():
    modelos = carregar_documentos()["lucas"]
    roteiro_base = carregar_dialogos()["lucas"]["ia"]

    # Guarda os dados antes de montar o atendimento.
    copia_modelos = deepcopy(modelos)
    copia_roteiro = deepcopy(roteiro_base)

    caso = carregar_casos()["lucas"]["ia"][-1]

    documento, roteiro = montar_caso(
        caso, modelos, roteiro_base, "ia"
    )

    # Altera somente os dados preparados para o atendimento.
    documento["nome"] = "Outro nome"
    roteiro["perguntas"][0]["resposta"] = "Outra resposta"

    # Os modelos devem continuar intactos para as próximas partidas.
    assert modelos == copia_modelos
    assert roteiro_base == copia_roteiro


def test_lucas_cadastro_clonado_exige_conferir_resposta():
    caso = carregar_casos()["lucas"]["ia"][-1]
    documento, roteiro = montar_lucas(caso, "ia")

    # Neste caso, a IA apresenta um documento igual ao humano.
    assert documento == carregar_documentos()["lucas"]["humano"]

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    # A contradição está no setor informado durante a conversa.
    assert "B-02" in motivo["resposta"]

    # Repetir a pergunta não pode apagar essa pista.
    assert "B-02" in roteiro["repetir"]


def test_lucas_ia_tem_contradicao_verificavel():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Lucas"
    )

    for caso in carregar_casos()["lucas"]["ia"]:
        documento, roteiro = montar_lucas(caso, "ia")

        # Compara os dados apresentados com a lista de moradores.
        dados_divergem = any(
            documento[campo] != cadastro[campo]
            for campo in ("nome", "codigo", "nascimento", "setor")
        )

        # Usa a data fictícia atual do jogo.
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

        # Cada caso precisa oferecer alguma pista verificável.
        assert dados_divergem or vencido or fala_diverge, caso["id"]


def test_lucas_humano_preserva_documento_e_roteiro():
    caso = carregar_casos()["lucas"]["humano"][0]
    documento, roteiro = montar_lucas(caso, "humano")

    # O caso humano regular não deve adulterar seus dados.
    assert documento == carregar_documentos()["lucas"]["humano"]
    assert roteiro == carregar_dialogos()["lucas"]["humano"]


# ==================== GAEL ====================

def test_gael_sem_documento_nao_entrega_passe():
    modelos = carregar_documentos()["gael"]

    # Tanto o humano quanto a IA chegam sem documentos.
    for tipo in ("humano", "ia"):
        visitante = {"documento": None}

        assert modelos[tipo] is None

        # Pedir um documento inexistente não deve gerar erro
        # nem criar um passe na mesa.
        assert entregar_documento(visitante, modelos[tipo]) is False
        assert visitante["documento"] is None


def test_caso_gael_funciona_sem_documento():
    for tipo in ("humano", "ia"):
        base = carregar_dialogos()["gael"][tipo]

        documento, roteiro = montar_caso(
            carregar_casos()["gael"][tipo][0],
            carregar_documentos()["gael"],
            base,
            tipo,
        )

        assert documento is None
        assert roteiro == base

        # O atendimento deve receber uma cópia independente.
        assert roteiro is not base

        # As duas versões oferecem as mesmas três perguntas.
        assert len(roteiro["perguntas"]) == 3


def test_repetir_pergunta_revela_contradicao_gael_ia():
    conversa = preparar_dialogo(
        carregar_dialogos()["gael"]["ia"], "Gael"
    )

    # Na primeira resposta, a IA atribui o ataque a "elas".
    responder_pergunta(conversa, 0)
    assert "mortos por elas" in conversa["fala"]

    # Na repetição, comete o deslize previsto no roteiro.
    responder_pergunta(conversa, 0)
    assert "mortos por nós" in conversa["fala"]

    assert conversa["nome"] == "Gael"


# ==================== TROCA DE PERSONAGEM ====================

def test_nova_conversa_nao_mistura_visitantes():
    gael = preparar_dialogo(
        carregar_dialogos()["gael"]["humano"], "Gael"
    )
    responder_pergunta(gael, 0)

    lucas = preparar_dialogo(
        carregar_dialogos()["lucas"]["humano"], "Lucas"
    )

    # A conversa anterior mantém seu próprio histórico.
    assert gael["perguntadas"] == {0}

    # O próximo personagem começa sem perguntas realizadas.
    assert lucas["perguntadas"] == set()
    assert lucas["nome"] == "Lucas"

# ==================== ESTEFANNY ====================

def test_estefanny_humana_confere_com_cadastro():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Estefanny"
    )

    documento, _ = montar_caso(
        carregar_casos()["estefanny"]["humano"][0],
        carregar_documentos()["estefanny"],
        carregar_dialogos()["estefanny"]["humano"],
        "humano",
    )

    # A versão humana apresenta dados iguais aos do cadastro.
    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert documento[campo] == cadastro[campo]


def test_estefanny_ia_tem_divergencia_no_documento():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Estefanny"
    )

    for caso in carregar_casos()["estefanny"]["ia"]:
        documento, _ = montar_caso(
            caso,
            carregar_documentos()["estefanny"],
            carregar_dialogos()["estefanny"]["ia"],
            "ia",
        )

        # O código válido sozinho não comprova que o passe é legítimo.
        assert documento["codigo"] == cadastro["codigo"]

        assert any(
            documento[campo] != cadastro[campo]
            for campo in ("nascimento", "setor")
        ), caso["id"]


def test_estefanny_nao_reaproveita_atendimento_do_lucas():
    modelos = carregar_documentos()

    lucas = {"documento": None}
    estefanny = {"documento": None}

    entregar_documento(lucas, modelos["lucas"]["humano"])
    entregar_documento(estefanny, modelos["estefanny"]["humano"])

    # Cada visitante recebe seu próprio documento.
    assert lucas["documento"]["nome"] == "Lucas"
    assert estefanny["documento"]["nome"] == "Estefanny"

    anterior = preparar_dialogo(
        carregar_dialogos()["lucas"]["humano"], "Lucas"
    )
    responder_pergunta(anterior, 0)

    nova = preparar_dialogo(
        carregar_dialogos()["estefanny"]["humano"], "Estefanny"
    )

    # As perguntas feitas ao Lucas não passam para a Estefanny.
    assert anterior["perguntadas"] == {0}
    assert nova["perguntadas"] == set()
    assert nova["nome"] == "Estefanny"

# ==================== NAYRA ====================

def test_nayra_humana_confere_com_cadastro():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Nayra"
    )

    documento, _ = montar_caso(
        carregar_casos()["nayra"]["humano"][0],
        carregar_documentos()["nayra"],
        carregar_dialogos()["nayra"]["humano"],
        "humano",
    )

    # A versão humana apresenta os dados registrados na lista.
    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert documento[campo] == cadastro[campo]


def test_nayra_ia_pode_apresentar_documento_identico():
    caso = next(
        caso
        for caso in carregar_casos()["nayra"]["ia"]
        if caso["id"] == "nayra_cadastro_clonado"
    )

    documento, roteiro = montar_caso(
        caso,
        carregar_documentos()["nayra"],
        carregar_dialogos()["nayra"]["ia"],
        "ia",
    )

    # Neste caso, todos os dados do documento estão corretos.
    assert documento == carregar_documentos()["nayra"]["humano"]

    # A pista está nas falas previstas no roteiro.
    assert "11 00" in roteiro["chegada"]


def test_nayra_ia_mantem_pista_ao_repetir_pergunta():
    conversa = preparar_dialogo(
        carregar_dialogos()["nayra"]["ia"], "Nayra"
    )

    responder_pergunta(conversa, 0)
    assert "11 00 11" in conversa["fala"]

    # Repetir a pergunta continua oferecendo uma pista.
    responder_pergunta(conversa, 0)
    assert "00 00 00" in conversa["fala"]

    assert conversa["nome"] == "Nayra"

# ==================== AMANDA ====================

def test_amanda_humana_confere_com_cadastro():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Amanda"
    )

    documento, _ = montar_caso(
        carregar_casos()["amanda"]["humano"][0],
        carregar_documentos()["amanda"],
        carregar_dialogos()["amanda"]["humano"],
        "humano",
    )

    # O caso humano preserva os dados registrados no cadastro.
    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert documento[campo] == cadastro[campo]


def test_amanda_data_impossivel_exige_consultar_calendario():
    caso = next(
        caso
        for caso in carregar_casos()["amanda"]["ia"]
        if caso["id"] == "amanda_data_impossivel"
    )

    documento, roteiro = montar_caso(
        caso,
        carregar_documentos()["amanda"],
        carregar_dialogos()["amanda"]["ia"],
        "ia",
    )

    # O documento clonado apresenta todos os dados corretos.
    assert documento == carregar_documentos()["amanda"]["humano"]

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    # A data relatada é posterior ao dia fictício da partida.
    assert "23/11/2042" in motivo["resposta"]
    assert date(2042, 11, 23) > date(2042, 11, 22)

    conversa = preparar_dialogo(roteiro, "Amanda")
    indice = roteiro["perguntas"].index(motivo)

    responder_pergunta(conversa, indice)
    responder_pergunta(conversa, indice)

    # Repetir a pergunta não apaga a pista.
    assert "23/11/2042" in conversa["fala"]


def test_amanda_setor_adulterado_diverge_do_cadastro():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Amanda"
    )

    caso = next(
        caso
        for caso in carregar_casos()["amanda"]["ia"]
        if caso["id"] == "amanda_setor_adulterado"
    )

    documento, _ = montar_caso(
        caso,
        carregar_documentos()["amanda"],
        carregar_dialogos()["amanda"]["ia"],
        "ia",
    )

    # O código válido não elimina a divergência do setor.
    assert documento["codigo"] == cadastro["codigo"]
    assert documento["setor"] != cadastro["setor"]

# ==================== NERO ====================

def test_nero_humano_confere_com_cadastro():
    moradores = carregar_moradores()

    cadastro = next(
        morador
        for morador in moradores
        if morador["nome"] == "Nero"
    )

    documento, roteiro = montar_caso(
        carregar_casos()["nero"]["humano"][0],
        carregar_documentos()["nero"],
        carregar_dialogos()["nero"]["humano"],
        "humano",
    )

    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert documento[campo] == cadastro[campo]

    # O novo código deve pertencer a um único morador.
    assert sum(
        morador["codigo"] == documento["codigo"]
        for morador in moradores
    ) == 1

    assert "fui montado" not in roteiro["repetir"]


def test_nero_documento_clonado_exige_analisar_fala():
    caso = next(
        caso
        for caso in carregar_casos()["nero"]["ia"]
        if caso["id"] == "nero_relato_montagem"
    )

    documento, roteiro = montar_caso(
        caso,
        carregar_documentos()["nero"],
        carregar_dialogos()["nero"]["ia"],
        "ia",
    )

    # Neste caso, os dados do passe conferem com os do humano.
    assert documento == carregar_documentos()["nero"]["humano"]

    pergunta = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "explicar_aparencia"
    )

    assert "fui montado" in pergunta["resposta"]

    conversa = preparar_dialogo(roteiro, "Nero")
    indice = roteiro["perguntas"].index(pergunta)

    responder_pergunta(conversa, indice)
    responder_pergunta(conversa, indice)

    # A repetição mantém a pista disponível.
    assert "fui montado" in conversa["fala"]


def test_nero_passe_vencido_tem_data_anterior_ao_turno():
    caso = next(
        caso
        for caso in carregar_casos()["nero"]["ia"]
        if caso["id"] == "nero_passe_vencido"
    )

    documento, _ = montar_caso(
        caso,
        carregar_documentos()["nero"],
        carregar_dialogos()["nero"]["ia"],
        "ia",
    )

    validade = datetime.strptime(
        documento["validade"], "%d/%m/%Y"
    ).date()

    assert validade < date(2042, 11, 22)

# ==================== SARAH ====================

def test_sarah_humana_confere_com_cadastro():
    cadastro = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Sarah"
    )

    documento, _ = montar_caso(
        carregar_casos()["sarah"]["humano"][0],
        carregar_documentos()["sarah"],
        carregar_dialogos()["sarah"]["humano"],
        "humano",
    )

    for campo in ("nome", "codigo", "nascimento", "setor"):
        assert documento[campo] == cadastro[campo]


def test_sarah_idade_incompativel_exige_conferir_nascimento():
    caso = next(
        caso
        for caso in carregar_casos()["sarah"]["ia"]
        if caso["id"] == "sarah_idade_incompativel"
    )

    documento, roteiro = montar_caso(
        caso,
        carregar_documentos()["sarah"],
        carregar_dialogos()["sarah"]["ia"],
        "ia",
    )

    # O documento clonado apresenta todos os dados corretos.
    assert documento == carregar_documentos()["sarah"]["humano"]

    nascimento = datetime.strptime(
        documento["nascimento"], "%d/%m/%Y"
    ).date()

    hoje = date(2042, 11, 22)
    idade = hoje.year - nascimento.year

    # Se o aniversário ainda não aconteceu, descontamos um ano.
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    assert idade == 19

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    # A idade declarada contradiz o nascimento apresentado.
    assert "16 anos" in motivo["resposta"]

    conversa = preparar_dialogo(roteiro, "Sarah")
    indice = roteiro["perguntas"].index(motivo)

    responder_pergunta(conversa, indice)
    responder_pergunta(conversa, indice)

    # Repetir a pergunta mantém a pista disponível.
    assert "16 anos" in conversa["fala"]


def test_sarah_codigo_copiado_pertence_a_outra_moradora():
    caso = next(
        caso
        for caso in carregar_casos()["sarah"]["ia"]
        if caso["id"] == "sarah_codigo_copiado"
    )

    documento, _ = montar_caso(
        caso,
        carregar_documentos()["sarah"],
        carregar_dialogos()["sarah"]["ia"],
        "ia",
    )

    dona_codigo = next(
        morador
        for morador in carregar_moradores()
        if morador["codigo"] == documento["codigo"]
    )

    assert documento["nome"] == "Sarah"
    assert dona_codigo["nome"] == "Amanda"

    assert (
        documento["codigo"]
        != carregar_documentos()["sarah"]["humano"]["codigo"]
    )

# ==================== VISITAS ====================

def test_moradores_de_visita_nao_tem_casos_de_atendimento():
    nomes = {
        morador["nome"]
        for morador in carregar_moradores()
    }

    assert {"Bia", "Helena", "Davi"}.issubset(nomes)

    # Cadastro de moradores e dados dos visitantes são separados.
    for nome in ("bia", "helena", "davi"):
        assert nome not in carregar_casos()
        assert nome not in carregar_dialogos()


def test_lucas_visita_davi_confere_com_setor_do_morador():
    davi = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Davi"
    )

    caso = next(
        caso
        for caso in carregar_casos()["lucas"]["humano"]
        if caso["id"] == "lucas_visita_davi"
    )

    documento, roteiro = montar_lucas(caso, "humano")

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "Davi" in motivo["resposta"]
    assert davi["setor"] in motivo["resposta"]

    # Cada pessoa possui seu próprio setor.
    assert documento["setor"] != davi["setor"]


def test_amanda_visita_familia_confere_com_cadastro():
    caso = next(
        caso
        for caso in carregar_casos()["amanda"]["humano"]
        if caso["id"] == "amanda_visita_familia"
    )

    _, roteiro = montar_caso(
        caso,
        carregar_documentos()["amanda"],
        carregar_dialogos()["amanda"]["humano"],
        "humano",
    )

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    for nome in ("Bia", "Helena"):
        morador = next(
            morador
            for morador in carregar_moradores()
            if morador["nome"] == nome
        )

        assert nome in motivo["resposta"]
        assert morador["setor"] in motivo["resposta"]


def test_amanda_visita_irregular_exige_conferir_morador():
    helena = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Helena"
    )

    caso = next(
        caso
        for caso in carregar_casos()["amanda"]["ia"]
        if caso["id"] == "amanda_visita_setor_incorreto"
    )

    documento, roteiro = montar_caso(
        caso,
        carregar_documentos()["amanda"],
        carregar_dialogos()["amanda"]["ia"],
        "ia",
    )

    # O documento correto não elimina a contradição na conversa.
    assert documento == carregar_documentos()["amanda"]["humano"]

    motivo = next(
        pergunta
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "Helena" in motivo["resposta"]
    assert "B-03" in motivo["resposta"]
    assert helena["setor"] != "B-03"
    assert "B-03" in roteiro["repetir"]


def montar_adicional(personagem, tipo, id_caso):
    """Prepara um caso específico para os testes."""
    caso = next(
        caso
        for caso in carregar_casos()[personagem][tipo]
        if caso["id"] == id_caso
    )

    return montar_caso(
        caso,
        carregar_documentos()[personagem],
        carregar_dialogos()[personagem][tipo],
        tipo,
    )


def test_dez_personagens_tem_dados_completos():
    esperados = {
        "lucas", "gael", "estefanny", "nayra", "amanda",
        "nero", "sarah", "matheus", "lia", "otavio",
    }

    documentos = carregar_documentos()
    roteiros = carregar_dialogos()
    casos = carregar_casos()

    # Os três arquivos precisam reconhecer os mesmos dez personagens.
    assert set(documentos) == set(roteiros) == set(casos) == esperados

    for personagem in esperados:
        for tipo in ("humano", "ia"):
            assert tipo in documentos[personagem]
            assert len(roteiros[personagem][tipo]["perguntas"]) == 3
            assert casos[personagem][tipo]


def test_novos_humanos_conferem_com_cadastro():
    moradores = carregar_moradores()

    for personagem in ("matheus", "lia", "otavio"):
        documento = carregar_documentos()[personagem]["humano"]

        cadastro = next(
            morador
            for morador in moradores
            if morador["nome"] == documento["nome"]
        )

        for campo in ("nome", "codigo", "nascimento", "setor"):
            assert documento[campo] == cadastro[campo]

    # Cada código deve identificar um único cadastro.
    codigos = [morador["codigo"] for morador in moradores]
    assert len(codigos) == len(set(codigos))


def test_matheus_ia_tem_pistas_verificaveis():
    documento, _ = montar_adicional(
        "matheus", "ia", "matheus_codigo_copiado"
    )

    dono_codigo = next(
        morador
        for morador in carregar_moradores()
        if morador["codigo"] == documento["codigo"]
    )

    assert dono_codigo["nome"] == "Nero"

    documento, roteiro = montar_adicional(
        "matheus", "ia", "matheus_setor_declarado_incorreto"
    )

    assert documento == carregar_documentos()["matheus"]["humano"]

    motivo = next(
        pergunta["resposta"]
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "D-02" in motivo
    assert documento["setor"] == "D-01"
    assert "D-02" in roteiro["repetir"]


def test_lia_ia_exige_conferir_visita_ou_validade():
    helena = next(
        morador
        for morador in carregar_moradores()
        if morador["nome"] == "Helena"
    )

    documento, roteiro = montar_adicional(
        "lia", "ia", "lia_visita_setor_incorreto"
    )

    assert documento == carregar_documentos()["lia"]["humano"]

    motivo = next(
        pergunta["resposta"]
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "Helena" in motivo and "B-03" in motivo
    assert helena["setor"] != "B-03"
    assert "B-03" in roteiro["repetir"]

    documento, _ = montar_adicional(
        "lia", "ia", "lia_passe_vencido"
    )

    validade = datetime.strptime(
        documento["validade"], "%d/%m/%Y"
    ).date()

    assert validade < date(2042, 11, 22)


def test_otavio_ia_exige_conferir_nascimento_ou_data():
    documento, _ = montar_adicional(
        "otavio", "ia", "otavio_nascimento_adulterado"
    )

    assert (
        documento["nascimento"]
        != carregar_documentos()["otavio"]["humano"]["nascimento"]
    )

    documento, roteiro = montar_adicional(
        "otavio", "ia", "otavio_data_impossivel"
    )

    assert documento == carregar_documentos()["otavio"]["humano"]

    motivo = next(
        pergunta["resposta"]
        for pergunta in roteiro["perguntas"]
        if pergunta.get("acao") == "informar_motivo"
    )

    assert "23/11/2042" in motivo
    assert "23/11/2042" in roteiro["repetir"]