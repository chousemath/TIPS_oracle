from bs4 import BeautifulSoup
from os import listdir, path
from htmlmin import minify

def compress(route: str):
    for fname in (x for x in listdir(route) if '.html' in x):
        try:
            src_path = path.join(route, fname)
            print(src_path)
            with open(src_path, 'r') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                for tag in soup():
                    for attribute in ["style", 'link']:
                        del tag[attribute]
                for style in soup.find_all('style'):
                    style.decompose()
                for link in soup.find_all('link'):
                    link.decompose()

                with open(src_path, 'w') as f:
                    f.write(minify(str(soup).replace('\n', '').replace('\r', '').replace('  ', ''), remove_comments=True, convert_charrefs=True))
        except Exception as e:
            print(str(e))

