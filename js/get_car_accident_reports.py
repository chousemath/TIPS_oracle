import requests
from os import path
from random import shuffle

root = 'http://www.encar.com'
links = {}

def run():
    with open('./car_ids.txt', 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        shuffle(lines)
        for line in lines:
            if len(line) != 24:
                continue
            line = line.replace('carid=', '').replace('carType=', '')
            car_id, car_type = line.split('&')
            print(car_id, car_type)
            dst = path.join('encar_accident_reports', f'{car_id}.html')
            if path.isfile(dst):
                continue
            if car_type == '2':
                url = f'{root}/md/sl/mdsl_regcar.do?method=inspectionTruckView&carid={car_id}'
            else:
                url = f'{root}/md/sl/mdsl_regcar.do?method=inspectionViewNew&carid={car_id}'
            page = requests.get(url)
            with open(dst, 'w') as writer:
                writer.write(page.text)
    
run()
