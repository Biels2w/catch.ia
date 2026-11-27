from pathlib import Path

import pygame


def carregar_par(pasta, caminho_humano, caminho_ia, altura=280):
    """Carrega as duas formas de um personagem com o mesmo tamanho."""
    humano = pygame.image.load(
        pasta / caminho_humano
    ).convert_alpha()

    ia = pygame.image.load(
        pasta / caminho_ia
    ).convert_alpha()

    # Remove margens transparentes e pixels quase invisíveis.
    # Assim, o busto alcança o peitoril após o redimensionamento.
    humano = humano.subsurface(
        humano.get_bounding_rect(min_alpha=128)
    ).copy()

    ia = ia.subsurface(
        ia.get_bounding_rect(min_alpha=128)
    ).copy()

    # Mantém a proporção da imagem humana.
    largura = round(
        humano.get_width() * altura / humano.get_height()
    )
    tamanho = (largura, altura)

    # A revelação não altera o tamanho do retângulo.
    return {
        "humano": pygame.transform.scale(humano, tamanho),
        "ia": pygame.transform.scale(ia, tamanho),
    }


def preparar_foto(imagem):
    """Ajusta uma imagem humana ao espaço disponível no documento."""

    # Desconsidera as margens transparentes.
    recorte = imagem.subsurface(
        imagem.get_bounding_rect()
    ).copy()

    # A foto precisa caber tanto na largura quanto na altura.
    escala = min(
        90 / recorte.get_width(),
        106 / recorte.get_height(),
    )

    tamanho = (
        max(1, round(recorte.get_width() * escala)),
        max(1, round(recorte.get_height() * escala)),
    )

    return pygame.transform.scale(recorte, tamanho)


def carregar_personagens(imagens_lucas, foto_lucas):
    """Carrega os personagens uma única vez, depois de criar a janela."""
    pasta = (
        Path(__file__).resolve().parent.parent
        / "assets" / "imagens" / "personagens"
    )

    imagens_gael = carregar_par(
        pasta,
        "Gael/gael_transparente.png",
        "Gael IA/gael_ia_transparente.png",
    )

    imagens_estefanny = carregar_par(
        pasta,
        "estefanny/estefanny_transparente.png",
        "estefanny/estefanny_ia_transparente.png",
    )

    # Carrega as duas formas com o mesmo tamanho.
    imagens_nayra = carregar_par(
        pasta,
        "Nayra/nayra_transparente.png",
        "Nayra/nayra_ia_transparente.png",
    )

    # Foto antiga com cabelo preto e franja, conforme o roteiro.
    foto_nayra = pygame.image.load(
        pasta / "Nayra" / "nayra_documento.png"
    ).convert_alpha()

    # Carrega a aparência de chegada e a forma revelada.
    imagens_amanda = carregar_par(
        pasta,
        "amanda/amanda_transparente.png",
        "amanda/amanda_ia_transparente.png",
    )

    # Carrega as duas formas do Nero antes do loop principal.
    imagens_nero = carregar_par(
        pasta,
        "Nero/nero_transparente.png",
        "Nero/nero_ia_transparente.png",
    )

    # Carrega a aparência inicial e a forma revelada.
    imagens_sarah = carregar_par(
        pasta,
        "Sarah/sarah_transparente.png",
        "Sarah/sarah_ia_transparente.png",
    )

    # A foto antiga mostra o cabelo antes do corte.
    foto_sarah = pygame.image.load(
        pasta / "Sarah" / "sarah_documento.png"
    ).convert_alpha()

    return {
        "lucas": {
            "nome": "Lucas",
            "imagens": imagens_lucas,

            # Preserva a foto antiga do Lucas com cabelo curto.
            "foto": foto_lucas,
        },
        "gael": {
            "nome": "Gael",
            "imagens": imagens_gael,

            # Gael não apresenta documento.
            "foto": None,
        },
        "estefanny": {
            "nome": "Estefanny",
            "imagens": imagens_estefanny,

            # A foto apresentada não revela a identidade sorteada.
            "foto": preparar_foto(imagens_estefanny["humano"]),
        },
        "nayra": {
            "nome": "Nayra",
            "imagens": imagens_nayra,

            # A foto antiga é apresentada pelas duas identidades.
            "foto": preparar_foto(foto_nayra),
        },
            "amanda": {
            "nome": "Amanda",
            "imagens": imagens_amanda,

            # As duas identidades apresentam a mesma foto humana.
            "foto": preparar_foto(imagens_amanda["humano"]),
        },
            "nero": {
            "nome": "Nero",
            "imagens": imagens_nero,

            # O documento usa a foto humana nas duas identidades.
            "foto": preparar_foto(imagens_nero["humano"]),
        },
            "sarah": {
            "nome": "Sarah",
            "imagens": imagens_sarah,

            # A foto antiga é usada pelas duas identidades.
            "foto": preparar_foto(foto_sarah),
        },
    }

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
