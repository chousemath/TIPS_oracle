import pandas as pd
import numpy as np
from datetime import datetime as dt
import os
import unicodedata as ud
import urllib.parse
import json
import io


def norm(input: str) -> str:
    return ud.normalize('NFC', urllib.parse.unquote(input))

names = [
    'timestamp',
    'item_id',
    'target_value', # price
    'modelyear',
    'regist_year',
    'mileage',
    'transmission',
    'fuel',
    'plate_num',
    'color',
    'noaccident',
    'yeswarranty',
    'options'
]
df = pd.read_csv('carmanager.csv', sep=',', names=names)
with open('allowed_by_color.json') as json_file:
    allowed = json.load(json_file)

def item_id(row) -> str:
    return norm(row.get('item_id', '').strip())

def _color(row) -> str:
    c = row.get('color', '')
    if not isinstance(c, str):
        return ''
    return norm(c.strip())

def _transmission(row) -> str:
    t = row.get('transmission', '')
    if not isinstance(t, str):
        return ''
    return norm(t.strip())

def no_accident(row) -> str:
    if row.get('noaccident', 0) == 0:
        return 'acc'
    else:
        return 'noacc'

def yes_warranty(row) -> str:
    if row.get('yeswarranty', 0) == 0:
        return 'nowarr'
    else:
        return 'warr'

def gen_nm_yr_color(row) -> str:
    nm = row.get('item_id', 'xxx').strip()
    yr = str(row.get('modelyear', 'xxx')).strip()
    color = str(row.get('color', 'xxx')).strip()
    transmission = str(row.get('transmission', 'xxx')).strip()
    return norm(f'{nm or "xxx"} {yr or "xxx"} {color or "xxx"} {transmission or "xxx"}')

df['noaccident'] = df.apply(lambda x: no_accident(x), axis=1)
df['color'] = df.apply(lambda x: _color(x), axis=1)
df['item_id'] = df.apply(lambda x: item_id(x), axis=1)
df['transmission'] = df.apply(lambda x: _transmission(x), axis=1)
df['yeswarranty'] = df.apply(lambda x: yes_warranty(x), axis=1)
df['name_year_color'] = df.apply(lambda x: gen_nm_yr_color(x), axis=1)
df = df[~df['name_year_color'].str.contains('xxx')]

df = df[['item_id', 'modelyear', 'color', 'noaccident', 'yeswarranty', 'transmission']]
df = df.dropna()
df.drop_duplicates(inplace=True)

transmissions = {}
colors = {}
accidents = {}
warranties = {}
years = {}

for _, row in df.iterrows():
    id = row['item_id']
    color = row['color']
    accident = row['noaccident']
    warranty = row['yeswarranty']
    transmission = row['transmission']
    year = str(row['modelyear'])

    n1 = f'{id} {color}'
    n2 = f'{id} {color} {transmission}'
    n3 = f'{id} {color} {transmission} {accident}'
    n4 = f'{id} {color} {transmission} {accident} {warranty}'

    if id in colors:
        colors[id][color] = 1
    else:
        colors[id] = {color: 1}

    if n1 in transmissions:
        transmissions[n1][transmission] = 1
    else:
        transmissions[n1] = {transmission: 1}

    if n2 in accidents:
        accidents[n2][accident] = 1
    else:
        accidents[n2] = {accident: 1}

    if n3 in warranties:
        warranties[n3][warranty] = 1
    else:
        warranties[n3] = {warranty: 1}

    if n4 in years:
        years[n4][year] = 1
    else:
        years[n4] = {year: 1}

color_keys = colors.keys()
for k in allowed:
    allowed[k] = 1 if len([x for x in color_keys if x.startswith(k)])>0 else 0

with io.open('carmanager_allowed.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(allowed, ensure_ascii=False, indent=4))
with io.open('carmanager_colors.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(colors, ensure_ascii=False, indent=4))
with io.open('carmanager_transmissions.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(transmissions, ensure_ascii=False, indent=4))
with io.open('carmanager_accidents.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(accidents, ensure_ascii=False, indent=4))
with io.open('carmanager_warranties.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(warranties, ensure_ascii=False, indent=4))
with io.open('carmanager_years.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(years, ensure_ascii=False, indent=4))

