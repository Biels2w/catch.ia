# Testes do Catch.IA

Esta pasta contém testes automatizados da lógica do jogo e da persistência de dados.

## Arquivos

### `test_logica.py`

Verifica:

- As quatro combinações entre identidade e decisão.
- A manutenção das vidas nas decisões corretas.
- A perda de uma vida nas decisões erradas.
- A proteção contra vidas negativas.
- A gravação e a leitura de ocorrências em JSON.
- O primeiro uso, quando o arquivo de ocorrências ainda não existe.

O teste de persistência utiliza uma pasta temporária fornecida pelo pytest, sem precisar sobrescrever o arquivo real da partida.

### `test_relatorio.py`

Verifica:

- A continuidade da partida antes da meta, com vidas disponíveis.
- A vitória ao completar 10 atendimentos com uma vida restante.
- A derrota ao esgotar as vidas no décimo atendimento.
- A formatação da data e da duração.
- Os acertos, os erros e o total de atendimentos do relatório.

O conjunto atual contém cinco funções de teste.

## Como executar

Abra o terminal na raiz do projeto, onde está `main.py`.

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Execute todos os testes:

```powershell
python -m pytest
```

Para executar somente os testes do relatório:

```powershell
python -m pytest tests/test_relatorio.py
```

Execute os comandos a partir da raiz para que o Python encontre o pacote `src`.

## Verificação manual

Os testes atuais não verificam automaticamente a interface, as animações, o áudio ou a integração completa dos contadores com o loop.

Execute:

```powershell
python main.py
```

Confira os seguintes comportamentos:

1. A campainha chama um visitante quando o posto está livre.
2. Os botões avaliam a decisão somente quando o visitante está aguardando.
3. Cliques repetidos não geram vários registros para a mesma decisão.
4. Um erro retira uma vida e acrescenta exatamente um erro e um atendimento.
5. Errar os três primeiros atendimentos gera um relatório com três atendimentos, zero acertos e três erros.
6. Completar 10 atendimentos com vidas restantes gera vitória.
7. Visitantes autorizados saem pela direita.
8. IAs recusadas são desativadas.
9. Humanos recusados são capturados para cima.
10. O livro mostra três registros por página e permite navegar.
11. Reiniciar pela tela de resultado zera os contadores, o tempo e o livro.
12. B abre o livro na tela de resultado e Esc retorna ao relatório.
13. As consultas fecham com Esc ou clique fora da folha.
14. A luminária liga e desliga.
15. A trilha e os efeitos são reproduzidos.
16. A duração permanece congelada no relatório.

A aprovação dos testes de funções deve ser acompanhada da verificação manual do fluxo completo.