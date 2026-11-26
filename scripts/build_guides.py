#!/usr/bin/env python3
"""Generate the coffee guides at /guides/ and /guides/<slug>/.

Run after editing GUIDES below:

    python3 scripts/build_guides.py

Each guide is a static page with its own title and description, a short answer,
and links to the bags it relates to. Sitemap entries are added to sitemap.xml.
"""
import html
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://kaifcoffee.net"
TODAY = date.today().isoformat()

GUIDES = [
    {
        "slug": "moka-pot",
        "ar_title": "إزاي تعمل قهوة بالموكا بوت؟",
        "en_title": "How to brew coffee in a moka pot",
        "answer": "Fill the bottom chamber with hot water up to just below the valve. Fill the basket with medium-fine coffee, a little coarser than espresso, level it without pressing, and screw the top on tight. Heat on low to medium. When the coffee starts to flow, wait until it turns pale and begins to sputter, then take the pot off the heat and run the base under cold water to stop the brew. Stir, and pour. If the cup tastes bitter or burnt, use lower heat or a slightly coarser grind.",
        "links": [("ember-blend", "Ember Blend"), ("aura-blend", "Aura Blend"), ("dolce-blend", "Dolce Blend")],
    },
    {
        "slug": "cold-brew",
        "ar_title": "إزاي تعمل كولد برو في البيت؟",
        "en_title": "How to make cold brew at home",
        "answer": "Mix 100 grams of coarsely ground coffee with 1 litre of cold water in a jar. Stir so all the grounds are wet, cover, and leave in the fridge for 12 to 16 hours. Strain through a paper filter or fine cloth. This makes a strong concentrate, so serve it over ice and dilute with water or milk to taste. Keep it in the fridge and drink it within about five days.",
        "links": [("brazil-parana", "Brazil Paraná"), ("colombia-huila", "Colombia Huila"), ("ember-blend", "Ember Blend")],
    },
    {
        "slug": "v60-pour-over",
        "ar_title": "إزاي تعمل قهوة V60 في البيت؟",
        "en_title": "How to brew V60 pour-over at home",
        "answer": "Use 15 grams of coffee and 250 ml of water as a starting point. Grind medium-fine, a little finer than table salt, and use water just off the boil. Rinse the paper filter, add the coffee, and pour 50 ml to wet the grounds. Wait 30 seconds, then pour the rest in slow circles. Aim to finish in about two and a half to three minutes. If it drips through too fast and tastes sour, grind finer. If it drips slowly and tastes bitter, grind coarser.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("colombia-huila", "Colombia Huila")],
    },
    {
        "slug": "turkish-coffee-at-home",
        "ar_title": "إزاي تعمل قهوة تركي في البيت؟",
        "en_title": "How to make Turkish coffee at home",
        "answer": "Use about 7 grams of finely ground Turkish coffee and 70 ml of cold water for each small cup. Put both in a cezve, add sugar now if you want it, and stir once. Heat on low and do not stir again. When the foam rises to the rim, take the cezve off the heat before it boils over. Pour slowly so the foam lands in the cup, and let it rest for a minute so the grounds settle. Sip, and leave the grounds at the bottom. A 20 g bag makes about 2 to 3 cups, so it is an easy way to try.",
        "links": [("turkish-coffee-plain-light", "Turkish Plain Light"), ("turkish-coffee-plain-medium", "Turkish Plain Medium"), ("turkish-coffee-spiced-light", "Turkish Spiced Light"), ("turkish-coffee-spiced-medium", "Turkish Spiced Medium"), ("turkish-coffee-plain-light-20g", "Try a 20 g bag")],
    },
    {
        "slug": "filter-coffee-at-home",
        "ar_title": "كيف أعمل قهوة فلتر في البيت؟",
        "en_title": "How to brew filter coffee at home",
        "answer": "Use 300 ml of water for 20 grams of coffee as a starting point. Grind to a medium size, and use water just off the boil. Pour in slow circles, and finish the brew in about three to four minutes. Adjust the grind if the cup tastes sour or bitter.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("brazil-parana", "Brazil Paraná")],
    },
    {
        "slug": "french-press",
        "ar_title": "إزاي تعمل قهوة الفرنش برس في البيت؟",
        "en_title": "How to brew French press at home",
        "answer": "Use 300 ml of water for 20 grams of coffee as a starting point. Grind coarse, like sea salt, and use water just off the boil. Pour the water over the grounds, stir gently, and put the lid on with the plunger up. Wait four minutes, then press down slowly and pour out the whole cup at once so the coffee stops brewing. If the cup tastes bitter, use a slightly coarser grind or a shorter wait. If it tastes sour, wait a little longer or grind a little finer.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("brazil-parana", "Brazil Paraná")],
    },
    {
        "slug": "grind-size",
        "ar_title": "درجة الطحن المناسبة لكل طريقة تحضير",
        "en_title": "How to choose your grind size",
        "answer": "Espresso needs a fine grind, like sand. Filter needs a medium grind, like table salt. French press needs a coarse grind, like sea salt. If your coffee tastes sour, grind finer. If it tastes bitter or harsh, grind coarser.",
        "links": [],
    },
    {
        "slug": "espresso-or-filter",
        "ar_title": "الإسبريسو ولا الفلتر؟ الفرق بينهم",
        "en_title": "Espresso or filter: which is right for you?",
        "answer": "Espresso is a small, strong shot made under pressure, so the body feels heavy and the flavour is concentrated. Filter is a larger, lighter cup that shows more of the coffee's fruit and floral notes. Choose espresso if you drink milk drinks or want a strong shot. Choose filter if you want to taste the origin.",
        "links": [("ember-blend", "Ember Blend"), ("aura-blend", "Aura Blend"), ("dolce-blend", "Dolce Blend"), ("ethiopia-guji", "Ethiopia Guji")],
    },
    {
        "slug": "store-coffee-beans",
        "ar_title": "إزاي تحافظ على البن بعد ما تفتحه",
        "en_title": "How to store coffee beans after opening",
        "answer": "Keep beans in their airtight bag, or move them to an airtight jar. Store them in a cool, dark place away from heat and sunlight. Do not keep them in the fridge, because moisture gets in every time you open it. Use the beans within a few weeks of opening for the best flavour.",
        "links": [],
    },
]


def esc(s):
    return html.escape(str(s), quote=True)


def shared_styles():
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    return re.search(r"<style>(.*?)</style>", index, re.S).group(1)


def page(title, description, canonical, body, styles):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="KAIF">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<style>{styles}
.guide{{max-width:760px;margin:0 auto;padding:48px 20px}}
.guide h1{{font-size:34px;margin:0 0 6px}}
.guide .en{{color:#5d6a6e;font-size:18px;margin:0 0 24px}}
.guide .answer{{font-size:18px;line-height:1.7;color:#2b3538}}
.guide .shop-links{{margin-top:28px}}
.guide .shop-links a{{display:inline-block;margin:6px 8px 0 0;padding:8px 14px;border:1px solid #cfc7b6;border-radius:999px;color:#1f2a2e;text-decoration:none}}
</style>
</head>
<body>
<header>
  <div class="container nav">
    <a href="/" class="brand" aria-label="KAIF home"><span class="cat " aria-hidden="true"><img src="/cat-hero.png" alt="" width="44" height="44"><i class="lid lid-l"></i><i class="lid lid-r"></i><i class="steam"></i><i class="steam s2"></i></span><span>KAIF</span></a>
    <ul class="nav-links" id="navLinks"><li><a href="/#shop">Shop</a></li><li><a href="/guides/">Articles</a></li><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul>
    <div class="nav-actions">
      <a class="cart-btn" href="/#shop" aria-label="Open cart"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.4 12.2a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L21 8H6"/></svg></a>
      <button class="menu-toggle" id="menuToggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<script>document.getElementById("menuToggle").addEventListener("click",function(){{var n=document.getElementById("navLinks");n.classList.toggle("open");this.setAttribute("aria-expanded",n.classList.contains("open"));}});</script>
<main>
{body}
</main>
</body>
</html>
"""


def guide_body(g):
    links = ""
    if g["links"]:
        links = '<div class="shop-links">' + "".join(
            f'<a href="/{esc(slug)}">{esc(label)}</a>' for slug, label in g["links"]
        ) + "</div>"
    else:
        links = '<div class="shop-links"><a href="/#shop">Shop KAIF coffee</a></div>'
    return f"""<article class="guide">
  <h1 lang="ar" dir="rtl">{esc(g["ar_title"])}</h1>
  <p class="en">{esc(g["en_title"])}</p>
  <p class="answer">{esc(g["answer"])}</p>
  {links}
</article>"""


def build():
    styles = shared_styles()
    guides_dir = ROOT / "guides"
    guides_dir.mkdir(exist_ok=True)
    listing = "".join(
        f'<li><a href="/guides/{esc(g["slug"])}">{esc(g["en_title"])}</a></li>' for g in GUIDES
    )
    index_body = f"""<style>body{{background:linear-gradient(rgba(251,250,247,.6),rgba(251,250,247,.6)),url('/hero_bg.jpg') center/cover fixed no-repeat;min-height:100vh}}.guides-index{{background:rgba(251,250,247,.9);border-radius:0;padding:72px 8vw;margin:0;max-width:none;width:100%;min-height:calc(100vh - 72px);box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;box-shadow:none}}.guides-index h1{{font-size:44px;margin-bottom:14px}}.guides-index .answer{{font-size:18px;margin-bottom:28px}}.guides-index ul{{list-style:none;padding:0}}.guides-index li{{padding:16px 0;border-bottom:1px solid rgba(31,42,46,.12);font-size:18px}}.guides-index li:last-child{{border-bottom:0}}.guides-index a{{text-decoration:none;color:var(--ink);font-weight:600}}.guides-index a:hover{{color:var(--teal-dark);text-decoration:underline}}</style>
<article class="guide guides-index">
  <h1>Coffee guides</h1>
  <p class="answer">Short, practical answers about brewing, grinding and buying specialty coffee.</p>
  <ul class="answer">{listing}</ul>
</article>"""
    (guides_dir / "index.html").write_text(
        page("Coffee guides | KAIF", "Short guides on brewing, grinding and storing specialty coffee, from KAIF in Egypt.",
             f"{SITE}/guides/", index_body, styles),
        encoding="utf-8",
    )
    urls = [f"{SITE}/guides/"]
    for g in GUIDES:
        out = guides_dir / g["slug"]
        out.mkdir(exist_ok=True)
        desc = g["answer"][:157].rsplit(" ", 1)[0] + "..." if len(g["answer"]) > 160 else g["answer"]
        (out / "index.html").write_text(
            page(f'{g["en_title"]} | KAIF', desc, f'{SITE}/guides/{g["slug"]}', guide_body(g), styles),
            encoding="utf-8",
        )
        urls.append(f'{SITE}/guides/{g["slug"]}')
    # add guide URLs to the sitemap (drop any earlier guide entries first)
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    text = re.sub(r"\s*<url>\s*<loc>https://kaifcoffee\.net/guides[^<]*</loc>.*?</url>", "", text, flags=re.S)
    entries = "".join(
        f"\n  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
        for u in urls
    )
    text = text.replace("</urlset>", entries + "\n</urlset>")
    sm.write_text(text, encoding="utf-8")
    print(f"built {len(GUIDES)} guides + index")


if __name__ == "__main__":
    build()
