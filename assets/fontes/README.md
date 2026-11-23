# Fontes do Catch.IA

Esta pasta é destinada a arquivos de fontes, como `.ttf` e `.otf`.

## Uso atual

A versão atual não carrega fontes personalizadas desta pasta.

Os textos utilizam `pygame.font.Font(None, tamanho)`, que seleciona a fonte padrão disponibilizada pelo Pygame.

Os tamanhos são definidos no código de acordo com o uso:

- Rótulos do cenário.
- Códigos do manual.
- Conteúdo das consultas.
- Informações do livro.
- Relatório final.

## Adição de novas fontes

Ao incorporar uma fonte:

1. Coloque o arquivo nesta pasta.
2. Atualize seu carregamento no código.
3. Registre aqui seu nome, autoria, origem e licença.
4. Preserve os arquivos de licença fornecidos junto da fonte.

Priorize fontes legíveis nos tamanhos utilizados pela interface.