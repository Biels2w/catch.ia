# Código-fonte do Catch.IA

Esta pasta contém os módulos responsáveis pelo funcionamento do jogo.

## Arquivos

- `jogo.py`: inicializa o Pygame, executa o loop principal, processa os eventos e desenha o cenário e as interações.
- `consultas.py`: desenha o calendário e o jornal, incluindo a organização das datas e dos avisos.
- `config.py`: reúne configurações como dimensões da tela, título, cores e FPS.
- `funcoes.py`: contém funções auxiliares para pontuação, vidas, colisões e limitação de valores.
- `dados.py`: contém funções para carregar e salvar um recorde em arquivo.
- `sprites.py`: contém a função de recorte de spritesheet e remoção de uma cor de fundo.
- `__init__.py`: identifica a pasta como um pacote Python.

## Organização atual

O controle das interações e a maior parte do desenho do cenário estão em `jogo.py`. O desenho das consultas do calendário e do jornal está separado em `consultas.py`.

As funções de pontuação, vidas e persistência já possuem uma base, mas ainda não estão integradas à mecânica atual de fiscalização.

## Execução

Inicie o projeto pelo arquivo `main.py`, localizado na raiz do repositório:

    python main.py