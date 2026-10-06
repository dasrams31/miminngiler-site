#!/usr/bin/env python3
"""Generate halaman detail produk p-<id>.html dari products.json + ig-posts.json"""
import json, html, os

SITE = os.path.dirname(os.path.abspath(__file__))

def esc(s): return html.escape(s or "")

def reel_embed(url):
    if not url:
        return ('<div class="reel-ph"><img src="img/logo.png" alt="">'
                '<strong>Video unboxing segera tayang~</strong>'
                '<p>Follow <a href="https://instagram.com/mimin.ngiler" target="_blank" rel="noopener" '
                'style="color:var(--yellow);font-weight:700">@mimin.ngiler</a> biar nggak ketinggalan!</p></div>')
    return (f'<blockquote class="instagram-media" data-instgrm-permalink="{esc(url)}" '
            'data-instgrm-version="14" style="margin:0 auto"></blockquote>')

def desc_html(p):
    parts = []
    if p.get("shopee_desc"):
        for line in p["shopee_desc"].split("\n"):
            line = line.strip()
            if line: parts.append(f"<li>{esc(line)}</li>")
    if parts:
        return "<ul class='speclist'>" + "".join(parts) + "</ul>"
    return ""

def page(p, reels, related):
    price = p.get("price") or "Cek harga terbaru di Shopee"
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p['name'])} — MiminNgiler</title>
<meta name="description" content="{esc(p['name'])} — {esc(p.get('desc',''))} Rekomendasi jujur MiminNgiler.">
<link rel="icon" type="image/png" href="img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<style>
.detail{{max-width:68rem;margin:0 auto;padding:2rem clamp(1rem,4vw,2.5rem)}}
.back{{display:inline-flex;align-items:center;gap:.4rem;color:var(--muted);text-decoration:none;font-weight:700;margin-bottom:1.5rem}}
.back:hover{{color:var(--yellow)}}
.dgrid{{display:grid;grid-template-columns:1fr 1.1fr;gap:2rem;align-items:start}}
@media(max-width:720px){{.dgrid{{grid-template-columns:1fr}}}}
.dthumb{{border-radius:var(--radius);overflow:hidden;border:1px solid var(--line);box-shadow:var(--shadow);position:relative}}
.dthumb img{{width:100%;aspect-ratio:4/5;object-fit:cover}}
.dinfo .cat{{font-size:.75rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--yellow)}}
.dinfo h1{{font-size:clamp(1.5rem,4.5vw,2.2rem);font-weight:800;line-height:1.2;margin:.4rem 0 .8rem}}
.price{{font-size:clamp(1.6rem,5vw,2.2rem);font-weight:800;color:var(--yellow);margin:.6rem 0}}
.price-note{{font-size:.8rem;color:var(--muted)}}
.speclist{{list-style:none;margin:1rem 0;display:grid;gap:.5rem}}
.speclist li{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.7rem 1rem;font-size:.92rem}}
.speclist li::before{{content:"✓ ";color:var(--yellow);font-weight:800}}
.buybox{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:1.4rem;margin-top:1.2rem;display:grid;gap:.9rem}}
.dreel{{margin-top:2.5rem}}
.dreel h2{{font-size:1.4rem;font-weight:800;margin-bottom:1rem}}
.dreel h2 em{{font-style:normal;color:var(--yellow)}}
.rel{{margin-top:2.5rem}}
.rel h2{{font-size:1.4rem;font-weight:800;margin-bottom:1rem}}
</style>
</head>
<body>
<div class="grain" aria-hidden="true"></div>
<header class="topbar">
  <a class="brand" href="index.html"><img src="img/logo.png" alt="Logo MiminNgiler" width="36" height="36"><span>MiminNgiler</span></a>
  <nav class="topnav"><a href="index.html#katalog">Katalog</a><a href="index.html#cara-beli">Cara Beli</a><a href="index.html#reels">Reels</a></nav>
  <a class="btn btn-small" href="https://instagram.com/mimin.ngiler" target="_blank" rel="noopener">Follow IG</a>
</header>
<main class="detail">
  <a class="back" href="index.html#katalog">← Kembali ke katalog</a>
  <div class="dgrid">
    <div class="dthumb">
      <div class="sticker">{esc(p.get('badge','Rekomendasi'))}</div>
      {"<img src='"+esc(p['thumb'])+"' alt='"+esc(p['name'])+"'>" if p.get('thumb') else '<div class="thumb-ph"><img src="img/logo.png" alt=""><span>Foto segera hadir~</span></div>'}
    </div>
    <div class="dinfo">
      <span class="cat">{esc(p.get('category',''))}</span>
      <h1>{esc(p['name'])}</h1>
      <div class="price">{esc(price)}</div>
      {f'<div class="price-note">{esc(p["price_note"])}</div>' if p.get('price_note') else ''}
      <p style="color:var(--muted);margin:.8rem 0">{esc(p.get('desc',''))}</p>
      {desc_html(p)}
      <div class="buybox">
        <a class="buy-btn" href="{esc(p['link'])}" target="_blank" rel="noopener nofollow">🛒 Beli di Shopee</a>
        <div class="code-row"><code>{esc(p['code'])}</code><button class="copy-btn" data-code="{esc(p['code'])}">Salin Kode</button></div>
        <p style="font-size:.82rem;color:var(--muted)">Nggak mau ribet buka link? Salin kodenya, tempel di kolom pencarian aplikasi Shopee~</p>
      </div>
    </div>
  </div>
  <section class="dreel">
    <h2>Video <em>Unboxing</em> Mimin</h2>
    {reel_embed(reels.get(p['id']))}
  </section>
  {"<section class='rel'><h2>Bunda-bunda juga <em style='font-style:normal;color:var(--yellow)'>ngiler</em> ini</h2><div class='grid'>" + "".join(
    f"<article class='card'><a href='p-{r['id']}.html' style='text-decoration:none;color:inherit'>"
    + ("<div class='thumb'><img src='"+esc(r['thumb'])+"' alt='"+esc(r['name'])+"' loading='lazy'></div>" if r.get('thumb') else "<div class='thumb'><div class='thumb-ph'><img src='img/logo.png' alt=''></div></div>")
    + f"<div class='card-body'><span class='cat'>{esc(r.get('category',''))}</span><h3>{esc(r['name'])}</h3></div></a></article>"
    for r in related) + "</div></section>" if related else ""}
  <section class="section disclaimer"><p>💛 Link di halaman ini link affiliate ya Bun — <strong>harga tetap sama</strong>, nggak ada biaya tambahan. Setiap checkout bantu Mimin terus bikin review jujur. Makasih banyak!</p></section>
</main>
<footer>
  <img src="img/logo.png" alt="" width="44" height="44">
  <p><strong>MiminNgiler</strong> — “Mimin aja ngiler, apalagi kamu~”</p>
  <p class="foot-small">© 2026 MiminNgiler • Dibuat dengan 💛 dan sedikit ngiler</p>
</footer>
<div class="toast" id="toast" role="status"></div>
<script async src="https://www.instagram.com/embed.js"></script>
<script>
document.querySelectorAll('.copy-btn').forEach(b=>b.addEventListener('click',async()=>{{
  try{{await navigator.clipboard.writeText(b.dataset.code)}}catch(e){{}}
  const t=document.getElementById('toast');t.textContent='Kode '+b.dataset.code+' tersalin! Tempel di pencarian Shopee 🛒';t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2200);
}}));
if(window.instgrm)window.instgrm.Embeds.process();
</script>
</body>
</html>"""

def main():
    products = json.load(open(os.path.join(SITE, "products.json")))
    try:
        ig = json.load(open(os.path.join(SITE, "ig-posts.json")))
    except Exception:
        ig = []
    reels = {}
    for e in ig:
        if isinstance(e, dict) and e.get("product_id") and e.get("url"):
            reels[e["product_id"]] = e["url"]
        elif isinstance(e, dict) and e.get("url"):
            pass  # entri lama tanpa product_id -> hanya tampil di grid utama
    for p in products:
        related = [r for r in products if r["id"] != p["id"] and r.get("category") == p.get("category")][:3]
        out = os.path.join(SITE, f"p-{p['id']}.html")
        open(out, "w").write(page(p, reels, related))
        print("wrote", out)

if __name__ == "__main__":
    main()
