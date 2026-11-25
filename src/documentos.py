import json
from pathlib import Path

import pygame


def carregar_documentos():
    """Carrega os modelos de documentos antes do loop."""
    caminho = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "documentos.json"
    )

    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def entregar_documento(visitante, modelo):
    """Entrega um passe somente quando existe um modelo disponível."""

    # Não cria um documento inexistente e não troca um já entregue.
    if modelo is None or visitante["documento"] is not None:
        return False

    # A cópia protege os dados originais carregados do JSON.
    visitante["documento"] = modelo.copy()
    return True


def desenhar_documento(
    tela, area, fonte, fonte_menor, dados, foto
):
    """Desenha os dados apresentados, sem revelar a identidade real."""
    cor = (48, 43, 35)

    titulo = fonte.render("IDENTIFICAÇÃO", True, cor)
    tela.blit(
        titulo,
        titulo.get_rect(center=(area.centerx, area.top + 38)),
    )

    subtitulo = fonte_menor.render(
        "REFÚGIO - CONTROLE DE ACESSO", True, cor
    )
    tela.blit(
        subtitulo,
        subtitulo.get_rect(
            center=(area.centerx, area.top + 64)
        ),
    )

    # Foto apresentada no documento.
    area_foto = pygame.Rect(
        area.left + 22, area.top + 95, 96, 112
    )

    pygame.draw.rect(tela, (104, 115, 112), area_foto)
    tela.blit(foto, foto.get_rect(center=area_foto.center))
    pygame.draw.rect(tela, (125, 112, 90), area_foto, 2)

    # Informações ao lado da foto.
    for texto, y in [
        ("Nome:", area.top + 100),
        (dados["nome"], area.top + 126),
        ("Registro:", area.top + 166),
        (dados["registro"], area.top + 188),
    ]:
        imagem = fonte_menor.render(texto, True, cor)
        tela.blit(imagem, (area.left + 138, y))

    campos = [
        ("Código:", dados["codigo"]),
        ("Nascimento:", dados["nascimento"]),
        ("Setor:", dados["setor"]),
        ("Validade:", dados["validade"]),
    ]

    for indice, (rotulo, valor) in enumerate(campos):
        y = area.top + 232 + indice * 30

        tela.blit(
            fonte_menor.render(rotulo, True, cor),
            (area.left + 24, y),
        )

        imagem = fonte_menor.render(valor, True, cor)

        # Alinha os valores pela margem direita da folha.
        tela.blit(
            imagem,
            imagem.get_rect(topright=(area.right - 24, y)),
        )

    aviso = fonte_menor.render(
        "Esc ou clique fora para fechar.", True, cor
    )

    tela.blit(
        aviso,
        aviso.get_rect(
            center=(area.centerx, area.bottom - 30)
        ),
    )

def preparar_passe(sprite_base, foto):
    """Monta a miniatura sem alterar o sprite original do passe."""
    passe = sprite_base.copy()

    if foto is not None:
        # Ajusta a foto ao espaço à esquerda da miniatura.
        escala = min(
            30 / foto.get_width(),
            40 / foto.get_height(),
        )

        tamanho = (
            max(1, round(foto.get_width() * escala)),
            max(1, round(foto.get_height() * escala)),
        )

        miniatura = pygame.transform.scale(foto, tamanho)

        passe.blit(
            miniatura,
            miniatura.get_rect(center=(24, 32)),
        )

    return passe