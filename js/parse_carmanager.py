from typing import List
import threading
from bs4 import BeautifulSoup
import csv
from os import path, listdir, remove
import json

if path.exists('carmanager.csv'):
    remove('carmanager.csv')

root_dirs = ['pages_detail_carmanager']
#root_dirs = ['carmanager_to_zip']
writer = None # global variable

def write_rows(thread_id: int, files: List[str]):
    for (p, file_name) in files:
        ts = int(file_name.split('-')[0]) // 1000
        try:
            with open(p, 'r') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                car_name = soup.find(id='ui_ViewCarName').text
                car_price = int(
                    soup.find(id='ui_ViewCarAmount').text.replace(',', '')) * 10_000
                car_year = int(soup.find(id='ui_ViewCarRegYear').text)
                car_regist_year = soup.find(id='ui_ViewCarReg').text
    
                car_mileage = 0
                car_transmission = ''
                car_fuel = ''
                car_plate_num = ''
                car_color = ''
    
                detail_info = soup.find(id='detail_info').text
                no_accident = 1 if '무사고' in detail_info else 0
                yes_warranty = 1 if '워런티' in detail_info else 0
    
                car_options = []
                for inp in [x for x in soup.find_all('input', checked=True, id=False)]:
                    car_options.append(inp.findNext('label').text.strip())
    
                for th in soup.find_all('th'):
                    # 미 션, 연 료, 색 상, 차량번호
                    if th.text == '차량번호':
                        car_plate_num = th.findNext('td').text.strip()
                    if th.text == '연 료':
                        car_fuel = th.findNext('td').text.strip()
                    if th.text == '미 션':
                        car_transmission = th.findNext('td').text.strip()
                    if th.text == '주행거리':
                        car_mileage = int(th.findNext('td').text.replace(
                            ',', '').replace(' km', '').strip())
                    if th.text == '색 상':
                        car_color = th.findNext('td').text.strip()
                car_options = '|'.join(car_options)
                writer.writerow([
                    ts,
                    car_name,
                    car_price,
                    car_year,
                    car_regist_year,
                    car_mileage,
                    car_transmission,
                    car_fuel,
                    car_plate_num,
                    car_color,
                    no_accident,
                    yes_warranty,
                    car_options,
                ])
                print(f'thread-{thread_id}, row written, {car_plate_num}')
        except Exception as e:
            print(str(e))

with open('carmanager.csv', 'a+') as fd:
    writer = csv.writer(fd)
    for root_dir in root_dirs:
        files = [(path.join(root_dir, f), f) for f in listdir(root_dir) if '.html' in f]

        file_count = len(files)

        t1_limit = 1 * file_count // 6
        t2_limit = 2 * file_count // 6
        t3_limit = 3 * file_count // 6
        t4_limit = 4 * file_count // 6
        t5_limit = 5 * file_count // 6

        t1 = threading.Thread(target=write_rows, args=(1, files[:t1_limit],))
        t2 = threading.Thread(target=write_rows, args=(2, files[t1_limit:t2_limit],))
        t3 = threading.Thread(target=write_rows, args=(3, files[t2_limit:t3_limit],))
        t4 = threading.Thread(target=write_rows, args=(4, files[t3_limit:t4_limit],))
        t5 = threading.Thread(target=write_rows, args=(5, files[t4_limit:t5_limit],))
        t6 = threading.Thread(target=write_rows, args=(6, files[t5_limit:],))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()

