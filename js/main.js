/* =========================================================
   Shahnaz Ali · Portfolio scripts
   Each feature is a small, self-contained block.
   ========================================================= */
(function () {
  'use strict';

  const root = document.documentElement;
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Light / dark theme ---------- */
  const themeBtn = $('#theme-toggle');
  themeBtn.addEventListener('click', () => {
    const next = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.dataset.theme = next;
    $('meta[name="theme-color"]').setAttribute('content', next === 'light' ? '#f7f7fc' : '#0b0b1a');
    try { localStorage.setItem('theme', next); } catch (e) { /* private mode */ }
  });
  if (root.dataset.theme === 'light') $('meta[name="theme-color"]').setAttribute('content', '#f7f7fc');

  /* ---------- Mobile menu ---------- */
  const nav = $('.nav');
  const menuBtn = $('#menu-toggle');
  const links = $('#nav-links');

  function setMenu(open) {
    links.classList.toggle('is-open', open);
    nav.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  menuBtn.addEventListener('click', () => setMenu(!links.classList.contains('is-open')));
  $$('a', links).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  document.addEventListener('click', (e) => { if (!nav.contains(e.target)) setMenu(false); });

  /* ---------- Scroll effects: nav style, progress bar, back-to-top ---------- */
  const progress = $('.progress');
  const toTop = $('#to-top');
  function onScroll() {
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    nav.classList.toggle('is-scrolled', y > 20);
    toTop.classList.toggle('is-visible', y > 600);
    progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Highlight the nav link of the section on screen ---------- */
  const navLinks = $$('.nav__links a');
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      navLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  $$('main section[id]').forEach((s) => spy.observe(s));

  /* ---------- Reveal-on-scroll animations ---------- */
  const revealer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      revealer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  $$('.reveal').forEach((el) => {
    // Stagger items that sit side by side in the same parent
    const siblings = $$(':scope > .reveal', el.parentElement);
    el.style.transitionDelay = `${Math.min(siblings.indexOf(el), 6) * 80}ms`;
    revealer.observe(el);
  });

  /* ---------- Count-up numbers in the hero ---------- */
  function countUp(el) {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduceMotion) { el.textContent = target + suffix; return; }
    const start = performance.now();
    const duration = 1600;
    (function tick(now) {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(tick);
    })(start);
  }
  const counter = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      countUp(entry.target);
      counter.unobserve(entry.target);
    });
  });
  $$('[data-count]').forEach((el) => counter.observe(el));

  /* ---------- Typing effect ---------- */
  const typed = $('#typed');
  const words = ['Python games', 'modern websites', 'playful ideas', 'things that work'];
  if (!reduceMotion) {
    let word = 0, letters = words[0].length, deleting = false;
    (function type() {
      const current = words[word];
      letters += deleting ? -1 : 1;
      typed.textContent = current.slice(0, letters);
      let wait = deleting ? 45 : 90;
      if (!deleting && letters === current.length) { deleting = true; wait = 1800; }
      else if (deleting && letters === 0) { deleting = false; word = (word + 1) % words.length; wait = 350; }
      setTimeout(type, wait);
    })();
  }

  /* ---------- Project filters ---------- */
  const chips = $$('.chip');
  chips.forEach((chip) => chip.addEventListener('click', () => {
    const filter = chip.dataset.filter;
    chips.forEach((c) => {
      const active = c === chip;
      c.classList.toggle('is-active', active);
      c.setAttribute('aria-pressed', String(active));
    });
    $$('.project').forEach((card) => {
      const show = filter === 'all' || card.dataset.tags.split(' ').includes(filter);
      card.classList.toggle('is-hidden', !show);
      if (show) card.classList.add('is-visible');
    });
  }));

  /* ---------- Share button (uses the phone's share sheet when available) ---------- */
  const toast = $('#toast');
  let toastTimer;
  function showToast(msg) {
    toast.textContent = msg;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { toast.textContent = ''; }, 3000);
  }
  $('#share-btn').addEventListener('click', async () => {
    const data = { title: document.title, text: 'Check out Shahnaz Ali\'s portfolio!', url: location.href.split('#')[0] };
    if (navigator.share) {
      try { await navigator.share(data); } catch (e) { /* user closed the share sheet */ }
      return;
    }
    try {
      await navigator.clipboard.writeText(data.url);
      showToast('✓ Link copied to clipboard');
    } catch (e) {
      showToast('Copy this link: ' + data.url);
    }
  });

  /* ---------- Footer year ---------- */
  $('#year').textContent = new Date().getFullYear();

  /* =========================================================
     Sky Hopper: a JavaScript remake of flappy_bird.py
     Uses the same numbers as the Python version.
     ========================================================= */
  const canvas = $('#game');
  const ctx = canvas.getContext('2d');
  const W = 400, H = 600;
  const S = {
    groundHeight: 70, birdRadius: 15, gravity: 0.45, flapStrength: -8, maxFall: 10,
    pipeWidth: 60, pipeGap: 160, pipeSpeed: 3, pipeSpacing: 220,
  };
  const STEP = 1000 / 60; // the Python game runs at 60 frames per second

  // Draw sharply on high-resolution (Retina) screens
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  ctx.scale(dpr, dpr);

  const bestEl = $('#best-score');
  let best = 0;
  try { best = Number(localStorage.getItem('skyhopper-best')) || 0; } catch (e) {}
  bestEl.textContent = best;

  let bird, pipes, score, state, groundOffset = 0, overAt = 0, ticks = 0;

  function reset() {
    bird = { x: Math.floor(W / 3), y: H / 2, v: 0 };
    pipes = [];
    score = 0;
    state = 'ready'; // ready, playing, paused, over
  }

  function newPipe(x) {
    const min = 60, max = H - S.groundHeight - 60 - S.pipeGap;
    return { x, gapTop: min + Math.floor(Math.random() * (max - min + 1)), passed: false };
  }

  function flap() {
    if (state === 'ready') { state = 'playing'; bird.v = S.flapStrength; }
    else if (state === 'playing') bird.v = S.flapStrength;
    else if (state === 'paused') state = 'playing';
    else if (state === 'over' && performance.now() - overAt > 450) reset(); // short delay stops accidental restarts
  }

  function hits(rx, ry, rw, rh) {
    const r = S.birdRadius - 2; // a little forgiving, like the Python version
    return bird.x - r < rx + rw && bird.x + r > rx && bird.y - r < ry + rh && bird.y + r > ry;
  }

  function update() {
    ticks++;
    if (state === 'ready' || state === 'playing') groundOffset = (groundOffset + S.pipeSpeed) % 24;
    if (state === 'ready') { bird.y = H / 2 + 6 * Math.sin(ticks * 0.07); return; }
    if (state !== 'playing') return;

    bird.v = Math.min(bird.v + S.gravity, S.maxFall);
    bird.y += bird.v;

    if (!pipes.length || pipes[pipes.length - 1].x < W - S.pipeSpacing) pipes.push(newPipe(W));
    for (const p of pipes) {
      p.x -= S.pipeSpeed;
      if (!p.passed && p.x + S.pipeWidth < bird.x) { p.passed = true; score++; }
    }
    pipes = pipes.filter((p) => p.x + S.pipeWidth >= 0);

    if (bird.y < -S.birdRadius) bird.y = -S.birdRadius;
    const groundY = H - S.groundHeight;
    const hitPipe = pipes.some((p) => {
      const bottomY = p.gapTop + S.pipeGap;
      return hits(p.x, 0, S.pipeWidth, p.gapTop) || hits(p.x, bottomY, S.pipeWidth, groundY - bottomY);
    });
    if (hitPipe || bird.y + S.birdRadius >= groundY) {
      state = 'over';
      overAt = performance.now();
      if (score > best) {
        best = score;
        bestEl.textContent = best;
        try { localStorage.setItem('skyhopper-best', best); } catch (e) {}
      }
    }
  }

  function rect(x, y, w, h, fill, stroke) {
    ctx.fillStyle = fill; ctx.fillRect(x, y, w, h);
    ctx.lineWidth = 3; ctx.strokeStyle = stroke; ctx.strokeRect(x + 1.5, y + 1.5, w - 3, h - 3);
  }

  function text(str, size, y, color = '#fff') {
    ctx.font = `800 ${size}px "Plus Jakarta Sans", system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(0,0,0,0.35)'; ctx.fillText(str, W / 2 + 2, y + 2);
    ctx.fillStyle = color; ctx.fillText(str, W / 2, y);
  }

  function draw() {
    // Sky
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, '#6fc3ee'); sky.addColorStop(1, '#bfe9fb');
    ctx.fillStyle = sky; ctx.fillRect(0, 0, W, H);

    // Pipes with lips at the open ends
    const groundY = H - S.groundHeight;
    for (const p of pipes) {
      const bottomY = p.gapTop + S.pipeGap;
      rect(p.x, -3, S.pipeWidth, p.gapTop + 3, '#3c963c', '#1e5a1e');
      rect(p.x, bottomY, S.pipeWidth, groundY - bottomY, '#3c963c', '#1e5a1e');
      rect(p.x - 5, p.gapTop - 20, S.pipeWidth + 10, 20, '#46a846', '#1e5a1e');
      rect(p.x - 5, bottomY, S.pipeWidth + 10, 20, '#46a846', '#1e5a1e');
    }

    // Ground with moving stripes
    ctx.fillStyle = '#6eb450'; ctx.fillRect(0, groundY, W, S.groundHeight);
    ctx.fillStyle = '#dcc88c'; ctx.fillRect(0, groundY + 18, W, S.groundHeight);
    ctx.strokeStyle = '#5aa03c'; ctx.lineWidth = 4;
    for (let x = -groundOffset; x < W; x += 24) {
      ctx.beginPath(); ctx.moveTo(x, groundY); ctx.lineTo(x + 12, groundY + 18); ctx.stroke();
    }
    ctx.strokeStyle = '#285a1e'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(0, groundY); ctx.lineTo(W, groundY); ctx.stroke();

    // Bird
    const { x } = bird, y = Math.round(bird.y), r = S.birdRadius;
    ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = '#fac828'; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#000'; ctx.stroke();
    const wingY = y + (bird.v < 0 ? -4 : 4);
    ctx.beginPath(); ctx.ellipse(x - r + 7, wingY, 7, 4, 0, 0, Math.PI * 2); ctx.fillStyle = '#f0f0f0'; ctx.fill();
    ctx.beginPath(); ctx.arc(x + 6, y - 5, 5, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
    ctx.beginPath(); ctx.arc(x + 7, y - 5, 2, 0, Math.PI * 2); ctx.fillStyle = '#000'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(x + r - 2, y - 1); ctx.lineTo(x + r + 9, y + 2); ctx.lineTo(x + r - 2, y + 5);
    ctx.fillStyle = '#f06e28'; ctx.fill();

    // Words on screen
    if (state === 'ready') {
      text('Sky Hopper', 48, 160);
      text('Tap or press Space to flap', 20, 420);
    } else {
      text(String(score), 56, 90);
    }
    if (state === 'paused') text('Paused', 48, 260);
    if (state === 'over') {
      text('Game Over', 48, 220, '#ff5a5a');
      text(`Score: ${score}   Best: ${best}`, 22, 270);
      text('Tap to play again', 20, 310);
    }
  }

  // Fixed-speed game loop: same speed on 60 Hz and 120 Hz screens
  let last = performance.now(), acc = 0, visible = false;
  function loop(now) {
    acc += Math.min(now - last, 100);
    last = now;
    while (acc >= STEP) { update(); acc -= STEP; }
    draw();
    requestAnimationFrame(loop);
  }

  // Controls
  canvas.addEventListener('pointerdown', (e) => { e.preventDefault(); flap(); });
  document.addEventListener('keydown', (e) => {
    if (!visible) return;
    if (e.code === 'Space' || e.code === 'ArrowUp') { e.preventDefault(); flap(); }
    else if (e.code === 'KeyP' && (state === 'playing' || state === 'paused')) state = state === 'playing' ? 'paused' : 'playing';
  });

  // Pause automatically when the game scrolls off screen or the tab is hidden
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (!visible && state === 'playing') state = 'paused';
  }, { threshold: 0.5 }).observe(canvas);
  document.addEventListener('visibilitychange', () => { if (document.hidden && state === 'playing') state = 'paused'; });

  reset();
  requestAnimationFrame(loop);
})();
