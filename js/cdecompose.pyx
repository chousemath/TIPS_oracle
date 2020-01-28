from bs4 import BeautifulSoup
from typing import List, Tuple
from os import listdir, path
from htmlmin import minify

Route = Tuple[str, str]

def decompose(route: Route):
    src_dir, dst_dir = route
    for fname in (x for x in listdir(src_dir) if '.html' in x):
        dst_path = path.join(dst_dir, fname)
        if path.isfile(dst_path):
            continue
        with open(path.join(src_dir, fname), 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            for head in soup.findAll('head'):
                head.decompose()
            with open(dst_path, 'w') as f:
                f.write(minify(str(soup)))

