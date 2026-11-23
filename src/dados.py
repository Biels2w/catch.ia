import json
from pathlib import Path

def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except FileNotFoundError:
        return 0

# Encontra a pasta data a partir da localização deste módulo.
CAMINHO_OCORRENCIAS = (
    Path(__file__).resolve().parent.parent / "data" / "ocorrencias.json"
)


def carregar_ocorrencias(caminho=CAMINHO_OCORRENCIAS):
    """Lê o histórico; no primeiro uso, começa com uma lista vazia."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)
    except FileNotFoundError:
        return []

    if not isinstance(registros, list):
        raise ValueError("O arquivo de ocorrências precisa conter uma lista.")

    return registros


def salvar_ocorrencias(ocorrencias, caminho=CAMINHO_OCORRENCIAS):
    """Grava os registros preservando os acentos."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(ocorrencias, arquivo, ensure_ascii=False, indent=2)