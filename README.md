# Catch.IA

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido em Python com Pygame.

## Integrantes do grupo

- Gabriel de Oliveira Costa
- Ana Ayla Pires Reis
- Gabriel Rodrigues Lima
- Patrick Souza

## Descrição do jogo

Catch.IA é um jogo de investigação e tomada de decisões ambientado em um futuro fictício. O jogador assume o papel de um fiscal responsável por controlar a entrada em uma área protegida da humanidade.

A proposta é analisar documentos, respostas e pistas para identificar humanos e inteligências artificiais disfarçadas, decidindo quem pode entrar.

## Tema e uso responsável da IA

O jogo aborda segurança e confiabilidade na identificação de IAs. A investigação incentiva a comparação de informações e a análise de evidências antes de tomar uma decisão, considerando tanto o risco de autorizar uma IA quanto o de recusar um humano indevidamente.

A identificação será simulada pelas regras do jogo, sem implementar uma inteligência artificial real.

## Objetivo e regras previstas

O objetivo será concluir todos os atendimentos com pelo menos uma vida restante.

- O jogador começará com três vidas.
- Um visitante por vez solicitará entrada.
- Será possível consultar documentos e fazer perguntas antes de decidir.
- Autorizar uma IA ou recusar um humano custará uma vida.
- A decisão será definitiva após a confirmação.
- Concluir todos os atendimentos com vidas restantes representará vitória.
- Perder todas as vidas representará derrota.

Essas regras ainda não estão totalmente implementadas.

## Estado atual do desenvolvimento

A versão atual permite explorar o posto de fiscalização e interagir com os elementos do cenário.

Já estão implementados:

- Janela do Pygame, loop principal e controle de FPS.
- Cenário com texturas na parede, janela, balcão e ambiente externo.
- Pasta interativa com um manual de códigos permitidos.
- Navegação entre as páginas do manual.
- Manutenção da página selecionada ao fechar e reabrir o manual durante a execução.
- Luminária que pode ser ligada e desligada.
- Botões para autorizar ou recusar a entrada, com mensagem de confirmação.
- Calendário com a data fictícia da partida.
- Jornal com avisos da semana.
- Fechamento das consultas com clique fora da folha ou com a tecla Esc.

Ainda serão desenvolvidos os visitantes, os documentos individuais, as perguntas e a avaliação das decisões, além do sistema de vidas e das condições de vitória e derrota.

Atualmente, os botões de decisão apenas registram e exibem a escolha. Eles ainda não verificam se um visitante é humano ou IA.

## Controles

- **Clique esquerdo:** interagir com a pasta, a luminária, o calendário, o jornal e os botões de decisão.
- **Anterior / Próxima:** trocar a página do manual.
- **Clique fora da folha aberta:** fechar a consulta.
- **Esc:** fechar o manual, o calendário ou o jornal.
- **X da janela:** encerrar o jogo.

Na versão atual, uma decisão de entrada já registrada só pode ser reiniciada ao abrir o jogo novamente.

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/jogo.py`: inicialização, eventos, interações e desenho do cenário.
- `src/consultas.py`: desenho do calendário e do jornal.
- `src/config.py`: configurações de tela, título, cores e FPS.
- `src/funcoes.py`: funções auxiliares de lógica.
- `src/dados.py`: funções para leitura e gravação de recorde.
- `src/sprites.py`: função para recortar imagens de uma spritesheet.
- `assets/`: imagens e pastas destinadas a fontes e sons.
- `data/`: arquivos destinados à persistência de dados.
- `tests/`: testes automatizados de lógica.
- `docs/`: documentação e proposta do grupo.
- `requirements.txt`: dependências do projeto.

## Como executar

Com o Python instalado, abra o terminal na raiz do projeto, onde está o arquivo `main.py`.

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute o jogo:

```powershell
python main.py
```

Execute os comandos na raiz do projeto para que os caminhos relativos das imagens sejam encontrados corretamente.

## Como executar os testes

Na raiz do projeto:

```powershell
python -m pytest
```

Os testes atuais verificam funções de cálculo de pontos, identificação de derrota e limitação de valores. Eles não cobrem as interações gráficas.

## Recursos externos e ferramentas de apoio

As imagens do cenário, da pasta, dos botões, da folha do manual, do calendário e do jornal foram geradas com auxílio do ChatGPT e integradas ao projeto pelo grupo.

O projeto também recebeu apoio do ChatGPT para explicações de programação, sugestões de código e documentação.

A estrutura inicial foi fornecida pelo template da disciplina. O desenvolvimento utiliza Python, Pygame e pytest.

Outros recursos externos incorporados ao jogo deverão ter sua origem e licença, quando disponível, registradas nesta documentação.

## Planejamento

A proposta e o escopo planejado estão disponíveis em [docs/proposta.MD](docs/proposta.MD).