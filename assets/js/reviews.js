(() => {
  'use strict';
  const section = document.querySelector('.reviews');
  if (!section) return;
  const slide = section.querySelector('.reviews__slide');
  const image = section.querySelector('.reviews__image');
  const author = section.querySelector('#review-author');
  const date = section.querySelector('.reviews__date');
  const quote = section.querySelector('.reviews__text');
  const status = section.querySelector('.reviews__status');
  // Один предоставленный отзыв и три временные копии для проверки слайдера.
  const reviews = Array.from({ length: 4 }, () => ({
    author: author.textContent,
    date: date.textContent,
    datetime: date.dateTime,
    text: quote.textContent,
    image: image.getAttribute('src'),
    alt: image.alt,
  }));
  let index = 0;
  let request = 0;
  async function show(next) {
    const currentRequest = ++request;
    next = (next + reviews.length) % reviews.length;
    const review = reviews[next];
    if (image.getAttribute('src') !== review.image) {
      const preload = new Image();
      preload.src = review.image;
      await preload.decode().catch(() => {});
    }
    if (currentRequest !== request) return;
    index = next;
    author.textContent = review.author;
    date.textContent = review.date;
    date.dateTime = review.datetime;
    quote.textContent = review.text;
    image.src = review.image;
    image.alt = review.alt;
    slide.setAttribute('aria-label', `Отзыв ${index + 1} из ${reviews.length}`);
    status.textContent = `Отзыв ${index + 1} из ${reviews.length}`;
    slide.classList.remove('is-changing');
    void slide.offsetWidth;
    slide.classList.add('is-changing');
  }
  section.querySelector('.reviews__arrow--prev').addEventListener('click', () => show(index - 1));
  section.querySelector('.reviews__arrow--next').addEventListener('click', () => show(index + 1));
  section.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    show(index + (event.key === 'ArrowRight' ? 1 : -1));
  });
})();
