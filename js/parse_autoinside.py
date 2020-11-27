from typing import List
from bs4 import BeautifulSoup
import csv
from os import path, listdir, remove, system
import json

root_dirs = ['pages_detail_autoinside']
with open('autoinside.csv', 'a+') as fd:
    writer = csv.writer(fd)
    for root_dir in root_dirs:
        files = ((path.join(root_dir, f), f) for f in listdir(root_dir) if '.html' in f)
        for (p, fname) in files:
            print(p)
            ts = int(fname.split('-')[0]) // 1000
            try:
                with open(p, 'r') as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    car_box = 'box_car_ltem';
                    boxes = soup.find_all('div', class_=car_box)
                    print('boxes', boxes)
                    for box in boxes:
                        row = []
                        a_detail = box.find(class_='a_detail')
                        row.append(a_detail.id)
                        icon = box.find(class_='ico').find('img')
                        row.append(icon.alt)
                        row.append(box.find(class_='car_info_top').find('dd').text.replace('\n', '').replace('\r', ''))
                        bottom = box.find(class_='car_info_bottom')
                        for sect in [x.text for x in bottom.find_all('li')]:
                            row.append(sect)
                        row.append(bottom.find('dt').text)
                        print(row)
                        # writer.writerow(row)
                # cmd = f'aws s3 cp {p} s3://{p.replace("_", "-")}'
                # system(cmd)
            except Exception as e:
                print(str(e))
            finally:
                print('done')
                #if path.exists(p):
                #    remove(p)

