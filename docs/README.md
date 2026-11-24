# Documentação do Catch.IA

Esta pasta reúne os documentos de planejamento e apoio ao desenvolvimento do jogo.

Catch.IA é um projeto em Python e Pygame da disciplina de Introdução a Algoritmos/Programação.

## Arquivos

- [proposta.MD](proposta.MD): proposta do grupo, com integrantes, tema, objetivos, regras, controles e escopo planejado.
- `README.md`: apresentação da documentação e orientações de atualização.

## Tema

O tema escolhido é segurança e confiabilidade na identificação de IAs.

A proposta é que o jogador compare documentos, respostas e outras evidências para controlar o acesso a um refúgio humano.

## Acompanhamento do desenvolvimento

O protótipo já possui:

- Atendimentos com o personagem Lucas.
- Decisões de autorizar ou recusar.
- Sistema de três vidas.
- Meta de 10 atendimentos.
- Animações de revelação e desfecho.
- Livro de ocorrências com gravação em JSON.
- Consultas do cenário.
- Trilha e efeitos sonoros.
- Relatório final de vitória ou derrota.

O interfone, a lista de moradores, o scanner com falhas e a conexão das pistas à identidade do visitante continuam em desenvolvimento.

A existência de imagens ou sons preparados não significa que essas funcionalidades já estejam implementadas.

## Atualização da proposta

Mudanças nas regras, nos controles e no escopo devem ser registradas em `proposta.MD`.

A proposta deve diferenciar as funcionalidades implementadas das melhorias planejadas e acompanhar decisões como:

- Quantidade de atendimentos.
- Condições de vitória e derrota.
- Comportamento do livro ao reiniciar.
- Integração das pistas à investigação.
- Organização dos módulos.
- Recursos externos utilizados.

## Outros documentos

As instruções de instalação, os controles e o estado atual do jogo estão no [README principal](../README.md).

Os testes automatizados e o roteiro de verificação manual estão em [tests/README.md](../tests/README.md).