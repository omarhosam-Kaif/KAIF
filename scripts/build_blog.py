#!/usr/bin/env python3
"""Generate the blog listing and post pages at /blog/ and /blog/<slug>.

Articles are stored in the Supabase `blogs` table. The pages fetch published
posts on load, so a new article only needs to be written and switched to
is_published = true in Supabase. No rebuild or deploy is needed for articles.
Run this script only when the page design changes:

    python3 scripts/build_blog.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUPABASE_URL = "https://snkzghazwdmhvomtythb.supabase.co"
SUPABASE_KEY = "sb_publishable_HxC3TGER6J4J4CVheOgakg_VJuqXHLu"

index = (ROOT / "index.html").read_text(encoding="utf-8")
SHARED_CSS = re.search(r"<style>(.*?)</style>", index, re.S).group(1)

BLOG_CSS = """
.blog{padding:48px 0 72px}
.blog-head{text-align:center;margin-bottom:36px}
.blog-head h1{font-size:40px;margin-bottom:8px}
.blog-head p{color:var(--ink-soft)}
.blog-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px}
.post-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;text-decoration:none;display:flex;flex-direction:column;transition:box-shadow .25s,transform .25s}
.post-card:hover{box-shadow:0 18px 36px rgba(31,42,46,.14);transform:translateY(-4px)}
.post-card img{width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--beige-light)}
.post-card .pc-body{padding:20px;display:flex;flex-direction:column;gap:8px}
.post-card h2{font-size:20px;line-height:1.3;color:var(--ink)}
.post-card p{color:var(--ink-soft);font-size:15px}
.post-card .date{font-size:13px;color:var(--teal-dark);font-weight:600}
.post{max-width:760px;margin:0 auto}
.post .crumbs{font-size:14px;color:var(--ink-soft);margin-bottom:20px}
.post .crumbs a{color:var(--ink-soft)}
.post h1{font-size:42px;line-height:1.15;margin:8px 0 14px}
.post .lead{font-size:19px;color:var(--ink-soft);margin-bottom:28px}
.post img.cover{width:100%;border-radius:var(--radius);margin-bottom:28px}
.post .body p{font-size:17px;line-height:1.8;margin-bottom:18px}
.post .body-ar{direction:rtl;text-align:right;margin-top:48px;padding-top:36px;border-top:1px solid var(--line)}
.post .body-ar h2{font-size:30px;margin-bottom:14px;font-family:inherit}
.post .body-ar p{font-size:18px;line-height:1.9}
.blog-msg{text-align:center;color:var(--ink-soft);padding:60px 0}
"""

HEADER = """<header>
  <div class="container nav">
    <a class="brand" href="/"><span>KAIF</span></a>
    <div class="nav-actions"><a class="btn btn-outline" href="/#shop">Shop all coffee</a></div>
  </div>
</header>"""

FOOTER = """<footer>
  <div class="container" style="padding:32px 0;font-size:14px">
    KAIF &middot; Specialty coffee beans roasted in small batches in Egypt &middot;
    <a href="/guides/">Guides</a> &middot; <a href="/blog/">Blog</a> &middot;
    <a href="https://www.instagram.com/kaif.coffee_eg" target="_blank" rel="noopener">Instagram</a>
  </div>
</footer>"""


def page(title, description, canonical, main, script):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="KAIF">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<meta name="theme-color" content="#4AA9BA">
<style>{SHARED_CSS}{BLOG_CSS}</style>
</head>
<body>
{HEADER}
<main class="blog">
{main}
</main>
{FOOTER}
<script>
const SB_URL = "{SUPABASE_URL}";
const SB_KEY = "{SUPABASE_KEY}";
function esc(s) {{
  return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));
}}
function paras(text) {{
  return String(text || "").split(/\\n\\s*\\n/).map(p => p.trim()).filter(Boolean)
    .map(p => "<p>" + esc(p).replace(/\\n/g, "<br>") + "</p>").join("");
}}
function fmtDate(d) {{
  return d ? new Date(d).toLocaleDateString("en-GB", {{ day: "numeric", month: "long", year: "numeric" }}) : "";
}}
async function sbFetch(path) {{
  const res = await fetch(SB_URL + "/rest/v1/" + path, {{ headers: {{ apikey: SB_KEY }} }});
  if (!res.ok) throw new Error("Request failed");
  return res.json();
}}
{script}
</script>
</body>
</html>
"""


LIST_MAIN = """  <div class="container">
    <div class="blog-head">
      <h1>KAIF Blog</h1>
      <p>Coffee notes, brewing help and news from KAIF. &middot; مقالات عن القهوة والتحضير وأخبار KAIF</p>
    </div>
    <div id="list" class="blog-grid"></div>
    <p class="blog-msg" id="none" hidden>No posts yet. Check back soon.</p>
  </div>"""

LIST_JS = """
(async function () {
  const list = document.getElementById("list");
  const none = document.getElementById("none");
  try {
    const rows = await sbFetch("blogs?is_published=eq.true&select=slug,title,title_ar,excerpt,excerpt_ar,cover_url,published_at&order=published_at.desc");
    if (!rows.length) { none.hidden = false; return; }
    list.innerHTML = rows.map(p => `
      <a class="post-card" href="/blog/${esc(p.slug)}">
        ${p.cover_url ? `<img src="${esc(p.cover_url)}" alt="">` : ""}
        <div class="pc-body">
          <span class="date">${esc(fmtDate(p.published_at))}</span>
          <h2>${esc(p.title)}</h2>
          ${p.title_ar ? `<h2 dir="rtl" lang="ar">${esc(p.title_ar)}</h2>` : ""}
          <p>${esc(p.excerpt || "")}</p>
        </div>
      </a>`).join("");
  } catch (e) {
    none.textContent = "Sorry, the blog could not load. Please try again.";
    none.hidden = false;
  }
})();
"""

POST_MAIN = """  <div class="container">
    <article class="post" id="post">
      <p class="blog-msg">Loading…</p>
    </article>
  </div>"""

POST_JS = """
(async function () {
  const slug = location.pathname.replace(/^\\/blog\\//, "").replace(/\\/+$/, "");
  const box = document.getElementById("post");
  if (!slug) { box.innerHTML = '<p class="blog-msg">Post not found.</p>'; return; }
  try {
    const rows = await sbFetch("blogs?slug=eq." + encodeURIComponent(slug) + "&is_published=eq.true&select=*");
    if (!rows.length) {
      box.innerHTML = '<p class="blog-msg">Post not found. <a href="/blog/">Back to the blog</a></p>';
      document.title = "Post not found | KAIF";
      return;
    }
    const p = rows[0];
    document.title = p.title + " | KAIF";
    document.querySelector('meta[name="description"]').setAttribute("content", p.excerpt || p.title);
    box.innerHTML = `
      <div class="crumbs"><a href="/">KAIF</a> &rsaquo; <a href="/blog/">Blog</a> &rsaquo; ${esc(p.title)}</div>
      <span class="date">${esc(fmtDate(p.published_at))}</span>
      <h1>${esc(p.title)}</h1>
      ${p.excerpt ? `<p class="lead">${esc(p.excerpt)}</p>` : ""}
      ${p.cover_url ? `<img class="cover" src="${esc(p.cover_url)}" alt="">` : ""}
      <div class="body">${paras(p.body)}</div>
      ${p.body_ar ? `<div class="body body-ar" lang="ar" dir="rtl">
        ${p.title_ar ? `<h2>${esc(p.title_ar)}</h2>` : ""}
        ${p.excerpt_ar ? `<p class="lead">${esc(p.excerpt_ar)}</p>` : ""}
        ${paras(p.body_ar)}</div>` : ""}`;
  } catch (e) {
    box.innerHTML = '<p class="blog-msg">Sorry, this post could not load. Please try again.</p>';
  }
})();
"""

out = ROOT / "blog"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(
    page("KAIF Blog | Coffee notes and brewing help",
         "Coffee notes, brewing help and news from KAIF, a specialty coffee roaster in Egypt.",
         "https://kaifcoffee.net/blog/", LIST_MAIN, LIST_JS),
    encoding="utf-8")
(out / "post.html").write_text(
    page("KAIF Blog",
         "Read the latest coffee notes and brewing help from KAIF.",
         "https://kaifcoffee.net/blog/", POST_MAIN, POST_JS),
    encoding="utf-8")
print("wrote blog/index.html and blog/post.html")
