(function () {
  const preloader = document.getElementById('preloader');
  const bar = document.querySelector('.speedometer-bar');
  const pct = document.getElementById('preloaderPercent');

  let progress = 0;
  const timer = setInterval(() => {
    // ease towards 100
    const increment = Math.max(1, Math.round((100 - progress) * 0.08));
    progress = Math.min(100, progress + increment);
    if (bar) bar.style.width = progress + '%';
    if (pct) pct.textContent = progress + '%';

    if (progress >= 100) {
      clearInterval(timer);
      setTimeout(() => {
        if (preloader) preloader.classList.add('hidden');
        // allow scroll again
        document.body.classList.remove('preloader-active');
      }, 250);
    }
  }, 60);

  // Safety: hide preloader after max 6 seconds
  setTimeout(() => {
    if (!preloader) return;
    if (!preloader.classList.contains('hidden')) {
      progress = 100;
      if (bar) bar.style.width = '100%';
      if (pct) pct.textContent = '100%';
      preloader.classList.add('hidden');
      document.body.classList.remove('preloader-active');
    }
  }, 6000);
})();

(function(){
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  if(toggle && links){
    toggle.addEventListener('click', ()=>{
      const isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });
  }
})();
