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
NAV = [('about', 'About'), ('experience', 'Experience'), ('education', 'Education'), ('projects', 'Projects'), ('contact', 'Contact')]
CV = 'Long-Yin-Chu-CV.pdf'


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
        for key in ('image',):
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
    nav += f'<a class="nav-cv" href="../{CV}">CV<span class="visually-hidden"> (PDF)</span></a>'
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


def tldr(p):
    """Skim view built only from text already on the page: the card question and answer, the takeaway, tools and section titles."""
    q = p['card']['quiz']
    parts = ''.join(f'<li><a href="#{s["id"]}">{E(s["title"])}</a></li>' for s in p['sections'])
    return (f'<section class="tldr wrap" id="tldr" aria-labelledby="tldr-title"><h2 id="tldr-title">TL;DR</h2>'
            f'<div class="tldr-qa"><div><p class="tldr-label">The question</p><p class="tldr-q">{E(q["question"])}</p></div>'
            f'<div><p class="tldr-label">What I found</p><p class="tldr-a">{E(q["reveal"])}</p></div></div>'
            f'<div class="tldr-body"><div><p class="tldr-label">What I did</p><p>{E(p["takeaway"])}</p>'
            f'<p class="tldr-label">Tools &amp; methods</p><p class="tldr-tools">{E(p["tools"])}</p></div>'
            f'<div><p class="tldr-label">The full story, in {len(p["sections"])} parts</p><ol class="tldr-parts">{parts}</ol></div></div></section>')


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
        f'<div><span>Project stage</span><strong>{E(p["status"])}</strong></div></div>'
        '<div class="read-mode" role="group" aria-label="How much to read"><button type="button" data-mode="full" aria-pressed="true">Full story</button>'
        '<button type="button" data-mode="tldr" aria-pressed="false">TL;DR</button></div></header>',
        tldr(p),
        f'<div class="case-lead wrap"><figure class="case-image case-image-{fit}"><img src="../{p["image"]}" alt="{E(p["alt"])}" width="{w}" height="{h}"></figure>'
        f'<div class="case-summary"><h2>At a glance</h2><p>{E(p["takeaway"])}</p><dl><dt>Tools &amp; methods</dt><dd>{E(p["tools"])}</dd></dl></div></div>',
        f'<div class="article-layout wrap"><aside class="article-nav"><nav aria-label="On this page"><p>In this project</p>{toc}<a href="#sources">Project material</a></nav></aside>',
        '<article class="article-body">' + ''.join(section(s) for s in p['sections']),
        f'<section class="article-section resources" id="sources"><h2>Project material</h2>{material}</section></article></div>',
        thread_nav(p),
        f'<nav class="next-project wrap" aria-label="Project navigation"><span>More projects, in date order</span><div class="pager">{pager}</div>{link("../index.html#archive", "All projects", "back-link")}</nav>',
        '</main>', footer(), '</body></html>', ''])


# ---------- homepage work sections ----------
THREAD_NAMES = {'biosignals': 'Biosignals', 'translation': 'Medtech translation', 'surgical-ai': 'Surgical AI'}
UNITS = {'tall': 6, 'reg': 4}  # grid rows each card spans on wider screens


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
        threads.append(f'<div class="thread" id="thread-{t["id"]}"><div class="thread-head"><h4 class="thread-title">{E(t["title"])}</h4><p>{E(t["subtitle"])}</p></div>'
                       f'<ol class="thread-track" style="--steps:{len(t["steps"])}">\n' + '\n'.join(steps) + '\n</ol></div>')
    solo = ' and '.join(f'<a href="projects/{s}.html">{E(by_slug[s]["name"])}</a>' for s in timeline['standalone'])
    trace = ('<svg class="evolution-trace" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M0 40H360l18-22 22 52 24-74 22 66 16-22H690l14-14 18 34 20-50 20 44 12-14H1200"/></svg>')
    return (f'<div class="evolution" id="evolution">{trace}<div class="sub-heading"><h3>How my work has evolved</h3>'
            f'<p>{E(timeline["intro"])}</p></div>\n' + '\n'.join(threads) +
            f'\n<p class="standalone-note">Standing on their own: {solo}. Both are in the archive below.</p></div>')


def masonry(cards, cols):
    """Place cards newest-first into the shortest column; stretch each column's last card so the grid ends level."""
    heights, place, last = [1] * cols, {}, {}
    for p in cards:
        c = heights.index(min(heights))
        span = UNITS[p['card']['size']]
        place[p['slug']] = [c + 1, heights[c], span]
        heights[c] += span
        last[c] = p['slug']
    top = max(heights)
    for c, slug in last.items():
        place[slug][2] += top - heights[c]
    return place


def art(p):
    c = p['card']
    kind = c['art']
    if kind in ('photo', 'product', 'logo', 'circuit', 'render'):
        w, h = image_size(c['src'])
        pos = f' style="object-position:{c["pos"]}"' if 'pos' in c else ''
        img = f'<img class="vc-img vc-{kind}" src="{c["src"]}" alt="" loading="lazy" width="{w}" height="{h}"{pos}>'
        if 'loop' in c:
            # A short turntable video that plays only while the card is on screen; main.js picks
            # the .webm twin when the browser plays VP9 and falls back to the .mp4 (Safari).
            img += (f'<video class="vc-loop" data-src="{c["loop"]}" muted loop playsinline preload="none" '
                    f'aria-hidden="true" tabindex="-1"{pos}></video>')
        if 'steps' in c:
            img += '<ol class="vc-steps" aria-hidden="true">' + ''.join(f'<li style="--i:{i}">{E(t)}</li>' for i, t in enumerate(c['steps'])) + '</ol>'
        return img
    if kind == 'fnirs':
        # Illustrative oxy/deoxy-haemoglobin style curves, not study data.
        waves = ''.join(f'<path class="w{i}" d="M0 {150 + i * 26}' + ''.join(f' Q{x + 25} {150 + i * 26 - (38 - i * 6) * (1 if (x // 50) % 2 else -1)} {x + 50} {150 + i * 26}' for x in range(0, 600, 50)) + '"/>' for i in range(5))
        return f'<svg class="vc-svg vc-waves" viewBox="0 0 600 340" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{waves}</svg>'
    if kind == 'ce':
        q = p['card']['quiz']
        lit = q['options'][q['answer']].removeprefix('Class ')
        items = ''.join(f'<li{" class=\"is-answer\"" if k == lit else ""}>{k}</li>' for k in ('I', 'IIa', 'IIb', 'III'))
        return f'<ol class="vc-classes" aria-hidden="true">{items}</ol>'
    if kind == 'workflow':
        # Seven phases, as in Cholec80; widths are illustrative.
        widths = [8, 22, 10, 26, 9, 15, 10]
        bars = ''.join(f'<span style="--w:{w};--i:{i}"></span>' for i, w in enumerate(widths))
        return (f'<div class="vc-flow" aria-hidden="true"><div class="vc-flow-frame"><i></i><i></i><i></i></div>'
                f'<div class="vc-flow-bar">{bars}<b class="vc-playhead"></b></div><p>Phase 1 … 7 · time remaining ?</p></div>')
    if kind == 'sds':
        items = [('01', 'Ultrasound', 'image quality'), ('02', 'Skill + CT', 'classification'), ('03', 'ECG beats', 'clustering')]
        cells = ''.join(f'<li style="--i:{i}"><span>{n}</span><strong>{a}</strong><em>{b}</em></li>' for i, (n, a, b) in enumerate(items))
        return f'<ol class="vc-sds" aria-hidden="true">{cells}</ol>'
    raise ValueError(f'unknown card art: {kind}')


def sandbox(q):
    """Optional try-it-yourself widget shown above the answer chips (needs JavaScript)."""
    if q.get('sandbox') != 'gates':
        return ''
    return ('<div class="vc-gates" role="group" aria-label="Logic gate sandbox">'
            '<div class="vc-ins"><button type="button" class="vc-in" aria-pressed="false">A <b>0</b></button>'
            '<button type="button" class="vc-in" aria-pressed="false">B <b>0</b></button></div>'
            '<span class="vc-wire" aria-hidden="true"></span>'
            '<button type="button" class="vc-gate" aria-label="Gate: AND. Click to change.">AND</button>'
            '<span class="vc-wire" aria-hidden="true"></span>'
            '<output class="vc-lamp" aria-live="polite"><i aria-hidden="true"></i><span>Out <b>0</b></span></output>'
            '<p class="vc-gate-hint">Tap A, B and the gate to try it</p></div>')


def quiz(p, tid):
    """Guess-first panel: a question, answer chips, then the answer and a link to the case study."""
    q = p['card']['quiz']
    opts = ''.join(f'<button type="button" class="vc-opt" data-correct="{str(i == q["answer"]).lower()}">{E(o)}</button>'
                   for i, o in enumerate(q['options']))
    return (f'<div class="vc-quiz"><p class="vc-q">{E(q["question"])}</p>{sandbox(q)}'
            f'<div class="vc-opts" role="group" aria-label="Your guess">{opts}</div>'
            f'<div class="vc-reveal" aria-live="polite"><p><span class="vc-verdict"></span>{E(q["reveal"])}</p></div>'
            f'<a class="vc-btn" href="projects/{p["slug"]}.html" aria-describedby="{tid}">See how I found out</a></div>')


def archive():
    cards = sorted(data, key=lambda p: p['date'], reverse=True)
    p3, p2 = masonry(cards, 3), masonry(cards, 2)
    out = []
    for p in cards:
        c = p['card']
        tid = f'vc-{p["slug"]}'
        c3, r3, s3 = p3[p['slug']]
        c2, r2, s2 = p2[p['slug']]
        out.append(f'<article class="vc vc-{c["theme"]} vc-{c["size"]} vc-art-{c["art"]} reveal" data-thread="{c["thread"]}" '
                   f'style="--c3:{c3};--r3:{r3};--s3:{s3};--c2:{c2};--r2:{r2};--s2:{s2}">'
                   f'<div class="vc-art">{art(p)}</div><span class="vc-glare" aria-hidden="true"></span>'
                   f'<div class="vc-top"><p class="vc-eyebrow">{E(c["eyebrow"])}</p>'
                   f'<h3 id="{tid}"><a class="vc-link" href="projects/{p["slug"]}.html">{E(c["title"])}</a></h3></div>'
                   f'{quiz(p, tid)}</article>')
    chips = '<button type="button" aria-pressed="true" data-filter="all">All</button>' + ''.join(
        f'<button type="button" aria-pressed="false" data-filter="{k}">{v}</button>' for k, v in THREAD_NAMES.items())
    return (f'<div class="vault" id="archive"><div class="vault-head"><div><h3 class="spaced">Archive</h3>'
            f'<p class="vault-intro">Every project starts with a question. Guess the answer, or switch on TL;DR to skim them all.'
            f' <span class="vault-score" hidden>You have guessed <b>0</b> of {len(cards)}, <b>0</b> right.</span></p></div>'
            f'<div class="vault-tools"><button type="button" class="vault-tldr" aria-pressed="false" title="Show every answer without guessing">TL;DR</button>'
            f'<div class="vault-filter" role="group" aria-label="Filter projects">{chips}</div></div></div>'
            f'<div class="vault-grid">\n' + '\n'.join(out) + '\n</div></div>')


def projects_section():
    return ('<section class="work section" id="projects"><div class="wrap"><div class="section-heading"><h2>Projects</h2>'
            '<p>From Year 2 labs to an MSc dissertation.</p></div>\n' + evolution() + '\n' + archive() + '\n</div></section>')


def main():
    check()
    for p in data:
        assert 'card' in p and p['card']['size'] in UNITS and p['card']['thread'] in THREAD_NAMES, f'bad card for {p["slug"]}'
        assert 'src' not in p['card'] or (root / p['card']['src']).exists(), f'missing card image for {p["slug"]}'
        if 'loop' in p['card']:
            for ext in ('.mp4', '.webm'):
                assert (root / p['card']['loop']).with_suffix(ext).exists(), f'missing loop video ({ext}) for {p["slug"]}'
    for i, p in enumerate(data):
        (root / 'projects' / f'{p["slug"]}.html').write_text(case_page(i, p), encoding='utf-8')
    idx = root / 'index.html'
    page = idx.read_text(encoding='utf-8')
    a, b = '<!-- work:start -->', '<!-- work:end -->'
    i0, i1 = page.index(a) + len(a), page.index(b)
    idx.write_text(page[:i0] + '\n' + projects_section() + '\n' + page[i1:], encoding='utf-8')
    print(f'Rendered {len(data)} case studies and the homepage projects section.')


if __name__ == '__main__':
    main()
