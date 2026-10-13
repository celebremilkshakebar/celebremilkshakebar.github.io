# Celebre Milkshake Bar

Landing page estática em português, pronta para hospedagem. Não exige instalação de pacotes, banco de dados ou serviços externos para exibir o conteúdo.

## Prévia

Para uma visualização rápida, abra `index.html` em seu navegador. Para reproduzir o vídeo e testar em condições semelhantes à hospedagem, use Node.js:

```text
node preview.mjs
```

Abra `http://127.0.0.1:4173`. Para encerrar, pressione Ctrl+C no terminal. Se a porta estiver ocupada, defina a variável `CELEBRE_PREVIEW_PORT` antes de iniciar.

## Hospedagem

Envie `index.html`, `styles.css`, `script.js` e a pasta `assets` para a raiz da hospedagem ou para a subpasta desejada. Todos os caminhos de arquivos são relativos. `preview.mjs` serve somente para prévia e não precisa ser publicado. A página não depende de `C:\landing-celebre\media` nem dos arquivos do projeto sincronizado.

Ao definir o endereço público, substitua o valor de `og:image` pela URL absoluta de `assets/compartilhamento.jpg` e acrescente o endereço canônico e `og:url` ao cabeçalho. O arquivo de compartilhamento já está incluído.

## Atualizar o conteúdo

- **Textos, menus, condições e depoimentos:** `index.html`.
- **Cores e aparência:** variáveis no início de `styles.css`.
- **Navegação e reprodução dos vídeos:** `script.js`.
- **Mídias:** versões otimizadas na pasta `assets`.

Os botões de contato usam o número `5551980363985` e a mensagem “Olá! Vim pelo site da Celebre e gostaria de um orçamento para meu evento.” A mensagem é preenchida ao abrir o WhatsApp; o visitante decide enviá-la.

## Condições utilizadas

Atendimento em Novo Hamburgo, região e proximidades, no Rio Grande do Sul. Eventos com no mínimo 30 convidados. Serviço de 3 horas, com extensão combinada conforme necessidade. Milkshakes à vontade durante as horas contratadas; chantilly opcional; deslocamento incluído no orçamento; pagamento facilitado; reserva mediante sinal e condições especiais para pagamento integral.

As condições comerciais mais recentes do briefing prevalecem sobre as referências anteriores a 3–4 horas e atendimento em todo o estado. Taças mostradas nas fotos não constituem promessa de inclusão padrão.

As avaliações são estáticas: nota 5,0, 14 avaliações e quatro depoimentos fornecidos no briefing. Verifique a nota e a contagem no Google antes de campanhas futuras e atualize as duas áreas da página que mostram esses números. Os textos dos depoimentos mantêm o conteúdo fornecido, com ajuste de pontuação no primeiro.

## Privacidade e acessibilidade

A página não tem formulário, armazenamento de dados do visitante, cookies de rastreamento ou fontes externas. WhatsApp, Instagram, Google e Casamentos.com.br só são abertos ao seguir os respectivos links. Fotos têm descrições alternativas; menu e perguntas funcionam pelo teclado; animações respeitam a preferência de movimento reduzido. Os três vídeos de feedback iniciam por interação e mantêm o áudio e as legendas presentes no material original. O vídeo de abertura reproduz automaticamente em loop, sem áudio, com a foto dos dois milkshakes como capa até a reprodução começar. Há um botão de pausa/retomada; quando o visitante prefere movimento reduzido, a capa é mantida até ele optar por reproduzir.

Os arquivos originais de mídia e a pasta `sources/` não foram modificados. As cópias web são os arquivos incluídos em `assets`.

## Vídeo da abertura

O vídeo enviado como `Design sem nome (2).mp4` foi convertido em duas versões H264 com faststart e sem faixa de áudio: `assets/hero-loop.mp4` e `assets/hero-loop-mobile.mp4`. A versão é selecionada ao abrir a página, conforme a largura do navegador; não há troca durante a reprodução ao redimensionar. O vídeo mantém a moldura, o selo de avaliações e o sticker originais. Se houver bloqueio de reprodução automática, o visitante pode iniciar pelo botão. Em falhas de carregamento, a foto original permanece como capa.

## Carrossel de feedbacks

O bloco “O melhor feedback vem com um sorriso.” reúne o vídeo original e os dois novos depoimentos, em `assets/feedback.mp4`, `assets/feedback-2.mp4` e `assets/feedback-3.mp4`. As capas WebP aparecem antes da reprodução. Cada vídeo é carregado somente após o clique em assistir, com controles nativos e áudio.

O visitante pode navegar pelas setas, pelos três indicadores, deslizando horizontalmente no celular ou pelas teclas de seta quando o foco está no carrossel. As teclas do player continuam disponíveis para controlar o vídeo. Ao mudar de slide, a reprodução anterior pausa; retornar ao vídeo mantém a pausa até o visitante retomar pelos controles. Não há passagem automática entre os depoimentos.

Os novos arquivos foram convertidos para MP4 H264/AAC, resolução 720×1280 e faststart, preservando a duração completa, a orientação e as legendas embutidas. Os materiais originais foram preservados.
