(function(){
  function ensureModal(id){
    let el = document.getElementById(id);
    if(el) return el;
    el = document.createElement('div');
    el.id = id;
    el.className = 'modal-overlay';
    el.innerHTML = `<div class="modal" role="dialog" aria-modal="true">
      <div class="modal-head">
        <h3 class="modal-title"></h3>
        <button class="modal-close" aria-label="Close">✕</button>
      </div>
      <div class="modal-body"></div>
    </div>`;
    document.body.appendChild(el);
    el.addEventListener('click', (e)=>{ if(e.target === el) el.classList.remove('open'); });
    el.querySelector('.modal-close').addEventListener('click', ()=> el.classList.remove('open'));
    return el;
  }

  window.CarWorldsModals = {
    openCar(car, currency){
      const modal = ensureModal('carModal');
      modal.querySelector('.modal-title').textContent = car.name;
      const price = currency === 'USD' ? car.priceUSD : car.priceINR;
      modal.querySelector('.modal-body').innerHTML = `
        <div class="modal-grid">
          <img class="modal-img" src="${car.image}" alt="${car.name}" onerror="this.onerror=null;this.src='assets/images/cars/ferrari-sf90.jpg'">
          <div class="modal-specs">
            <p><span class="k">Brand</span><span class="v">${car.brand}</span></p>
            <p><span class="k">Category</span><span class="v">${car.category}</span></p>
            <p><span class="k">Year</span><span class="v">${car.year}</span></p>
            <p><span class="k">Price</span><span class="v">${price}</span></p>
            <p><span class="k">Horsepower</span><span class="v">${car.horsepower} HP</span></p>
            <p><span class="k">Top Speed</span><span class="v">${car.topSpeed} km/h</span></p>
            <p><span class="k">0-60</span><span class="v">${car.zeroToSixty}s</span></p>
            <p><span class="k">Fuel</span><span class="v">${car.fuelType}</span></p>
          </div>
        </div>
        <p class="modal-desc">${car.description || ''}</p>
      `;
      modal.classList.add('open');
    },
    openArticle(article){
      const modal = ensureModal('blogModal');
      modal.querySelector('.modal-title').textContent = article.title;
      modal.querySelector('.modal-body').innerHTML = `
        <p class="blog-meta">${article.category} • ${article.readTime}</p>
        <img class="modal-img" src="${article.cover}" alt="${article.title}" onerror="this.onerror=null;this.src='assets/images/cars/ferrari-sf90.jpg'">
        <div class="modal-desc">${article.content}</div>
      `;
      modal.classList.add('open');
    }
  };
})();
