/* MiminNgiler catalog app */
const grid = document.getElementById('productGrid');
const chipsBox = document.getElementById('chips');
const searchInput = document.getElementById('searchInput');
const emptyState = document.getElementById('emptyState');
const toast = document.getElementById('toast');

let products = [];
let activeCat = 'Semua';
let query = '';

function showToast(msg){
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(showToast._t);
  showToast._t = setTimeout(()=>toast.classList.remove('show'), 2200);
}

function copyIcon(){
  return '<svg viewBox="0 0 24 24"><path d="M8 2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8zm0 2h10v12H8V4zm-4 4v12a2 2 0 0 0 2 2h10v-2H6V8H4z"/></svg>';
}

function thumbHTML(p){
  if(p.thumb){
    return '<div class="thumb"><img src="'+p.thumb+'" alt="'+p.name+'" loading="lazy"></div>';
  }
  return '<div class="thumb"><div class="thumb-ph"><img src="img/logo.png" alt="">'
    + '<span>Video segera tayang~</span></div></div>';
}

function cardHTML(p){
  const detail = 'p-'+p.id+'.html';
  return '<article class="card reveal">'
    + '<div class="sticker">'+p.badge+'</div>'
    + '<a class="cardlink" href="'+detail+'" aria-label="Detail '+p.name+'">'+thumbHTML(p)+'</a>'
    + '<div class="card-body">'
    + '<span class="cat">'+p.category+'</span>'
    + '<h3><a class="cardlink" href="'+detail+'">'+p.name+'</a></h3>'
    + '<p class="desc">'+p.desc+'</p>'
    + '<div class="code-row"><code>'+p.code+'</code>'
    + '<button class="copy-btn" data-code="'+p.code+'">'+copyIcon()+'Salin Kode</button></div>'
    + '<a class="buy-btn" href="'+p.link+'" target="_blank" rel="noopener nofollow">🛒 Beli di Shopee</a>'
    + '<a class="detail-btn" href="'+detail+'">📝 Lihat Detail</a>'
    + '</div></article>';
}

function render(){
  const q = query.trim().toLowerCase();
  const list = products.filter(p =>
    (activeCat==='Semua' || p.category===activeCat) &&
    (!q || (p.name+' '+p.desc+' '+p.category).toLowerCase().includes(q))
  );
  grid.innerHTML = list.map(cardHTML).join('');
  emptyState.hidden = list.length > 0;
  observeReveals();
  grid.querySelectorAll('.copy-btn').forEach(b=>{
    b.addEventListener('click', async ()=>{
      const code = b.dataset.code;
      try{ await navigator.clipboard.writeText(code); }
      catch(e){
        const ta=document.createElement('textarea');
        ta.value=code; document.body.appendChild(ta); ta.select();
        document.execCommand('copy'); ta.remove();
      }
      b.innerHTML = '✓ Tersalin!';
      showToast('Kode '+code+' tersalin! Tempel di pencarian Shopee 🛒');
      setTimeout(()=>{ b.innerHTML = copyIcon()+'Salin Kode'; }, 2000);
    });
  });
}

function renderChips(){
  const cats = ['Semua', ...new Set(products.map(p=>p.category))];
  chipsBox.innerHTML = cats.map(c=>
    '<button class="chip'+(c===activeCat?' active':'')+'" data-cat="'+c+'">'+c+'</button>'
  ).join('');
  chipsBox.querySelectorAll('.chip').forEach(ch=>{
    ch.addEventListener('click', ()=>{
      activeCat = ch.dataset.cat;
      renderChips(); render();
    });
  });
}

searchInput.addEventListener('input', e=>{ query = e.target.value; render(); });

/* reveal on scroll */
let io;
function observeReveals(){
  if(!io && 'IntersectionObserver' in window){
    io = new IntersectionObserver(es=>{
      es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    },{threshold:.12});
  }
  document.querySelectorAll('.reveal:not(.in)').forEach(el=>{
    if(io) io.observe(el); else el.classList.add('in');
  });
  /* safety: reveal anything stuck in viewport after 2.5s */
  setTimeout(()=>{
    const vh = window.innerHeight;
    document.querySelectorAll('.reveal:not(.in)').forEach(el=>{
      const r = el.getBoundingClientRect();
      if(r.top < vh && r.bottom > 0) el.classList.add('in');
    });
  }, 2500);
}

/* reels */
async function loadReels(){
  const box = document.getElementById('reelGrid');
  try{
    const r = await fetch('ig-posts.json');
    const posts = await r.json();
    if(posts && posts.length){
      box.innerHTML = posts.map(p=>
        '<div class="reel-card"><blockquote class="instagram-media" data-instgrm-permalink="'+p.url
        +'" data-instgrm-version="14"></blockquote></div>'
      ).join('');
      if(window.instgrm) window.instgrm.Embeds.process();
      return;
    }
  }catch(e){}
  box.innerHTML = '<div class="reel-ph"><img src="img/logo.png" alt="">'
    + '<strong>Reels perdana segera tayang~</strong>'
    + '<p>Sambil nunggu, follow dulu <a href="https://instagram.com/mimin.ngiler" target="_blank" rel="noopener" style="color:var(--yellow);font-weight:700">@mimin.ngiler</a> biar nggak ketinggalan!</p></div>';
}

/* boot */
fetch('products.json')
  .then(r=>r.json())
  .then(data=>{
    products = data;
    document.getElementById('statProduk').textContent = products.length;
    renderChips(); render(); observeReveals(); loadReels();
  })
  .catch(()=>{ grid.innerHTML='<p class="empty">Katalog lagi dimasak Mimin, bentar ya~ 🍳</p>'; });
