from bs4 import BeautifulSoup
import os
import json

root = 'https://www.autoinside.co.kr/auc/car/auc_car_view.do?i_sEntryCd='
froot = 'pages_list_autoinside'
links = {}

def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            ids = [a.get('id') for a in soup.findAll('a', class_='a_detail') if a.get('href') == 'javascript:;']
            for id in ids:
                links[f'{root}{id}'] = True
    
    with open('links_autoinside.json', 'w') as json_file:
        json.dump(links, json_file)
