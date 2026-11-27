# Código-fonte do Catch.IA

O ponto de entrada é main.py, na raiz do projeto.
Ele importa e chama executar_jogo(), de jogo.py.

## Módulos

| Arquivo | Responsabilidade |
| --- | --- |
| jogo.py | Inicialização, eventos, estados, animações e desenho do cenário |
| config.py | Tela, FPS, título, cores, caminhos e meta de atendimentos |
| instrucoes.py | Páginas de orientação antes da partida |
| personagens.py | Imagens, formas reveladas e fotos dos personagens |
| casos.py | Carregamento e montagem das variações dos atendimentos |
| dialogos.py | Roteiros, perguntas, respostas e apresentação das falas |
| documentos.py | Modelos, entrega do documento, ficha e miniatura do passe |
| moradores.py | Cadastro, ordenação, paginação e desenho da lista |
| scanner.py | Estado, duração e resultados simulados da leitura |
| funcoes.py | Avaliação das decisões e desenho do relógio e das vidas |
| consultas.py | Calendário, jornal e livro de ocorrências |
| dados.py | Leitura e gravação de ocorrências |
| efeitos.py | Tremor e rachaduras ao perder uma vida |
| relatorio.py | Condições de encerramento e relatório final |
| audio.py | Carregamento da trilha e dos efeitos |
| sprites.py | Carregamento das imagens das vidas e do relatório |
| __init__.py | Identificação do pacote Python |

## Inicialização

O jogo inicializa o Pygame, cria a janela e carrega os recursos.

As imagens que utilizam convert() ou convert_alpha() são carregadas
depois da criação da janela.

As instruções são exibidas antes do primeiro turno. Sua função
retorna True para iniciar ou False para encerrar.

Os relógios da partida começam após a leitura.

## Loop principal

Cada quadro executa três tarefas:

1. Processar eventos.
2. Atualizar estados, movimentos e regras.
3. Desenhar a tela e atualizar a exibição.

Clock.tick limita os quadros por segundo. O tempo entre quadros
é convertido para segundos e usado na movimentação.

## Atendimento

A campainha inicia um atendimento quando o posto está livre.

São sorteados personagem, identidade e caso. Documento e roteiro
são preparados uma única vez e mantidos durante a investigação.

O visitante entra pela esquerda e aguarda uma decisão.

avaliar_decisao retorna as vidas atualizadas e um booleano
indicando se houve acerto.

A chave registrado impede que a decisão seja contabilizada
novamente nos quadros seguintes.

## Desfecho e encerramento

- Visitantes autorizados saem pela direita.
- IAs recusadas são desativadas.
- Humanos recusados são capturados para cima.

O relatório aparece após a última animação. A derrota tem prioridade
quando a última vida é perdida no décimo atendimento.

O relatório é montado uma vez, mantendo a duração congelada.

## Estruturas de dados

- Dicionários representam visitante, scanner, casos e recursos.
- Listas armazenam páginas, moradores e ocorrências.
- Um conjunto guarda os índices das perguntas realizadas.
- Retângulos representam posições e áreas clicáveis.

deepcopy protege os modelos e roteiros originais durante a montagem
de um caso. Cópias das superfícies preservam as imagens reutilizadas.

## Moradores e visitantes

A fila utiliza o banco de src/personagens.py.

O cadastro utiliza data/moradores.json. Uma pessoa cadastrada
não passa automaticamente a integrar a fila da recepção.

As visitas são descritas nos casos. O jogador confere o nome
e o setor citado na lista.

## Persistência e utilitários da base

As decisões são gravadas em data/ocorrencias.json. O arquivo é
limpo ao iniciar ou reiniciar a partida.

Os utilitários salvar_recorde e carregar_recorde, e algumas constantes
da base inicial, não estão integrados à mecânica atual.

A função criar_som_campainha permanece em funcoes.py, mas o jogo
utiliza o arquivo de áudio carregado por audio.py.

## Execução

Consulte o [README principal](../README.md) para instalação, controles e regras.