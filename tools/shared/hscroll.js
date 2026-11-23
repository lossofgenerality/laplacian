/* CCN: arrow buttons for horizontally scrolling tab strips; keeps the current tab in view */
(function () {
  function wire(strip) {
    if (!strip || strip.dataset.hs) return; strip.dataset.hs = 1;
    const wrap = document.createElement('div'); wrap.className = 'hs-wrap';
    strip.parentNode.insertBefore(wrap, strip);
    const L = document.createElement('button'), R = document.createElement('button');
    L.className = R.className = 'hs-btn'; L.type = R.type = 'button';
    L.textContent = '‹'; R.textContent = '›'; L.setAttribute('aria-label', 'Scroll tabs left'); R.setAttribute('aria-label', 'Scroll tabs right');
    strip.classList.add('hs-strip'); wrap.append(L, strip, R);
    const upd = () => {
      const horiz = getComputedStyle(strip).overflowX !== 'visible' && strip.scrollWidth > strip.clientWidth + 2 && getComputedStyle(strip).flexDirection !== 'column';
      wrap.classList.toggle('hs-over', horiz);
      L.disabled = strip.scrollLeft <= 1; R.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 1;
    };
    L.onclick = () => strip.scrollBy({ left: -strip.clientWidth * 0.7, behavior: 'smooth' });
    R.onclick = () => strip.scrollBy({ left: strip.clientWidth * 0.7, behavior: 'smooth' });
    strip.addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd);
    new MutationObserver(upd).observe(strip, { childList: true, subtree: true, attributes: true });
    const show = () => { const a = strip.querySelector('[aria-current="true"], [aria-current="page"]'); if (a && wrap.classList.contains('hs-over')) { const sr = strip.getBoundingClientRect(), ar = a.getBoundingClientRect(); if (ar.left < sr.left || ar.right > sr.right) strip.scrollLeft += ar.left - sr.left - (sr.width - ar.width) / 2; } upd(); };
    addEventListener('hashchange', () => setTimeout(show, 30)); upd(); setTimeout(show, 80); setTimeout(show, 600);
  }
  function go() { document.querySelectorAll('[data-hscroll]').forEach(wire); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();

/* CCN: a drawn horizontal slider under anything that scrolls sideways (works in every browser, incl. Firefox overlay scrollbars) */
(function () {
  const seen = new WeakSet();
  function bar(el) {
    if (seen.has(el)) return; seen.add(el);
    const b = document.createElement('div'), t = document.createElement('div');
    b.className = 'hs-bar'; t.className = 'hs-thumb'; b.appendChild(t); b.hidden = true;
    b.setAttribute('role', 'scrollbar'); b.setAttribute('aria-orientation', 'horizontal');
    const strip = el.closest('.hs-wrap');
    if (strip) strip.after(b);
    else { const box = document.createElement('div'); box.className = 'hs-box'; el.before(box); box.appendChild(el); if (el.offsetHeight > 220) { box.insertBefore(b, el); b.classList.add('hs-top'); } else box.appendChild(b); }
    const upd = () => {
      const over = el.scrollWidth - el.clientWidth;
      if (over <= 2 || el.offsetParent === null) { b.hidden = true; el.classList.remove('hs-nonative'); return; }
      b.hidden = false; el.classList.toggle('hs-nonative', el.scrollHeight <= el.clientHeight + 1);
      const W = b.clientWidth, tw = Math.max(28, W * el.clientWidth / el.scrollWidth);
      t.style.width = tw + 'px'; t.style.left = ((W - tw) * el.scrollLeft / over) + 'px';
      b.setAttribute('aria-valuenow', Math.round(100 * el.scrollLeft / over));
    };
    let drag = null;
    const xOf = e => (e.touches ? e.touches[0] : e).clientX;
    const onMove = e => { if (!drag) return; const over = el.scrollWidth - el.clientWidth, W = b.clientWidth - t.offsetWidth;
      el.scrollLeft = drag.s + (xOf(e) - drag.x) * over / Math.max(1, W); e.preventDefault(); };
    const onUp = () => { drag = null; b.classList.remove('drag'); };
    t.addEventListener('mousedown', e => { drag = { x: xOf(e), s: el.scrollLeft }; b.classList.add('drag'); e.preventDefault(); e.stopPropagation(); });
    t.addEventListener('touchstart', e => { drag = { x: xOf(e), s: el.scrollLeft }; b.classList.add('drag'); e.stopPropagation(); }, { passive: true });
    addEventListener('mousemove', onMove); addEventListener('touchmove', onMove, { passive: false });
    addEventListener('mouseup', onUp); addEventListener('touchend', onUp);
    b.addEventListener('mousedown', e => { if (e.target !== b) return; const r = t.getBoundingClientRect();
      el.scrollBy({ left: (e.clientX < r.left ? -1 : 1) * el.clientWidth * 0.8, behavior: 'smooth' }); });
    el.addEventListener('scroll', upd, { passive: true });
    if (window.ResizeObserver) { const ro = new ResizeObserver(upd); ro.observe(el); if (el.firstElementChild) ro.observe(el.firstElementChild); }
    addEventListener('resize', upd); upd(); setTimeout(upd, 300);
    el._hsUpd = upd;
  }
  function scan() {
    document.querySelectorAll('body *').forEach(el => {
      if (el.classList.contains('hs-bar') || el.closest('.hs-bar') || el.classList.contains('hs-box')) return;
      const ox = getComputedStyle(el).overflowX;
      if ((ox === 'auto' || ox === 'scroll') && el.tagName !== 'TEXTAREA' && el.tagName !== 'BODY' && el.tagName !== 'HTML') bar(el);
    });
    document.querySelectorAll('.hs-bar').forEach(b => {});
  }
  let tm; const later = () => { clearTimeout(tm); tm = setTimeout(() => { scan(); document.querySelectorAll('*').forEach(e => e._hsUpd && e._hsUpd()); }, 120); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', later); else later();
  addEventListener('load', later); addEventListener('hashchange', later);
  new MutationObserver(later).observe(document.documentElement, { childList: true, subtree: true });
})();
