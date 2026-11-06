#!/usr/bin/env python3
"""Generate one static page per active product, e.g. /ember-blend/index.html.

Reads data/products.json (a snapshot of the Supabase product tables) and the
shared stylesheet from index.html. Each page is server-rendered for search
engines and refreshes its price from Supabase on load, so price changes made
in the database show up without a redeploy. Re-run this script whenever a
product is added, removed, or its description changes:

    python3 scripts/build_product_pages.py
"""
import html
import json
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://kaifcoffee.net"
SUPABASE_URL = "https://snkzghazwdmhvomtythb.supabase.co"
SUPABASE_KEY = "sb_publishable_HxC3TGER6J4J4CVheOgakg_VJuqXHLu"

ROAST = {"light": "Light", "medium": "Medium", "medium_dark": "Medium dark", "dark": "Dark"}


def esc(s):
    return html.escape(str(s), quote=True)


def shared_styles():
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", index, re.S)
    return m.group(1)


def describe(p):
    if p.get("description"):
        return p["description"]
    notes = ", ".join(p.get("tasting_notes") or [])
    base = p.get("subtitle") or "Specialty coffee"
    if notes:
        return f"{base}. Tasting notes: {notes.lower()}."
    return base


def meta_description(p):
    text = f"{describe(p)} Order from KAIF, roasted in small batches in Egypt."
    return text if len(text) <= 160 else text[:157].rsplit(" ", 1)[0] + "..."


def build_page(p, variant, images, styles):
    name = p["name"]
    slug = p["slug"]
    url = f"{SITE}/{slug}"
    desc = describe(p)
    price = variant.get("price") if variant else None
    image = images[0]["url"] if images else f"{SITE}/icon-512.png"
    image_alt = images[0].get("alt_text") or name if images else name

    details = []
    if p.get("roast_level"):
        details.append(("Roast", ROAST.get(p["roast_level"], p["roast_level"])))
    if p.get("process"):
        details.append(("Process", p["process"]))
    if p.get("brew_methods"):
        details.append(("Brew", ", ".join(m.capitalize() for m in p["brew_methods"])))
    if variant:
        details.append(("Pack", f"{variant['weight_grams']} g whole beans"))
    detail_rows = "".join(
        f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in details
    )
    notes_html = ""
    if p.get("tasting_notes"):
        notes_html = (
            '<h2>Tasting notes</h2><ul class="notes">'
            + "".join(f"<li>{esc(n)}</li>" for n in p["tasting_notes"])
            + "</ul>"
        )

    price_text = f"EGP {price}" if price is not None else "Price on request"
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": f"{url}#product",
                "name": name,
                "description": meta_description(p),
                "image": image,
                "sku": variant.get("sku") if variant else slug,
                "brand": {"@type": "Brand", "name": "KAIF"},
                "offers": {
                    "@type": "Offer",
                    "url": url,
                    "priceCurrency": "EGP",
                    "price": str(price) if price is not None else None,
                    "availability": "https://schema.org/InStock",
                    "itemCondition": "https://schema.org/NewCondition",
                    "seller": {"@id": f"{SITE}/#organization"},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "KAIF", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": url},
                ],
            },
        ],
    }
    # Drop empty offer price rather than publishing a null value.
    if json_ld["@graph"][0]["offers"]["price"] is None:
        del json_ld["@graph"][0]["offers"]["price"]
    json_ld_text = json.dumps(json_ld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} | KAIF Specialty Coffee</title>
<meta name="description" content="{esc(meta_description(p))}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="KAIF">
<meta property="og:title" content="{esc(name)} | KAIF">
<meta property="og:description" content="{esc(meta_description(p))}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="/icon-512.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#4AA9BA">
<script type="application/ld+json">
{json_ld_text}
</script>
<style>{styles}
.pp{{padding:48px 0 72px}}
.pp-crumbs{{font-size:14px;color:var(--ink-soft);margin-bottom:24px}}
.pp-crumbs a{{color:var(--ink-soft)}}
.pp-grid{{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}}
.pp-img{{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:24px}}
.pp-img img{{width:100%;height:auto;border-radius:8px}}
.pp h1{{font-size:44px;line-height:1.1;margin:8px 0 12px}}
.pp .sub{{color:var(--ink-soft);font-size:17px;margin-bottom:20px}}
.pp .price{{font-size:28px;font-weight:700;margin:24px 0 8px}}
.pp .price small{{font-size:14px;font-weight:500;color:var(--ink-soft)}}
.pp h2{{font-size:20px;margin:28px 0 10px}}
.pp dl{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}}
.pp dl div{{background:var(--white);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.pp dt{{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--ink-soft)}}
.pp dd{{font-weight:600;margin-top:2px}}
.notes{{list-style:none;display:flex;flex-wrap:wrap;gap:8px}}
.notes li{{background:var(--beige-light);border-radius:999px;padding:6px 14px;font-size:14px}}
@media (max-width:820px){{.pp-grid{{grid-template-columns:1fr}} .pp h1{{font-size:34px}}}}
</style>
</head>
<body>
<header>
  <div class="container nav">
    <a class="brand" href="/"><span>KAIF</span></a>
    <div class="nav-actions"><a class="btn btn-outline" href="/#shop">Shop all coffee</a></div>
  </div>
</header>
<main class="pp">
  <div class="container">
    <nav class="pp-crumbs" aria-label="Breadcrumb"><a href="/">KAIF</a> &rsaquo; <a href="/#shop">Shop</a> &rsaquo; {esc(name)}</nav>
    <div class="pp-grid">
      <div class="pp-img"><img src="{esc(image)}" alt="{esc(image_alt)}" width="512" height="512"></div>
      <div>
        <p class="eyebrow">{esc(p.get("subtitle") or "")}</p>
        <h1>{esc(name)}</h1>
        <p>{esc(desc)}</p>
        <p class="price" id="price">{esc(price_text)} <small>/ 250 g</small></p>
        <p><a class="btn btn-primary" href="/#shop">Order this coffee</a></p>
        {notes_html}
        <h2>Details</h2>
        <dl>{detail_rows}</dl>
      </div>
    </div>
  </div>
</main>
<footer>
  <div class="container" style="padding:32px 0;font-size:14px">
    KAIF &middot; Specialty coffee beans roasted in small batches in Egypt &middot;
    <a href="/#faq">FAQ</a> &middot; <a href="https://www.instagram.com/kaif.coffee_eg" target="_blank" rel="noopener">Instagram</a>
  </div>
</footer>
<script>
// Refresh the price from Supabase so database changes show without a redeploy.
(function () {{
  var url = "{SUPABASE_URL}/rest/v1/product_variants?select=price,grind,is_active,product:products!inner(slug)&product.slug=eq.{slug}&grind=eq.whole_beans&is_active=eq.true&limit=1";
  fetch(url, {{ headers: {{ apikey: "{SUPABASE_KEY}" }} }})
    .then(function (r) {{ return r.ok ? r.json() : null; }})
    .then(function (rows) {{
      if (!rows || !rows.length || rows[0].price == null) return;
      document.getElementById("price").firstChild.textContent = "EGP " + rows[0].price + " ";
    }})
    .catch(function () {{}});
}})();
</script>
</body>
</html>
"""


def main():
    data = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
    styles = shared_styles()
    variants = {}
    for v in data["product_variants"]:
        if v.get("is_active") and v.get("grind") == "whole_beans":
            variants.setdefault(v["product_slug"], v)
    images = {}
    for img in sorted(data["product_images"], key=lambda i: i.get("sort_order", 0)):
        images.setdefault(img["product_slug"], []).append(img)

    slugs = []
    for p in data["products"]:
        if not p.get("is_active"):
            continue
        slug = p["slug"]
        out_dir = ROOT / slug
        out_dir.mkdir(exist_ok=True)
        page = build_page(p, variants.get(slug), images.get(slug, []), styles)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        slugs.append(slug)
        print("wrote", slug)

    today = date.today().isoformat()
    urls = [f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>"]
    for slug in slugs:
        urls.append(
            f"  <url>\n    <loc>{SITE}/{slug}</loc>\n    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    print("sitemap updated with", len(slugs) + 1, "URLs")


if __name__ == "__main__":
    main()
