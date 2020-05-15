from bs4 import BeautifulSoup
from os import path, listdir
import json

root_dirs = ['pages_detail_encar_domestic', 'pages_detail_encar_foreign']
for root_dir in root_dirs:
    for p in (path.join(root_dir, f) for f in listdir(root_dir) if '.html' in f):
        print(p)
        #with open(path, 'r') as f:
        #    contents = f.read()
        #    soup = BeautifulSoup(contents, 'lxml')

