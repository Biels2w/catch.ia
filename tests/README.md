# Testes do Catch.IA

Esta pasta reúne testes de lógica e de dados utilizando pytest.

## Arquivos

| Arquivo | Verificações |
| --- | --- |
| test_logica.py | Decisões, vidas e persistência das ocorrências |
| test_relatorio.py | Vitória, derrota e dados do relatório |
| test_dialogos.py | Perguntas, repetição e conversas independentes |
| test_documentos.py | Entrega única e preservação dos modelos |
| test_moradores.py | Cadastro, paginação e limites |
| test_scanner.py | Probabilidades, duração e tentativas permitidas |
| test_personagens.py | Casos dos personagens e visitas a moradores |

Os testes específicos dos personagens permanecem reunidos
em test_personagens.py.

O teste de persistência utiliza uma pasta temporária fornecida
pelo pytest.

## Execução

Abra o terminal na raiz do projeto.

Instale as dependências:
`python -m pip install -r requirements.txt`

Execute todos os testes:
`python -m pytest`

Execute apenas os testes dos personagens:
`python -m pytest tests/test_personagens.py -v`

Executar pela raiz permite que o Python encontre o pacote src.

## Verificação manual

Execute `python main.py` e confira:

1. Navegação das três páginas de instruções.
2. Início do tempo somente após selecionar Iniciar.
3. Campainha e chegada do visitante.
4. Perguntas e pedido de documentos pelo interfone.
5. Foto correta na ficha e na miniatura do passe.
6. Consultas e paginação do manual, moradores e ocorrências.
7. Visitas com dados corretos e contraditórios.
8. Leitura do scanner e repetição após resultado inconclusivo.
9. Uma única contagem e gravação por decisão.
10. Perda de uma vida por erro.
11. Vitória após dez atendimentos com vidas restantes.
12. Derrota após três erros.
13. Animações, iluminação, efeito de dano e áudio.
14. Reinício com R e consulta ao livro com B no resultado.
15. Duração congelada no relatório final.

Os testes de funções devem ser acompanhados da verificação
do fluxo gráfico completo.