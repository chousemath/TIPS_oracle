# -*- coding: utf-8 -*-

from typing import Type, List
import sys
from bs4 import BeautifulSoup
import codecs
import csv
import os
import re
from time import time


def encar_certified_vehicle(bs_obj: Type[BeautifulSoup], timestamp: str, carid: str) -> List[str]:
    """Extract car details from a certified encar vehicle page"""
    elem_brand = bs_obj.find('span', {'class': 'brand'})
    brand = elem_brand.text.strip() if elem_brand else ''
    elem_model = bs_obj.find('span', {'class': 'detail'})
    model = elem_model.text.strip() if elem_model else ''

    mileage = ''
    color = ''
    transmission = ''
    car_number = ''
    fuel = ''
    model_year = ''
    price = ''
    registered_at = ''

    if (car_info := bs_obj.find('ul', {'class': 'list_carinfo'})) is not None:
        lis = car_info.findAll('li')
        color = lis[6].text.replace('색상:', '').strip()
        _mileage = lis[0].text.replace('주행거리:', '')
        mileage = re.sub('[-=.#,/?:$}Kkm]', '', _mileage).strip()
        yearString = lis[1].text.strip()
        cut_string_1 = yearString.replace('자세히보기', '').strip()
        cut_string_2 = cut_string_1.replace('연식:', '').strip()
        cut_string_3 = cut_string_2.replace('년 ', '.')
        registered_at = '20'+cut_string_3.replace('월식', '')

        if '(' in registered_at:
            model_year = '20'+re.sub('[(년형)]', '', registered_at)[-2:]
            registered_at = registered_at[:7]
        else:
            model_year = registered_at[:4]

        transmission = lis[5].text.replace('변속기:', '').strip()
        fuel = lis[2].text.replace('연료:', '').strip()

    checked_options = bs_obj.findAll('dd', {'class': 'on'})
    elem_accident = bs_obj.find('strong', {'class', 'tit_inspect'})
    accident = elem_accident.text.strip() if elem_accident else ''
    if '무사고' in accident:
        accident = 2
    if lis[7] is not None:
        car_number = lis[7].text.replace('차량번호', '').replace(' ', '').strip()
    if (_price := bs_obj.find('em', {'class', 'emph_price'})) is not None:
        price = _price.find(
            'span', {'class', 'txt_num'}).text.replace(',', '').strip()

    _options = [x.find('a') for x in checked_options]
    options: str = '///'.join([x.text.strip() for x in _options if x])
    output = [carid, timestamp, brand+model, car_number, price, mileage,
              color, model_year, registered_at, fuel, transmission, options, accident]
    # print(output)
    return output


def encar_vehicle(bs_obj: Type[BeautifulSoup], timestamp: str, carid: str) -> List[str]:
    mileage = ''
    color = ''
    transmission = ''
    car_number = ''
    fuel = ''
    registered_at = ''
    model_year = ''
    price = ''
    accident = ''

    elem_brand = bs_obj.find('span', {'class': 'brand'})
    brand = elem_brand.text.strip() if elem_brand else ''
    elem_model = bs_obj.find('span', {'class': 'detail'})
    model = elem_model.text.strip() if elem_model else ''

    if (car_info := bs_obj.find('div', {'class': 'prod_infomain'})) is not None:
        lis = car_info.findAll("li")
        color = lis[6].text.replace('색상:', '').strip()
        _mileage = lis[0].text.replace('주행거리:', '')
        mileage = re.sub('[-=.#,/?:$}Kkm]', '', _mileage).strip()
        yearString = lis[1].text.strip()
        cut_string_1 = yearString.replace('자세히보기', '')
        cut_string_2 = cut_string_1.replace('연식:', '').strip()
        cut_string_3 = cut_string_2.replace('년 ', '.')
        registered_at = '20'+cut_string_3.replace('월식', '')  # 최초 등록일
        if '(' in registered_at:
            model_year = '20'+re.sub('[(년형)]', '', registered_at)[-2:]
            registered_at = registered_at[:7]
        else:
            model_year = registered_at[:4]
        transmission = lis[5].text.replace('변속기:', '').strip()
        fuel = lis[2].text.replace('연료:', '').strip()
        car_number = lis[7].text.replace('차량번호', '').replace(' ', '').strip()

    car_options = bs_obj.find('div', {'class': 'con option_hover'})

    checked_options = bs_obj.findAll('dd', {'class': 'on'})
    # if car_options is not None:
    #    checked_options = bs_obj.findAll('dd', {'class': 'on'})

    _options = [x.find('a') for x in checked_options]
    options: str = '///'.join([x.text.strip() for x in _options if x])

    if bs_obj.find('div', {'class': 'prod_price'}) is not None:
        _price = bs_obj.find('div', {'class': 'prod_price'})
        price_string = _price.find('span', {'class': 'num'}).text
        price = re.sub('[,만원]', '', price_string)

    output = [carid, timestamp, brand+model, car_number, price, mileage,
              color, model_year, registered_at, fuel, transmission, options, '']
    return output


_from = sys.argv[1]  # source directory for html files
_to = sys.argv[2]  # destination directory for csv file
fname = f'encar-{int(time())}.csv'

with open(os.path.join(_to, fname), 'w', encoding='utf-8', newline='') as csv_file:
    write = csv.writer(csv_file)
    for file in [os.path.join(_from, f) for f in os.listdir(_from) if f.endswith('.html')]:
        with codecs.open(file, 'r', 'utf-8') as f:
            bs_obj = BeautifulSoup(f.read(), 'lxml')
            timestamp = file.split('-')[0][0:-3][-10:]
            if (elem_carid := bs_obj.find('input', id='rgsid')) is None:
                continue
            carid = elem_carid.get('value')
            # print('carid:', carid)
            if bs_obj.find('em', {'class': 'ass'}):
                write.writerow(encar_certified_vehicle(
                    bs_obj, timestamp, carid))
            else:
                write.writerow(encar_vehicle(bs_obj, timestamp, carid))
