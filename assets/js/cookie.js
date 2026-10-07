(() => {
  'use strict';
  const notice = document.querySelector('.cookie-notice');
  if (!notice) return;
  const key = 'pogruzchik-cookie-accepted-v1';
  let accepted = false;
  try { accepted = localStorage.getItem(key) === 'yes'; } catch {}
  notice.hidden = accepted;
  notice.querySelector('.cookie-notice__accept').addEventListener('click', () => {
    try { localStorage.setItem(key, 'yes'); } catch {}
    notice.hidden = true;
  });
  window.addEventListener('storage', event => {
    if (event.key === key) notice.hidden = event.newValue === 'yes';
  });
})();
