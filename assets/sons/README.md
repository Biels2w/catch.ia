# Sons do Catch.IA

Esta pasta contém a trilha ambiente e os efeitos sonoros do projeto.

O módulo `src/audio.py` carrega os sons antes do loop principal e define seus volumes.

## Arquivos utilizados

| Arquivo | Uso |
| --- | --- |
| `trilha_refugio.wav` | Trilha ambiente reproduzida em repetição |
| `pagina_generica.wav` | Abertura, fechamento e troca de páginas das consultas |
| `botao.wav` | Confirmação de autorizar ou recusar |
| `luz_ligar.wav` | Interruptor ao acender a luminária |
| `luz_desligar.wav` | Interruptor ao apagar a luminária |
| `campainha.wav` | Chamada do próximo visitante |

## Reprodução

O mesmo arquivo de papel é utilizado nas ações `abrir`, `fechar` e `pagina`, com volumes definidos separadamente.

Essas ações são utilizadas pelo manual, calendário, jornal e livro de ocorrências.

A trilha usa `pygame.mixer.music`. Os efeitos usam `pygame.mixer.Sound`.

Se o mixer não estiver inicializado, o módulo permite que o jogo continue sem reproduzir áudio.

## Recursos reservados

Os seguintes arquivos estão disponíveis na pasta, mas não são carregados pelo mapa de efeitos atual:

- `interfone_chamar.wav`
- `interfone_resposta.wav`
- `lista_abrir.wav`
- `livro_abrir.wav`
- `scanner_ler.wav`
- `scanner_ok.wav`
- `scanner_falha.wav`
- `virar_pagina.wav`

O livro usa atualmente `pagina_generica.wav`.

A integração do interfone, da lista de moradores e do scanner continua em desenvolvimento.

## Origem e referências

A trilha e os efeitos sintéticos preparados durante o projeto foram produzidos com apoio do ChatGPT.

O arquivo `pagina_generica.wav` foi preparado a partir da referência sonora fornecida pelo grupo nos vídeos anexados durante o desenvolvimento.

Também foi indicada esta [referência de som de papel no YouTube](https://www.youtube.com/watch?v=CPVDvxPlhlc).

A autoria original e a licença da gravação utilizada como referência para o efeito de papel ainda não estão documentadas no repositório. Esse efeito não é apresentado como uma criação inteiramente sintetizada ou como um recurso de licença livre.

Ao acrescentar ou substituir sons, registre o arquivo, sua origem, autoria e licença disponível.