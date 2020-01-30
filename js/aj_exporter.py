from typing import List
from sys import argv, exit
from os import path, listdir
from bs4 import BeautifulSoup as BS
from time import time
from csv import writer
from shutil import copy2


def clean(in_val: str) -> str:
    return in_val.replace('\n', '').replace('\t', '').replace('  ', '').replace('차량번호', '').replace('차대번호', '').replace('원동기형식', '').replace('연료', '').replace('주행거리', '').replace('배기량', '').replace('변속기', '').replace('색상', '').replace('차종', '').replace('사고이력', '').replace('Km', '').replace('cc', '').replace('인증중고차 여부', '').replace(',', '').replace('과세구분', '').replace('최초등록일 :', '').replace('( ', '(').replace(' )', ')').replace('연식', '').replace('경력', '').strip()


if __name__ == '__main__':
    if len(argv) != 3:
        print('\nYou are using this script incorrectly')
        print('Instructions: python aj_exporter.py <SOURCE_DIR> <DESTINATION_DIR>')
        print('Example usage: python aj_exporter.py html_src_aj csv_aj\n')
        exit()

    while True:
        latest = sorted([x for x in listdir(argv[2]) if '.csv' in x])[-1]
        copy2(path.join(argv[2], latest), '../aj.csv')
        full_data: List[List[str]] = []
        for fname in [x for x in listdir(argv[1]) if '.html' in x]:
            ts = fname.split('-')[0]
            fpath = path.join(argv[1], fname)
            with open(fpath, 'r') as f:
                soup = BS(f, 'lxml')
                div = soup.find('div', class_='details-block')
                data: List[str] = [clean(x.text)
                                   for x in div.find_all('li') if x.text]
                h2 = ''.join([x.text for x in soup.find_all('h2', class_='tit_style2')]).replace(
                    '\n', '').replace('  ', '')
                h2 = ''.join([x for x in h2.split('\t') if x][1:])
                data.append(h2)
                for table in soup.find_all('table', class_='keepStuff'):
                    if '편의' in table.text:
                        inps_arr: List[str] = [x.get('title', '') for x in table.find_all(
                            'input', class_='inpu_chek') if x.get('checked') == 'checked']
                        inps: str = '///'.join(inps_arr)
                price = soup.find('strong', class_='i_comm_main_txt2').text
                data.append(inps)
                data.append(price)
                data.append(ts)
                full_data.append(data)

        name = f'aj-{int(time())}.csv'
        with open(path.join(argv[2], name), 'w', newline='') as f:
            wr = writer(f)
            wr.writerows(full_data)
