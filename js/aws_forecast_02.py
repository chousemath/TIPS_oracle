import pandas as pd
import numpy as np
from datetime import datetime as dt
import os
import unicodedata as ud
import urllib.parse
import json
import io
from math import ceil


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

def gen_mileage_tag(mileage: int) -> int:
    return 10_000 * ceil(mileage / 10_000)

def gen_item_id(row) -> str:
    nm = row.get('item_id', 'xxx').strip()
    yr = str(row.get('modelyear', 'xxx')).strip()
    color = str(row.get('color', 'xxx')).strip()
    transmission = str(row.get('transmission', 'xxx')).strip()
    accident = str(row.get('accident', 'xxx')).strip()
    #warranty = str(row.get('warranty', 'xxx')).strip()
    mileage_tag = gen_mileage_tag(row.get('mileage', 0))
    return norm(f'{nm} {color} {accident} {yr} {mileage_tag}')
    #return norm(f'{nm} {color} {transmission} {accident} {warranty} {yr}')
    #return norm(f'{nm} {color} {transmission} {accident} {warranty} {yr} {mileage_tag}')


def adjust_price(row) -> int:
    return int(row.get('target_value', 0))

#df = df[['timestamp', 'target_value', 'item_id', 'modelyear', 'color', 'transmission', 'mileage', 'accident', 'warranty']]
df = df[['timestamp', 'plate_num']]
df = df.dropna()
df = df.sort_values(by=['timestamp'])

df.to_csv('carmanager_forecast.csv', index=False, header=False)
headers = list(df.columns.values)
attributes = []
for h in headers:
    t = str(df[h].dtype)
    if h == 'timestamp':
        t = 'timestamp'
    elif t == 'object':
        t = 'string'
    elif t == 'int64':
        t = 'integer'

    attributes.append({
        #"AttributeName": option_alias[h] if h in option_alias else h,
        "AttributeName": h,
        "AttributeType": t,
    })

with io.open('carmanager_forecast.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps({'Attributes': attributes}, ensure_ascii=False, indent=4))

#with io.open('option_alias.json', 'w', encoding='utf-8') as f:
#    f.write(json.dumps(option_alias, ensure_ascii=False, indent=4))
#
