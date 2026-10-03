(() => {
  'use strict';
  const section = document.querySelector('.popular');
  if (!section) return;
  const tabs = [...section.querySelectorAll('.popular__tab')];
  const cards = [...section.querySelectorAll('.product-card')];
  const panel = section.querySelector('.popular__panel');
  const empty = section.querySelector('.popular__empty');
  const status = section.querySelector('.popular__status');
  const previous = section.querySelector('.popular__arrow--prev');
  const next = section.querySelector('.popular__arrow--next');
  const tablet = matchMedia('(max-width: 1024px)');
  const mobile = matchMedia('(max-width: 767px)');
  let category = tabs[0].dataset.category;
  let offset = 0;
  const pageSize = () => mobile.matches ? 1 : tablet.matches ? 2 : 4;
  function render(announce = false) {
    const products = cards.filter(card => card.dataset.category === category);
    const count = Math.min(pageSize(), products.length);
    offset = products.length ? offset % products.length : 0;
    cards.forEach(card => { card.hidden = true; });
    for (let i = 0; i < count; i++) {
      const card = products[(offset + i) % products.length];
      card.hidden = false;
      card.style.order = i;
      // Скрытые карточки не загружают фото до первого показа.
      const image = card.querySelector('img');
      if (image.dataset.src) { image.src = image.dataset.src; delete image.dataset.src; }
    }
    empty.hidden = products.length > 0;
    previous.disabled = next.disabled = products.length < 2;
    if (announce) status.textContent = products.length
      ? `Показано ${count} из ${products.length}. Первый товар: ${offset + 1}.`
      : 'Товары этой категории скоро появятся.';
  }
  function selectTab(tab) {
    category = tab.dataset.category;
    offset = 0;
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    panel.setAttribute('aria-labelledby', tab.id);
    render(true);
  }
  tabs.forEach((tab, position) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (position + 1) % tabs.length;
      if (event.key === 'ArrowLeft') target = (position - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = tabs.length - 1;
      if (target === undefined) return;
      event.preventDefault();
      tabs[target].focus();
      selectTab(tabs[target]);
    });
  });
  previous.addEventListener('click', () => { const length = cards.filter(card => card.dataset.category === category).length; offset = (offset - 1 + length) % length; render(true); });
  next.addEventListener('click', () => { offset++; render(true); });
  tablet.addEventListener('change', () => render());
  mobile.addEventListener('change', () => render());
  render();
})();
