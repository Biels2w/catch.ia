# Código-fonte do Catch.IA

Esta pasta contém os módulos responsáveis pelo funcionamento do jogo. O ponto de entrada é `main.py`, localizado na raiz do projeto.

## Módulos

| Arquivo | Responsabilidade |
| --- | --- |
| `jogo.py` | Inicializa a partida, processa eventos, controla visitantes, decisões e animações e desenha o cenário |
| `config.py` | Define tela, FPS, título, cores, caminhos e meta de 10 atendimentos |
| `funcoes.py` | Avalia decisões, atualiza vidas e desenha o relógio e os corações |
| `consultas.py` | Desenha o calendário, o jornal e o livro de ocorrências |
| `relatorio.py` | Verifica o encerramento, monta os dados do resultado e desenha o relatório |
| `audio.py` | Carrega os efeitos e inicia a trilha ambiente em repetição |
| `dados.py` | Salva e recupera ocorrências em JSON e mantém utilitários de recorde da base inicial |
| `sprites.py` | Carrega os sprites da interface e mantém a função de recorte de spritesheet |
| `__init__.py` | Identifica a pasta como um pacote Python |

## Fluxo da partida

A campainha chama Lucas quando o posto está livre. Sua identidade é sorteada como `humano` ou `ia`, mantendo inicialmente a aparência humana.

O visitante entra pela esquerda, aguarda no centro da janela e recebe uma decisão do jogador.

A função `avaliar_decisao` retorna as vidas atualizadas e um valor booleano que indica se a escolha foi correta. O atendimento é contado e gravado uma única vez.

A chave `registrado` do visitante impede que a mesma decisão seja contabilizada novamente nos quadros seguintes.

Depois da revelação:

- Visitantes autorizados saem pela direita.
- IAs recusadas são desativadas.
- Humanos recusados são capturados para cima e desaparecem antes de expor o corte inferior do sprite.

## Encerramento

Completar 10 atendimentos com vidas restantes resulta em vitória.

Esgotar as três vidas resulta em derrota, inclusive no décimo atendimento.

O relatório é montado uma única vez, após a animação final. Isso mantém a duração congelada enquanto o resultado está sendo consultado.

## Estruturas de dados

- O visitante é representado por um dicionário com imagem, posição, identidade e estado.
- As ocorrências são dicionários armazenados em uma lista.
- O manual utiliza uma lista de páginas contendo códigos.
- Os sprites e os efeitos sonoros são organizados em dicionários.

## Persistência

Os atendimentos são gravados em `data/ocorrencias.json`.

O livro começa vazio ao abrir o jogo e é limpo ao reiniciar o turno.

Os utilitários de recorde e de recorte de spritesheet permanecem na base do projeto, mas não representam um ranking ou uma mecânica de coleta integrada à partida atual.

## Datas e tempo

O relógio e as ocorrências usam o expediente fictício do jogo.

O relatório usa a data real do computador e a duração medida pelo Pygame.

## Desenvolvimento em andamento

Os diálogos, os documentos individuais, a lista de moradores e o scanner ainda precisam ser conectados à identidade do visitante.

As consultas existentes ainda não fornecem evidências que permitam deduzir a identidade sorteada antes da decisão.

## Execução

Na raiz do projeto:

```powershell
python main.py
```

Imagens que utilizam `convert()` ou `convert_alpha()` devem ser carregadas depois da criação da janela com `pygame.display.set_mode()`.

Consulte o [README principal](../README.md) para instalação, controles e regras.