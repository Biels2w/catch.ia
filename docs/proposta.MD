# Proposta do projeto — Catch.IA

Proposta atualizada em 27/11/2026. Versão final do game.

## 1. Nome do jogo

**Catch.IA**

## 2. Integrantes

- Gabriel de Oliveira Costa
- Ana Ayla Pires Reis
- Gabriel Rodrigues Lima
- Patrick Souza

## 3. Tema específico e uso responsável

Dentro do eixo **Inteligência Artificial no Cotidiano: Aplicações e Uso Responsável**, o grupo escolheu **segurança e confiabilidade de sistemas automatizados de identificação**, com ênfase na conferência de informações e na supervisão humana.

O jogo aborda o risco de confiar em uma única evidência ou aceitar automaticamente a resposta de uma ferramenta. O scanner pode falhar, um documento pode conter dados copiados e diferenças na aparência não bastam para determinar uma identidade.

## 4. Integração do tema com a jogabilidade

O jogador precisa cruzar documentos, respostas, códigos, cadastro e datas para decidir quem pode entrar no refúgio. Uma leitura do scanner funciona apenas como indício. Liberar uma IA ou recusar um humano retira uma vida, fazendo a análise crítica das informações influenciar diretamente o resultado da partida.

As identidades e leituras são simuladas por regras, estruturas de dados e sorteios. O projeto não implementa uma tecnologia real de detecção de IA.

## 5. Estilo e descrição geral

Jogo de investigação e tomada de decisões, com visão em primeira pessoa de um posto de fiscalização.

Em um futuro fictício, após uma revolta de inteligências artificiais, o jogador assume o papel de fiscal de um refúgio humano. Um visitante por vez chega à janela. O jogador controla o atendimento com o mouse, consulta os objetos do cenário, faz perguntas e decide entre autorizar e recusar a entrada.

O desafio está nas contradições entre fontes: documentos adulterados, códigos pertencentes a outra pessoa, datas incompatíveis, relatos inconsistentes e resultados falhos do scanner. Alguns casos apresentam documentos corretos e exigem conferir a conversa.

## 6. Objetivo

Concluir 10 atendimentos com pelo menos uma vida restante, identificando humanos e IAs disfarçadas por meio da análise das evidências disponíveis.

## 7. Regras principais

1. O jogador começa com 3 vidas.
2. Um turno completo apresenta 10 personagens diferentes, em ordem embaralhada; a identidade humana ou IA e o caso são sorteados na chegada.
3. Antes de decidir, o jogador pode fazer perguntas e consultar os recursos do posto. Uma leitura inconclusiva do scanner pode ser repetida.
4. Liberar um humano ou recusar uma IA conta como acerto; a decisão contrária retira uma vida.
5. Uma escolha confirmada é registrada uma única vez, não pode ser desfeita e inicia a revelação e a saída do visitante.

## 8. Vitória

O jogador vence ao concluir os 10 atendimentos com pelo menos uma vida. Após o desfecho do último visitante, é exibido um relatório com resultado, quantidade de atendimentos, acertos, erros, duração e data real da partida.

## 9. Derrota e encerramento

O jogador perde ao cometer três erros e esgotar suas vidas. Isso também vale se o terceiro erro ocorrer no décimo atendimento. A derrota pode encerrar o turno antes da apresentação dos 10 personagens.

Não existe limite de tempo para decidir. No relatório, `R` inicia uma nova partida e limpa as ocorrências do turno anterior. Fechar a janela encerra o programa.

## 10. Personagens e moradores

O jogo possui 10 personagens atendidos: Lucas, Gael, Estefanny, Nayra, Amanda, Nero, Sarah, Matheus, Lia e Otávio. Cada personagem possui formas humana e IA. Portanto, são 10 nomes disponíveis, com duas formas visuais cada, e não 20 visitantes diferentes.

Todos chegam com aparência humana. Gael não apresenta documento e não consta no cadastro, exigindo atenção ao diálogo.

Bia, Helena e Davi constam apenas na lista de moradores e podem ser mencionados como pessoas que recebem visitas. Eles não entram na fila da recepção.

## 11. Elementos e interações

| Elemento | Participação no jogo |
| --- | --- |
| Posto e janela | Espaço do atendimento e das animações |
| Campainha | Chamada do próximo visitante |
| Interfone | Perguntas, respostas, repetições e pedido de documento |
| Passe | Conferência de identificação e dados apresentados |
| Manual | Páginas de códigos permitidos |
| Lista de moradores | Conferência de nomes, códigos, nascimentos e setores |
| Calendário e jornal | Referências de data e informações do refúgio |
| Scanner | Leitura com duração e possibilidade de erro ou resultado inconclusivo |
| Botões verde e vermelho | Autorização ou recusa da entrada |
| Livro de ocorrências | Consulta das decisões registradas no turno |
| Relógio e luminária | Horário do expediente e iluminação interativa |
| Corações e relatório | Vidas, progresso e resultado |

O scanner leva aproximadamente 2,2 segundos por leitura. Cada tentativa possui 25% de chance de ser inconclusiva, 15% de apresentar um indício incorreto e 60% de apresentar um indício correto. Um resultado regular ou irregular permanece associado ao visitante até o fim do atendimento.

O universo utiliza 22/11/2042 como data de referência e inicia o expediente às 08:00. O relatório final registra a data real do computador.

## 12. Controles

- Mouse: objetos, perguntas, páginas e decisões.
- Clique fora da consulta ou `Esc`: fechar a consulta.
- Mouse, setas esquerda/direita e `Enter`: navegar pelas instruções.
- `Esc` nas instruções: encerrar o jogo.
- `R` no relatório: reiniciar a partida.
- `B` no relatório: abrir o livro de ocorrências.

## 13. Organização do código e dos dados

`main.py` inicia a aplicação. `src/jogo.py` coordena o cenário, os eventos e os estados da partida. Os demais módulos separam personagens, regras, interface, casos, diálogos, documentos, moradores, scanner, consultas, arquivos, relatório, efeitos, áudio, sprites e instruções.

As responsabilidades de cada módulo estão descritas em `src/README.md`. Todos os personagens e fotos são carregados por `personagens.py`.

Listas organizam a fila e as páginas; dicionários representam personagens, casos e estados; conjuntos controlam perguntas realizadas. Arquivos JSON armazenam casos, documentos, diálogos, moradores e ocorrências. Cópias dos modelos evitam que um atendimento altere os dados originais.

O histórico é gravado em `data/ocorrencias.json` durante o turno e limpo ao começar uma nova partida. Os testes com `pytest` verificam funções de lógica e a coerência dos dados.

## 14. Recursos

- Python e Pygame para implementação e interface.
- Pytest para testes de lógica.
- Sprites e texturas PNG, efeitos WAV e fonte padrão do Pygame.
- Git e GitHub para versionamento e colaboração.
- Roteiro fornecido pelo grupo, com adaptações para os casos.
- Apoio do ChatGPT em explicações, código, documentação e preparação de recursos.

As origens conhecidas e as informações disponíveis sobre licenças estão registradas nos READMEs de `assets/`.

## 15. Dificuldades do desenvolvimento

- Manter documentos, diálogos e casos coerentes para as duas identidades dos 10 personagens.
- Controlar cliques, consultas e animações sem duplicar decisões ou perder o estado do atendimento.
- Preparar imagens com transparência, proporção e posicionamento adequados.
- Integrar sons e efeitos sem interromper o loop.
- Separar responsabilidades e manter os testes e a documentação consistentes.

## 16. Escopo mínimo e melhorias possíveis

O escopo mínimo compreende cenário funcional, instruções, 10 personagens disponíveis, turno de 10 atendimentos sem repetição, investigação por documentos e diálogos, consultas, scanner com falhas, três vidas, vitória, derrota, relatório, reinício, gravação de ocorrências e testes de lógica.

A versão desenvolvida contempla esses elementos. Melhorias futuras podem incluir novos casos, mais informações de acessibilidade, ajustes de dificuldade e separação adicional do desenho do cenário em módulos. Essas melhorias não são necessárias para concluir o turno atual.

## 17. Originalidade, autoria e referências

O projeto parte do template da disciplina e foi adaptado à proposta de investigação do grupo. That's Not My Neighbor serviu como referência de ambientação e organização visual do posto; o código e os recursos do jogo de referência não são apresentados como produção do grupo.

O roteiro-base foi fornecido no documento `Roteiro- Catch.ia.pdf`, com adaptações e complementos para os atendimentos. Recursos e trechos preparados com apoio do ChatGPT são reconhecidos na documentação.

O grupo declara que não apresenta um jogo integralmente copiado de projetos anteriores, tutoriais ou repositórios prontos. Cada integrante deve compreender e explicar suas contribuições e as principais rotinas implementadas. Recursos externos devem manter os créditos e as informações de licença disponíveis; não é declarada uma licença única para todo o material.