(function(){
  window.CarWorldsFilters = {
    state: {
      q: '',
      category: 'All',
      brand: 'All',
      sort: 'default',
      currency: 'INR'
    },
    apply(list){
      let out = list.slice();
      const s = this.state;
      if(s.category !== 'All') out = out.filter(c => c.category === s.category);
      if(s.brand !== 'All') out = out.filter(c => c.brand === s.brand);
      if(s.q){
        const q = s.q.toLowerCase();
        out = out.filter(c =>
          c.name.toLowerCase().includes(q) ||
          c.brand.toLowerCase().includes(q) ||
          String(c.horsepower).includes(q) ||
          String(c.topSpeed).includes(q)
        );
      }
      if(s.sort === 'price_asc' || s.sort === 'price_desc'){
        out.sort((a,b)=>{
          const av = parseFloat(String(a.priceUSD).replace(/[^0-9.]/g,'')) || 0;
          const bv = parseFloat(String(b.priceUSD).replace(/[^0-9.]/g,'')) || 0;
          return s.sort === 'price_asc' ? av-bv : bv-av;
        });
      } else if(s.sort === 'hp_desc'){
        out.sort((a,b)=> (b.horsepower||0)-(a.horsepower||0));
      }
      return out;
    }
  };
})();
