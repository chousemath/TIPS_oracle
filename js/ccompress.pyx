from bs4 import BeautifulSoup
from os import listdir, path
from htmlmin import minify

def compress(route: str):
    for fname in (x for x in listdir(route) if '.html' in x):
        src_path = path.join(route, fname)
        print(src_path)
        with open(src_path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            with open(src_path, 'w') as f:
                f.write(minify(str(soup), remove_comments=True, convert_charrefs=True))

