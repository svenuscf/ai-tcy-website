"""Extract an auditable public-HTML inventory; no network or source rewriting."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

class InventoryParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.blocks, self.references = [], [], []
        self.active = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('data-testid') == 'richTextElement':
            assert self.active is None, 'Unexpected nested rich text'
            self.active = {'wix_id': attrs.get('id'), 'text_fragments': [], 'links': [], 'depth': len(self.stack)}
        for key in ('href', 'src', 'srcset', 'poster', 'data-src'):
            if key in attrs:
                ref = {'tag': tag, 'attribute': key, 'value': attrs[key], 'element_id': attrs.get('id'), 'target': attrs.get('target')}
                self.references.append(ref)
                if self.active is not None:
                    self.active['links'].append(ref)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.active is not None:
            self.active['text_fragments'].append(data)

    def handle_endtag(self, tag):
        if tag in self.stack:
            pos = len(self.stack) - 1 - self.stack[::-1].index(tag)
            del self.stack[pos:]
            if self.active is not None and len(self.stack) == self.active['depth']:
                block = self.active
                del block['depth']
                block['text'] = ''.join(block['text_fragments'])
                block['text_sha256'] = hashlib.sha256(block['text'].encode()).hexdigest()
                block['order'] = len(self.blocks)
                self.blocks.append(block)
                self.active = None

def main():
    pages = []
    for file in sorted((ROOT / 'inventory/raw').glob('*.html')):
        if not file.name.startswith(('zh-', 'en-')):
            continue
        language, slug = file.stem.split('-', 1)
        route = '' if slug == 'home' else slug
        url = 'https://www.tsechunyan.com/' + ('en/' if language == 'en' else '') + route
        data = file.read_bytes()
        parser = InventoryParser()
        parser.feed(data.decode('utf-8'))
        assert parser.active is None
        assert parser.blocks, f'No source text found in {file}'
        pages.append({'source_url': url.rstrip('/'), 'language': language, 'raw_file': str(file.relative_to(ROOT)), 'raw_sha256': hashlib.sha256(data).hexdigest(), 'blocks': parser.blocks, 'references': parser.references, 'verification': 'public HTML extraction only; rendered and backend reconciliation pending'})
    result = {'capture_date': '2026-09-28', 'scope': 'Ten known public pages. Rich-text fragments preserve decoded text nodes without trimming or normalization. Layout breaks remain in raw HTML. References include DOM attributes only; runtime and embedded JSON assets are not fully inventoried.', 'pages': pages}
    (ROOT / 'inventory/content-baseline.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for page in pages:
        print(page['source_url'], len(page['blocks']), 'text blocks;', len(page['references']), 'reference attributes')

if __name__ == '__main__':
    main()
