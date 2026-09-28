"""Export only website files for a GitHub Pages project URL; no private inventory."""
import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('destination',type=Path)
p.add_argument('--base',default='/tcy-review')
a=p.parse_args()
assert re.fullmatch(r'/[a-zA-Z0-9_-]+',a.base)
a.destination.mkdir(parents=True,exist_ok=True)
for source in (ROOT/'site').rglob('*'):
    if not source.is_file(): continue
    dest=a.destination/source.relative_to(ROOT/'site')
    dest.parent.mkdir(parents=True,exist_ok=True)
    if source.suffix=='.html':
        text=re.sub(r'(href|src)="/(?!/)',lambda m:m[1]+'="'+a.base+'/',source.read_text())
        dest.write_text(text)
    else: shutil.copy2(source,dest)
(a.destination/'.nojekyll').touch()
(a.destination/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(a.destination/'README.md').write_text('# Tse Chun Yan — design review\n\nPublic design preview for review and approval. The live Wix website is unchanged.\n\nOriginal text and media retain their existing rights; no new license is granted.\n')
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src') and value.startswith('/'):
                assert value.startswith(a.base+'/'),value
                path=urlsplit(value).path[len(a.base)+1:]
                assert (a.destination/path).exists(),value
for page in a.destination.rglob('*.html'): Links().feed(page.read_text())
print(f'Exported 10 pages with verified project paths to {a.destination}')
