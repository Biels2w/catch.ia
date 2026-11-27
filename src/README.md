# Código do Catch.IA

`main.py` chama `executar_jogo()`. Os módulos abaixo dividem as responsabilidades da aplicação.

| Arquivo | Responsabilidade |
| --- | --- |
| `jogo.py` | Inicialização, cenário, eventos, estados do visitante e coordenação da partida |
| `config.py` | Dimensões da janela, FPS, título, cor de fundo e meta de atendimentos |
| `personagens.py` | Catálogo, imagens, fotos, redimensionamento e fila dos 10 visitantes |
| `regras.py` | Avaliação da decisão e atualização das vidas |
| `interface.py` | Desenho dos ponteiros do relógio e dos corações |
| `casos.py` | Leitura e montagem das variações de documentos e falas |
| `dialogos.py` | Roteiros, perguntas, repetições e apresentação das conversas |
| `documentos.py` | Modelos, entrega do passe, miniatura e consulta ampliada |
| `moradores.py` | Leitura, paginação e apresentação do cadastro |
| `scanner.py` | Estados, tempo de leitura e resultados simulados do aparelho |
| `consultas.py` | Desenho do calendário, jornal e livro de ocorrências |
| `dados.py` | Leitura e gravação das ocorrências em JSON |
| `relatorio.py` | Condições de encerramento, cálculo e desenho do relatório |
| `efeitos.py` | Tremor e rachaduras ao perder uma vida |
| `sprites.py` | Carregamento dos corações e elementos do relatório |
| `audio.py` | Carregamento, volumes e reprodução da trilha e dos efeitos |
| `instrucoes.py` | Telas de orientação antes da primeira partida |
| `__init__.py` | Identificação de `src` como pacote Python |

## Fluxo para explicar o código

1. Inicializar o Pygame, criar a janela e carregar os recursos.
2. Mostrar as instruções e iniciar a contagem do tempo.
3. Embaralhar os identificadores e chamar um visitante pela campainha.
4. Sortear identidade e caso, preparando cópias do documento e do roteiro.
5. Processar consultas, perguntas e leitura do scanner.
6. Avaliar a decisão uma única vez, atualizar contadores e salvar a ocorrência.
7. Animar o desfecho e liberar o próximo atendimento ou mostrar o relatório.

`jogo.py` coordena essas etapas. Ele ainda concentra o desenho do cenário e o tratamento dos cliques. Os detalhes das funcionalidades ficam nos módulos correspondentes.

## Cuidados da implementação

- Todos os personagens, incluindo Lucas, são carregados em `personagens.py`.
- As imagens são preparadas depois da criação da janela e antes do loop.
- A fila é uma lista embaralhada; `pop(0)` retira cada identificador uma única vez.
- `montar_caso()` usa cópias para preservar os dados originais dos JSONs.
- O estado do visitante impede decisões durante entrada e saída.
- A flag `registrado` evita contabilizar a mesma decisão em vários quadros.
- O scanner usa tempo decorrido, sem bloquear o loop com espera.
- As imagens usadas em animações são copiadas para preservar o catálogo.

O antigo `funcoes.py` foi dividido entre `regras.py` e `interface.py`. A geração antiga de campainha e as funções de recorde foram removidas por não participarem da versão atual.

## Execução

Consulte o [README principal](../README.md) para instalação, controles e regras.