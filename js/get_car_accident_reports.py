import requests
from random import shuffle
from typing import List
from sys import argv, exit
from os import path, listdir, remove
from bs4 import BeautifulSoup as BS
from time import time, sleep
from shutil import copy2

root = 'http://www.encar.com'
dst = 'encar_accident_reports'
src = 'pages_detail'
src2 = 'pages_detail_encar_domestic'
links = {}


def get_html(car_type: int, car_id: str, final_path: str):
    print(f'creating {final_path}')
    if car_type == 2:
        url = f'{root}/md/sl/mdsl_regcar.do?method=inspectionTruckView&carid={car_id}'
    elif car_type == 1:
        url = f'{root}/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid={car_id}'
    else:
        print(f'car type of {car_type} could not be reconciled')
        return
    page = requests.get(url)
    with open(final_path, 'w') as writer:
        writer.write(page.text)


def run():
    while True:
        for fname in (x for x in listdir(src) if '.html' in x):
            fpath = path.join(src, fname)
            with open(fpath, 'r') as f:
                soup = BS(f, 'lxml')
                try:
                    value = soup.find('input', {'id': 'carid'}).get('value')
                except:
                    continue

                final_path = path.join(dst, f'{value}.html')
                if path.isfile(final_path):
                    continue

                text = soup.text
                if '&carType=1' in text:
                    car_type = 1
                elif '&carType=2' in text:
                    car_type = 2
                else:
                    continue

                print(car_type, final_path)
                get_html(car_type, value, final_path)

        for fname in (x for x in listdir(src2) if '.html' in x):
            fpath = path.join(src2, fname)
            with open(fpath, 'r') as f:
                soup = BS(f, 'lxml')
                try:
                    value = soup.find('input', {'id': 'carid'}).get('value')
                except:
                    continue

                final_path = path.join(dst, f'{value}.html')
                if path.isfile(final_path):
                    continue

                text = soup.text
                if '&carType=1' in text:
                    car_type = 1
                elif '&carType=2' in text:
                    car_type = 2
                else:
                    continue

                print(car_type, final_path)
                get_html(car_type, value, final_path)


if __name__ == '__main__':
    run()
