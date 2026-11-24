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
    """Entrega uma cópia do modelo somente na primeira solicitação."""
    if visitante["documento"] is not None:
        return False

    # A cópia evita modificar o modelo original do arquivo.
    visitante["documento"] = modelo.copy()
    return True


def criar_miniatura_documento(papel):
    """Prepara o pequeno passe que ficará sobre o balcão."""
    imagem = pygame.transform.scale(papel, (110, 62))

    # Pequena silhueta representando a foto.
    pygame.draw.rect(
        imagem, (102, 112, 109), (9, 14, 22, 31)
    )
    pygame.draw.circle(
        imagem, (209, 201, 179), (20, 24), 5
    )
    pygame.draw.rect(
        imagem, (209, 201, 179), (14, 30, 12, 12)
    )

    fonte = pygame.font.Font(None, 16)
    imagem.blit(
        fonte.render("PASSE", True, (55, 48, 39)),
        (40, 10),
    )

    # Linhas decorativas que representam os dados do documento.
    for y, largura in ((28, 54), (36, 44), (44, 50)):
        pygame.draw.line(
            imagem,
            (125, 112, 90),
            (40, y),
            (40 + largura, y),
            2,
        )

    return imagem


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
            center=(area.centerx, area.bottom - 18)
        ),
    )