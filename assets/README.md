# Recursos do Catch.IA

Esta pasta reúne os recursos visuais e sonoros do jogo.

## Organização

- [imagens/](imagens/README.md): texturas, sprites de objetos, personagens e ícones.
- [sons/](sons/README.md): trilha ambiente e efeitos sonoros.
- [fontes/](fontes/README.md): pasta destinada a arquivos de fontes.

## Uso no projeto

Os recursos utilizados são carregados antes do loop principal.

As imagens transparentes usam PNG e `convert_alpha()`, após a criação da janela.

A trilha e os efeitos sonoros são controlados pelo módulo `src/audio.py`.

A interface atual utiliza a fonte padrão do Pygame.

## Caminhos

Preserve os nomes e as pastas referenciados pelo código.

Vários caminhos são relativos à raiz do projeto. Execute o jogo com `python main.py` a partir da pasta que contém esse arquivo.

Ao mover ou renomear um recurso, atualize sua referência no código.

## Recursos em preparação

Existem imagens e sons preparados para funcionalidades futuras, como interfone, lista de moradores e scanner.

Os READMEs das subpastas indicam quais recursos já estão integrados à versão atual.

## Origem e autoria

Os recursos produzidos com apoio do ChatGPT e as referências fornecidas pelo grupo estão descritos nos READMEs de imagens e sons.

Não há uma licença única declarada para todo o conteúdo desta pasta.

Ao adicionar recursos externos, registre o nome do arquivo, sua origem, autoria e licença, quando essas informações estiverem disponíveis.