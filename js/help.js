(function(){
  window.CarWorldsHelp = {
    init(){
      document.querySelectorAll('.accordion-btn').forEach(btn=>{
        btn.addEventListener('click', ()=>{
          const item = btn.parentElement;
          item.classList.toggle('open');
        });
      });
      const form = document.getElementById('helpForm');
      if(form){
        form.addEventListener('submit', (e)=>{
          e.preventDefault();
          const msg = document.getElementById('helpFormMsg');
          if(msg){ msg.textContent = 'Thanks! Your message has been recorded (demo).'; }
          form.reset();
        });
      }
    }
  };
})();
