(() => {
  const button = document.querySelector('.about__more[aria-controls]');
  if (!button) return;
  const text = document.getElementById(button.getAttribute('aria-controls'));
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'true';
    text.hidden = !expanded;
    button.setAttribute('aria-expanded', String(expanded));
    button.textContent = expanded ? 'Скрыть текст' : 'Читать больше...';
  });
})();
