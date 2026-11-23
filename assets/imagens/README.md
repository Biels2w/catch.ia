# Imagens do Catch.IA

Esta pasta reúne as texturas, os sprites e os ícones do projeto.

A presença de um arquivo na pasta não significa que ele já esteja integrado à partida.

## Cenário

| Arquivo | Uso |
| --- | --- |
| `parede.png` | Parede interna do posto |
| `moldura.png` | Moldura e peitoril da janela |
| `ceu.png` | Céu visto pela janela |
| `muro.png` | Muro externo |
| `floor.png` | Chão externo |
| `balcao.png` | Textura do tampo e da frente do balcão |

## Objetos e consultas

| Arquivo | Uso |
| --- | --- |
| `arquivo.png` | Pasta que abre o manual de códigos |
| `folha_manual.png` | Fundo das consultas abertas |
| `botoes.png` | Painel de autorizar e recusar |
| `calendario.png` | Calendário da parede |
| `jornal.png` | Boletim do refúgio |
| `relogio.png` | Base do relógio |
| `campainha.png` | Campainha que chama o visitante |
| `livro_ocorrencias.png` | Livro sobre o balcão |

Os ponteiros do relógio, a luminária e os efeitos de iluminação são desenhados pelo Pygame.

## Vidas e relatório

| Arquivo | Uso |
| --- | --- |
| `coracao_cheio.png` | Vida disponível |
| `coracao_vazio.png` | Vida perdida |
| `icone_derrota.png` | Caveira exibida na derrota |
| `icone_vitoria.png` | Escudo exibido na vitória |
| `fundo_relatorio.png` | Folha do relatório final |

Esses arquivos são carregados pela função `carregar_sprites_interface()`, em `src/sprites.py`.

## Personagens

O atendimento atual utiliza:

- `personagens/Lucas/Lucas_transparente.png`
- `personagens/Lucas_ia/lucas_ia_transparente.png`

O código ajusta as imagens para a altura do visitante, usando a proporção da versão humana.

Lucas chega com aparência humana. Sua identidade é sorteada a cada atendimento e revelada depois da decisão.

As demais pastas de personagens contêm materiais em preparação, como imagens, GIFs e scripts auxiliares. Esses personagens ainda não são selecionados pelo atendimento atual.

## Recursos preparados

- `interfone.png`: futura interação de diálogos.
- `lista_moradores.png`: futura consulta de moradores.
- `scanner.png`: futuro scanner com falhas.

Esses equipamentos ainda não estão conectados às interações da versão atual.

## Textos e transparência

Os códigos, datas, avisos, registros e resultados são desenhados pelo Pygame sobre os sprites.

Os PNGs transparentes usam `convert_alpha()` após a criação da janela.

## Origem e autoria

As texturas e os sprites gerados para o cenário, os objetos, as vidas, o relatório e as versões transparentes de Lucas foram produzidos com auxílio do ChatGPT e integrados ao projeto pelo grupo.

O calendário e os avisos na parede tiveram como referência de ambientação o jogo *That's Not My Neighbor*.

Os materiais dos demais personagens foram adicionados ao repositório pelo grupo. Sua origem e licença ainda precisam ser individualizadas na documentação antes da integração à entrega final.
