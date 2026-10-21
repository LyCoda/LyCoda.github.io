from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1]
data=sorted(json.loads((root/'content.json').read_text(encoding='utf-8')),key=lambda p:p['date'])
timeline=json.loads((root/'timeline.json').read_text(encoding='utf-8'))
by_slug={p['slug']:p for p in data}
E=html.escape
arrow='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
def link(href,label,cls='text-link'):
    return f'<a class="{cls}" href="{E(href)}"'+(' target="_blank" rel="noreferrer"' if href.startswith('http') else '')+f'>{label}{arrow}</a>'
def head(title,desc,prefix='',path=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Nate Chu</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f7f8fa"><link rel="canonical" href="https://lycoda.github.io/{path}"><meta property="og:title" content="{E(title)} | Nate Chu"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="https://lycoda.github.io/images/hero-original.png"><link rel="stylesheet" href="{prefix}fonts.css"><link rel="stylesheet" href="{prefix}theme.css"><script src="{prefix}main.js" defer></script></head>'''
def header(home=False):
    pre='' if home else '../index.html'
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="{pre}#top" aria-label="Nate Chu home"><svg class="brand-mark" viewBox="0 0 40 24" aria-hidden="true"><path d="M1 12h9l4-7 7 15 5-8h13"/></svg><span>Nate Chu<span class="brand-sub">Biomedical engineering</span></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button><nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(f'<a href="{pre}#{id}">{text}</a>' for id,text in NAV)}</nav></div></header>'''
NAV=[('about','About'),('academics','Academics'),('projects','Work'),('evolution','Evolution'),('archive','Archive'),('experience','Experience'),('contact','Contact')]
def footer():return f'<footer class="site-footer"><p>© 2026 Nate Chu</p><p>Biomedical engineering · London / Hong Kong</p>{link("#top","Back to top")}</footer>'
def paragraphs(items):return ''.join(f'<p>{E(p)}</p>' for p in items)
def section(s):
    body=paragraphs(s.get('paragraphs',[]))
    body+=''.join(f'<h3>{E(x["title"])}</h3><p>{E(x["text"])}</p>' for x in s.get('subsections',[]))
    if 'steps' in s:body+='<ol class="workflow">'+''.join(f'<li><strong>{E(a)}</strong><span>{E(b)}</span></li>' for a,b in s['steps'])+'</ol>'
    if 'table' in s:
        t=s['table'];body+='<div class="table-scroll" tabindex="0" role="region" aria-label="'+E(t['caption'])+'"><table><caption>'+E(t['caption'])+'</caption><thead><tr>'+''.join('<th scope="col">'+E(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join((f'<th scope="row">{E(x)}</th>' if i==0 else f'<td>{E(x)}</td>') for i,x in enumerate(row))+'</tr>' for row in t['rows'])+'</tbody></table></div>'
    if 'figure' in s:
        f=s['figure'];body+=f'<figure class="article-figure"><a href="../{f["src"]}" target="_blank" rel="noreferrer" aria-label="Open figure at full size"><img src="../{f["src"]}" alt="{E(f["alt"])}" loading="lazy"></a><figcaption>{E(f["caption"])}</figcaption></figure>'
    return f'<section id="{s["id"]}" class="article-section"><h2>{E(s["title"])}</h2>{body}{paragraphs(s.get("after",[]))}</section>'

def thread_of(slug):
    for t in timeline['threads']:
        slugs=[s.get('slug') for s in t['steps']]
        if slug in slugs:return t,slugs.index(slug)
    return None,None

def thread_nav(p):
    t,i=thread_of(p['slug'])
    if not t:return ''
    steps=t['steps']
    items=''
    for j,st in enumerate(steps):
        q=by_slug.get(st.get('slug'))
        name=E(q['name'] if q else st['name']);year=E(q['year'] if q else st['year'])
        href=(q['slug']+'.html') if q else '../index.html'+st['href']
        cur=' aria-current="step"' if j==i else ''
        items+=f'<li{cur}><a href="{href}"><span>{year}</span>{name}</a></li>'
    return f'<nav class="thread-nav wrap" aria-label="{E(t["title"])} thread"><p><span>Part of the thread</span><strong>{E(t["title"])}</strong> {E(t["subtitle"])}</p><ol>{items}</ol></nav>'

for i,p in enumerate(data):
    nextp=data[(i+1)%len(data)]
    body=head(p['name'],p['summary'],'../','projects/'+p['slug']+'.html')+'<body class="case-page" id="top">'+header()+f'''<main id="main"><header class="case-header wrap">{link('../index.html#archive','All projects','back-link')}<p class="case-kicker">{E(p['stage'])} · {E(p['year'])}</p><h1>{E(p['title'])}</h1><p class="case-intro">{E(p['summary'])}</p><div class="case-meta"><div><span>My role</span><strong>{E(p['role'])}</strong></div><div><span>Context</span><strong>{E(p['institution'])}</strong></div><div><span>Project stage</span><strong>{E(p['status'])}</strong></div></div></header><div class="case-lead wrap"><figure class="case-image"><img src="../{p['image']}" alt="{E(p['alt'])}" width="640" height="440"></figure><div class="case-summary"><h2>At a glance</h2><p>{E(p['takeaway'])}</p><dl><dt>Tools &amp; methods</dt><dd>{E(p['tools'])}</dd></dl></div></div><div class="article-layout wrap"><aside class="article-nav"><nav aria-label="On this page"><p>In this project</p>{''.join(f'<a href="#{s["id"]}">{E(s["title"])}</a>' for s in p['sections'])}<a href="#sources">Project material</a></nav></aside><article class="article-body">{''.join(section(s) for s in p['sections'])}<section class="article-section resources" id="sources"><h2>Project material</h2>'''
    if p['resources']:body+='<ul>'+''.join(f'<li>{link(r["href"],E(r["label"]))}<span>{E(r["detail"])}</span></li>' for r in p['resources'])+'</ul>'
    else:body+=paragraphs([p['sourceNote']])
    body+=f'</section></article></div>{thread_nav(p)}<nav class="next-project wrap" aria-label="Project navigation"><span>Next project, in date order</span>{link(nextp["slug"]+".html",E(nextp["name"]))}{link("../index.html#archive","All projects","back-link")}</nav></main>'+footer()+'</body></html>'
    (root/'projects'/(p['slug']+'.html')).write_text(body,encoding='utf-8')

# ---------- homepage work sections ----------
def img(p,cls=''):
    fit=p.get('cardFit','contain')
    return f'<img class="fit-{fit}{cls}" src="{p["image"]}" alt="" loading="lazy" width="640" height="420">'

def recent():
    picks=[p for p in reversed(data) if p.get('featured')]+[p for p in reversed(data) if not p.get('featured')]
    picks=picks[:3]
    rows=''
    for n,p in enumerate(picks,1):
        rows+=f'''<article class="recent-item reveal"><a class="recent-link" href="projects/{p['slug']}.html"><span class="recent-index">{n:02d}</span><div class="recent-copy"><p class="eyebrow">{E(p['label'])} · {E(p['year'])}</p><h3>{E(p['title'])}</h3><p>{E(p['summary'])}</p><span class="text-link">Read the case study{arrow}</span></div><div class="recent-media">{img(p)}</div></a></article>'''
    return f'''<section class="work section" id="projects"><div class="wrap"><div class="section-heading"><h2>Recent work</h2><p>The latest projects, in depth.</p></div><div class="recent-list">{rows}</div></div></section>'''

def evolution():
    out=''
    for t in timeline['threads']:
        steps=''
        for st in t['steps']:
            q=by_slug.get(st.get('slug'))
            if q:href,year,name,label=f'projects/{q["slug"]}.html',q['year'],q['name'],q['label']
            else:href,year,name,label=st['href'],st['year'],st['name'],st['label']
            steps+=f'''<li class="thread-step reveal"><span class="thread-node" aria-hidden="true"></span><p class="thread-year">{E(year)}</p><p class="eyebrow">{E(label)}</p><h4><a href="{href}">{E(name)}</a></h4><dl><dt>Built</dt><dd>{E(st['built'])}</dd><dt>Reported</dt><dd>{E(st['reported'])}</dd></dl></li>'''
        out+=f'''<div class="thread" id="thread-{t['id']}"><div class="thread-head"><h3>{E(t['title'])}</h3><p>{E(t['subtitle'])}</p></div><ol class="thread-track" style="--steps:{len(t['steps'])}">{steps}</ol></div>'''
    solo=''.join(f'''<li class="reveal"><a href="projects/{by_slug[s]['slug']}.html"><p class="eyebrow">{E(by_slug[s]['label'])} · {E(by_slug[s]['year'])}</p><h4>{E(by_slug[s]['name'])}</h4><p>{E(by_slug[s]['summary'])}</p><span class="text-link">Learn more{arrow}</span></a></li>''' for s in timeline['standalone'])
    ecg='<svg class="evolution-trace" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40H360l18-22 22 52 24-74 22 66 16-22H690l14-14 18 34 20-50 20 44 12-14H1200"/></svg>'
    return f'''<section class="evolution section" id="evolution">{ecg}<div class="wrap"><div class="section-heading"><h2>How my work has evolved</h2><p>{E(timeline['intro'])}</p></div>{out}<div class="standalone"><div class="thread-head"><h3>Standalone projects</h3><p>Focused pieces that sit outside the two threads</p></div><ul>{solo}</ul></div></div></section>'''

def archive():
    years=sorted({p['year'] for p in data},reverse=True)
    groups=''
    for y in years:
        cards=''
        for p in sorted([p for p in data if p['year']==y],key=lambda p:p['date'],reverse=True):
            cards+=f'''<article class="archive-card reveal"><a href="projects/{p['slug']}.html"><div class="archive-media">{img(p)}</div><p class="eyebrow">{E(p['label'])}</p><h4>{E(p['name'])}</h4><p>{E(p['summary'])}</p><span class="text-link">Learn more{arrow}</span></a></article>'''
        groups+=f'<div class="archive-year"><h3>{y}</h3><div class="archive-grid">{cards}</div></div>'
    return f'<section class="archive section" id="archive"><div class="wrap"><div class="section-heading"><h2 class="spaced">Archive</h2><p>Every project, newest first.</p></div>{groups}</div></section>'

idx=root/'index.html';html_=idx.read_text(encoding='utf-8')
a,b='<!-- work:start -->','<!-- work:end -->'
i0,i1=html_.index(a)+len(a),html_.index(b)
idx.write_text(html_[:i0]+recent()+evolution()+archive()+html_[i1:],encoding='utf-8')
print(f'Rendered {len(data)} case studies and the homepage work sections.')
