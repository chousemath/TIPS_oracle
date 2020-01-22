from bs4 import BeautifulSoup
import os
import json

root = 'http://www.m-park.co.kr'
froot = 'pages_list_mpark'
links = {}

def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'html.parser')
            hrefs = [a.get('href') for a in soup.findAll('a')]
            hrefs = [f'{root}{h}' for h in hrefs if h and 'my_car_view' in h]
            for href in hrefs:
                links[href] = True
            os.remove(path)

    with open('links_mpark.json', 'w') as json_file:
        json.dump(links, json_file)
