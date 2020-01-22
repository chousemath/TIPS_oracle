from bs4 import BeautifulSoup
import os
import json
from pprint import pprint

root = 'http://www.encar.com'
froot = 'pages_list'
links = {}
def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            hrefs = [a.get('href') for a in soup.findAll('a')]
            hrefs = [f'{root}{h}' for h in hrefs if h and 'cardetailview' in h]
            for href in hrefs:
                links[href] = True
            os.remove(path)
    
    with open('links.json', 'w') as json_file:
        json.dump(links, json_file)

