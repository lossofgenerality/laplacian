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
