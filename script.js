/* Contato direto, navegação acessível, vídeo de abertura e feedback sob demanda. */
(() => {
  'use strict';
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navegacao');
  const setMenuOpen = (open, restoreFocus = false) => {
    menuButton?.setAttribute('aria-expanded', String(open));
    menuButton?.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    navigation?.classList.toggle('is-open', open);
    if (restoreFocus) menuButton?.focus();
  };
  menuButton?.addEventListener('click', () => {
    setMenuOpen(menuButton.getAttribute('aria-expanded') !== 'true');
  });
  navigation?.addEventListener('click', event => {
    if (event.target.closest('a')) setMenuOpen(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
      setMenuOpen(false, true);
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) setMenuOpen(false);
  });
  document.addEventListener('focusin', event => {
    if (!event.target.closest('.site-header')) setMenuOpen(false);
  });
  window.matchMedia('(min-width: 768px)').addEventListener('change', event => {
    if (event.matches) setMenuOpen(false);
  });

  const heroVideo = document.querySelector('#hero-video');
  const heroFrame = document.querySelector('.hero-arch');
  const heroToggle = document.querySelector('.hero-video-toggle');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (heroVideo && heroToggle && heroFrame) {
    const heroSource = heroVideo.querySelector('source');
    let userPaused = false;
    let sourceFailed = false;
    heroVideo.muted = true;
    heroVideo.defaultMuted = true;
    const updateHeroControl = () => {
      const paused = heroVideo.paused;
      heroToggle.setAttribute('aria-label', paused ? 'Reproduzir vídeo de abertura' : 'Pausar vídeo de abertura');
      heroToggle.title = paused ? 'Reproduzir vídeo' : 'Pausar vídeo';
      heroToggle.querySelector('use').setAttribute('href', paused ? '#i-play' : '#i-pause');
    };
    const loadHeroVideo = () => {
      if (!heroSource.src) {
        const mobile = window.matchMedia('(max-width: 767px)').matches;
        heroSource.src = mobile ? heroSource.dataset.mobileSrc : heroSource.dataset.src;
        heroVideo.load();
      }
    };
    const playHeroVideo = () => {
      loadHeroVideo();
      const playing = heroVideo.play();
      if (playing) playing.catch(error => {
        if (sourceFailed || heroVideo.error || error.name === 'NotSupportedError') {
          heroFrame.classList.remove('is-video-ready');
          heroToggle.hidden = true;
          return;
        }
        heroToggle.hidden = false;
        updateHeroControl();
      });
    };
    heroVideo.addEventListener('playing', () => {
      heroFrame.classList.add('is-video-ready');
      heroToggle.hidden = false;
      updateHeroControl();
    });
    heroVideo.addEventListener('pause', updateHeroControl);
    heroVideo.addEventListener('waiting', () => heroFrame.classList.remove('is-video-ready'));
    const keepCoverOnError = () => {
      sourceFailed = true;
      heroFrame.classList.remove('is-video-ready');
      heroToggle.hidden = true;
    };
    heroVideo.addEventListener('error', keepCoverOnError);
    heroSource.addEventListener('error', keepCoverOnError);
    heroToggle.addEventListener('click', () => {
      if (heroVideo.paused) {
        userPaused = false;
        playHeroVideo();
      } else {
        userPaused = true;
        heroVideo.pause();
      }
    });
    reducedMotion.addEventListener('change', event => {
      heroVideo.autoplay = !event.matches;
      if (event.matches) {
        heroVideo.pause();
        heroFrame.classList.remove('is-video-ready');
        heroToggle.hidden = false;
        updateHeroControl();
      } else if (!userPaused) playHeroVideo();
    });
    if (reducedMotion.matches) {
      heroVideo.autoplay = false;
      heroVideo.preload = 'none';
      heroToggle.hidden = false;
      updateHeroControl();
    } else playHeroVideo();
  }

  const carousel = document.querySelector('.feedback-carousel');
  if (carousel) {
    const track = carousel.querySelector('.feedback-track');
    const slides = Array.from(carousel.querySelectorAll('.feedback-slide'));
    const videos = slides.map(slide => slide.querySelector('video'));
    const dots = Array.from(carousel.querySelectorAll('[data-slide]'));
    const previous = carousel.querySelector('.feedback-prev');
    const next = carousel.querySelector('.feedback-next');
    const status = carousel.querySelector('.feedback-status');
    let current = 0;
    let scrollTimer;

    const setActiveSlide = index => {
      index = Math.max(0, Math.min(slides.length - 1, index));
      const oldSlide = slides[current];
      if (index !== current && oldSlide.contains(document.activeElement)) {
        track.focus({ preventScroll: true });
      }
      current = index;
      slides.forEach((slide, slideIndex) => {
        const active = slideIndex === current;
        slide.inert = !active;
        if (active) slide.removeAttribute('aria-hidden');
        else {
          slide.setAttribute('aria-hidden', 'true');
          videos[slideIndex].pause();
        }
      });
      dots.forEach((dot, dotIndex) => {
        if (dotIndex === current) dot.setAttribute('aria-current', 'true');
        else dot.removeAttribute('aria-current');
      });
      previous.disabled = current === 0;
      next.disabled = current === slides.length - 1;
      const message = `Vídeo ${current + 1} de ${slides.length}`;
      if (status.textContent !== message) status.textContent = message;
    };

    const goToSlide = index => {
      const target = Math.max(0, Math.min(slides.length - 1, index));
      setActiveSlide(target);
      track.scrollTo({ left: target * track.clientWidth, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
    };
    previous.addEventListener('click', () => goToSlide(current - 1));
    next.addEventListener('click', () => goToSlide(current + 1));
    dots.forEach(dot => dot.addEventListener('click', () => goToSlide(Number(dot.dataset.slide))));
    track.addEventListener('scroll', () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(() => {
        if (track.clientWidth) setActiveSlide(Math.round(track.scrollLeft / track.clientWidth));
      }, 120);
    }, { passive: true });
    carousel.addEventListener('keydown', event => {
      if (event.target.closest('video') || event.altKey || event.ctrlKey || event.metaKey) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        goToSlide(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    new ResizeObserver(() => {
      clearTimeout(scrollTimer);
      track.scrollTo({ left: current * track.clientWidth, behavior: 'auto' });
    }).observe(track);

    slides.forEach((slide, index) => {
      const video = videos[index];
      const playButton = slide.querySelector('.video-play');
      const errorMessage = slide.querySelector('.video-error');
      const source = video.querySelector('source');
      const showVideoError = () => {
        if (video.getAttribute('data-ready') === 'true') errorMessage.hidden = false;
      };
      playButton.addEventListener('click', () => {
        if (index !== current) return;
        videos.forEach(other => { if (other !== video) other.pause(); });
        if (!source.src) {
          source.src = source.dataset.src;
          video.setAttribute('data-ready', 'true');
          video.removeAttribute('aria-hidden');
          video.controls = true;
          video.load();
        }
        errorMessage.hidden = true;
        playButton.hidden = true;
        video.setAttribute('tabindex', '0');
        video.focus({ preventScroll: true });
        const playing = video.play();
        if (playing) playing.catch(error => {
          if (error.name !== 'AbortError' && current === index) showVideoError();
        });
      });
      video.addEventListener('play', () => {
        if (index !== current) video.pause();
        else videos.forEach(other => { if (other !== video) other.pause(); });
      });
      video.addEventListener('error', showVideoError);
      source.addEventListener('error', showVideoError);
    });
    setActiveSlide(0);
  }

  const year = document.querySelector('#copyright-year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
