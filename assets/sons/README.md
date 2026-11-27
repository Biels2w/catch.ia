# Sons do Catch.IA

`src/audio.py` carrega os efeitos antes do loop e define os volumes.

| Arquivo | Uso |
| --- | --- |
| `trilha_refugio.wav` | Trilha ambiente em repetição |
| `pagina_generica.wav` | Abertura, fechamento e troca de páginas |
| `botao.wav` | Botões de decisão |
| `luz_ligar.wav`, `luz_desligar.wav` | Luminária |
| `campainha.wav` | Chamada de visitante |
| `interfone_chamar.wav`, `interfone_resposta.wav` | Interação com o interfone |
| `lista_abrir.wav` | Abertura do cadastro de moradores |
| `scanner_ler.wav` | Início da leitura |
| `scanner_ok.wav` | Leitura concluída |
| `scanner_falha.wav` | Leitura inconclusiva |

O som de conclusão do scanner não garante que o indício esteja correto. O equipamento pode produzir um resultado incorreto sem reconhecer o próprio erro.

`livro_abrir.wav` e `virar_pagina.wav` estão reservados e não fazem parte do mapa atual. O livro utiliza o efeito genérico de papel.

## Reprodução

A música usa `pygame.mixer.music`; os efeitos usam `pygame.mixer.Sound`. Se o mixer não iniciar, o carregador retorna um dicionário vazio e permite continuar sem áudio.

## Origem

A trilha e os efeitos sintéticos preparados durante o projeto foram produzidos com apoio do ChatGPT.

O efeito de papel foi preparado a partir das referências sonoras fornecidas pelo grupo nos vídeos anexados. Também foi indicada esta [referência no YouTube](https://www.youtube.com/watch?v=CPVDvxPlhlc).

A autoria e a licença da gravação original usada como referência do papel ainda não estão documentadas. Esse efeito não é declarado como inteiramente sintetizado ou de licença livre.