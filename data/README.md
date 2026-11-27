# Dados do Catch.IA

Os arquivos JSON usam UTF-8 e separam o conteúdo dos atendimentos
do código responsável por executá-los.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| roteiros_interfone.json | Chegadas, perguntas, respostas e reações |
| documentos.json | Modelos de documentos por personagem e identidade |
| casos.json | Variações e alterações aplicadas aos atendimentos |
| moradores.json | Cadastro de referência consultado pelo jogador |
| ocorrencias.json | Decisões da partida atual |
| recorde.txt | Arquivo da base inicial, sem uso na partida atual |
| ranking.txt | Arquivo reservado, sem ranking integrado |

## Roteiros e documentos

Os visitantes são identificados por chaves como lucas e amanda.
As identidades usam humano e ia.

As perguntas possuem ações, como informar_motivo e entregar_documento.
Essas ações permitem conectar as respostas às regras do jogo.

O valor null indica ausência de documento, como nos modelos de Gael.

## Casos

Cada caso possui um id.

Pode utilizar:

- base_documento: modelo usado como origem.
- documento: campos que substituem os dados do modelo.
- respostas: substituições selecionadas pela ação da pergunta.
- chegada: fala inicial alternativa.
- repetir: reação alternativa à repetição.

O caso é sorteado uma vez na chegada. Reabrir consultas não muda
os dados do atendimento.

## Cadastro e visitas

O cadastro contém nome, código, nascimento e setor.

Bia, Helena e Davi recebem visitas, mas não integram a fila
de personagens atendidos.

O setor do visitante pode ser diferente do setor da pessoa visitada.

## Ocorrências

Cada registro contém:

- nome e caso.
- tipo: identidade real.
- decisao: liberar ou recusar.
- acertou: resultado booleano.
- vidas: quantidade restante após a decisão.
- data e hora: informações fictícias do expediente.

O livro apresenta três registros por página.

Ao abrir o jogo ou reiniciar o turno, a lista e o arquivo são
esvaziados. Não há histórico acumulado entre partidas.

## Informações mantidas na memória

As páginas das consultas e o relatório final não são gravados
em arquivos próprios.

O relatório usa a data real do computador. O expediente e
as ocorrências usam a data fictícia 22/11/2042.

Todos os dados pessoais do cadastro pertencem à narrativa fictícia.