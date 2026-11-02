(function () {
  'use strict';
  // Native image preview keeps document illustrations usable without jQuery.
  var imageLinks = document.querySelectorAll('a[data-fancybox]');
  if (imageLinks.length && typeof HTMLDialogElement !== 'undefined') {
    var dialog = document.createElement('dialog');
    dialog.className = 'image-preview';
    dialog.setAttribute('aria-label', '图片预览');
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = '关闭 ×';
    var image = document.createElement('img');
    dialog.append(close, image);
    document.body.appendChild(dialog);
    close.addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (event) {
      if (event.target === dialog) dialog.close();
    });
    imageLinks.forEach(function (link) {
      link.addEventListener('click', function (event) {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        image.src = link.href;
        image.alt = link.querySelector('img').alt;
        dialog.showModal();
      });
    });
  }
  var sidebar = document.getElementById('td-section-nav');
  document.querySelectorAll('.td-sidebar__toggle').forEach(function (button) {
    button.addEventListener('click', function () {
      if (!sidebar) return;
      var open = sidebar.classList.toggle('show');
      document.querySelectorAll('.td-sidebar__toggle').forEach(function (toggle) {
        toggle.setAttribute('aria-expanded', String(open));
      });
    });
  });

  document.querySelectorAll('#td-section-nav .with-child > input[type="checkbox"]').forEach(function (checkbox) {
    var label = checkbox.nextElementSibling;
    var children = label && label.nextElementSibling;
    if (!label || !children || children.tagName !== 'UL') return;
    var title = label.textContent.trim();
    var toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'section-toggle';
    toggle.textContent = '›';
    children.id = checkbox.id + '-children';
    toggle.setAttribute('aria-controls', children.id);
    function refresh() {
      toggle.setAttribute('aria-expanded', String(checkbox.checked));
      toggle.setAttribute('aria-label', (checkbox.checked ? '收起' : '展开') + title);
    }
    toggle.addEventListener('click', function () { checkbox.checked = !checkbox.checked; refresh(); });
    checkbox.addEventListener('change', refresh);
    checkbox.parentElement.classList.add('has-section-toggle');
    checkbox.parentElement.insertBefore(toggle, checkbox);
    refresh();
  });

  document.querySelectorAll('.td-content .highlight').forEach(function (block) {
    var code = block.querySelector('pre code');
    if (!code || !navigator.clipboard) return;
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'code-copy';
    button.textContent = '复制代码';
    button.setAttribute('aria-label', '复制此代码示例');
    button.setAttribute('aria-live', 'polite');
    button.addEventListener('click', function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        button.textContent = '已复制';
        window.setTimeout(function () { button.textContent = '复制代码'; }, 1800);
      }).catch(function () { button.textContent = '请选中代码复制'; });
    });
    block.appendChild(button);
  });

  // Preserve native table semantics while giving wide technical tables their own scroll region.
  document.querySelectorAll('.td-content table').forEach(function (table) {
    var region = document.createElement('div');
    region.className = 'doc-table-scroll';
    table.parentNode.insertBefore(region, table);
    region.appendChild(table);
    function refreshTable() {
      var overflowing = region.scrollWidth > region.clientWidth + 1;
      if (overflowing) {
        region.tabIndex = 0;
        region.setAttribute('role', 'region');
        region.setAttribute('aria-label', '表格，可横向滚动');
      } else {
        region.removeAttribute('tabindex');
        region.removeAttribute('role');
        region.removeAttribute('aria-label');
      }
    }
    refreshTable();
    if (typeof ResizeObserver !== 'undefined') new ResizeObserver(refreshTable).observe(region);
    else window.addEventListener('resize', refreshTable);
  });

  var toc = document.getElementById('TableOfContents');
  if (!toc) return;
  var entries = Array.from(toc.querySelectorAll('a[href*="#"]')).map(function (link) {
    var id;
    try { id = decodeURIComponent(link.hash.slice(1)); } catch (_) { return null; }
    var heading = document.getElementById(id);
    return heading ? { link: link, heading: heading } : null;
  }).filter(Boolean);
  if (!entries.length) return;
  var scheduled = false;
  function update() {
    scheduled = false;
    var current = entries[0];
    entries.forEach(function (entry) {
      if (entry.heading.getBoundingClientRect().top <= 120) current = entry;
    });
    entries.forEach(function (entry) {
      entry.link.classList.toggle('active', entry === current);
      if (entry === current) entry.link.setAttribute('aria-current', 'location');
      else entry.link.removeAttribute('aria-current');
    });
  }
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(update);
  }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  window.addEventListener('load', schedule);
  update();
})();
