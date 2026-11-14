"""No-dependency source checks: python3 tests/test_structure.py"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.images = []
        self.title_count = 0
        self.h1_count = 0
        self.last_tag = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'link' and a.get('href'): self.images.append(a['href'])
        if tag == 'script' and a.get('src'): self.images.append(a['src'])
        if tag == 'h1': self.h1_count += 1
        if tag == 'title': self.title_count += 1

for page in ['index.html','privacy.html','terms.html']:
    content = (ROOT / page).read_text()
    parser = Inspect()
    parser.feed(content)
    assert parser.title_count == 1, f'{page}: missing title'
    assert parser.h1_count == 1, f'{page}: expected one h1'
    assert len(parser.ids) == len(set(parser.ids)), f'{page}: duplicate IDs'
    assert 'noindex,nofollow' in content, f'{page}: preview should be noindex'
    for href in parser.links:
        if href.startswith(('http://','https://','mailto:','tel:')): continue
        path, _, fragment = href.partition('#')
        if path:
            assert (ROOT / path).is_file(), f'{page}: missing linked file {path}'
        if fragment and (not path or path == page):
            assert fragment in parser.ids, f'{page}: missing anchor #{fragment}'
    for asset in parser.images:
        if asset.startswith(('http:','https:')): continue
        assert (ROOT / asset).is_file(), f'{page}: missing asset {asset}'
    print('PASS', page, 'semantic structure, anchors, preview settings')

script = (ROOT / 'script.js').read_text()
assert 'fetch(' not in script and 'localStorage' not in script
assert 'preventDefault()' in script
assert 'aria-expanded' in script
css = (ROOT / 'styles.css').read_text()
assert '@media(max-width:590px)' in css and 'prefers-reduced-motion' in css
json.loads((ROOT / 'vercel.json').read_text())
assert 'Disallow: /' in (ROOT / 'robots.txt').read_text()
print('PASS local-only tool, mobile styles, security config and robots rules')
