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
        "slug": "filter-coffee-at-home",
        "ar_title": "كيف أعمل قهوة فلتر في البيت؟",
        "en_title": "How to brew filter coffee at home",
        "answer": "Use about 15 grams of water for every 1 gram of coffee as a starting point. Grind to a medium size, and use water just off the boil. Pour in slow circles, and finish the brew in about three to four minutes. Adjust the grind if the cup tastes sour or bitter.",
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("brazil-parana", "Brazil Paraná")],
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
    {
        "slug": "single-origin",
        "ar_title": "يعني إيه أحادي المصدر؟",
        "en_title": "What does single origin mean?",
        "answer": "Single origin means every bean in the bag comes from one farm, one region or one country. The flavour reflects that place, its altitude and how the beans were processed. A blend mixes beans from several origins to create one balanced taste.",
        "links": [("brazil-parana", "Brazil Paraná"), ("colombia-huila", "Colombia Huila"), ("ethiopia-dijammah", "Ethiopia Dijammah"), ("ethiopia-guji", "Ethiopia Guji")],
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
    <a href="/" class="brand" aria-label="KAIF home"><span>KAIF</span></a>
    <ul class="nav-links"><li><a href="/#shop">Shop</a></li><li><a href="/guides/">Guides</a></li></ul>
  </div>
</header>
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
    index_body = f"""<article class="guide">
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
