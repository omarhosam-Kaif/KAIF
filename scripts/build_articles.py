#!/usr/bin/env python3
"""Generate the longer reads at /articles/ and /articles/<slug>/.

    python3 scripts/build_articles.py

Guides are short how-tos. Articles are longer pieces that explain coffee.
"""
import pathlib
import re
import sys
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_guides import ROOT, SITE, esc, page, shared_styles  # noqa: E402

TODAY = date.today().isoformat()

ARTICLES = [
    {
        "slug": "what-is-specialty-coffee",
        "ar_title": "يعني إيه قهوة سبيشالتي؟",
        "en_title": "What is specialty coffee?",
        "intro": "Specialty coffee is coffee that is grown with care, roasted fresh and sold with details you can check. It is a different product from the supermarket tin, and you can taste the difference.",
        "sections": [
            ("What the word means", [
                "In the coffee trade, specialty coffee is coffee that scores 80 points or more out of 100 when trained tasters grade it. The score looks at flavour, sweetness, acidity, body and how clean the cup is. Coffee with obvious faults cannot reach that score.",
                "In everyday life it also means the coffee is traceable. You know the country it came from, and often the region and the variety. A bag that only says \"coffee\" tells you nothing.",
            ]),
            ("Why it tastes different", [
                "Most of the flavour is decided before the beans reach the roaster: where the coffee grew, how it was picked and how it was dried. Good beans are picked ripe, sorted carefully and roasted in small batches, so the roaster can bring out the fruit, sweetness and chocolate notes instead of burning them away.",
                "Dark, oily roasts hide a lot of this. A lighter or medium roast lets the origin show, which is why a Colombian coffee and an Ethiopian one taste so different in the cup.",
            ]),
            ("Freshness matters", [
                "Roasted coffee is at its best in the weeks after roasting. Beans that sat for months in a warehouse taste flat, however good they were. Buying from a roaster in your own country means the bag reaches you quickly.",
            ]),
            ("How to start", [
                "Pick one single origin and one blend and compare them side by side with the same brew method. Notice what you like: fruity or chocolatey, light or heavy. That tells you which coffees to buy next.",
            ]),
        ],
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("aura-blend", "Aura Blend")],
    },
    {
        "slug": "single-origin-or-blend",
        "ar_title": "سينجل أوريجن ولا بليند؟",
        "en_title": "Single origin or blend: which should you buy?",
        "intro": "Neither is better. A single origin shows you one place. A blend is built to taste balanced every time. The right choice depends on how you drink your coffee.",
        "sections": [
            ("Single origin", [
                "A single origin comes from one country, and often one region or farm. It shows the character of that place, so it can taste fruity, floral or sharp, and it changes from harvest to harvest. It suits filter brewing, where you want to taste what the coffee is.",
            ]),
            ("Blend", [
                "A blend mixes coffees from more than one origin. The roaster chooses them to cover each other's weak points, for example one for sweetness and one for body. The result is steady and balanced, and it works well in espresso and with milk.",
            ]),
            ("How to choose", [
                "If you like to taste differences and drink your coffee black, start with a single origin. If you make espresso or milk drinks every morning and want the same cup each time, start with a blend.",
                "You do not have to pick one for good. Many people keep a blend for daily espresso and a single origin for weekends.",
            ]),
        ],
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("brazil-parana", "Brazil Paraná"), ("ember-blend", "Ember Blend"), ("dolce-blend", "Dolce Blend")],
    },
    {
        "slug": "why-fresh-roasted-coffee-matters",
        "ar_title": "ليه البن المحمص جديد أحسن؟",
        "en_title": "Why freshly roasted coffee tastes better",
        "intro": "Coffee starts to lose flavour soon after roasting. Buying it fresh, in smaller bags, is the easiest way to make your coffee taste better without buying any new equipment.",
        "sections": [
            ("What happens after roasting", [
                "Roasting creates the aromas you smell in a coffee shop. Over the next weeks those aromas fade as the beans react with air, and the cup gets duller. Freshly roasted beans also release gas for the first days, which is normal.",
            ]),
            ("Whole beans last longer", [
                "Ground coffee has a much larger surface touching the air, so it goes stale faster. If you can, buy whole beans and grind just before brewing. If you cannot grind at home, ask for the coffee to be ground for your brew method and use it quickly.",
            ]),
            ("Buy smaller bags", [
                "A bag you finish in two to three weeks will taste better than a big bag that takes two months. That is why smaller sizes, such as a 20 g bag to try a new coffee, are useful. Once you know what you like, buy the full bag.",
            ]),
            ("Keep it fresh at home", [
                "Keep the beans in an airtight bag or jar, in a cool dark place. Avoid the fridge, because moisture gets in each time you open it.",
            ]),
        ],
        "links": [("ethiopia-guji", "Ethiopia Guji"), ("colombia-huila", "Colombia Huila"), ("ember-blend", "Ember Blend")],
    },
]


def body(a):
    secs = "".join(
        f"<h2>{esc(h)}</h2>" + "".join(f"<p>{esc(p)}</p>" for p in ps) for h, ps in a["sections"]
    )
    links = '<div class="shop-links">' + "".join(
        f'<a href="/{esc(s)}">{esc(l)}</a>' for s, l in a["links"]
    ) + "</div>"
    return f"""<article class="guide article">
  <h1 lang="ar" dir="rtl">{esc(a["ar_title"])}</h1>
  <p class="en">{esc(a["en_title"])}</p>
  <p class="answer">{esc(a["intro"])}</p>
  <div class="answer article-body">{secs}</div>
  {links}
</article>"""


EXTRA_CSS = "<style>.article-body h2{font-size:24px;margin:32px 0 8px}.article-body p{margin:0 0 14px}</style>"


def build():
    styles = shared_styles()
    out_dir = ROOT / "articles"
    out_dir.mkdir(exist_ok=True)
    listing = "".join(
        f'<li><a href="/articles/{esc(a["slug"])}">{esc(a["en_title"])}</a></li>' for a in ARTICLES
    )
    index_body = f"""{EXTRA_CSS}<article class="guide">
  <h1>Articles</h1>
  <p class="answer">Longer reads about specialty coffee: what it is, how to choose it and how to keep it fresh. For step-by-step brewing, see our <a href="/guides/">guides</a>.</p>
  <ul class="answer" style="list-style:none;padding:0">{listing}</ul>
</article>"""
    (out_dir / "index.html").write_text(
        page("Articles | KAIF", "Longer reads about specialty coffee from KAIF in Egypt: what it is, single origin vs blend, and keeping beans fresh.",
             f"{SITE}/articles/", index_body, styles),
        encoding="utf-8",
    )
    urls = [f"{SITE}/articles/"]
    for a in ARTICLES:
        d = out_dir / a["slug"]
        d.mkdir(exist_ok=True)
        desc = a["intro"] if len(a["intro"]) <= 160 else a["intro"][:157].rsplit(" ", 1)[0] + "..."
        (d / "index.html").write_text(
            page(f'{a["en_title"]} | KAIF', desc, f'{SITE}/articles/{a["slug"]}', EXTRA_CSS + body(a), styles),
            encoding="utf-8",
        )
        urls.append(f'{SITE}/articles/{a["slug"]}')
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    text = re.sub(r"\s*<url>\s*<loc>https://kaifcoffee\.net/articles[^<]*</loc>.*?</url>", "", text, flags=re.S)
    entries = "".join(
        f"\n  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>"
        for u in urls
    )
    text = text.replace("</urlset>", entries + "\n</urlset>")
    sm.write_text(text, encoding="utf-8")
    print(f"built {len(ARTICLES)} articles + index")


if __name__ == "__main__":
    build()
