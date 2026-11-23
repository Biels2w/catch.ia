# Dados do Catch.IA

Esta pasta é destinada aos arquivos de persistência do jogo.

## Arquivos

- `recorde.txt`: arquivo destinado ao armazenamento da melhor pontuação.
- `ranking.txt`: arquivo reservado para uma possível implementação de ranking.

## Estado atual

O módulo `src/dados.py` possui funções para carregar e salvar um recorde em arquivo.

Essas funções ainda não estão integradas à versão atual da fiscalização. O jogo também não possui um ranking funcional neste momento.

A página selecionada no manual é mantida apenas na memória durante a execução. Essa informação não é gravada em arquivo e volta à primeira página ao reiniciar o jogo.