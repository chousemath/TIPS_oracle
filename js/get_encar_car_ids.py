from typing import List
from sys import argv, exit
from os import path, listdir, remove
from bs4 import BeautifulSoup as BS
from time import time
from shutil import copy2

dst = 'encar_accident_reports'
src = 'pages_detail'
src2 = 'pages_detail_encar_domestic'

file_path = 'encar_car_ids.txt'
try:
    remove(file_path)
except:
    print(f'{file_path} does not exist')

with open(file_path, 'a+') as fd:
    for fname in (x for x in listdir(src) if '.html' in x):
        fpath = path.join(src, fname)
        with open(fpath, 'r') as f:
            soup = BS(f, 'lxml')
            try:
                value = soup.find('input', {'id': 'carid'}).get('value')
            except:
                continue

            if path.isfile(path.join(dst, f'{value}.html')):
                continue

            text = soup.text
            if '&carType=1' in text:
                car_type = 1
            elif '&carType=2' in text:
                car_type = 2
            else:
                continue

            line = f'{value},{car_type}\n'
            fd.write(line)
            print(line)

    for fname in (x for x in listdir(src2) if '.html' in x):
        fpath = path.join(src2, fname)
        with open(fpath, 'r') as f:
            soup = BS(f, 'lxml')
            try:
                value = soup.find('input', {'id': 'carid'}).get('value')
            except:
                continue

            if path.isfile(path.join(dst, f'{value}.html')):
                continue

            text = soup.text
            if '&carType=1' in text:
                car_type = 1
            elif '&carType=2' in text:
                car_type = 2
            else:
                continue

            line = f'{value},{car_type}\n'
            fd.write(line)
            print(line)
