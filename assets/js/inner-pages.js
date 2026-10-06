(() => {
  'use strict';
  document.querySelectorAll('[data-file-list]').forEach(input => {
    const list = document.getElementById(input.dataset.fileList);
    input.addEventListener('change', () => {
      const limit = Number(input.dataset.maxFiles || 5);
      const selected = [...input.files];
      const status = input.closest('form').querySelector('.inner-form__file-status');
      if (selected.length > limit) {
        const transfer = new DataTransfer();
        selected.slice(0, limit).forEach(file => transfer.items.add(file));
        input.files = transfer.files;
      }
      if (status) {
        status.hidden = selected.length <= limit;
        status.textContent = `Можно прикрепить до ${limit} фотографий. Оставлены первые ${limit}.`;
      }
      list.replaceChildren();
      [...input.files].forEach(file => {
        const item = document.createElement('li');
        item.textContent = file.name;
        list.append(item);
      });
    });
  });
  document.querySelectorAll('.inner-faq').forEach(group => {
    const items = [...group.querySelectorAll('details')];
    function select(item, open) {
      items.forEach(other => { other.open = other === item && open; });
    }
    items.forEach(item => {
      item.addEventListener('click', event => {
        if (event.target.closest('a, button, input')) return;
        event.preventDefault();
        select(item, !item.open);
      });
      item.addEventListener('toggle', () => {
        if (item.open) items.filter(other => other !== item).forEach(other => { other.open = false; });
      });
    });
  });
  const tabs = [...document.querySelectorAll('.inner-review-tab')];
  function activate(tab) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(tab));
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') target = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') target = 0;
      if (event.key === 'End') target = tabs.length - 1;
      if (target === undefined) return;
      event.preventDefault();
      activate(tabs[target]);
      tabs[target].focus();
    });
  });
  const dialog = document.querySelector('.inner-dialog');
  if (!dialog) return;
  let opener;
  document.querySelectorAll('[data-contact-topic]').forEach(button => {
    button.addEventListener('click', () => {
      opener = button;
      dialog.querySelector('[name="topic"]').value = button.dataset.contactTopic;
      dialog.querySelector('#contact-dialog-title').textContent = button.dataset.contactTopic;
      dialog.showModal();
      document.body.classList.add('has-dialog');
    });
  });
  dialog.querySelector('.inner-dialog__close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('has-dialog');
    if (opener) opener.focus();
  });
})();
