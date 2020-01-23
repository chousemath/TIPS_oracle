from bs4 import BeautifulSoup
from typing import List, Tuple
from os import listdir, path

Route = Tuple[str, str]


def decompose(src_dir: str, dst_dir: str):
    for fname in (x for x in listdir(src_dir) if '.html' in x):
        with open(path.join(src_dir, fname), 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')


routes: List[Route] = [
    ('pages_detail', 'html_src_encar'),
    ('pages_detail_encar_domestic', 'html_src_encar'),
]
