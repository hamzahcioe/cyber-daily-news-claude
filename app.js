/* Security Brief front end. Plain JS, no dependencies.
   Data (all relative to this folder):
     data/index.json          list of briefs, newest first
     data/briefs/YYYY-MM-DD.json   one file per day
   See DATA-FORMAT.md for the schemas. */
(function () {
  'use strict';

  var CYBER = [
    { id: 'outage',       title: 'Outages and service incidents' },
    { id: 'attack',       title: 'Cyber attacks and campaigns' },
    { id: 'breach',       title: 'Breaches and hacks' },
    { id: 'leak',         title: 'Data leaks and exposures' },
    { id: 'claim',        title: 'Ransomware and unconfirmed claims' },
    { id: 'supply-chain', title: 'Supply chain' },
    { id: 'vuln',         title: 'Major vulnerabilities and active exploitation' },
    { id: 'law',          title: 'Law enforcement and policy' },
    { id: 'other',        title: 'Other' }
  ];
  var GLOBAL = [
    { id: 'world',        title: 'Major international news' },
    { id: 'economy',      title: 'Economy and trade' },
    { id: 'geopolitics',  title: 'Geopolitics and tech' },
    { id: 'ai',           title: 'AI developments' },
    { id: 'energy',       title: 'Energy and climate tech' },
    { id: 'science',      title: 'Science and discovery' },
    { id: 'research-policy', title: 'Research and innovation policy' },
    { id: 'infra-attack', title: 'Physical and infrastructure attacks' },
    { id: 'surveillance', title: 'State spying and surveillance' },
    { id: 'tech',         title: 'Major tech news' }
  ];
  var NATURE = [{ id: 'nature', title: 'Travel and nature' }];
  var CATEGORIES = CYBER.concat(GLOBAL, NATURE);
  var LABELS = {
    'CONFIRMED': { cls: 't-confirmed', text: 'CONFIRMED' },
    'VENDOR-ACKNOWLEDGED': { cls: 't-vendor', text: 'VENDOR-ACKNOWLEDGED' },
    'UNCONFIRMED CLAIM': { cls: 't-unconfirmed', text: 'UNCONFIRMED CLAIM' }
  };

  var $ = function (id) { return document.getElementById(id); };
  var state = { index: [], current: null, brief: null, filter: 'ALL' };

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function safeUrl(u) { return /^https?:\/\//i.test(u || '') ? u : '#'; }
  // Very small text formatter: escapes everything, then supports `code`, **bold**, ``` blocks and blank-line paragraphs.
  function fmt(text) {
    if (!text) return '';
    var parts = String(text).split(/```/);
    return parts.map(function (chunk, i) {
      if (i % 2 === 1) return '<pre><code>' + esc(chunk.replace(/^\w*\n/, '')) + '</code></pre>';
      return chunk.split(/\n{2,}/).map(function (p) {
        if (!p.trim()) return '';
        var h = esc(p.trim()).replace(/\n/g, '<br>')
          .replace(/`([^`]+)`/g, '<code>$1</code>')
          .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
        return '<p>' + h + '</p>';
      }).join('');
    }).join('');
  }
  function sevClass(s) { return 's-' + String(s || 'awareness').toLowerCase(); }
  function sevTag(s) { return s ? '<span class="sev ' + sevClass(s) + '">' + esc(s.toUpperCase()) + '</span>' : ''; }
  function labelTag(l) {
    var d = LABELS[l]; if (!d) return l ? '<span class="tag">' + esc(l) + '</span>' : '';
    return '<span class="tag ' + d.cls + '">' + d.text + '</span>';
  }
  function fmtDate(d) {
    var dt = new Date(d + 'T12:00:00');
    return dt.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }
  function fmtShortDate(d) {
    var dt = new Date(d + 'T12:00:00');
    return dt.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
  }
  function ago(iso) {
    var t = new Date(iso).getTime(); if (isNaN(t)) return '';
    var m = Math.max(0, Math.round((Date.now() - t) / 60000));
    if (m < 2) return 'just now';
    if (m < 60) return m + ' min ago';
    var h = Math.round(m / 60); if (h < 48) return h + ' h ago';
    return Math.round(h / 24) + ' d ago';
  }
  function getJSON(url) {
    return fetch(url + (url.indexOf('?') < 0 ? '?t=' + Date.now() : ''), { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error(url + ' ' + r.status); return r.json(); });
  }
  function slug(s) { return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }


  /* ---------- brief rendering ---------- */
  function itemCard(it, idx) {
    var id = it.id || ('item-' + idx);
    var s = it.sections || {};
    function sec(title, html) { return html ? '<h4>' + title + '</h4>' + html : ''; }
    var main = '';
    if (it.labelBasis) main += '<p class="basis"><strong>Label basis:</strong> ' + esc(it.labelBasis) + '</p>';
    main += sec('What happened', fmt(s.happened));
    main += sec('Technical detail', fmt(s.technical));
    var side = '';
    side += sec('Vendor and authority guidance', fmt(s.guidance));
    side += sec('Differing accounts', fmt(s.differing));
    side += sec('Still unknown', fmt(s.unknown));
    if (it.sources && it.sources.length) {
      side += '<h4>Sources</h4><ul class="srcs">' + it.sources.map(function (src) {
        return '<li><a href="' + esc(safeUrl(src.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(src.title || src.url) + '</a></li>';
      }).join('') + '</ul>';
    }
    var body = (main || side) ? '<div class="item-body"><div class="col-main">' + main + '</div>' + (side ? '<div class="col-side">' + side + '</div>' : '') + '</div>' : '<div class="item-body"><p class="muted">No further detail.</p></div>';
    return '<details class="item" id="' + esc(id) + '" data-sev="' + esc(it.severity || '') + '" data-label="' + esc(it.label || '') + '"' + (it.open ? ' open' : '') + '>' +
      '<summary><span class="item-title">' + esc(it.headline) + '</span>' +
      '<div class="item-meta">' + labelTag(it.label) + sevTag(it.severity) +
      (it.uk ? '<span class="tag t-uk">UK</span>' : '') +
      (it.coverage ? '<span class="cov">' + esc(it.coverage) + '</span>' : '') +
      (it.firstReported ? '<span class="cov">First reported ' + esc(it.firstReported) + '</span>' : '') +
      '</div>' +
      (it.summary ? '<p class="item-summary">' + esc(it.summary) + '</p>' : '') +
      '</summary>' + body + '</details>';
  }

  function renderBrief(b, isSample) {
    state.brief = b;
    $('briefTitle').textContent = b.title || fmtDate(b.date);
    var meta = [];
    if (b.date) meta.push(fmtDate(b.date));
    if (b.generated) meta.push('generated ' + new Date(b.generated).toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' }));
    $('briefMeta').textContent = meta.join(' · ');
    $('sampleBanner').hidden = !(isSample || b.sample);

    // top stories
    $('top3').setAttribute('data-n', String((b.top || []).length));
    $('top3').innerHTML = (b.top || []).map(function (t, i) {
      var link = t.ref ? '<a href="#' + esc(state.current) + '/' + esc(t.ref) + '" data-jump="' + esc(t.ref) + '">Read full story →</a>' : '';
      return '<div class="top-card" data-sev="' + esc(t.severity || '') + '"><span class="rank">' + (i + 1) + '</span><h3>' + esc(t.headline) + '</h3>' +
        '<div class="item-meta nopad">' + labelTag(t.label) + sevTag(t.severity) + (t.coverage ? '<span class="cov">' + esc(t.coverage) + '</span>' : '') + '</div>' +
        '<p>' + esc(t.summary) + '</p>' + (link ? '<p>' + link + '</p>' : '') + '</div>';
    }).join('') || '<p class="muted">Nothing major today.</p>';

    // ongoing
    var og = b.ongoing || [];
    $('ongoingSection').hidden = !og.length;
    $('ongoing').innerHTML = og.map(function (o) {
      var link = !o.ref ? '' : (o.ref.indexOf('/') > 0 ? ' <a href="#' + esc(o.ref) + '">Earlier report →</a>' : ' <a href="#' + esc(state.current) + '/' + esc(o.ref) + '" data-jump="' + esc(o.ref) + '">Details →</a>');
      return '<div class="ongoing-card" data-sev="' + esc(o.severity || '') + '">' +
        '<div class="item-meta nopad"><b>' + esc(o.headline) + '</b></div>' +
        '<div class="item-meta nopad">' + labelTag(o.label) + sevTag(o.severity) +
        '<span class="cov">' + (o.since ? 'Since ' + esc(o.since) : '') + (o.status ? ' · ' + esc(o.status) : '') + '</span></div>' +
        '<p><b>Latest:</b> ' + esc(o.latest) + link + '</p>' +
        (o.log && o.log.length ? '<details class="oglog"><summary>Update log (' + o.log.length + ')</summary><ul class="plain">' + o.log.map(function (l) { return '<li><b>' + esc(l.date) + '</b> ' + esc(l.text) + '</li>'; }).join('') + '</ul></details>' : '') +
        '</div>';
    }).join('');

    // categories
    var items = (b.items || []).map(function (it, i) { it._i = i; return it; });
    var known = {}; CATEGORIES.forEach(function (c) { known[c.id] = 1; });
    function catOf(it) { return known[it.category] ? it.category : 'other'; }
    var present = [];
    function renderGroup(cats) {
      var html = '';
      cats.forEach(function (cat) {
        var list = items.filter(function (it) { return catOf(it) === cat.id; });
        if (!list.length) return;
        present.push(cat);
        html += '<section class="cat" id="cat-' + cat.id + '" data-cat="' + cat.id + '" data-nav="' + esc(cat.title) + '" aria-labelledby="h-' + cat.id + '">' +
          '<h2 id="h-' + cat.id + '">' + esc(cat.title) + ' <span class="count">' + list.length + '</span></h2>' +
          list.map(function (it) { return itemCard(it, it._i); }).join('') + '</section>';
      });
      return html;
    }
    var TAIL = { law: 1, other: 1 };
    var cyberHtml = renderGroup(CYBER.filter(function (c) { return !TAIL[c.id] && c.id !== 'vuln'; }));
    $('categoriesVuln').innerHTML = renderGroup(CYBER.filter(function (c) { return c.id === 'vuln'; }));
    $('categoriesCyber').innerHTML = cyberHtml || '<p class="muted">No cyber stories in this brief.</p>';
    $('categoriesCyberTail').innerHTML = renderGroup(CYBER.filter(function (c) { return TAIL[c.id]; }));
    var globalHtml = renderGroup(GLOBAL);
    $('categoriesGlobal').innerHTML = globalHtml;
    $('globalHeader').hidden = !globalHtml;
    $('categoriesNature').innerHTML = renderGroup(NATURE);

    // focus sections (cross-listed)
    function focusRows(list) {
      return list.map(function (it) {
        var id = it.id || 'item-' + it._i;
        return '<a class="uk-row" href="#' + esc(state.current) + '/' + esc(id) + '" data-jump="' + esc(id) + '">' +
          '<span>' + esc(it.headline) + '</span><span class="item-meta nopad">' + labelTag(it.label) + sevTag(it.severity) + '</span></a>';
      }).join('');
    }
    var ms = items.filter(function (it) { return it.microsoft; });
    $('microsoftSection').hidden = !ms.length; $('microsoft').innerHTML = focusRows(ms);
    var uk = items.filter(function (it) { return it.uk; });
    $('ukSection').hidden = !uk.length; $('uk').innerHTML = focusRows(uk);
    if (ms.length) present.push({ id: 'microsoftSection', title: 'Microsoft' });
    if (uk.length) present.push({ id: 'ukSection', title: 'UK focus' });

    // patch watch
    var pw = b.patchWatch || [];
    $('patchSection').hidden = !pw.length;
    $('patchTable').innerHTML = pw.length ? '<thead><tr><th>Product</th><th>CVE</th><th>CVSS</th><th>Exploited</th><th>Fixed in / release</th></tr></thead><tbody>' +
      pw.map(function (r) {
        var ex = String(r.exploited || 'unknown').toLowerCase();
        var cve = r.ref ? '<a href="#' + esc(state.current) + '/' + esc(r.ref) + '" data-jump="' + esc(r.ref) + '">' + esc(r.cve) + '</a>' : esc(r.cve);
        return '<tr><td>' + esc(r.product) + '</td><td>' + cve + '</td><td>' + esc(r.cvss || '') + '</td><td><span class="ex ex-' + esc(ex) + '">' + esc(ex) + '</span></td><td>' + esc(r.fixed || '') + '</td></tr>';
      }).join('') + '</tbody>' : '';
    if (pw.length) present.push({ id: 'patchSection', title: 'Patch watch' });

    // coming up
    var cu = b.comingUp || [];
    $('comingSection').hidden = !cu.length;
    $('coming').innerHTML = cu.map(function (c) { return '<li><span class="when">' + esc(c.date) + '</span><div>' + esc(c.text) + '</div></li>'; }).join('');


    // filters
    var labels = {}; items.forEach(function (it) { if (it.label) labels[it.label] = 1; });
    var fl = Object.keys(labels);
    $('filterbar').hidden = fl.length < 2;
    state.filter = 'ALL';
    $('filters').innerHTML = ['ALL'].concat(fl).map(function (l) {
      return '<button class="chip" data-filter="' + esc(l) + '" aria-pressed="' + (l === 'ALL') + '">' + (l === 'ALL' ? 'All' : esc(l.charAt(0) + l.slice(1).toLowerCase())) + '</button>';
    }).join('');

    // also reported
    var ar = b.alsoReported || [];
    $('alsoSection').hidden = !ar.length;
    $('also').innerHTML = ar.map(function (x) {
      var host = ''; try { host = new URL(x.url).hostname.replace(/^www\./, ''); } catch (e) {}
      return '<li><a href="' + esc(safeUrl(x.url)) + '" target="_blank" rel="noopener noreferrer">' + esc(x.headline) + '</a>' +
        '<span class="cov">' + esc(host) + (x.outlets > 1 ? ' · ' + esc(x.outlets) + ' outlets' : '') + '</span></li>';
    }).join('');


    $('brief').hidden = false;
    $('status').hidden = true;
    buildNav();
  }

  function buildNav() {
    var els = Array.prototype.filter.call($('brief').querySelectorAll('[data-nav]'), function (e) { return !e.hidden; });
    $('sectionNav').hidden = els.length < 2;
    $('sectionNav').innerHTML = '<span class="rail-title">On this page</span>' + els.map(function (e) {
      var n = e.querySelectorAll('details.item').length;
      return '<a href="#' + e.id + '" data-scroll="' + e.id + '">' + esc(e.getAttribute('data-nav')) + (n ? '<span class="n">' + n + '</span>' : '') + '</a>';
    }).join('');
    if (!('IntersectionObserver' in window)) return;
    if (state.spy) state.spy.disconnect();
    state.spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        Array.prototype.forEach.call($('sectionNav').querySelectorAll('a'), function (a) {
          a.classList.toggle('on', a.getAttribute('data-scroll') === en.target.id);
        });
      });
    }, { rootMargin: '-10% 0px -80% 0px' });
    els.forEach(function (e) { state.spy.observe(e); });
  }

  function applyFilter() {
    var f = state.filter;
    var cats = document.querySelectorAll('.cat');
    Array.prototype.forEach.call(cats, function (cat) {
      var shown = 0;
      Array.prototype.forEach.call(cat.querySelectorAll('details.item'), function (d) {
        var ok = f === 'ALL' || d.getAttribute('data-label') === f;
        d.hidden = !ok; if (ok) shown++;
      });
      cat.hidden = shown === 0;
    });
    Array.prototype.forEach.call(document.querySelectorAll('#filters .chip'), function (c) {
      c.setAttribute('aria-pressed', String(c.getAttribute('data-filter') === f));
    });
  }

  function openItem(id) {
    var el = document.getElementById(id);
    if (!el) return;
    if (el.hidden) { state.filter = 'ALL'; applyFilter(); }
    if (el.tagName === 'DETAILS') el.open = true;
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ---------- navigation ---------- */
  function setNavState() {
    var i = state.index.findIndex(function (b) { return b.date === state.current; });
    $('olderBtn').disabled = i < 0 || i >= state.index.length - 1;
    $('newerBtn').disabled = i <= 0;
    $('dateSelect').value = state.current || '';
  }
  function go(date, itemId) {
    location.hash = '#' + date + (itemId ? '/' + itemId : '');
  }
  function route() {
    var h = decodeURIComponent((location.hash || '').replace(/^#/, ''));
    var m = h.match(/^(\d{4}-\d{2}-\d{2})(?:\/([\w-]+))?$/);
    if (h.indexOf('cat-') === 0) { var t = document.getElementById(h); if (t) t.scrollIntoView({ behavior: 'smooth' }); return; }
    var date = m ? m[1] : (state.index[0] && state.index[0].date);
    var item = m && m[2];
    if (!date) { showStatus('No briefs have been published yet. The first one will appear here after the next scheduled run.'); return; }
    if (date === state.current && state.brief) { if (item) openItem(item); return; }
    state.current = date; setNavState();
    showStatus('Loading ' + fmtShortDate(date) + '…');
    getJSON('data/briefs/' + date + '.json').then(function (b) {
      var meta = state.index.find(function (x) { return x.date === date; });
      renderBrief(b, meta && meta.sample);
      applyFilter();
      document.title = (b.title || fmtDate(date)) + ' · Security Brief';
      if (item) setTimeout(function () { openItem(item); }, 50); else window.scrollTo(0, 0);
    }).catch(function () {
      $('brief').hidden = true;
      showStatus('Could not load the brief for ' + fmtShortDate(date) + '.');
    });
  }
  function showStatus(msg) { var s = $('status'); s.textContent = msg; s.hidden = false; }

  function loadIndex() {
    return getJSON('data/index.json').then(function (idx) {
      state.index = (idx.briefs || []).slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; });
      $('dateSelect').innerHTML = state.index.map(function (b) {
        return '<option value="' + esc(b.date) + '">' + esc(fmtShortDate(b.date)) + (b.title ? ' — ' + esc(b.title) : '') + '</option>';
      }).join('');
    }).catch(function () { state.index = []; showStatus('Could not load the brief index.'); });
  }

  /* ---------- events ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-jump]');
    if (a) { e.preventDefault(); var id = a.getAttribute('data-jump'); history.replaceState(null, '', '#' + state.current + '/' + id); openItem(id); return; }
    var s = e.target.closest && e.target.closest('[data-scroll]');
    if (s) { e.preventDefault(); var t = document.getElementById(s.getAttribute('data-scroll')); if (t) t.scrollIntoView({ behavior: 'smooth' }); return; }
    var c = e.target.closest && e.target.closest('[data-filter]');
    if (c) { state.filter = c.getAttribute('data-filter'); applyFilter(); }
  });
  $('olderBtn').addEventListener('click', function () {
    var i = state.index.findIndex(function (b) { return b.date === state.current; });
    if (i >= 0 && i < state.index.length - 1) go(state.index[i + 1].date);
  });
  $('newerBtn').addEventListener('click', function () {
    var i = state.index.findIndex(function (b) { return b.date === state.current; });
    if (i > 0) go(state.index[i - 1].date);
  });
  $('dateSelect').addEventListener('change', function (e) { go(e.target.value); });
  $('brand').addEventListener('click', function (e) { e.preventDefault(); if (state.index[0]) go(state.index[0].date); });
  document.addEventListener('keydown', function (e) {
    if (/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) return;
    if (e.key === 'ArrowLeft') $('olderBtn').click();
    if (e.key === 'ArrowRight') $('newerBtn').click();
  });
  window.addEventListener('hashchange', route);

  /* ---------- boot ---------- */
  loadIndex().then(route);
})();
