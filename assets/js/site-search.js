/* Site-local search: Chinese phrases and identifiers, scoped by documentation version. */
(function (root) {
  'use strict';
  function versionFromPath(path) {
    var match = path.match(/\/docs\/(latest|5\.x|4\.0|3\.1)(?:\/|$)/);
    return match ? match[1] : 'all';
  }
  function search(pages, query, version) {
    var terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return pages.filter(function (page) {
      if (version !== 'all' && page.version !== version) return false;
      var text = (page.title + ' ' + page.body).toLocaleLowerCase();
      return terms.every(function (term) { return text.includes(term); });
    }).map(function (page) {
      var title = page.title.toLocaleLowerCase();
      return { page: page, score: terms.reduce(function (sum, term) {
        return sum + (title === term ? 20 : title.includes(term) ? 10 : 1);
      }, 0) };
    }).sort(function (a, b) { return b.score - a.score || a.page.url.localeCompare(b.page.url); })
      .slice(0, 30).map(function (result) { return result.page; });
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { search: search, versionFromPath: versionFromPath };
  if (!root.document) return;
  var triggers = document.querySelectorAll('.macula-search-input');
  if (!triggers.length) return;
  var dialog = document.createElement('dialog');
  dialog.className = 'site-search-dialog';
  dialog.setAttribute('aria-labelledby', 'site-search-title');
  dialog.innerHTML = '<div class="site-search-heading"><h2 id="site-search-title">搜索文档</h2><button type="button" aria-label="关闭搜索">关闭 ×</button></div>' +
    '<form role="search"><label for="site-search-query">关键词</label><input id="site-search-query" type="search" autocomplete="off" placeholder="输入中文、模块名或配置键">' +
    '<label for="site-search-scope">搜索范围</label><select id="site-search-scope"><option value="latest">latest（当前）</option><option value="5.x">5.x</option><option value="4.0">4.0</option><option value="3.1">3.1</option><option value="all">全部版本及公共内容</option></select></form>' +
    '<p class="site-search-status" role="status" aria-live="polite"></p><ol class="site-search-results"></ol>';
  document.body.appendChild(dialog);
  var query = dialog.querySelector('input'), scope = dialog.querySelector('select');
  var status = dialog.querySelector('[role="status"]'), list = dialog.querySelector('ol');
  var indexPromise, pages, opener, request = 0;
  function render() {
    list.replaceChildren();
    if (!pages) return;
    if (!query.value.trim()) { status.textContent = '输入关键词搜索；多个词以空格分隔。'; return; }
    var results = search(pages, query.value, scope.value);
    status.textContent = results.length ? '找到 ' + results.length + ' 条结果（最多显示 30 条）' : '没有匹配结果，可切换搜索范围或缩短关键词。';
    results.forEach(function (page) {
      var item = document.createElement('li'), link = document.createElement('a'), excerpt = document.createElement('p');
      link.href = page.url; link.textContent = (page.version ? '[' + page.version + '] ' : '') + page.title;
      excerpt.textContent = page.excerpt;
      item.append(link, excerpt); list.appendChild(item);
    });
  }
  function open(trigger) {
    opener = trigger;
    scope.value = versionFromPath(location.pathname);
    query.value = trigger.value;
    if (!dialog.open) dialog.showModal();
    query.focus();
    var current = ++request;
    if (pages) { render(); return; }
    status.textContent = '正在加载本站搜索索引…';
    if (!indexPromise) indexPromise = fetch(trigger.dataset.searchIndexSrc).then(function (response) {
      if (!response.ok) throw new Error('index');
      return response.json();
    }).catch(function (error) { indexPromise = null; throw error; });
    indexPromise.then(function (data) { pages = data; if (current === request) render(); })
      .catch(function () { if (current === request) status.textContent = '搜索索引加载失败，请关闭后重试或浏览左侧目录。'; });
  }
  triggers.forEach(function (trigger) {
    trigger.addEventListener('input', function (event) { if (!event.isComposing) open(trigger); });
    trigger.addEventListener('compositionend', function () { open(trigger); });
    trigger.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' && !event.isComposing) { event.preventDefault(); event.stopPropagation(); open(trigger); }
    });
  });
  dialog.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); dialog.close(); }
  });
  dialog.querySelector('button').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', function () { if (opener) { opener.value = ''; opener.focus(); } });
  dialog.querySelector('form').addEventListener('submit', function (event) { event.preventDefault(); render(); });
  query.addEventListener('input', render); scope.addEventListener('change', render);
  if (/\/search\/?$/.test(location.pathname)) {
    var initialQuery = new URLSearchParams(location.search).get('q');
    if (initialQuery) { triggers[0].value = initialQuery; open(triggers[0]); }
  }
})(typeof window === 'undefined' ? globalThis : window);
