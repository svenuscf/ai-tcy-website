"""Map media to original text through Wix's published component hierarchy."""
from pathlib import Path
import json
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def main():
    pages = {}
    downloads = {}
    for lang in ['zh','en']:
        for route in ['compositions','reconstruction']:
            page = f'{lang}-{route}'
            data = json.loads((ROOT/f'inventory/raw/{page}-features.json').read_text())
            components = data['structure']['components']
            props = data['props']['render']['compProps']
            parent = {child:key for key,val in components.items() for child in val.get('components',[])}
            def texts(key):
                comp = components.get(key,{})
                if comp.get('componentType') == 'WRichText':
                    return [key]
                return sum((texts(child) for child in comp.get('components',[])),[])
            entries = []
            for key, comp in components.items():
                kind = comp.get('componentType')
                if kind not in ['MusicPlayer','VideoPlayer']:
                    continue
                ancestor = parent.get(key)
                siblings = []
                while ancestor and not siblings:
                    siblings = texts(ancestor)
                    if not siblings:
                        ancestor = parent.get(ancestor)
                assert 0 < len(siblings) <= 2, (key,siblings)
                item = {'component_id':key,'source_text_ids':siblings,'source_container_id':ancestor,'kind':kind,'evidence':f'inventory/raw/{page}-features.json'}
                info = props[key]
                if kind == 'MusicPlayer':
                    tracks = []
                    for track in info['playlist']:
                        local = '/media/audio/' + Path(urlsplit(track['url']).path).name
                        downloads[local] = track['url']
                        tracks.append({'title':track['trackName'],'artist':track['artistName'] if info['showArtistName'] else '', 'url':track['url'],'local_url':local,'duration':info['duration']})
                    item['tracks'] = tracks
                else:
                    item['url'] = info['src']
                entries.append(item)
            pages[page] = entries
    image_ids = ['7a7959_48926c570bcc4867943edef403304cee~mv2.jpg', '54385b_34b0d48f8850456f8c8758ba9cd98790~mv2.jpg']
    covers = {}
    image_data = json.loads((ROOT/'inventory/raw/zh-cds-and-books-features.json').read_text())
    for key, comp in image_data['structure']['components'].items():
        if comp['componentType'] == 'WPhoto':
            p = image_data['props']['render']['compProps'][key]
            covers[key] = {'uri':p['uri'],'alt':p.get('alt',''),'local_url':'/media/images/'+p['uri']}
            image_ids.append(p['uri'])
    for uri in image_ids:
        downloads['/media/images/'+uri] = 'https://static.wixstatic.com/media/'+uri
    result = {'capture_date':'2026-09-28','mapping_method':'Published Wix component hierarchy; no filename-only audio matching. Original source links retained.','pages':pages,'covers':covers,'downloads':[{'local_url':local,'source_url':remote} for local,remote in downloads.items()]}
    (ROOT/'inventory/media-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'Mapped {sum(len(v) for v in pages.values())} bilingual player instances; {len(downloads)} unique local assets planned.')

if __name__ == '__main__':
    main()
