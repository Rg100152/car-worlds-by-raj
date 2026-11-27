(function () {
  // Preloader
  const preloader = document.getElementById('preloader');
  const bar = document.querySelector('.speedometer-bar');
  const pct = document.getElementById('preloaderPercent');

  let progress = 0;
  const timer = setInterval(() => {
    const increment = Math.max(1, Math.round((100 - progress) * 0.08));
    progress = Math.min(100, progress + increment);
    if (bar) bar.style.width = progress + '%';
    if (pct) pct.textContent = progress + '%';
    if (progress >= 100) {
      clearInterval(timer);
      setTimeout(() => {
        if (preloader) preloader.classList.add('hidden');
        document.body.classList.remove('preloader-active');
      }, 250);
    }
  }, 60);

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

  // Nav toggle
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

  // Explorer
  const PAGE_SIZE = 24;
  let allCars = (window.CAR_WORLDS_DATA || []).slice();
  let filtered = allCars.slice();
  let page = 1;

  function priceLabel(car){
    const cur = window.CarWorldsFilters?.state?.currency || 'INR';
    return cur === 'USD' ? car.priceUSD : car.priceINR;
  }

  function renderGrid(){
    const grid = document.getElementById('carsGrid');
    const meta = document.getElementById('resultsMeta');
    if(!grid) return;

    const start = 0;
    const end = page * PAGE_SIZE;
    const view = filtered.slice(0, end);

    grid.innerHTML = view.map(car => `
      <article class="car-card" tabindex="0" role="button" data-id="${car.id}">
        <div class="car-imgwrap">
          <img class="car-img" src="${car.image}" alt="${car.name}" onerror="this.onerror=null;this.src='assets/images/cars/supercar-01.jpg';">
          <span class="car-badge">${car.category}</span>
        </div>
        <div class="car-body">
          <h3 class="car-name">${car.name}</h3>
          <p class="car-sub">${car.brand} • ${car.year}</p>
          <div class="car-specs">
            <span>${car.horsepower} HP</span>
            <span>${car.topSpeed} km/h</span>
            <span>0-60 ${car.zeroToSixty}s</span>
          </div>
          <div class="car-price">${priceLabel(car)}</div>
        </div>
      </article>
    `).join('');

    if(meta){
      meta.textContent = `Showing ${Math.min(end, filtered.length)} of ${filtered.length} cars (Total loaded: ${allCars.length})`;
    }

    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if(loadMoreBtn){
      loadMoreBtn.style.display = end >= filtered.length ? 'none' : 'inline-flex';
    }

    // card click
    grid.querySelectorAll('.car-card').forEach(card=>{
      card.addEventListener('click', ()=>{
        const id = card.getAttribute('data-id');
        const car = allCars.find(c=>c.id===id);
        if(car && window.CarWorldsModals) window.CarWorldsModals.openCar(car, window.CarWorldsFilters.state.currency);
      });
      card.addEventListener('keydown', (e)=>{
        if(e.key==='Enter' || e.key===' '){
          e.preventDefault();
          card.click();
        }
      });
    });
  }

  function populateBrands(){
    const sel = document.getElementById('brandSelect');
    if(!sel) return;
    const brands = Array.from(new Set(allCars.map(c=>c.brand))).sort();
    brands.forEach(b=>{
      const opt = document.createElement('option');
      opt.value = b; opt.textContent = b;
      sel.appendChild(opt);
    });
  }

  function applyAndRender(resetPage=true){
    if(resetPage) page = 1;
    if(window.CarWorldsFilters){
      filtered = window.CarWorldsFilters.apply(allCars);
    } else {
      filtered = allCars.slice();
    }
    renderGrid();
  }

  // Wire controls
  const searchInput = document.getElementById('searchInput');
  const categorySelect = document.getElementById('categorySelect');
  const brandSelect = document.getElementById('brandSelect');
  const sortSelect = document.getElementById('sortSelect');

  if(searchInput){
    let t;
    searchInput.addEventListener('input', ()=>{
      clearTimeout(t);
      t = setTimeout(()=>{
        window.CarWorldsFilters.state.q = searchInput.value.trim();
        applyAndRender(true);
      }, 120);
    });
  }
  if(categorySelect){
    categorySelect.addEventListener('change', ()=>{
      window.CarWorldsFilters.state.category = categorySelect.value;
      applyAndRender(true);
    });
  }
  if(brandSelect){
    brandSelect.addEventListener('change', ()=>{
      window.CarWorldsFilters.state.brand = brandSelect.value;
      applyAndRender(true);
    });
  }
  if(sortSelect){
    sortSelect.addEventListener('change', ()=>{
      window.CarWorldsFilters.state.sort = sortSelect.value;
      applyAndRender(true);
    });
  }

  document.querySelectorAll('.currency-btn').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      document.querySelectorAll('.currency-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      window.CarWorldsFilters.state.currency = btn.getAttribute('data-currency') || 'INR';
      renderGrid();
    });
  });

  const loadMoreBtn = document.getElementById('loadMoreBtn');
  if(loadMoreBtn){
    loadMoreBtn.addEventListener('click', ()=>{
      page += 1;
      renderGrid();
      const pageJump = document.getElementById('pageJump');
      if(pageJump) pageJump.value = String(page);
    });
  }
  const goPageBtn = document.getElementById('goPageBtn');
  if(goPageBtn){
    goPageBtn.addEventListener('click', ()=>{
      const pageJump = document.getElementById('pageJump');
      const val = Math.max(1, parseInt(pageJump?.value || '1', 10) || 1);
      page = val;
      renderGrid();
    });
  }

  // Blog render
  function renderBlog(){
    const grid = document.getElementById('blogGrid');
    if(!grid || !window.CarWorldsBlog) return;
    const posts = window.CarWorldsBlog.getAll();
    grid.innerHTML = posts.map(p=>`
      <article class="blog-card" tabindex="0" role="button" data-id="${p.id}">
        <img class="blog-cover" src="${p.cover}" alt="${p.title}" onerror="this.onerror=null;this.src='assets/images/cars/luxury-01.jpg';">
        <div class="blog-body">
          <div class="blog-tags"><span class="tag">${p.category}</span><span class="muted small">${p.readTime}</span></div>
          <h3 class="blog-title">${p.title}</h3>
          <p class="blog-excerpt">${(p.content.replace(/<[^>]*>/g,'')).slice(0,110)}…</p>
        </div>
      </article>
    `).join('');
    grid.querySelectorAll('.blog-card').forEach(card=>{
      card.addEventListener('click', ()=>{
        const id = card.getAttribute('data-id');
        const post = posts.find(x=>x.id===id);
        if(post && window.CarWorldsModals) window.CarWorldsModals.openArticle(post);
      });
      card.addEventListener('keydown', (e)=>{
        if(e.key==='Enter' || e.key===' '){ e.preventDefault(); card.click(); }
      });
    });
  }

  // Init
  populateBrands();
  applyAndRender(true);
  renderBlog();
  if(window.CarWorldsHelp) window.CarWorldsHelp.init();
})();
