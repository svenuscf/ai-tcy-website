"""Build the private design preview from frozen, auditable Wix HTML snapshots.

No network requests. Original text and anchor targets remain in source components.
Added interface text lives only in templates, outside data-source-id containers.
"""
from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
from datetime import datetime
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
CURRENT_YEAR = datetime.now().year
OUT = ROOT / 'site'
MEDIA = json.loads((ROOT/'inventory/media-manifest.json').read_text())
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
ROUTES = ['home', 'compositions', 'reconstruction', 'cds-and-books', 'academic']
LABELS = {
    'zh': ['首頁', '創作樂曲', '打譜', '唱片書籍', '論文'],
    'en': ['Home', 'Compositions', 'Reconstructions', 'CDs and Books', 'Academic Papers'],
}
# Publication years checked against the full bibliographies, not conference dates
# or dates of the historic source under discussion. IDs are shared across languages.
YEARS = [2025,2025,2024,2023,2023,2023,2023,2023,2023,2022,2021,2021,
         2020,2020,2020,2020,2020,2019,2019,2019,2018,2018,2017,2017,
         2016,2016,2016,2015,2015,2015,2014,2014,2013,2013,2012,
         2011,2011,2011,2010,2010,2010,2009,2007,2005,2002,2001,2000,1999,1998]

@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    @property
    def text(self):
        return ''.join(n if isinstance(n, str) else n.text for n in self.children)

def visible(text):
    return text.replace('\u200b', '').replace('\xa0', ' ').strip()

class SourceParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('data-testid') == 'richTextElement':
            assert self.active is None
            self.active = Node(tag, attrs)
            self.stack = [self.active]
        elif self.active is not None:
            node = Node(tag, attrs)
            self.stack[-1].children.append(node)
            if tag not in VOID:
                self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.active is not None:
            self.stack[-1].children.append(data)

    def handle_endtag(self, tag):
        if self.active is not None:
            assert self.stack[-1].tag == tag, (self.stack[-1].tag, tag)
            self.stack.pop()
            if not self.stack:
                self.blocks.append(self.active)
                self.active = None

def render(node):
    if isinstance(node, str):
        return escape(node)
    tag = node.tag
    if tag in {'h1','h2','h3','h4','h5','h6'}:
        tag = 'p'
    attrs = ''
    if tag == 'a' and not node.attrs.get('href'):
        tag = 'span'
    if tag == 'a':
        href = node.attrs.get('href', '')
        if not href.startswith(('https://', 'http://', 'mailto:', '#', '/')):
            raise ValueError(f'Unexpected source link: {href}')
        original = href
        parsed = urlsplit(href)
        if parsed.netloc in {'www.tsechunyan.com','tsechunyan.com'} and not parsed.query and not parsed.fragment:
            path = parsed.path.rstrip('/')
            if path in {'','/en'} or path in {f'/{r}' for r in ROUTES[1:]} | {f'/en/{r}' for r in ROUTES[1:]}:
                href = path + '/'
        attrs = f' href="{escape(href, quote=True)}" data-original-href="{escape(original, quote=True)}"'
        if node.attrs.get('target') == '_blank' and href == original:
            attrs += ' target="_blank" rel="noopener noreferrer"'
    elif tag not in {'p','h1','h2','h3','h4','h5','h6','span','em','strong','b','i','u','br','sup','sub','ul','ol','li'}:
        tag = 'span'
    classes = []
    if not visible(node.text) and tag not in VOID:
        classes.append('source-spacer')
    style = node.attrs.get('style', '').replace(' ', '')
    if 'font-style:italic' in style:
        classes.append('italic')
    if 'font-weight:bold' in style or 'font-weight:700' in style:
        classes.append('bold')
    if classes:
        attrs += f' class="{" ".join(classes)}"'
    if tag in VOID:
        return f'<{tag}{attrs}>'
    return f'<{tag}{attrs}>' + ''.join(render(n) for n in node.children) + f'</{tag}>'

def fragment(nodes):
    return ''.join(render(n) for n in nodes)

def source(node, children=None, extra=''):
    content = fragment(node.children) if children is None else children
    if node.attrs['id'] == 'comp-kyw9tprf':
        content = content.replace(
            '© 2022',
            f'© 2022–<span data-current-year>{CURRENT_YEAR}</span>',
        )  # Owner-approved rolling copyright range.
    heading = ' role="heading" aria-level="1"' if extra in {'home-title','collection-title'} else ''
    return f'<div class="source {extra}" data-source-id="{node.attrs["id"]}"{heading}>{content}</div>'

def url(lang, route='home'):
    return ('/en' if lang == 'en' else '') + ('/' if route == 'home' else f'/{route}/')

def pair(a, b, lang):
    return a if lang == 'zh' else b

def motif():
    return '<div class="strings" aria-hidden="true">' + ''.join(f'<i style="--n:{n}"></i>' for n in range(7)) + '<span class="string-dot dot-one"></span><span class="string-dot dot-two"></span><span class="string-dot dot-three"></span></div>'

def shell(lang, route, body):
    label = LABELS[lang][ROUTES.index(route)]
    name = pair('謝俊仁', 'TSE Chun-Yan', lang)
    other = 'en' if lang == 'zh' else 'zh'
    nav = ''.join(f'<a href="{url(lang,r)}"'+(' aria-current="page"' if route == r else '')+f'>{t}</a>' for r,t in zip(ROUTES,LABELS[lang]))
    return f'''<!doctype html>
<html lang="{'zh-Hant' if lang == 'zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{label} · {name}</title><link rel="stylesheet" href="/assets/style.css?v=3"><script defer src="/assets/app.js"></script></head>
<body data-language="{lang}" data-page="{route}"><a class="skip" href="#main">{pair('跳至內容','Skip to content',lang)}</a>
<div class="preview-bar"><span class="preview-dot"></span>{pair('謝俊仁官方網站','Official website of TSE Chun-Yan',lang)}<span class="preview-note">{pair('古琴創作 · 打譜 · 研究','Qin compositions · reconstructions · research',lang)}</span></div>
<header class="site-header"><a class="brand" href="{url(lang)}"><span>{name}<small>{pair('古琴創作樂曲、打譜與論文','Qin compositions · Reconstructions · Papers',lang)}</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">{pair('目錄','Menu',lang)} <span aria-hidden="true">☰</span></button><nav id="site-nav" aria-label="{pair('主目錄','Main navigation',lang)}">{nav}</nav><a class="language" href="{url(other,route)}" lang="{other}">{pair('EN','繁中',lang)} <span aria-hidden="true">↗</span></a></header>
<main id="main">{body}</main>
<footer class="site-footer"><a class="footer-brand" href="{url(lang)}">{name}</a><span>{pair('官方網站','Official website',lang)} · <span data-current-year>{CURRENT_YEAR}</span></span><a href="#main">{pair('回到頁首','Back to top',lang)} ↑</a></footer></body></html>'''

def home(lang, blocks):
    title = source(blocks[0], extra='home-title')
    cards = ''.join(f'<div class="entry"><span class="entry-number">0{i+1}</span>{source(blocks[i+3])}<span class="entry-arrow" aria-hidden="true">↗</span></div>' for i,r in enumerate(ROUTES[1:]))
    return f'''<section class="home-hero wrap"><div class="hero-topline">TSE CHUN-YAN</div>{title}<a class="hero-link" href="{url(lang,'academic')}">{pair('瀏覽論文','Browse academic papers',lang)} <span aria-hidden="true">↗</span></a><div class="hero-bottom">{pair('創作 / 打譜 / 研究','COMPOSITIONS / RECONSTRUCTIONS / RESEARCH',lang)}<span>01 — 04</span></div></section>
<section class="entry-grid wrap" aria-label="{pair('內容目錄','Explore the collection',lang)}">{cards}</section>
<section class="biography wrap"><aside><div class="eyebrow">{pair('關於','ABOUT',lang)}</div>{source(blocks[1])}<img class="portrait" src="/media/images/7a7959_48926c570bcc4867943edef403304cee~mv2.jpg" alt="{pair('謝俊仁','TSE Chun-Yan',lang)}" loading="lazy"></aside><div class="prose">{source(blocks[2])}<div class="contact-links"><a href="mailto:tsecy1@gmail.com">{source(blocks[7])}</a><a href="https://www.youtube.com/channel/UCoFkDyAR1Ymf7_jFqSwCr0g" target="_blank" rel="noopener">{source(blocks[8])}</a></div></div></section>
<section class="credits wrap"><div>{source(blocks[9])}<p class="management-credit">{pair('本網站繼2022年改版後，於2026年重新設計及整理，現由AI助理協助管理及維護。','Following the 2022 redesign, this website was redesigned and reorganized in 2026 and is now managed and maintained with the assistance of an AI assistant.',lang)}</p></div>{source(blocks[10])}</section>'''

def academic(lang, blocks):
    papers = blocks[1:]
    assert len(papers) == len(YEARS)
    counts = {y: YEARS.count(y) for y in dict.fromkeys(YEARS)}
    groups = []
    for year in counts:
        rows = []
        for index, (node, y) in enumerate(zip(papers, YEARS)):
            if y != year:
                continue
            split = next((i for i,n in enumerate(node.children) if isinstance(n,Node) and re.fullmatch(r'(摘要|Abstract)\s*[:：]', visible(n.text), re.I)), None)
            if split is None:
                body = source(node)
            else:
                before, after = node.children[:split], node.children[split:]
                body = source(node, fragment(before) + f'<details class="abstract"><summary data-interface="true">{pair("閱讀摘要", "Read abstract", lang)}<span aria-hidden="true">＋</span></summary><div class="abstract-body">' + fragment(after) + '</div></details>')
            rows.append(f'<article class="paper" id="paper-{index+1}" data-year="{year}"><span class="paper-index" aria-hidden="true">{index+1:02}</span>{body}</article>')
        groups.append(f'<section class="year-group" id="year-{year}" data-year="{year}"><div class="year-heading"><h2>{year}</h2><span>{counts[year]:02}</span></div>{"".join(rows)}</section>')
    years = ''.join(f'<a href="#year-{y}" data-year-link="{y}">{y}<span>{n:02}</span></a>' for y,n in counts.items())
    options = ''.join(f'<option value="{y}">{y}</option>' for y in counts)
    return f'''<section class="page-hero wrap"><div class="eyebrow">04 / {pair('學術研究','RESEARCH',lang)}</div><div class="page-title-row"><h1>{LABELS[lang][4]}</h1><span class="catalogue-range">1998 — 2025</span></div>{source(blocks[0],extra='hero-description')}</section>
<section class="library wrap" aria-label="{LABELS[lang][4]}"><aside class="year-rail"><div class="rail-top"><span>{pair('出版年份','PUBLICATION YEAR',lang)}</span><a href="#main">↑</a></div><a class="all-years" href="#catalogue">{pair('全部論文','All papers',lang)}<span>49</span></a><div class="year-links">{years}</div><div class="rail-foot">{pair('按年份瀏覽，或搜尋書目與摘要。','Browse by year, or search bibliographies and abstracts.',lang)}</div></aside><div class="catalogue" id="catalogue"><form class="search-tools" role="search"><div class="search-box"><span aria-hidden="true">⌕</span><label class="sr-only" for="paper-search">{pair('搜尋論文','Search papers',lang)}</label><input id="paper-search" type="search" placeholder="{pair('搜尋題名、作者、關鍵字…','Search titles, authors, keywords…',lang)}" autocomplete="off"></div><label class="sr-only" for="year-select">{pair('出版年份','Publication year',lang)}</label><select id="year-select"><option value="">{pair('所有年份','All years',lang)}</option>{options}</select></form><div class="results-line"><span id="result-count" aria-live="polite">{pair('共 49 篇','49 papers',lang)}</span><button type="button" id="expand-all" aria-expanded="false">{pair('展開全部摘要','Expand all abstracts',lang)} <span aria-hidden="true">＋</span></button></div><noscript><p>{pair('搜尋需啟用 JavaScript；全部原文仍可閱讀。','Search requires JavaScript; all original entries remain readable.',lang)}</p></noscript><div id="paper-groups">{"".join(groups)}</div><div class="empty-state" id="empty-state" hidden><h2>{pair('沒有符合的論文','No matching papers',lang)}</h2><button type="button" id="clear-search">{pair('清除搜尋條件','Clear filters',lang)} ↗</button></div></div></section>'''

def work_media(lang, route, record, index):
    if route == 'cds-and-books':
        cover = list(MEDIA['covers'].values())[index]
        return f'<img class="publication-cover" src="{cover["local_url"]}" alt="{escape(cover["alt"],quote=True)}" loading="lazy">'
    ids = {n.attrs['id'] for n in record}
    output = []
    for item in MEDIA['pages'].get(f'{lang}-{route}', []):
        if not ids.intersection(item['source_text_ids']):
            continue
        if item['kind'] == 'MusicPlayer':
            for track in item['tracks']:
                title = escape(track['title'])
                artist = f'<span>{escape(track["artist"])}</span>' if track['artist'] else ''
                output.append(f'<div class="recording"><div class="recording-label"><span aria-hidden="true">♫</span><strong>{title}</strong>{artist}</div><audio controls preload="none" src="{track["local_url"]}" aria-label="{escape(track["title"],quote=True)}"><a href="{track["local_url"]}">{title}</a></audio></div>')
        else:
            parsed = urlsplit(item['url'])
            query = parse_qs(parsed.query)
            video_id = query.get('v', [parsed.path.rsplit('/',1)[-1]])[0]
            assert re.fullmatch(r'[A-Za-z0-9_-]{11}',video_id), item['url']
            start = query.get('t',query.get('start',['0']))[0]
            seconds = sum(int(n)*{'h':3600,'m':60,'s':1,'':1}[u] for n,u in re.findall(r'(\d+)([hms]?)',start))
            embed = f'https://www.youtube-nocookie.com/embed/{video_id}?start={seconds}'
            output.append(f'<div class="performance"><iframe loading="lazy" src="{embed}" title="{pair("演出影片","Performance video",lang)} {index+1}" allow="encrypted-media; picture-in-picture; fullscreen" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe><a href="{escape(item["url"],quote=True)}" target="_blank" rel="noopener">{pair("在 YouTube 觀看","Watch on YouTube",lang)} ↗</a></div>')
    return ''.join(output)

def collection(lang, route, blocks):
    label = LABELS[lang][ROUTES.index(route)]
    index = ROUTES.index(route)
    if route == 'compositions':
        intro = source(blocks[1])
        records = [[b] for b in blocks[2:]]
        title = source(blocks[0],extra='collection-title')
    elif route == 'reconstruction':
        # Preserve the complete introduction including the score-use restriction.
        intro = source(blocks[0])
        records = [blocks[i:i+2] for i in range(1,len(blocks),2)]
        title = f'<h1>{label}</h1>'
    else:
        intro = ''
        # The source HTML puts the 2016 book contents before its title. Keep both
        # source blocks intact and map their explicit new reading positions.
        records = [blocks[1:3],blocks[3:5],[blocks[6],blocks[5]],[blocks[7]],[blocks[8],blocks[9]]]
        title = source(blocks[0],extra='collection-title')
    links, articles = [], []
    for i,record in enumerate(records):
        first = visible(record[0].text.split('\n')[0])
        if route == 'cds-and-books' and i < 2:
            first = visible(record[1].text.split('\n')[0])
        links.append(f'<a href="#work-{i+1}"><span>{i+1:02}</span>{escape(first)}</a>')
        articles.append(f'<article class="work" id="work-{i+1}"><div class="work-number">{i+1:02} <span>↘</span></div><div class="work-body prose">'+''.join(source(n) for n in record)+work_media(lang,route,record,i)+'</div></article>')
    return f'''<section class="page-hero wrap"><div class="eyebrow">0{index} / {LABELS['en'][index].upper()}</div>{title}</section><div class="collection-layout wrap"><aside class="work-rail"><h2>{pair('目錄','CONTENTS',lang)}</h2>{"".join(links)}</aside><div class="works"><div class="collection-intro prose">{intro}</div>{"".join(articles)}</div></div>'''

def main():
    baseline = json.loads((ROOT/'inventory/content-baseline.json').read_text())
    mapping = []
    for page in baseline['pages']:
        raw = ROOT/page['raw_file']
        assert hashlib.sha256(raw.read_bytes()).hexdigest() == page['raw_sha256']
        parser = SourceParser()
        parser.feed(raw.read_text())
        assert len(parser.blocks) == len(page['blocks'])
        lang = page['language']
        route = raw.stem.split('-',1)[1]
        for node,block in zip(parser.blocks,page['blocks']):
            assert node.attrs['id'] == block['wix_id']
            assert node.text == block['text'], (raw,block['wix_id'])
            mapping.append({'source_url':page['source_url'],'source_id':block['wix_id'],'source_order':block['order'],'text_sha256':block['text_sha256'],'preview_url':url(lang,route),'preview_selector':f'[data-source-id="{block["wix_id"]}"]','status':('owner-approved copyright year update: 2022 to 2026' if block['wix_id']=='comp-kyw9tprf' else 'exact decoded text nodes verified against frozen public HTML; backend reconciliation pending')})
        body = home(lang,parser.blocks) if route == 'home' else academic(lang,parser.blocks) if route == 'academic' else collection(lang,route,parser.blocks)
        dest = OUT/url(lang,route).lstrip('/')/'index.html'
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(shell(lang,route,body))
    (ROOT/'inventory/preview-source-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
    print(f'Built 10 pages; verified and mapped {len(mapping)} original text components.')

if __name__ == '__main__':
    main()
