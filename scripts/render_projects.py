from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'content.json').read_text(encoding='utf-8'))
E=html.escape
arrow='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
def link(href,label,cls='text-link'):
    return f'<a class="{cls}" href="{E(href)}"'+(' target="_blank" rel="noreferrer"' if href.startswith('http') else '')+f'>{label}{arrow}</a>'
def head(title,desc,prefix='',path=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Nate Chu</title><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#f7f8fa"><link rel="canonical" href="https://lycoda.github.io/{path}"><meta property="og:title" content="{E(title)} | Nate Chu"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="https://lycoda.github.io/images/hero-original.png"><link rel="stylesheet" href="{prefix}fonts.css"><link rel="stylesheet" href="{prefix}theme.css"><script src="{prefix}main.js" defer></script></head>'''
def header(home=False):
    pre='' if home else '../index.html'
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="{pre}#top" aria-label="Nate Chu home"><svg class="brand-mark" viewBox="0 0 40 24" aria-hidden="true"><path d="M1 12h9l4-7 7 15 5-8h13"/></svg><span>Nate Chu<span class="brand-sub">Biomedical engineering</span></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu</button><nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(f'<a href="{pre}#{id}">{text}</a>' for id,text in [('about','About'),('academics','Academics'),('projects','Projects'),('experience','Experience'),('contact','Contact')])}</nav></div></header>'''
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
for i,p in enumerate(data):
    nextp=data[(i+1)%len(data)]
    body=head(p['name'],p['summary'],'../','projects/'+p['slug']+'.html')+'<body class="case-page" id="top">'+header()+f'''<main id="main"><header class="case-header wrap">{link('../index.html#projects','All projects','back-link')}<h1>{E(p['title'])}</h1><p class="case-intro">{E(p['summary'])}</p><div class="case-meta"><div><span>My role</span><strong>{E(p['role'])}</strong></div><div><span>Context</span><strong>{E(p['institution'])}</strong></div><div><span>Project stage</span><strong>{E(p['status'])}</strong></div></div></header><div class="case-lead wrap"><figure class="case-image"><img src="../{p['image']}" alt="{E(p['alt'])}" width="640" height="440"></figure><div class="case-summary"><h2>At a glance</h2><p>{E(p['takeaway'])}</p><dl><dt>Tools &amp; methods</dt><dd>{E(p['tools'])}</dd></dl></div></div><div class="article-layout wrap"><aside class="article-nav"><nav aria-label="On this page"><p>In this project</p>{''.join(f'<a href="#{s["id"]}">{E(s["title"])}</a>' for s in p['sections'])}<a href="#sources">Project material</a></nav></aside><article class="article-body">{''.join(section(s) for s in p['sections'])}<section class="article-section resources" id="sources"><h2>Project material</h2>'''
    if p['resources']:body+='<ul>'+''.join(f'<li>{link(r["href"],E(r["label"]))}<span>{E(r["detail"])}</span></li>' for r in p['resources'])+'</ul>'
    else:body+=paragraphs([p['sourceNote']])
    body+=f'</section></article></div><nav class="next-project wrap" aria-label="Project navigation"><span>Next project</span>{link(nextp["slug"]+".html",E(nextp["name"]))}{link("../index.html#projects","All projects","back-link")}</nav></main>'+footer()+'</body></html>'
    (root/'projects'/(p['slug']+'.html')).write_text(body,encoding='utf-8')
print('Rendered four static case studies from content.json.')
