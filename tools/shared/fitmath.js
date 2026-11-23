/* CCN: formulas shrink to fit their column instead of being clipped (min 55%); beyond that the drawn slider takes over */
(function () {
  var MIN = 0.55, busy = false;
  function room(m) {
    var p = m.parentElement;
    while (p && getComputedStyle(p).display.indexOf('inline') === 0) p = p.parentElement;
    if (!p) return 0;
    var s = getComputedStyle(p);
    return p.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight);
  }
  function fit() {
    busy = true;
    document.querySelectorAll('mjx-container').forEach(function (m) {
      if (!m.offsetParent) return;
      var svg = m.querySelector('svg'); if (!svg) return;
      m.style.fontSize = '';
      var w = svg.getBoundingClientRect().width, r = room(m);
      if (r > 0 && w > r) {
        m.style.fontSize = (Math.max(MIN, (r - 2) / w) * 100).toFixed(1) + '%';
      }
    });
    setTimeout(function () { busy = false; }, 0);
  }
  var t; function soon() { if (busy) return; clearTimeout(t); t = setTimeout(fit, 80); }
  window.addEventListener('resize', soon);
  window.addEventListener('hashchange', function () { setTimeout(fit, 250); });
  new MutationObserver(function (ms) {
    for (var i = 0; i < ms.length; i++) for (var j = 0; j < ms[i].addedNodes.length; j++) {
      var n = ms[i].addedNodes[j];
      if (n.nodeType === 1 && (n.tagName === 'MJX-CONTAINER' || n.querySelector && n.querySelector('mjx-container'))) { soon(); return; }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
  document.addEventListener('click', function () { setTimeout(fit, 300); }, true);
  window.ccnFitMath = fit;
})();
