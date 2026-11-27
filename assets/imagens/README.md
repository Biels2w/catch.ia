# Imagens do Catch.IA

Esta pasta reúne texturas, sprites, fotos e ícones.

## Cenário

| Arquivo | Uso |
| --- | --- |
| parede.png | Parede interna |
| moldura.png | Moldura e peitoril |
| ceu.png | Céu externo |
| muro.png | Muro externo |
| floor.png | Chão externo |
| balcao.png | Tampo e frente do balcão |

## Objetos e consultas

| Arquivo | Uso |
| --- | --- |
| arquivo.png | Pasta do manual |
| folha_manual.png | Fundo das consultas |
| botoes.png | Painel de autorizar e recusar |
| calendario.png | Calendário |
| jornal.png | Boletim do refúgio |
| relogio.png | Base do relógio |
| campainha.png | Campainha |
| livro_ocorrencias.png | Livro sobre o balcão |
| interfone.png | Interfone |
| lista_moradores.png | Prancheta de moradores |
| scanner.png | Scanner |
| passe_documento.png | Passe sobre a mesa |
| fundo_documento.png | Fundo da identificação aberta |

Os textos, ponteiros, luminária e efeitos de iluminação são
desenhados pelo Pygame.

## Vidas e relatório

- coracao_cheio.png
- coracao_vazio.png
- icone_derrota.png
- icone_vitoria.png
- fundo_relatorio.png

Esses arquivos são carregados por carregar_sprites_interface().

## Personagens utilizados

| Personagem | Pasta e arquivos |
| --- | --- |
| Lucas | Lucas/Lucas_transparente.png e Lucas_ia/lucas_ia_transparente.png |
| Gael | Gael/gael_transparente.png e Gael IA/gael_ia_transparente.png |
| Estefanny | estefanny/estefanny_transparente.png e estefanny_ia_transparente.png |
| Nayra | Nayra/nayra_transparente.png e nayra_ia_transparente.png |
| Amanda | amanda/amanda_transparente.png e amanda_ia_transparente.png |
| Nero | Nero/nero_transparente.png e nero_ia_transparente.png |
| Sarah | Sarah/sarah_transparente.png e sarah_ia_transparente.png |

Os caminhos da tabela partem de personagens/.

Todos chegam com aparência humana. A forma correspondente à
identidade sorteada aparece após a decisão.

## Fotos dos documentos

- lucas_documento.png: foto antiga do Lucas.
- personagens/Nayra/nayra_documento.png: cabelo preto e franja.
- personagens/Sarah/sarah_documento.png: cabelo comprido.
- Estefanny, Amanda e Nero utilizam imagens humanas preparadas como foto.
- Gael não apresenta documento.

As duas identidades de um personagem podem apresentar a mesma foto.

## Preparação

carregar_par remove margens transparentes e ajusta as duas formas
ao mesmo tamanho.

preparar_foto ajusta as imagens ao espaço da identificação.
preparar_passe cria uma miniatura independente para o atendimento.

GIFs, imagens originais e scripts auxiliares não são carregados
automaticamente pela partida.

## Origem

As texturas e sprites preparados durante o desenvolvimento receberam
apoio da geração de imagens do ChatGPT, com referências fornecidas
pelo grupo.

That's Not My Neighbor foi uma referência de ambientação e
organização dos elementos de fiscalização.
