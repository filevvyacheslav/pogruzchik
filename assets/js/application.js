(() => {
  'use strict';
  document.querySelectorAll('.application__form').forEach(form => {
    const status = form.querySelector('.application__status');
    const input = form.querySelector('.application__file-input');
    let updateFile;
    if (input) {
      const file = form.querySelector('.application__file');
      const filename = form.querySelector('.application__filename');
      updateFile = () => {
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
      updateFile();
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      status.hidden = false;
      status.textContent = 'Отправка заявок пока не подключена. Свяжитесь с нами по телефону или почте.';
    });
    form.addEventListener('reset', () => {
      status.hidden = true;
      if (updateFile) requestAnimationFrame(updateFile);
    });
  });
  const application = document.querySelector('.application');
  document.querySelectorAll('.product-card__button').forEach(button => {
    button.addEventListener('click', () => {
      application.scrollIntoView({ block: 'start' });
      application.querySelector('[name="name"]').focus({ preventScroll: true });
    });
  });
  document.querySelectorAll('[data-placeholder-link]').forEach(link => {
    link.addEventListener('click', event => { if (!link.getAttribute('href')) event.preventDefault(); });
  });
})();
