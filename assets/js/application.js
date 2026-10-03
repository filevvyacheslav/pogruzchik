(() => {
  'use strict';
  const form = document.querySelector('.application__form');
  if (!form) return;
  const input = form.querySelector('.application__file-input');
  const file = form.querySelector('.application__file');
  const filename = form.querySelector('.application__filename');
  const status = form.querySelector('.application__status');
  const updateFile = () => {
    const attachment = input.files[0];
    file.hidden = !attachment;
    filename.textContent = attachment ? attachment.name : '';
  };
  form.querySelector('.application__attach').addEventListener('click', () => input.click());
  input.addEventListener('change', updateFile);
  form.querySelector('.application__remove').addEventListener('click', () => {
    input.value = '';
    updateFile();
    form.querySelector('.application__attach').focus();
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    status.hidden = false;
    status.textContent = 'Отправка заявок пока не подключена. Свяжитесь с нами по телефону или почте.';
  });
  form.addEventListener('reset', () => {
    status.hidden = true;
    requestAnimationFrame(updateFile);
  });
  document.querySelectorAll('.product-card__button').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelector('.application').scrollIntoView({ block: 'start' });
      form.querySelector('[name="name"]').focus({ preventScroll: true });
    });
  });
  updateFile();
})();
