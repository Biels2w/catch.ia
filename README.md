# Catch.IA

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido em Python com Pygame.

## Integrantes do grupo

- Gabriel de Oliveira Costa
- Ana Ayla Pires Reis
- Gabriel Rodrigues Lima
- Patrick Souza

## Descrição do jogo

Catch.IA é um jogo de investigação e tomada de decisões. Em um futuro fictício, o jogador assume o papel de um fiscal responsável pela entrada em uma área protegida. A cada atendimento, ele precisa analisar documentos e respostas para descobrir se o visitante é humano ou uma inteligência artificial disfarçada.

O jogo aborda segurança e confiabilidade na identificação de IAs. A investigação exige comparar as informações disponíveis antes de decidir quem pode entrar.

## Objetivo do jogador

Concluir todos os atendimentos com pelo menos uma vida restante, autorizando a entrada de humanos e impedindo a infiltração de IAs.

## Regras previstas

- O jogador começa a partida com três vidas.
- Um visitante por vez solicita entrada na área protegida.
- Antes de decidir, o jogador pode consultar documentos e fazer perguntas ao visitante.
- Autorizar a entrada de uma IA ou barrar um humano custa uma vida.
- A decisão é definitiva após a confirmação.
- O jogador vence se concluir todos os atendimentos com pelo menos uma vida. Ao perder a última vida, a partida termina em derrota.

## Controles

- **Fechar a janela (X)** — encerra o jogo na versão atual.
- **Clique esquerdo (previsto)** — consulta documentos, seleciona perguntas e confirma se a entrada será autorizada ou negada.

## Estado do desenvolvimento

A versão atual possui a janela do Pygame com o título Catch.IA, o loop principal e o tratamento do fechamento da janela. A próxima etapa da Entrega 2 é implementar uma interação de fiscalização que permita ao jogador analisar uma pista e decidir se autoriza ou nega a entrada.

## Estrutura do projeto

- `main.py` — ponto de entrada do jogo.
- `src/jogo.py` — inicialização da janela e loop principal.
- `src/config.py` — configurações da janela, como título, dimensões e FPS.
- `assets/` — pasta para imagens, fontes e sons.
- `data/` — pasta para arquivos de dados do jogo.
- `tests/` — pasta destinada aos testes de lógica.
- `docs/proposta.MD` — proposta inicial do grupo.
- `requirements.txt` — dependências do projeto.

## Como executar

Na raiz do repositório, na pasta que contém `main.py`, execute:

```powershell
python -m pip install -r requirements.txt
python main.py
