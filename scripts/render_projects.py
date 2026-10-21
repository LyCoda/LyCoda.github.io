"""Render the case-study pages and the homepage work sections.

Reads content.json (one entry per project) and timeline.json (the
"How my work has evolved" threads), writes projects/<slug>.html and
replaces the block between <!-- work:start --> and <!-- work:end -->
in index.html. Standard library only.
"""
from pathlib import Path
import html
import json
import struct

root = Path(__file__).resolve().parents[1]
data = sorted(json.loads((root / 'content.json').read_text(encoding='utf-8')), key=lambda p: p['date'])
timeline = json.loads((root / 'timeline.json').read_text(encoding='utf-8'))
by_slug = {p['slug']: p for p in data}
E = html.escape
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
arrow = '<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
NAV = [('about', 'About'), ('academics', 'Academics'), ('projects', 'Work'), ('experience', 'Experience'), ('contact', 'Contact')]


# ---------- checks ----------
def check():
    """Fail loudly on content mistakes (run without python -O)."""
    placed = [s['slug'] for t in timeline['threads'] for s in t['steps'] if 'slug' in s] + timeline['standalone']
    for slug in placed:
        assert slug in by_slug, f'timeline.json names an unknown project: {slug}'
    dupes = {s for s in placed if placed.count(s) > 1}
    assert not dupes, f'projects placed more than once in timeline.json: {dupes}'
    missing = set(by_slug) - set(placed)
    assert not missing, f'projects missing from timeline.json: {missing}'
    for t in timeline['threads']:
        for s in t['steps']:
            if 'slug' not in s:
                for key in ('href', 'year', 'name', 'label'):
                    assert key in s, f'non-project step in {t["id"]} needs "{key}"'
    for p in data:
        for key in ('image', 'thumb'):
            assert key not in p or (root / p[key]).exists(), f'missing {key} for {p["slug"]}: {p.get(key)}'


def image_size(path):
    """Width and height of a PNG or JPEG, without third-party libraries."""
    b = (root / path).read_bytes()
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', b[16:24])
    i = 2
    while i < len(b):
        marker, length = b[i + 1], struct.unpack('>H', b[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack('>HH', b[i + 5:i + 9])
            return w, h
        i += 2 + length
    return 640, 420


def month(p):
    y, m = p['date'].split('-')
    return f'{MONTHS[int(m) - 1]} {y}'


# ---------- shared page parts ----------
def link(href, label, cls='text-link'):
    ext = ' target="_blank" rel="noreferrer"' if href.startswith('http') else ''
    return f'<a class="{cls}" href="{E(href)}"{ext}>{label}{arrow}</a>'


def head(title, desc, prefix='', path='', image='images/hero-original.png'):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)} | Nate Chu</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f7f8fa">'
            f'<link rel="canonical" href="https://lycoda.github.io/{path}"><meta property="og:title" content="{E(title)} | Nate Chu">'
            f'<meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">'
            f'<meta property="og:image" content="https://lycoda.github.io/{image}">'
            f'<script>if("IntersectionObserver" in window)document.documentElement.classList.add("js")</script>'
            f'<link rel="stylesheet" href="{prefix}fonts.css"><link rel="stylesheet" href="{prefix}theme.css"><script src="{prefix}main.js" defer></script></head>')


def header():
    nav = ''.join(f'<a href="../index.html#{id}">{text}</a>' for id, text in NAV)
    return ('<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner">'
            '<a class="brand" href="../index.html#top" aria-label="Nate Chu home"><svg class="brand-mark" viewBox="0 0 40 24" aria-hidden="true"><path d="M1 12h9l4-7 7 15 5-8h13"/></svg>'
            '<span>Nate Chu<span class="brand-sub">Biomedical engineering</span></span></a>'
            '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button>'
            f'<nav class="site-nav" id="site-nav" aria-label="Main navigation">{nav}</nav></div></header>')


def footer():
    return f'<footer class="site-footer"><p>© 2026 Nate Chu</p><p>Biomedical engineering · London / Hong Kong</p>{link("#top", "Back to top")}</footer>'


def paragraphs(items):
    return ''.join(f'<p>{E(p)}</p>' for p in items)


def section(s):
    body = paragraphs(s.get('paragraphs', []))
    body += ''.join(f'<h3>{E(x["title"])}</h3><p>{E(x["text"])}</p>' for x in s.get('subsections', []))
    if 'steps' in s:
        body += '<ol class="workflow">' + ''.join(f'<li><strong>{E(a)}</strong><span>{E(b)}</span></li>' for a, b in s['steps']) + '</ol>'
    if 'table' in s:
        t = s['table']
        rows = ''.join('<tr>' + ''.join((f'<th scope="row">{E(x)}</th>' if i == 0 else f'<td>{E(x)}</td>') for i, x in enumerate(row)) + '</tr>' for row in t['rows'])
        body += (f'<div class="table-scroll" tabindex="0" role="region" aria-label="{E(t["caption"])}"><table><caption>{E(t["caption"])}</caption>'
                 '<thead><tr>' + ''.join(f'<th scope="col">{E(x)}</th>' for x in t['headers']) + f'</tr></thead><tbody>{rows}</tbody></table></div>')
    if 'figure' in s:
        f = s['figure']
        w, h = image_size(f['src'])
        body += (f'<figure class="article-figure"><a href="../{f["src"]}" target="_blank" rel="noreferrer" aria-label="Open figure at full size">'
                 f'<img src="../{f["src"]}" alt="{E(f["alt"])}" width="{w}" height="{h}" loading="lazy"></a><figcaption>{E(f["caption"])}</figcaption></figure>')
    return f'<section id="{s["id"]}" class="article-section"><h2>{E(s["title"])}</h2>{body}{paragraphs(s.get("after", []))}</section>'


def thread_of(slug):
    for t in timeline['threads']:
        slugs = [s.get('slug') for s in t['steps']]
        if slug in slugs:
            return t, slugs.index(slug)
    return None, None


def thread_nav(p):
    t, i = thread_of(p['slug'])
    if not t:
        return ''
    items = ''
    for j, st in enumerate(t['steps']):
        q = by_slug.get(st.get('slug'))
        name, when = (q['name'], month(q)) if q else (st['name'], st['year'])
        href = f'{q["slug"]}.html' if q else '../index.html' + st['href']
        cur = ' aria-current="page"' if j == i else ''
        items += f'<li><a href="{href}"{cur}><span>{E(when)}</span>{E(name)}</a></li>'
    return (f'<nav class="thread-nav wrap" aria-label="{E(t["title"])} thread"><p><span>Part of the thread · step {i + 1} of {len(t["steps"])}</span>'
            f'<strong>{E(t["title"])}</strong> · {E(t["subtitle"])}</p><ol>{items}</ol></nav>')


def case_page(i, p):
    prev_p = data[i - 1] if i > 0 else None
    next_p = data[i + 1] if i + 1 < len(data) else None
    w, h = image_size(p['image'])
    fit = p.get('cardFit', 'contain')
    toc = ''.join(f'<a href="#{s["id"]}">{E(s["title"])}</a>' for s in p['sections'])
    if p['resources']:
        material = '<ul>' + ''.join(f'<li>{link(r["href"], E(r["label"]))}<span>{E(r["detail"])}</span></li>' for r in p['resources']) + '</ul>'
    else:
        material = paragraphs([p['sourceNote']])
    pager = ''
    if prev_p:
        pager += f'<a class="pager-link" href="{prev_p["slug"]}.html"><span>Earlier · {E(month(prev_p))}</span>{E(prev_p["name"])}</a>'
    if next_p:
        pager += f'<a class="pager-link pager-next" href="{next_p["slug"]}.html"><span>Later · {E(month(next_p))}</span>{E(next_p["name"])}</a>'
    return '\n'.join([
        head(p['name'], p['summary'], '../', f'projects/{p["slug"]}.html', p['image']),
        '<body class="case-page" id="top">', header(),
        '<main id="main">',
        f'<header class="case-header wrap">{link("../index.html#archive", "All projects", "back-link")}<p class="case-kicker">{E(p["label"])} · {E(month(p))}</p>'
        f'<h1>{E(p["title"])}</h1><p class="case-intro">{E(p["summary"])}</p>'
        f'<div class="case-meta"><div><span>My role</span><strong>{E(p["role"])}</strong></div><div><span>Context</span><strong>{E(p["institution"])}</strong></div>'
        f'<div><span>Project stage</span><strong>{E(p["status"])}</strong></div></div></header>',
        f'<div class="case-lead wrap"><figure class="case-image case-image-{fit}"><img src="../{p["image"]}" alt="{E(p["alt"])}" width="{w}" height="{h}"></figure>'
        f'<div class="case-summary"><h2>At a glance</h2><p>{E(p["takeaway"])}</p><dl><dt>Tools &amp; methods</dt><dd>{E(p["tools"])}</dd></dl></div></div>',
        f'<div class="article-layout wrap"><aside class="article-nav"><nav aria-label="On this page"><p>In this project</p>{toc}<a href="#sources">Project material</a></nav></aside>',
        '<article class="article-body">' + ''.join(section(s) for s in p['sections']),
        f'<section class="article-section resources" id="sources"><h2>Project material</h2>{material}</section></article></div>',
        thread_nav(p),
        f'<nav class="next-project wrap" aria-label="Project navigation"><span>More projects, in date order</span><div class="pager">{pager}</div>{link("../index.html#archive", "All projects", "back-link")}</nav>',
        '</main>', footer(), '</body></html>', ''])


# ---------- homepage work sections ----------
def card_img(p):
    """Card thumbnail: a card-scale image when one exists, otherwise the cover image."""
    src = p.get('thumb', p['image'])
    fit = p.get('thumbFit', 'cover') if 'thumb' in p else p.get('cardFit', 'contain')
    w, h = image_size(src)
    return f'<img class="fit-{fit}" src="{src}" alt="" loading="lazy" width="{w}" height="{h}">'


def featured():
    return sorted([p for p in data if p.get('featured')], key=lambda p: p['featured'])


def recent():
    rows = []
    for p in featured():
        tid = f'recent-{p["slug"]}'
        rows.append(f'<article class="recent-item reveal"><a class="recent-link" href="projects/{p["slug"]}.html" aria-labelledby="{tid}">'
                    f'<div class="recent-media">{card_img(p)}</div><div class="recent-copy"><p class="eyebrow">{E(p["label"])} · {E(month(p))}</p>'
                    f'<h3 id="{tid}">{E(p["title"])}</h3><p>{E(p["summary"])}</p><span class="text-link">Read the case study{arrow}</span></div></a></article>')
    return ('<section class="work section" id="projects"><div class="wrap"><div class="section-heading"><h2>Selected work</h2>'
            '<p>Three projects to start with.</p></div><div class="recent-list">\n' + '\n'.join(rows) + '\n</div></div></section>')


def evolution():
    threads = []
    for t in timeline['threads']:
        steps = []
        for st in t['steps']:
            q = by_slug[st['slug']] if 'slug' in st else None
            href, when, name, label = (f'projects/{q["slug"]}.html', month(q), q['name'], q['label']) if q else (st['href'], st['year'], st['name'], st['label'])
            steps.append(f'<li class="thread-step reveal"><span class="thread-node" aria-hidden="true"></span><p class="thread-year">{E(when)}</p>'
                         f'<p class="eyebrow">{E(label)}</p><h4><a href="{href}">{E(name)}</a></h4>'
                         f'<dl><dt>Built</dt><dd>{E(st["built"])}</dd><dt>Evidence</dt><dd>{E(st["evidence"])}</dd></dl></li>')
        threads.append(f'<div class="thread" id="thread-{t["id"]}"><div class="thread-head"><h3>{E(t["title"])}</h3><p>{E(t["subtitle"])}</p></div>'
                       f'<ol class="thread-track" style="--steps:{len(t["steps"])}">\n' + '\n'.join(steps) + '\n</ol></div>')
    solo = []
    for s in timeline['standalone']:
        p = by_slug[s]
        tid = f'solo-{p["slug"]}'
        solo.append(f'<li class="reveal"><a href="projects/{p["slug"]}.html" aria-labelledby="{tid}"><p class="eyebrow">{E(p["label"])} · {E(month(p))}</p>'
                    f'<h4 id="{tid}">{E(p["name"])}</h4><p>{E(p["summary"])}</p><span class="text-link">Learn more{arrow}</span></a></li>')
    trace = ('<svg class="evolution-trace" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M0 40H360l18-22 22 52 24-74 22 66 16-22H690l14-14 18 34 20-50 20 44 12-14H1200"/></svg>')
    return (f'<section class="evolution section" id="evolution">{trace}<div class="wrap"><div class="section-heading"><h2>How my work has evolved</h2>'
            f'<p>{E(timeline["intro"])}</p></div>\n' + '\n'.join(threads) +
            '\n<div class="standalone"><div class="thread-head"><h3>Standalone projects</h3><p>Focused pieces that sit outside the two threads</p></div>'
            '<ul>\n' + '\n'.join(solo) + '\n</ul></div></div></section>')


def archive():
    shown = {p['slug'] for p in featured()}
    rest = [p for p in data if p['slug'] not in shown]
    groups = []
    for y in sorted({p['year'] for p in rest}, reverse=True):
        cards = []
        for p in sorted([p for p in rest if p['year'] == y], key=lambda p: p['date'], reverse=True):
            tid = f'archive-{p["slug"]}'
            cards.append(f'<article class="archive-card reveal"><a href="projects/{p["slug"]}.html" aria-labelledby="{tid}"><div class="archive-media">{card_img(p)}</div>'
                         f'<p class="eyebrow">{E(p["label"])} · {E(month(p))}</p><h4 id="{tid}">{E(p["name"])}</h4><p>{E(p["summary"])}</p>'
                         f'<span class="text-link">Learn more{arrow}</span></a></article>')
        groups.append(f'<div class="archive-year"><h3>{y}</h3><div class="archive-grid">\n' + '\n'.join(cards) + '\n</div></div>')
    return ('<section class="archive section" id="archive"><div class="wrap"><div class="section-heading"><h2 class="spaced">Archive</h2>'
            '<p>Everything else, newest first.</p></div>\n' + '\n'.join(groups) + '\n</div></section>')


def main():
    check()
    for i, p in enumerate(data):
        (root / 'projects' / f'{p["slug"]}.html').write_text(case_page(i, p), encoding='utf-8')
    idx = root / 'index.html'
    page = idx.read_text(encoding='utf-8')
    a, b = '<!-- work:start -->', '<!-- work:end -->'
    i0, i1 = page.index(a) + len(a), page.index(b)
    idx.write_text(page[:i0] + '\n' + recent() + '\n' + evolution() + '\n' + archive() + '\n' + page[i1:], encoding='utf-8')
    print(f'Rendered {len(data)} case studies and the homepage work sections.')


if __name__ == '__main__':
    main()
