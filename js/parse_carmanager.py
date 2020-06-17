from bs4 import BeautifulSoup
import csv
from os import path, listdir
import json

root_dirs = ['pages_detail_carmanager']
with open('carmanager.csv','a+') as fd:
    writer = csv.writer(fd)
    for root_dir in root_dirs:
        for (p, file_name) in ((path.join(root_dir, f), f) for f in listdir(root_dir) if '.html' in f):
            # 1580627715862-57841662.html
            ts = int(file_name.split('-')[0]) // 1000
            try:
                with open(p, 'r') as f:
                    contents = f.read()
                    soup = BeautifulSoup(contents, 'lxml')
                    car_name = soup.find(id='ui_ViewCarName').text
                    car_price = int(soup.find(id='ui_ViewCarAmount').text.replace(',', '')) * 10_000
                    car_year = int(soup.find(id='ui_ViewCarRegYear').text)
                    car_regist_year = soup.find(id='ui_ViewCarReg').text
    
                    car_mileage = 0
                    car_transmission = ''
                    car_fuel = ''
                    car_plate_num = ''
                    car_color = ''
    
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
                            car_mileage = int(th.findNext('td').text.replace(',', '').replace(' km', '').strip())
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
                        car_options,
                    ])
                    print(f'row written, {car_plate_num}')
            except Exception as e:
                print(str(e))

