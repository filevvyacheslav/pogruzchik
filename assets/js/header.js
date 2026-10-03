(() => {
  'use strict';

  const header = document.querySelector('#site-header');
  const toggle = document.querySelector('.site-header__menu-toggle');
  const menu = document.querySelector('#header-mobile-menu');
  const mobile = window.matchMedia('(max-width: 767px)');

  if (!header || !toggle || !menu) return;

  const setMenuOpen = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    menu.hidden = !open;
  };

  // Место шапки в потоке сохраняет placeholder, поэтому контент не прыгает.
  let scrollPending = false;
  const updateFixed = () => {
    header.classList.toggle('is-fixed', window.scrollY > 200);
    scrollPending = false;
  };

  window.addEventListener('scroll', () => {
    if (scrollPending) return;
    scrollPending = true;
    window.requestAnimationFrame(updateFixed);
  }, { passive: true });

  toggle.addEventListener('click', () => setMenuOpen(menu.hidden));
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) setMenuOpen(false);
  });
  document.addEventListener('click', (event) => {
    if (!header.contains(event.target)) setMenuOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !menu.hidden) {
      setMenuOpen(false);
      toggle.focus();
    }
  });
  mobile.addEventListener('change', () => setMenuOpen(false));
  updateFixed();
})();
