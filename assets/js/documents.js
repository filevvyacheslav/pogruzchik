(() => {
  'use strict';
  const section = document.querySelector('.documents');
  if (!section) return;
  const items = [...section.querySelectorAll('.documents__item')];
  const status = section.querySelector('.documents__status');
  const tablet = matchMedia('(max-width: 1024px)');
  const mobile = matchMedia('(max-width: 767px)');
  let offset = 0;
  const visibleCount = () => Math.min(items.length, mobile.matches ? 1 : tablet.matches ? 3 : 4);
  function render(announce = false) {
    items.forEach(item => { item.hidden = true; });
    for (let i = 0; i < visibleCount(); i++) {
      const item = items[(offset + i) % items.length];
      item.hidden = false;
      item.style.order = i;
      const image = item.querySelector('img');
      if (image.dataset.src) { image.src = image.dataset.src; delete image.dataset.src; }
    }
    if (announce) status.textContent = `Показано ${visibleCount()} из ${items.length} документов. Первый документ: ${offset + 1}.`;
  }
  section.querySelector('.documents__arrow--prev').addEventListener('click', () => {
    offset = (offset - 1 + items.length) % items.length;
    render(true);
  });
  section.querySelector('.documents__arrow--next').addEventListener('click', () => {
    offset = (offset + 1) % items.length;
    render(true);
  });
  tablet.addEventListener('change', () => render());
  mobile.addEventListener('change', () => render());
  render();
})();
