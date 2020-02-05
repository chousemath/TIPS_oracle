from bs4 import BeautifulSoup
import os
import json

root = 'https://www.autoinside.co.kr/auc/car/auc_car_insp_info_pop.do?i_sFlagAction=VIEW&i_sCarCd='
froot = 'pages_detail_autoinside'
links = {}

def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            ids = [a.get('id') for a in soup.findAll('a', class_='performance') if a.get('href') == 'javascript:;']
            for id in ids:
                links[f'{root}{id}'] = True
    
    with open('links_autoinside_accident.json', 'w') as json_file:
        json.dump(links, json_file)
