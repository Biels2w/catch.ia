# Catch.IA

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido em Python com Pygame.

## Integrantes

- Gabriel de Oliveira Costa
- Ana Ayla Pires Reis
- Gabriel Rodrigues Lima
- Patrick Souza

## Sobre o jogo

Catch.IA é um jogo de investigação e tomada de decisões ambientado em um futuro fictício no qual algumas inteligências artificiais se voltaram contra a humanidade.

O jogador assume o papel de um fiscal responsável por controlar a entrada em um refúgio humano. Sua missão é identificar humanos e IAs disfarçadas, decidindo quem pode entrar.

## Tema e uso responsável da IA

O tema escolhido é segurança e confiabilidade na identificação de IAs.

A proposta destaca a importância de conferir informações, comparar evidências e considerar as consequências das decisões: autorizar uma IA compromete a segurança do refúgio, enquanto recusar um humano representa uma decisão injusta.

A identificação é simulada por regras e estruturas de dados do Python. O projeto não implementa uma IA real, e sua narrativa não representa um método real de identificação de conteúdos ou pessoas.

## Funcionalidades implementadas

- Janela de 800 × 600 pixels, loop principal e limite de 60 FPS.
- Cenário texturizado com parede, janela, balcão e ambiente externo.
- Campainha para chamar o próximo visitante.
- Entrada do personagem pela esquerda da janela.
- Identidade sorteada entre humano e IA.
- Botões para autorizar ou recusar a entrada.
- Revelação da identidade após a decisão.
- Saída pela direita para visitantes autorizados.
- Desativação de IAs recusadas.
- Captura para cima de humanos recusados.
- Sistema de três vidas com sprites de corações.
- Manual de códigos permitidos com navegação entre páginas.
- Calendário e jornal consultáveis.
- Relógio com ponteiros animados.
- Luminária que pode ser ligada e desligada.
- Livro de ocorrências com navegação entre páginas.
- Gravação dos atendimentos em arquivo JSON.
- Trilha ambiente e efeitos sonoros.
- Condições de vitória e derrota.
- Relatório final com data, duração, acertos, erros e atendimentos.
- Reinício da partida e consulta às ocorrências pela tela de resultado.

## Funcionalidades em desenvolvimento

O atendimento atual utiliza o personagem Lucas. Sua identidade é sorteada e revelada após a decisão.

Ainda serão integrados os documentos individuais, os diálogos pelo interfone, a lista de moradores e o scanner com falhas. Esses recursos deverão fornecer informações que permitam investigar a identidade do visitante antes de decidir.

O manual, o calendário e o jornal já podem ser consultados, mas seu conteúdo ainda não está conectado à identidade sorteada.

Existem imagens e sons preparados para outros equipamentos e personagens que ainda não participam do fluxo atual de atendimento.

## Objetivo e regras

O objetivo é concluir **10 atendimentos com pelo menos uma vida restante**.

1. O jogador começa com três vidas.
2. Um visitante é atendido por vez.
3. A campainha chama um visitante quando o posto está livre.
4. Autorizar um humano ou recusar uma IA conta como acerto.
5. Autorizar uma IA ou recusar um humano conta como erro e retira uma vida.
6. A escolha é definitiva para aquele atendimento.
7. Cada decisão gera apenas um registro no livro.
8. Completar 10 atendimentos com vidas restantes resulta em vitória.
9. Perder todas as vidas resulta em derrota, inclusive no décimo atendimento.

O relatório aparece após a última animação. A duração fica congelada nesse momento e inclui o tempo das animações.

O tempo é um indicador de desempenho, mas não causa derrota. Não há um sistema separado de pontos ou ranking integrado à partida atual.

## Como jogar

1. Clique na campainha.
2. Espere o visitante chegar ao centro da janela.
3. Consulte os elementos disponíveis no cenário.
4. Use o botão verde para autorizar ou o vermelho para recusar.
5. Aguarde a revelação e a animação.
6. Chame o próximo visitante.
7. Ao encerrar a partida, consulte o relatório e o livro de ocorrências.

## Controles

| Controle | Ação |
| --- | --- |
| Clique esquerdo na campainha | Chamar o próximo visitante |
| Clique esquerdo no botão verde | Autorizar a entrada |
| Clique esquerdo no botão vermelho | Recusar a entrada |
| Clique esquerdo na pasta | Abrir o manual de códigos |
| Clique no calendário, jornal ou livro | Abrir a consulta correspondente |
| Clique esquerdo na luminária | Acender ou apagar a luz |
| Anterior / Próxima | Navegar pelas páginas do manual ou do livro |
| Clique fora da folha ou Esc | Fechar a consulta |
| R, na tela de resultado | Iniciar outro turno |
| B, na tela de resultado | Consultar o livro de ocorrências |
| X da janela | Encerrar o jogo |

## Datas e armazenamento

O calendário e as ocorrências usam a data fictícia **22/11/2042**. O relógio representa um expediente iniciado às 08:00.

O relatório final utiliza a data real do computador e a duração real da partida.

Os atendimentos são gravados em `data/ocorrencias.json`. Ao abrir o jogo ou reiniciar o turno, o livro e esse arquivo são limpos. Os registros não são acumulados entre partidas.

A página selecionada no manual é preservada ao fechar e reabrir a pasta durante a execução, mas não é gravada em arquivo.

## Estrutura do projeto

| Caminho | Responsabilidade |
| --- | --- |
| `main.py` | Ponto de entrada |
| `src/jogo.py` | Eventos, estado da partida, animações e cenário |
| `src/config.py` | Configurações gerais e meta de atendimentos |
| `src/funcoes.py` | Avaliação das decisões e desenho das vidas e do relógio |
| `src/consultas.py` | Calendário, jornal e livro |
| `src/relatorio.py` | Encerramento e relatório final |
| `src/audio.py` | Trilha e efeitos sonoros |
| `src/dados.py` | Leitura e gravação de dados |
| `src/sprites.py` | Carregamento e recorte de imagens |
| `assets/` | Recursos visuais e sonoros |
| `data/` | Arquivos de dados |
| `tests/` | Testes automatizados |
| `docs/` | Documentação e proposta |
| `requirements.txt` | Dependências |

## Como executar

Com o Python instalado, abra o terminal na raiz do projeto, onde está `main.py`.

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute o jogo:

```powershell
python main.py
```

Preserve a organização das pastas e execute os comandos na raiz, pois vários recursos utilizam caminhos relativos.

No VS Code, selecione o interpretador Python no qual as dependências foram instaladas.

## Como executar os testes

Na raiz do projeto:

```powershell
python -m pytest
```

Os testes verificam decisões, vidas, persistência das ocorrências, condições de encerramento e dados do relatório.

As interações gráficas, as animações e o áudio precisam ser conferidos manualmente. Consulte [tests/README.md](tests/README.md).

## Autoria e recursos externos

A estrutura inicial foi fornecida pelo template da disciplina.

O projeto recebeu apoio do ChatGPT na criação de recursos visuais e sonoros, nas explicações de programação, nas sugestões de código e na documentação. A integração e a adaptação dos recursos fazem parte do desenvolvimento do grupo.

As origens e referências dos recursos estão documentadas em:

- [Imagens](assets/imagens/README.md)
- [Sons](assets/sons/README.md)
- [Fontes](assets/fontes/README.md)

O jogo *That's Not My Neighbor* foi utilizado como referência de ambientação e organização de elementos de fiscalização, como calendário e avisos na parede.

Não há uma licença única declarada para todos os recursos do projeto. Novos materiais externos devem ter sua origem, autoria e licença registradas quando disponíveis.

Cada integrante deve compreender e conseguir explicar as partes do projeto em que trabalhou.

## Planejamento

A proposta do grupo está em [docs/proposta.MD](docs/proposta.MD).

Mudanças nas regras, nos controles e no escopo devem ser registradas na proposta conforme o desenvolvimento avança.