from bs4 import BeautifulSoup
import os
import json

froot = 'pages_list_aj'
links = {}

def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            hrefs = [a.get('onclick') for a in soup.findAll('a')]
            hrefs = [h.replace("javascript:carInfo('", '').replace("');", '') for h in hrefs if h and 'javascript:carInfo(' in h]
            for href in hrefs:
                links[href] = True
            #os.remove(path)
    
    with open('links_aj.json', 'w') as json_file:
        json.dump(links, json_file)
