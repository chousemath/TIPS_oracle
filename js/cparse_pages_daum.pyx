from bs4 import BeautifulSoup
import os
import json
from pprint import pprint

froot = 'pages_daum_news'
links = {}
def run():
    for path in [os.path.join(froot, f) for f in os.listdir(froot) if '.html' in f]:
        with open(path, 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            texts = [x.text for x in soup.findAll('strong', {'class': 'tit_thumb'})]
            for text in texts:
                print(text)

