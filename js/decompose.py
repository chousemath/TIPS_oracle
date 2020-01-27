from bs4 import BeautifulSoup
from typing import List, Tuple
from os import listdir, path
from htmlmin import minify

Route = Tuple[str, str]


def decompose(route: Route):
    src_dir, dst_dir = route
    for fname in (x for x in listdir(src_dir) if '.html' in x):
        with open(path.join(src_dir, fname), 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            for head in soup.findAll('head'):
                head.decompose()
            with open(path.join(dst_dir, fname), 'w') as f:
                f.write(minify(str(soup)))


routes: List[Route] = [
    ('pages_detail', 'html_src_encar'),
    ('pages_detail_encar_domestic', 'html_src_encar'),
    ('pages_detail_mpark', 'html_src_mpark'),
    ('pages_detail_aj', 'html_src_aj'),
]

if __name__ == '__main__':
    while True:
        for route in routes:
            decompose(route)
        print('Finished with a round of decomposition')
