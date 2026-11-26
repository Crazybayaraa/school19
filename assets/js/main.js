/* Мобильное меню + версия для слабовидящих (без внешних зависимостей) */
(function () {
  var root = document.documentElement;
  var KEY = 'a11y-settings';

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || null; } catch (e) { return null; }
  }
  function save(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
  }
  function apply(s) {
    if (!s || !s.on) {
      root.classList.remove('a11y');
      ['data-fs', 'data-scheme', 'data-noimg', 'data-ls'].forEach(function (a) { root.removeAttribute(a); });
    } else {
      root.classList.add('a11y');
      root.setAttribute('data-fs', s.fs || '1');
      root.setAttribute('data-scheme', s.scheme || 'wb');
      root.setAttribute('data-noimg', s.noimg ? '1' : '0');
      root.setAttribute('data-ls', s.ls ? '1' : '0');
    }
    document.querySelectorAll('[data-a11y-set]').forEach(function (b) {
      var p = b.getAttribute('data-a11y-set').split(':');
      var v = s && s.on ? String(s[p[0]]) : '';
      b.setAttribute('aria-pressed', v === p[1] ? 'true' : 'false');
    });
    document.querySelectorAll('.btn-a11y').forEach(function (b) {
      b.setAttribute('aria-pressed', s && s.on ? 'true' : 'false');
      b.lastChild.textContent = s && s.on ? ' Обычная версия' : ' Версия для слабовидящих';
    });
  }

  var state = load() || { on: false, fs: '1', scheme: 'wb', noimg: false, ls: false };
  apply(state);

  document.addEventListener('click', function (e) {
    var t = e.target.closest('button');
    if (!t) return;
    if (t.classList.contains('btn-a11y')) {
      state.on = !state.on;
    } else if (t.hasAttribute('data-a11y-set')) {
      var p = t.getAttribute('data-a11y-set').split(':');
      state[p[0]] = p[1] === 'true' ? true : p[1] === 'false' ? false : p[1];
    } else if (t.classList.contains('nav-toggle')) {
      var nav = document.getElementById('main-nav');
      var open = nav.classList.toggle('is-open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      return;
    } else {
      return;
    }
    save(state);
    apply(state);
  });
})();
