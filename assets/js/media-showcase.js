(() => {
  'use strict';
  const section = document.querySelector('.media-showcase');
  if (!section) return;
  // Адреса страниц «Смотреть все» пока не заданы.
  section.querySelectorAll('.media-showcase__all').forEach(link => {
    link.addEventListener('click', event => { if (!link.getAttribute('href')) event.preventDefault(); });
  });
  const mobile = matchMedia('(max-width: 767px)');
  section.querySelectorAll('.media-showcase__panel').forEach(panel => {
    const videos = panel.classList.contains('videos');
    const items = [...panel.querySelectorAll('[data-item]')];
    const status = panel.querySelector('.media-showcase__status');
    let offset = 0;
    function render(announce = false) {
      const count = videos ? mobile.matches ? 1 : 2 : items.length;
      items.forEach(item => { item.hidden = true; });
      for (let i = 0; i < count; i++) {
        const item = items[(offset + i) % items.length];
        item.hidden = false;
        item.style.order = i;
      }
      if (announce) status.textContent = `${videos ? 'Видео' : 'Бренд'} ${offset + 1} из ${items.length}.`;
    }
    panel.querySelector('.media-showcase__arrow--prev').addEventListener('click', () => { offset = (offset - 1 + items.length) % items.length; render(true); });
    panel.querySelector('.media-showcase__arrow--next').addEventListener('click', () => { offset = (offset + 1) % items.length; render(true); });
    mobile.addEventListener('change', () => render());
    render();
  });
  section.querySelectorAll('.videos__play').forEach(button => {
    button.addEventListener('click', () => {
      const panel = button.closest('.media-showcase__panel');
      let notice = panel.querySelector('.media-showcase__notice');
      if (!notice) {
        notice = document.createElement('p');
        notice.className = 'media-showcase__notice p2';
        notice.setAttribute('role', 'status');
        panel.append(notice);
      }
      notice.textContent = 'Видео пока не добавлено.';
    });
  });
})();
