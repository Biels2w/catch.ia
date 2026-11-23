# Dados do Catch.IA

Esta pasta contém os arquivos de persistência do jogo.

## Arquivos

| Arquivo | Uso atual |
| --- | --- |
| `ocorrencias.json` | Armazena os atendimentos da partida atual |
| `recorde.txt` | Arquivo da base inicial, sem integração à mecânica atual |
| `ranking.txt` | Arquivo reservado; não há ranking funcional na partida atual |

## Ocorrências

O arquivo `ocorrencias.json` contém uma lista de registros.

Cada atendimento possui os seguintes campos:

| Campo | Informação |
| --- | --- |
| `nome` | Nome do visitante |
| `tipo` | Identidade real: `humano` ou `ia` |
| `decisao` | Escolha do jogador: `liberar` ou `recusar` |
| `acertou` | Valor booleano que indica se a decisão foi correta |
| `vidas` | Vidas restantes depois da decisão |
| `data` | Data fictícia do atendimento |
| `hora` | Horário fictício do atendimento |

Cada decisão gera uma gravação. O livro apresenta três registros por página.

## Reinício

Ao abrir o jogo ou reiniciar o turno:

- A lista de ocorrências é esvaziada.
- A página do livro volta à primeira.
- O arquivo JSON é sobrescrito com uma lista vazia.

Os registros não são acumulados entre partidas.

## Leitura e gravação

As funções estão em `src/dados.py`.

Os arquivos JSON usam UTF-8 e preservam os acentos. A função de gravação cria a pasta de destino quando necessário.

A função de leitura retorna uma lista vazia quando o arquivo ainda não existe.

## Informações mantidas na memória

O relatório final é montado e exibido durante a execução. Ele não é exportado como PDF ou salvo em um arquivo de relatório separado.

A página selecionada no manual também é mantida apenas na memória, sem gravação em arquivo.