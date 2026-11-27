# Catch.IA

Jogo de investigação e tomada de decisões desenvolvido em Python e Pygame para o projeto final de Introdução a Algoritmos/Programação.

## Integrantes

- Gabriel de Oliveira Costa
- Ana Ayla Pires Reis
- Gabriel Rodrigues Lima
- Patrick Souza

## Proposta

Em um futuro fictício, o jogador trabalha no posto de fiscalização de um refúgio humano. Sua tarefa é analisar documentos, conversar com visitantes e conferir informações antes de autorizar ou recusar a entrada.

O tema é **Inteligência Artificial no Cotidiano: Aplicações e Uso Responsável**, com foco em segurança, confiabilidade e análise crítica de resultados automatizados. O scanner pode errar, e uma IA pode apresentar dados copiados. A decisão exige comparar diferentes evidências.

O jogo simula identidades e leituras com regras e sorteios; não utiliza IA real para detectar pessoas.

## Regras e objetivo

- O turno possui 10 atendimentos, com personagens diferentes e ordem embaralhada.
- O jogador começa com 3 vidas.
- Liberar um humano ou recusar uma IA conta como acerto.
- Liberar uma IA ou recusar um humano retira uma vida.
- A decisão confirmada não pode ser desfeita.
- Concluir os 10 atendimentos com pelo menos uma vida resulta em vitória.
- Esgotar as vidas resulta em derrota, inclusive no último atendimento.

O relatório final apresenta resultado, atendimentos, acertos, erros, duração e data real da partida. Não há ranking nem pontuação em moedas.

## Investigação

| Item | Função |
| --- | --- |
| Campainha | Chama o próximo visitante quando o posto está livre |
| Interfone | Apresenta perguntas, respostas e pedido de documento |
| Passe | Permite conferir os dados apresentados pelo visitante |
| Manual | Consulta dos códigos permitidos |
| Lista de moradores | Consulta de nomes, códigos, nascimentos e setores |
| Calendário | Referência da data fictícia para conferir informações |
| Jornal | Boletim com informações do universo do jogo |
| Scanner | Leitura simulada que pode estar correta, errada ou inconclusiva |
| Livro de ocorrências | Registro das decisões do turno |
| Luminária e relógio | Iluminação interativa e acompanhamento do horário |

Os visitantes são Lucas, Gael, Estefanny, Nayra, Amanda, Nero, Sarah, Matheus, Lia e Otávio. Cada um possui formas humana e IA; todos chegam com aparência humana. Bia, Helena e Davi aparecem apenas no cadastro de moradores e podem ser citados nas conversas.

## Controles

- Mouse: interagir com os objetos, perguntas, páginas e botões.
- Clique fora de uma consulta ou `Esc`: fechar a consulta.
- Instruções: mouse, setas esquerda/direita e `Enter`; `Esc` encerra o jogo nessa tela.
- `R` no relatório: iniciar uma nova partida.
- `B` no relatório: consultar o livro de ocorrências.
- Fechar a janela: encerrar o programa.

## Execução e testes

Na pasta raiz do projeto, com Python instalado:

```bash
python -m pip install -r requirements.txt
python main.py
```

Para executar os testes:

```bash
python -m pytest
```

No VS Code, selecione o mesmo interpretador em que as dependências foram instaladas. Inicie pelo `main.py`. Parte dos caminhos de imagens depende da execução a partir da raiz.

## Organização

- `main.py`: entrada da aplicação.
- [src/](src/README.md): módulos do jogo e suas responsabilidades.
- [data/](data/README.md): casos, documentos, moradores, diálogos e ocorrências.
- [assets/](assets/README.md): recursos visuais e sonoros usados pela partida.
- [tests/](tests/README.md): testes automatizados de lógica.
- [docs/](docs/README.md): planejamento e [proposta](docs/proposta.MD).
- [referencias/](referencias/README.md): materiais de preparação e arquivos antigos.

## Tempo e arquivos

O mundo do jogo utiliza a data 22/11/2042 e inicia o expediente às 08:00. O relatório utiliza a data real do computador. As instruções não entram no tempo da partida.

As decisões são gravadas em `data/ocorrencias.json`. O arquivo é limpo ao começar um turno e ao reiniciar com `R`; não funciona como histórico de várias partidas. A página selecionada do manual permanece ao fechar e reabrir a consulta durante a execução, sem gravação dessa preferência em arquivo.

## Autoria e recursos externos

O projeto adapta o template disponibilizado pela disciplina. O grupo definiu e integrou a proposta, o roteiro e as mecânicas, com apoio do ChatGPT em código, explicações, documentação e preparação de recursos.

That's Not My Neighbor foi uma referência de ambientação e disposição dos elementos de fiscalização. O roteiro-base foi fornecido pelo grupo no documento `Roteiro- Catch.ia.pdf` e recebeu adaptações para os casos do jogo.

As origens conhecidas dos recursos estão em [imagens](assets/imagens/README.md) e [sons](assets/sons/README.md). Não há uma licença única declarada para todos os materiais. Cada integrante deve conseguir explicar as partes em que trabalhou e as principais rotinas.