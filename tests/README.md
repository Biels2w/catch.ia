# Testes do Catch.IA

Execute na raiz do projeto:

```bash
python -m pytest
```

Para executar um arquivo específico:

```bash
python -m pytest tests/test_personagens.py
```

Evite executar um arquivo de testes diretamente pelo botão de reprodução do editor; o comando acima mantém a raiz do projeto disponível para os imports de `src`.

## Organização

| Arquivo | Verificações |
| --- | --- |
| `test_logica.py` | Decisões, perda de vidas e entradas inválidas de `regras.py` |
| `test_relatorio.py` | Vitória, derrota, contagem e duração do relatório |
| `test_dialogos.py` | Perguntas, respostas e controle das repetições |
| `test_documentos.py` | Entrega do documento e independência dos dados |
| `test_moradores.py` | Cadastro, ordenação e paginação |
| `test_scanner.py` | Leitura, prazo, resultados e restrições de repetição |
| `test_personagens.py` | Coerência dos casos dos 10 visitantes e fila sem repetição |

Os testes de personagens verificam principalmente os dados e a lógica dos atendimentos. Eles não substituem a conferência visual dos sprites.

## Conferência manual

- Abrir o jogo pelo `main.py` e navegar pelas instruções.
- Conferir os 10 visitantes sem repetição em um turno completo.
- Consultar documentos, manual, moradores, calendário, jornal e ocorrências.
- Fazer perguntas pelo interfone e utilizar o scanner.
- Conferir efeitos, sons, vitória, derrota e reinício com `R`.
- Verificar que um erro retira apenas uma vida e gera uma ocorrência.