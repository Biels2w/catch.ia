# Imagens do Catch.IA

## Cenário

| Arquivos | Uso |
| --- | --- |
| `parede.png`, `moldura.png` | Parede interna e janela |
| `ceu.png`, `muro.png`, `floor.png` | Área externa |
| `balcao.png` | Tampo e frente do balcão |

## Objetos e interface

- `arquivo.png` e `folha_manual.png`: manual e fundo das consultas.
- `botoes.png`: painel de autorizar e recusar.
- `calendario.png`, `jornal.png`, `relogio.png`: objetos da parede.
- `campainha.png`, `interfone.png`, `scanner.png`: equipamentos.
- `lista_moradores.png`, `livro_ocorrencias.png`: consultas do posto.
- `passe_documento.png`, `fundo_documento.png`: documento entregue e identificação ampliada.
- `coracao_cheio.png`, `coracao_vazio.png`: vidas.
- `fundo_relatorio.png`, `icone_vitoria.png`, `icone_derrota.png`: encerramento.

A luminária, a iluminação, os ponteiros, os textos e alguns efeitos são desenhados pelo Pygame.

## Personagens

Cada pasta abaixo fica dentro de `personagens/` e reúne as duas formas do personagem:

| Identificador | Pasta |
| --- | --- |
| `lucas` | `Lucas/` |
| `gael` | `Gael/` |
| `estefanny` | `estefanny/` |
| `nayra` | `Nayra/` |
| `amanda` | `Amanda/` |
| `nero` | `Nero/` |
| `sarah` | `Sarah/` |
| `matheus` | `Matheus/` |
| `lia` | `Lia/` |
| `otavio` | `Otavio/` |

O catálogo `ARQUIVOS`, em `src/personagens.py`, informa os nomes exatos dos PNGs. Todos chegam com aparência humana. A identidade sorteada é revelada após a decisão.

As fotos antigas de Lucas, Nayra e Sarah ficam nas respectivas pastas, com nomes terminados em `_documento.png`. Os demais personagens com documento usam a imagem humana preparada como foto. Gael não apresenta documento.

`carregar_par()` ajusta as formas ao mesmo tamanho; `preparar_foto()` preserva a proporção dentro do espaço da identificação.

## Origem

Texturas e sprites preparados durante o desenvolvimento receberam apoio da geração de imagens do ChatGPT, com referências fornecidas pelo grupo. That's Not My Neighbor foi uma referência de ambientação e disposição dos objetos de fiscalização.

Os materiais originais e intermediários preservados em `referencias/personagens/` não são carregados pelo jogo. Autoria e licença de recursos externos devem ser registradas quando identificadas; não há uma licença única declarada para todas as imagens.