# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import codecs
import csv
import os
import re
from time import time


def encar_certified_vehicle(bs_obj, timestamp):
    brand = ''
    model = ''
    mileage = ''
    color = ''
    transmission = ''
    car_number = ''
    fuel = ''
    model_year = ''
    price = ''
    checked_options_list = []
    registered_at = ''

    if bs_obj.find("span", {"class": "brand"}) is not None:
        brand = bs_obj.find("span", {"class": "brand"}).text
    if bs_obj.find("span", {"class": "detail"}) is not None:
        model = bs_obj.find("span", {"class": "detail"}).text.strip()
    if bs_obj.find("ul", {"class": "list_carinfo"}) is not None:
        car_info = bs_obj.find("ul", {"class": "list_carinfo"})
        lis = car_info.findAll("li")
        color = lis[6].text.replace("색상:", "")
        _mileage = lis[0].text.replace("주행거리:", "")
        mileage = re.sub('[-=.#,/?:$}Kkm]', '', _mileage).strip()
        yearString = lis[1].text.strip()
        cut_string_1 = yearString.replace("자세히보기", "").strip()
        cut_string_2 = cut_string_1.replace("연식:", "").strip()
        cut_string_3 = cut_string_2.replace("년 ", ".")
        registered_at = "20"+cut_string_3.replace("월식", "")

        if "(" in registered_at:
            model_year = "20"+re.sub('[(년형)]', '', registered_at)[-2:]
            registered_at = registered_at[:7]
        else:
            model_year = registered_at[:4]

        transmission = lis[5].text.replace("변속기:", "").strip()
        fuel = lis[2].text.replace("연료:", "").strip()
    if bs_obj.find("div", {"id": "area_options view"}) is not None:
        car_options = bs_obj.find("div", {"id": "area_options view"})
    if bs_obj.findAll("dd", {"class": "on"}) is not None:
        checked_options = bs_obj.findAll("dd", {"class": "on"})
    if bs_obj.find("strong", {"class", "tit_inspect"}) is not None:
        _accident = bs_obj.find("strong", {"class", "tit_inspect"})
        accident = _accident.find("em", {"class", "emph_g"}).text
    if lis[7] is not None:
        car_number = lis[7].text.replace("차량번호", "").replace(" ", "").strip()
    if bs_obj.find("em", {"class", "emph_price"}) is not None:
        _price = bs_obj.find("em", {"class", "emph_price"})
        price = _price.find(
            "span", {"class", "txt_num"}).text.replace(",", "").strip()

    for option_item in checked_options:
        item = option_item.find("a")
        if item is not None:
            item_text = item.text.strip()
            checked_options_list.append(item_text)
    return [timeStamp, brand+model, car_number, price, mileage, color, model_year, registered_at, fuel, transmission, checked_options_list]


def encar_vehicle(bs_obj, timeStamp):
    # brand, model, mileage, color, transmission, car_number, fuel = ''
    brand = ''
    model = ''
    mileage = ''
    color = ''
    transmission = ''
    car_number = ''
    fuel = ''
    registered_at = ''
    model_year = ''
    price = ''
    checked_options_list = []
    if bs_obj.find("span", {"class": "brand"}) is not None:
        brand = bs_obj.find("span", {"class": "brand"}).text.strip()
    if bs_obj.find("span", {"class": "detail"}) is not None:
        model = bs_obj.find("span", {"class": "detail"}).text.strip()
    if bs_obj.find("div", {"class": "prod_infomain"}) is not None:
        car_info = bs_obj.find("div", {"class": "prod_infomain"})
        lis = car_info.findAll("li")
        color = lis[6].text.replace("색상:", "").strip()
        _mileage = lis[0].text.replace("주행거리:", "")
        mileage = re.sub('[-=.#,/?:$}Kkm]', '', _mileage).strip()
        yearString = lis[1].text.strip()
        cut_string_1 = yearString.replace("자세히보기", "")
        cut_string_2 = cut_string_1.replace("연식:", "").strip()
        cut_string_3 = cut_string_2.replace("년 ", ".")
        registered_at = "20"+cut_string_3.replace("월식", "")  # 최초 등록일
        if "(" in registered_at:
            model_year = "20"+re.sub('[(년형)]', '', registered_at)[-2:]
            registered_at = registered_at[:7]
        else:
            model_year = registered_at[:4]
        transmission = lis[5].text.replace("변속기:", "").strip()
        fuel = lis[2].text.replace("연료:", "").strip()
        car_number = lis[7].text.replace("차량번호", "").replace(" ", "").strip()
    if bs_obj.find("div", {"class": "con option_hover"}) is not None:
        car_options = bs_obj.find("div", {"class": "con option_hover"})
    if bs_obj.findAll("dd", {"class": "on"}) is not None:
        checked_options = bs_obj.findAll("dd", {"class": "on"})
        for option_item in checked_options:
            item = option_item.find("a")
            if item is not None:
                item_text = item.text.strip()
                checked_options_list.append(item_text)

    if bs_obj.find("div", {"class": "prod_price"}) is not None:
        _price = bs_obj.find("div", {"class": "prod_price"})
        price_string = _price.find("span", {"class": "num"}).text
        price = re.sub('[,만원]', '', price_string)
    if bs_obj.find("div", {"id": "wrapInsp"}) is not None:
        wrap_insp = bs_obj.find("div", {"id": "wrapInsp"})
        result_lists = wrap_insp.findAll("dl", {"class", "result_list"})
        for result_item in result_lists:
            item = result_item.find(
                "span", {"class", "t"}).text.replace("자세히보기", "").strip()
            if item == "사고이력":
                accident = result_item.find("dd", {"id", "txtInspAcc"})
    return [timeStamp, brand+model, car_number, price, mileage, color, model_year, registered_at, fuel, transmission, checked_options_list]


_from = sys.argv[1]  # source directory for html files
_to = sys.argv[2]  # destination directory for csv file
fname = f'encar-{int(time())}.csv'

with open(os.path.join(_to, fname), 'w', encoding='utf-8', newline='') as csv_file:
    write = csv.writer(csv_file)
    for file in [os.path.join(_from, f) for f in os.listdir(_from) if f.endswith('.html')]:
        with codecs.open(file, 'r', 'utf-8') as f:
            bs_obj = BeautifulSoup(f.read(), 'lxml')
            checked_vehicle = bs_obj.find('em', {'class': 'ass'})
            timeStamp = file.split('-')[0][0:-3]
            if checked_vehicle is not None:
                write.writerow(encar_certified_vehicle(bs_obj, timeStamp))

            else:
                write.writerow(encar_vehicle(bs_obj, timeStamp))
