"""Check rendered source text, original links, local routes and media completeness."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from build_site import CURRENT_YEAR, ROOT, OUT, VOID

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.blocks={}; self.links=[]; self.local=[]; self.active=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-source-id' in a:
            self.active=a['data-source-id']; assert self.active not in self.blocks
            self.blocks[self.active]={'text':'','links':[]}
        skip=a.get('data-interface')=='true' or bool(self.stack and self.stack[-1][1])
        if tag=='a':
            assert not any(t=='a' for t,_ in self.stack), 'Nested anchor'
            if self.active and not skip and 'data-original-href' in a:
                self.blocks[self.active]['links'].append(a['data-original-href'])
        for key in ('href','src'):
            if a.get(key,'').startswith('/'):
                self.local.append(urlsplit(a[key]).path)
        if tag not in VOID: self.stack.append((tag,skip))
    def handle_endtag(self,tag):
        assert self.stack and self.stack[-1][0]==tag, (tag,self.stack[-1:])
        self.stack.pop()
        if self.active and not any(t=='div' for t,_ in self.stack): self.active=None
        # Source wrappers end before their containing article, but whitespace outside
        # wrappers must not become source text. Track wrapper depth explicitly below.
    def handle_data(self,data):
        if self.active and not (self.stack and self.stack[-1][1]):
            self.blocks[self.active]['text']+=data

class CheckedPage(Page):
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs)
        if 'data-source-id' in dict(attrs): self.source_depth=len(self.stack)
    def handle_endtag(self,tag):
        closing=self.active and len(self.stack)==self.source_depth
        super().handle_endtag(tag)
        if closing: self.active=None

baseline=json.loads((ROOT/'inventory/content-baseline.json').read_text())
count=0
for page in baseline['pages']:
    raw=Path(page['raw_file']); route=raw.stem.split('-',1)[1]
    dest=OUT/('en' if page['language']=='en' else '')/('' if route=='home' else route)/'index.html'
    p=CheckedPage(); p.feed(dest.read_text())
    assert set(p.blocks)=={b['wix_id'] for b in page['blocks']}
    for b in page['blocks']:
        expected = b['text']
        if b['wix_id'] == 'comp-kyw9tprf':
            expected = expected.replace('© 2022', f'© 2022–{CURRENT_YEAR}')
        assert p.blocks[b['wix_id']]['text']==expected, (dest,b['wix_id'],repr(p.blocks[b['wix_id']]['text'][-200:]),repr(expected[-200:]))
        assert p.blocks[b['wix_id']]['links']==[a['value'] for a in b['links'] if a['tag']=='a' and a['attribute']=='href'], (dest,b['wix_id'],'links')
        count+=1
    for path in p.local:
        target=OUT/path.lstrip('/')
        assert target.exists(), (dest,path)
manifest=json.loads((ROOT/'inventory/media-manifest.json').read_text())
for asset in manifest['downloads']:
    assert (OUT/asset['local_url'].lstrip('/')).stat().st_size>1000
print(f'PASS: 10 pages, {count} source blocks (including two approved copyright updates), no nested anchors, all local links/assets, {len(manifest["downloads"])} media files.')
