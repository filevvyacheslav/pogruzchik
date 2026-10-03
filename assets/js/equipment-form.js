(() => {
  'use strict';
  const form = document.querySelector('.equipment-form');
  if (!form) return;
  const category = form.querySelector('[name="category"]');
  const capacity = form.querySelector('[name="capacity"]');
  const brand = form.querySelector('[name="brand"]');
  const icons = [...form.querySelectorAll('.equipment-form__icon')];
  function syncFields() {
    capacity.disabled = !category.value;
    brand.disabled = !category.value || !capacity.value;
    icons.forEach(icon => icon.classList.toggle('is-active', icon.dataset.category === category.value));
  }
  category.addEventListener('change', () => {
    capacity.value = '';
    brand.value = '';
    syncFields();
  });
  capacity.addEventListener('change', () => {
    brand.value = '';
    syncFields();
  });
  // Кнопки пока не отправляют заявки и не выполняют подбор.
  form.addEventListener('submit', event => event.preventDefault());
  window.addEventListener('pageshow', syncFields);
  syncFields();
})();
