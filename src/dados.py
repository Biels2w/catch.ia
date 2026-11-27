import json
from pathlib import Path


# Localiza o arquivo a partir da posição deste módulo.
CAMINHO_OCORRENCIAS = (
    Path(__file__).resolve().parent.parent
    / "data" / "ocorrencias.json"
)


def carregar_ocorrencias(caminho=CAMINHO_OCORRENCIAS):
    """Lê o histórico; começa vazio quando o arquivo não existe."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)

    except FileNotFoundError:
        return []

    if not isinstance(registros, list):
        raise ValueError(
            "O arquivo de ocorrências precisa conter uma lista."
        )

    return registros


def salvar_ocorrencias(ocorrencias, caminho=CAMINHO_OCORRENCIAS):
    """Grava os registros da partida preservando os acentos."""
    caminho = Path(caminho)

    # Garante que a pasta exista antes de salvar.
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(
            ocorrencias,
            arquivo,
            ensure_ascii=False,
            indent=2,
        )