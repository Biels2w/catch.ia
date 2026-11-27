# Dados do Catch.IA

Os arquivos JSON utilizam UTF-8 e são lidos pelos módulos de `src`.

| Arquivo | Conteúdo | Módulo principal |
| --- | --- | --- |
| `casos.json` | Variações de cada atendimento | `casos.py` |
| `documentos.json` | Modelos de documento para humano e IA | `documentos.py` |
| `roteiros_interfone.json` | Chegada, perguntas, respostas e repetições | `dialogos.py` |
| `moradores.json` | Nome, código, nascimento e setor dos moradores | `moradores.py` |
| `ocorrencias.json` | Decisões realizadas no turno | `dados.py` |

## Identificadores

Casos, documentos e roteiros reconhecem os mesmos 10 visitantes:

`lucas`, `gael`, `estefanny`, `nayra`, `amanda`, `nero`, `sarah`, `matheus`, `lia` e `otavio`.

Cada visitante possui dados para `humano` e `ia`. Gael possui documento `null` nas duas identidades, pois chega sem passe.

O cadastro de moradores possui 12 registros: nove visitantes cadastrados e Bia, Helena e Davi. Gael não está cadastrado. A lista de moradores não define quem entra na fila de atendimento.

## Casos e coerência

Um caso pode alterar campos do documento, escolher um modelo-base ou substituir falas por suas ações. Os identificadores das ações devem corresponder às perguntas do roteiro.

O documento pode estar copiado corretamente enquanto a contradição aparece na conversa. Códigos, nomes, setores, datas e falas precisam ser conferidos em conjunto. A data fictícia de referência é 22/11/2042.

## Ocorrências

Cada registro contém `nome`, `caso`, `tipo`, `decisao`, `acertou`, `vidas`, `data` e `hora`. A data e a hora do registro pertencem ao mundo fictício do jogo.

As ocorrências são atualizadas após uma decisão confirmada. O arquivo começa vazio no início da partida e é limpo ao reiniciar com `R`. Não representa um ranking ou histórico permanente de vários turnos.

`recorde.txt` e `ranking.txt` pertenciam ao template e foram separados em `referencias/template/`, pois não são usados nesta versão.