# Recursos do Catch.IA

Esta pasta reúne os recursos visuais e sonoros do jogo.

## Organização

- [imagens/](imagens/README.md): cenário, objetos, personagens e ícones.
- [sons/](sons/README.md): trilha ambiente e efeitos.
- [fontes/](fontes/README.md): pasta destinada a fontes externas.

## Carregamento

Os recursos utilizados são carregados antes do loop principal.

As imagens transparentes utilizam PNG e convert_alpha(), após
a criação da janela.

personagens.py organiza imagens e fotos dos visitantes.
sprites.py carrega as imagens das vidas e do relatório.
audio.py organiza os efeitos e inicia a trilha.

A interface utiliza a fonte padrão do Pygame.

## Caminhos

Preserve os nomes e as pastas utilizados pelo código.

Execute o projeto a partir da raiz, pois parte dos recursos
ainda utiliza caminhos relativos.

## Materiais auxiliares

Algumas pastas contêm GIFs, imagens originais e scripts de preparação.
A presença de um arquivo não significa que ele seja carregado
pela partida.

Os sprites transparentes referenciados pelo código são as imagens
utilizadas no atendimento atual.

## Origem

Os recursos gerados ou preparados com apoio do ChatGPT e as
referências do grupo estão registrados nos READMEs das subpastas.

Não há uma licença única declarada para todos os materiais.
Registre a origem, autoria e licença disponível de novos recursos.