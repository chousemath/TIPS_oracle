from typing import List
import threading
from bs4 import BeautifulSoup
import csv
from os import path, listdir, remove, system
import json

root_dirs = ['pages_detail_encar_domestic', 'pages_detail']
writer = None # global variable

def write_rows(thread_id: int, files: List[str]):
    for (p, fname) in files:
        ts = int(fname.split('-')[0]) // 1000
        try:
            with open(p, 'r') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')

                transmission = soup.find('meta', {'name': 'trns'})['content']
                fuel = soup.find('meta', {'name': 'whatfuel'})['content']
                color = soup.find('meta', {'name': 'clr'})['content']
                category = soup.find('meta', {'name': 'WT.z_vehcat'})['content']
                price = soup.find('meta', {'name': 'WT.z_price'})['content']
                make = soup.find('meta', {'name': 'WT.z_make'})['content']
                year = soup.find('meta', {'name': 'WT.z_year'})['content']
                month = soup.find('meta', {'name': 'WT.z_month'})['content']
                state = soup.find('meta', {'name': 'WT.z_state'})['content']
                car_id = soup.find('meta', {'name': 'WT.z_CarId'})['content']
                model_name = soup.find('meta', {'name': 'WT.z_model_name'})['content']
                model_trim = soup.find('meta', {'name': 'WT.z_model_trim'})['content']
                model = soup.find('meta', {'name': 'WT.z_model'})['content']
                description = soup.find('meta', {'name': 'description'})['content']
                seller = soup.find('div', {'class' :'detail_seller'}).text
                views = soup.find('div', {'class' :'prod_infoetc'}).text

                # ims = [x.get('src', 'xxx') for x in soup.findAll('img')]
                # ims = '|||'.join(ims)
                
                writer.writerow([
                    ts,
                    transmission,
                    fuel,
                    color,
                    category,
                    price,
                    make,
                    year,
                    month,
                    state,
                    car_id,
                    model_name,
                    model_trim,
                    model,
                    seller,
                    description,
                    views,
                    # ims,
                ])
            cmd = f'aws s3 cp {p} s3://pages-detail-encar/{fname}'
            system(cmd)
        except Exception as e:
            print(str(e))
        finally:
            if path.exists(p):
                remove(p)

with open('encar_new2.csv', 'a+') as fd:
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

