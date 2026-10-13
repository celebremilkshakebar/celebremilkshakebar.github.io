# Validação da landing page

Verificação realizada em 13/10/2026, no navegador integrado.

## Layout

- Larguras testadas: 390, 768 e 1440 pixels.
- Nenhuma rolagem horizontal nas três larguras.
- Menus empilhados no celular e lado a lado em tablet/computador.
- Cabeçalho e botão de contato cabem no tablet.
- Fotos reais das duas estações, com enquadramento ajustado para preservar o carrinho completo e a frente do balcão.

## Interações e arquivos

- Menu móvel abre, fecha com Escape e devolve o foco ao botão.
- Ao escolher uma seção, o menu móvel fecha e a navegação segue para a âncora.
- Pergunta sobre o mínimo de convidados abre por interação e fecha com Enter, usando o controle nativo de teclado.
- Os sete links de WhatsApp usam o número correto e a mesma mensagem do briefing. O teste não enviou mensagens.
- Nenhum arquivo referenciado ou destino de âncora ausente.
- Vídeo de feedback sem fonte carregada antes do clique; após o clique, reproduz com controles nativos, áudio e legendas embutidas.
- Reprodução completa confirmada: 11,82 segundos, resolução 720×1280 e nenhum erro de mídia.
- Página local respondeu HTTP 200.
- JavaScript e servidor de prévia passaram na verificação sintática.
- Nenhum erro de console registrado na verificação final.

## Conteúdo

- Clássico com quatro sabores e Premium com seis.
- Cinco categorias de eventos apresentadas com tratamento visual equivalente.
- Condições revisadas: 3 horas com possibilidade de extensão, mínimo de 30 convidados, Novo Hamburgo/região/proximidades, chantilly opcional, sinal para reserva, pagamento facilitado e deslocamento incluído no orçamento.
- Quatro depoimentos e nota/contagem do Google conforme o briefing.

## Contraste e carregamento

Contrastes calculados pelo método de luminância relativa WCAG:

- Terracota sobre creme: 5,18:1.
- Texto branco no botão terracota: 5,53:1.
- Texto secundário sobre creme: 5,21:1.
- Texto/ícone branco no botão flutuante: 6,77:1.

Imagens em WebP, versões responsivas e carregamento sob demanda abaixo da abertura. O vídeo de feedback é carregado após interação; o vídeo de abertura carrega automaticamente, com capa estática durante a preparação. A página não depende dos caminhos originais de mídia nem de fontes externas.

## Limites da verificação

Testes realizados em navegador integrado com larguras responsivas; não constituem teste em aparelhos físicos. Publicação em domínio público não faz parte desta entrega local. O domínio canônico e a URL absoluta de compartilhamento serão configurados ao escolher a hospedagem.

## Atualização do vídeo de abertura

- Vídeo completo de aproximadamente 60 segundos, em loop, sem áudio, com reprodução automática e `playsinline`.
- Capa original dos dois milkshakes confirmada visível enquanto o vídeo ainda carrega; troca para o vídeo após a reprodução começar.
- Reprodução, pausa e retomada verificadas no navegador. Reinício do loop observado, com o tempo passando de aproximadamente 30 para 19 segundos sem recarregar a página.
- Versão mobile de 480×854 selecionada em largura de 390 pixels, sem rolagem horizontal; vídeo reproduziu sem erro.
- Card do Google e sticker preservados; capas e vídeo ficam isolados dentro da moldura para não cobrir esses elementos.
- Desktop: 720×1280, 24 fps, aproximadamente 9,53 MB. Celular: 480×854, 24 fps, aproximadamente 4,67 MB. H264, faststart, sem faixa de áudio e decodificação completa verificados.
- Preferência por movimento reduzido mantém a capa até interação; botão de pausa/retomada disponível para controlar a animação.

## Substituição pelo segundo vídeo

Fonte atual: `Design sem nome (2).mp4`, preservada sem alterações. Vídeo completo de 60,18 s convertido para 60,17 s dentro do arredondamento de quadros a 24 fps. Mesmas otimizações: H264/yuv420p, CRF28 em 720px para desktop, CRF29 em 480px para celular, sem áudio e faststart. Qualidade visual e decodificação completa verificadas. As fontes na página usam `?v=2` para evitar reaproveitar o vídeo anterior em cache. Capa, loop, controle de pausa/retomada, card do Google e sticker preservados.

## Carrossel de três feedbacks

- Vídeo original mantido. Novos materiais: `Celebre - Video 02 - Feedbacks (1).mov` e `IMG_5193.MOV`, preservados sem alterações.
- Novos MP4 em 720×1280, H264/yuv420p, áudio AAC e faststart. Durações completas de 9,90 s e 33,18 s; tamanhos aproximados de 3,04 MB e 8,67 MB. Decodificação completa e orientação verificadas.
- Capas WebP próprias para cada depoimento; nenhum dos três vídeos é carregado antes da interação com seu botão de assistir.
- Reprodução dos três arquivos confirmada no navegador, com controles nativos, áudio habilitado e nenhum erro de mídia. Legendas embutidas preservadas.
- Setas anterior/próximo e indicadores selecionam o vídeo e atualizam o contador. Botões de extremidade desabilitados corretamente.
- Rolagem horizontal pelo navegador confirmou a passagem do primeiro para o segundo slide, com alinhamento e atualização do indicador após o fim da rolagem.
- Vídeo em reprodução pausa ao trocar de slide. Retornar ao vídeo mantém a pausa, sem reprodução automática.
- Teclas de seta navegam quando o foco está no carrossel; dentro do player, mantêm o controle nativo do vídeo. Slides inativos ficam fora da navegação por teclado e da leitura assistiva.
- Larguras de 390, 768 e 1440 pixels verificadas sem rolagem horizontal da página. Redimensionar mantém o slide selecionado alinhado.
- Verificação final sem erros ou avisos de console. Testes em navegador responsivo, sem teste em aparelho físico.

## Nova foto de “Os favoritos da festa.”

Fonte atual: `IMG_2684.HEIC`, enviada em Downloads e preservada. Imagem convertida em três cópias WebP responsivas, com orientação correta, texto alternativo atualizado e proporção 3:4. Exibição conferida no computador e em largura de 390 pixels: imagem carregada, brinde dos noivos visível e nenhuma rolagem horizontal na página. As URLs usam `?v=2` para atualizar a foto em navegadores que tenham a versão anterior em cache.
