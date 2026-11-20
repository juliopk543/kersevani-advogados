/* Slide dos princípios (Manifesto) */
(function () {
  var box = document.querySelector('[data-kv-slider]');
  if (!box) return;
  var slides = box.querySelectorAll('.kv-slide'), dots = box.querySelectorAll('.kv-dots button');
  var i = 0, timer, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  box.classList.add('kv-on');
  function go(n) {
    var next = (n + slides.length) % slides.length;
    if (next === i && slides[i].classList.contains('is-active')) return;
    var prev = slides[i];
    if (prev.classList.contains('is-active')) {
      prev.classList.remove('is-active'); prev.classList.add('is-prev');
      setTimeout(function () {
        prev.style.transition = 'none'; prev.classList.remove('is-prev');
        void prev.offsetWidth; prev.style.transition = '';
      }, 850);
    }
    i = next;
    slides.forEach(function (s, k) { s.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
    slides[i].classList.remove('is-prev'); slides[i].classList.add('is-active');
    dots.forEach(function (d, k) { d.setAttribute('aria-current', k === i ? 'true' : 'false'); });
  }
  function play() { if (reduce) return; stop(); timer = setInterval(function () { go(i + 1); }, 5000); }
  function stop() { clearInterval(timer); }
  dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); play(); }); });
  box.querySelector('.kv-prev').addEventListener('click', function () { go(i - 1); play(); });
  box.querySelector('.kv-next').addEventListener('click', function () { go(i + 1); play(); });
  box.addEventListener('mouseenter', stop); box.addEventListener('mouseleave', play);
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; stop(); }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 !== null) { var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(i + (dx < 0 ? 1 : -1)); }
    x0 = null; play();
  });
  slides[0].classList.add('is-active'); dots[0].setAttribute('aria-current', 'true');
  play();
})();

/* Áreas de atuação: a cor passa de card em card conforme a rolagem da página */
(function () {
  var sec = document.querySelector('.elementor-element-4b54dd5');
  if (!sec) return;
  var wr = Array.prototype.slice.call(sec.querySelectorAll('.jkit-icon-box-wrapper'));
  if (wr.length < 2) return;
  sec.classList.add('kv-areas-cycle');
  var hover = false, ticking = false, cur = null;

  function ordered() { // ordem visual: de cima para baixo, da esquerda para a direita
    return wr.slice().sort(function (a, b) {
      var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      return Math.abs(ra.top - rb.top) > 8 ? ra.top - rb.top : ra.left - rb.left;
    });
  }
  function set(w) {
    if (w === cur) return;
    cur = w;
    wr.forEach(function (x) { x.classList.toggle('kv-hot', x === w); });
  }
  function update() {
    ticking = false;
    if (hover) return;
    var H = window.innerHeight, r = sec.getBoundingClientRect();
    if (r.bottom < 0 || r.top > H) { set(null); return; }
    var list = ordered(), pick;
    var stacked = list.every(function (w) { return Math.abs(w.getBoundingClientRect().left - list[0].getBoundingClientRect().left) < 8; });
    if (stacked) { // celular: o card que está no meio da tela
      var best = 1e9;
      list.forEach(function (w) {
        var b = w.getBoundingClientRect(), d = Math.abs(b.top + b.height / 2 - H * 0.5);
        if (d < best) { best = d; pick = w; }
      });
    } else { // desktop: avança conforme a seção atravessa a tela
      var p = (H * 0.85 - r.top) / (r.height + H * 0.45);
      p = Math.max(0, Math.min(0.999, p));
      pick = list[Math.floor(p * list.length)];
    }
    set(pick);
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req);
  sec.addEventListener('mouseover', function (e) { if (e.target.closest('.jkit-icon-box-wrapper')) { hover = true; cur = null; wr.forEach(function (x) { x.classList.remove('kv-hot'); }); } });
  sec.addEventListener('mouseleave', function () { hover = false; req(); });
  update();
})();
