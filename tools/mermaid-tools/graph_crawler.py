import os
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'area', 'link'):
            for attr, value in attrs:
                if attr == 'href' and value:
                    self.links.append(value)
        elif tag in ('frame', 'iframe'):
            for attr, value in attrs:
                if attr == 'src' and value:
                    self.links.append(value)

def get_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        parser = LinkParser()
        parser.feed(content)
        return parser.links
    except Exception as e:
        return []

start_file = "index.html"
visited = set()
edges = set()

def normalize_path(base_path, ref_path):
    ref_path = urlparse(ref_path).path
    if not ref_path:
        return base_path
    ref_path = unquote(ref_path)
    base_dir = os.path.dirname(base_path)
    target_path = os.path.normpath(os.path.join(base_dir, ref_path))
    return target_path

def crawl(file_path):
    if file_path in visited:
        return
    if not os.path.isfile(file_path):
        return
    
    visited.add(file_path)
    
    links = get_links(file_path)
    
    for link in links:
        link = link.strip()
        if not link or link.startswith(('http://', 'https://', 'mailto:', 'javascript:', '#', 'ftp://')):
            continue
        if link.startswith('/'):
             continue
        
        target = normalize_path(file_path, link)
        if target.lower().endswith(('.html', '.htm')):
            edges.add((file_path, target))
            crawl(target)

crawl(start_file)

print("graph TD")
node_ids = {}
def get_node_id(path):
    if path not in node_ids:
        node_ids[path] = f"N{len(node_ids)}"
    return node_ids[path]

nodes = set([s for s, d in edges] + [d for s, d in edges])
for path in nodes:
    print(f'    {get_node_id(path)}["{path}"]')

for src, dst in edges:
    print(f'    {get_node_id(src)} --> {get_node_id(dst)}')
