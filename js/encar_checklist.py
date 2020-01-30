from typing import Type, List
import sys
from bs4 import BeautifulSoup
import codecs
import csv
import os
import re
from time import time

acc_map = {'있음': 1, '없음': 2}


def encar_checklist(bs_obj: Type[BeautifulSoup], carid: str) -> List:
    car_no = ''
    if (car_info := bs_obj.find('div', {'class': 'inspec_carinfo'})) is not None:
        tbody = car_info.find('tbody')
        for tr in tbody.findAll('tr'):
            if tr.findAll('th')[1].text == '차대번호':
                car_no = tr.findAll('td')[1].text
                break

    trs = bs_obj.find('div', {'class': 'section_repair'}).findAll("tr")
    for tr in trs:
        if (item := tr.find('th')) is not None:
            if '사고이력' in item.text and (accident_item := tr.find('span', {'class': 'txt_state on'})) is not None:
                return [carid, acc_map.get(accident_item.text, 3), car_no]
    return []


def encar_checklist_img(table: Type[BeautifulSoup], carid: str) -> List:
    tbody = table.find('tbody')
    trs = tbody.find('tr')
    tds = trs.findAll('td')
    return [carid, acc_map.get(tds[0].text, 3), '']


if __name__ == '__main__':
    _from = sys.argv[1]  # source directory for html files
    _to = sys.argv[2]  # destination directory for csv file
    fname = f'encar-checklist-{int(time())}.csv'
    with open(os.path.join(_to, fname), 'w', encoding='utf-8', newline='') as csv_file:
        write = csv.writer(csv_file)
        for file in os.listdir(_from):
            with open(os.path.join(_from, file)) as f:
                carid = file.replace('.html', '')
                bs_obj = BeautifulSoup(f, 'lxml')
                if bs_obj.find('div', {'class': 'section_repair'}):
                    if len(data := encar_checklist(bs_obj, carid)) > 0:
                        write.writerow(data)
                elif (table := bs_obj.find('table', {"class", 'spc_info2 tbl_photo'})):
                    write.writerow(encar_checklist_img(table, carid))
