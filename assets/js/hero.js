(() => {
  'use strict';
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const photo = hero.querySelector('.hero__image');
  const heading = hero.querySelector('h1');
  const description = hero.querySelector('.hero__description');
  const cta = hero.querySelector('.hero__cta');
  const stats = [...hero.querySelectorAll('.hero__stat')];
  const current = hero.querySelector('.hero__current');
  const status = hero.querySelector('.hero__status');
  const progress = hero.querySelector('.hero__progress-fill');
  const duration = 10000;
  // Каждый объект содержит весь контент слайда, включая фото и показатели.
  const slides = Array.from({ length: 4 }, () => ({
    title: 'Аренда погрузчиков в Москве',
    description: 'Погрузчики, штабелеры, рохли и ричтраки\nдля погрузки, перемещения и размещения грузов.',
    button: 'Подобрать оборудование',
    href: '#catalog',
    image: 'assets/images/hero1pogr-converted.webp',
    stats: [
      { value: '150+', label: 'Техники в каталоге' },
      { value: '5т', label: 'Грузоподъемность' },
      { value: '6м', label: 'Рабочая высота' },
    ],
  }));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const loaded = new Map();
  let index = 0;
  let timer;
  let animation;
  let pending = 0;
  let paused = document.hidden;

  function loadImage(source) {
    if (!loaded.has(source)) {
      const image = new Image();
      image.decoding = 'async';
      image.fetchPriority = 'low';
      image.src = source;
      loaded.set(source, image.decode().catch(() => {}));
    }
    return loaded.get(source);
  }

  function startTimer() {
    clearTimeout(timer);
    animation?.cancel();
    progress.style.transform = 'scaleX(0)';
    if (paused) return;
    if (!reducedMotion.matches) {
      animation = progress.animate(
        [{ transform: 'scaleX(0)' }, { transform: 'scaleX(1)' }],
        { duration, easing: 'linear', fill: 'forwards' }
      );
    }
    timer = setTimeout(() => show(index + 1, false), duration);
  }

  async function show(next, announce = true) {
    const request = ++pending;
    next = (next + slides.length) % slides.length;
    const slide = slides[next];
    await loadImage(slide.image);
    if (request !== pending) return;
    index = next;
    heading.textContent = slide.title;
    description.textContent = slide.description;
    cta.querySelector('span').textContent = slide.button;
    cta.setAttribute('href', slide.href);
    photo.src = slide.image;
    stats.forEach((stat, position) => {
      stat.querySelector('.hero__number').textContent = slide.stats[position].value;
      stat.querySelector('.hero__stat-label').textContent = slide.stats[position].label;
    });
    current.textContent = String(index + 1).padStart(2, '0');
    if (announce) status.textContent = `Слайд ${index + 1} из ${slides.length}`;
    hero.classList.remove('is-changing');
    void hero.offsetWidth;
    hero.classList.add('is-changing');
    startTimer();
  }

  hero.querySelector('.hero__arrow--prev').addEventListener('click', () => show(index - 1));
  hero.querySelector('.hero__arrow--next').addEventListener('click', () => show(index + 1));
  hero.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(index + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  hero.addEventListener('focusin', () => { paused = true; clearTimeout(timer); animation?.pause(); });
  hero.addEventListener('focusout', (event) => {
    if (!hero.contains(event.relatedTarget)) { paused = document.hidden; startTimer(); }
  });
  document.addEventListener('visibilitychange', () => {
    paused = document.hidden || hero.contains(document.activeElement);
    startTimer();
  });
  reducedMotion.addEventListener('change', startTimer);

  // Остальные фото запрашиваются после полной загрузки первого экрана.
  function deferImages() {
    const preload = () => slides.slice(1).forEach(slide => loadImage(slide.image));
    if ('requestIdleCallback' in window) window.requestIdleCallback(preload, { timeout: 2000 });
    else setTimeout(preload, 0);
    startTimer();
  }
  if (document.readyState === 'complete') deferImages();
  else window.addEventListener('load', deferImages, { once: true });
})();
