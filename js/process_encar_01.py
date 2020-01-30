from typing import List, Sequence, Tuple, Dict
import pandas as pd
from os import listdir, path
import json
import unicodedata as ud
import io
from operator import itemgetter

def norm(in_val: str) -> str:
    return ud.normalize('NFC', str(in_val)).strip()

def clean_price(in_val: str) -> int:
    return int(in_val) * 10_000

def clean_title(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()

def clean_plate(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()

def clean_fuel(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()

def clean_transmission(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()

def clean_color(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()

def clean_registered(in_val: str) -> str:
    return str(in_val).replace('자세히보기', '').strip()

def clean_mileage(in_val: str) -> int:
    return int(in_val)

def clean_model_year(in_val: str) -> int:
    return int(in_val)

def format_chartjs(in_val: Sequence[Tuple[str, int]]) -> Dict:
    data: List[int] = []
    labels: List[str] = []
    for x in in_val:
        labels.append(x[0])
        data.append(x[1])
    return {'data': data, 'labels': labels}

root = 'csv_encar'
latest = sorted([x for x in listdir(root) if '.csv' in x])[-1]
df = pd.read_csv(path.join(root, latest)).dropna()
df = df.drop(df.columns[[0, -1]], axis=1)
df.columns = ['title', 'plate', 'price', 'mileage', 'color', 'model_year', 'registered', 'fuel', 'transmission']
df_aj = df.drop_duplicates(subset='plate', keep='last', inplace=False)
df.title = df.title.map(clean_title)
df.plate = df.plate.map(clean_plate)
df.price = df.price.map(clean_price)
df.mileage = df.mileage.map(clean_mileage)
df.color = df.color.map(clean_color)
df.model_year = df.model_year.map(clean_model_year)
df.registered = df.registered.map(clean_registered)
df.fuel = df.fuel.map(clean_fuel)
df.transmission = df.transmission.map(clean_transmission)
df_encar = df[(df.plate != '') & (df.price > 0)]
fuels = [(norm(x), len(df_encar[df_encar.fuel == x].index)) for x in df_encar.fuel.unique()]
transmissions = [(norm(x), len(df_encar[df_encar.transmission == x].index))
                 for x in df_encar.transmission.unique()]
colors = [(norm(x), len(df_encar[df_encar.color == x])) for x in df_encar.color.unique()]
titles = [(norm(x), len(df_encar[df_encar.title == x])) for x in df_encar.title.unique()]
model_years = [(norm(x), len(df_encar[df_encar.model_year == x])) for x in df_encar.model_year.unique()]
registereds = [(norm(x), len(df_encar[df_encar.registered == x])) for x in df_encar.registered.unique()]

fuels.sort(key=itemgetter(1), reverse=True)
transmissions.sort(key=itemgetter(1), reverse=True)
colors.sort(key=itemgetter(1), reverse=True)
titles.sort(key=itemgetter(1), reverse=True)
registereds.sort(key=itemgetter(1), reverse=True)

output = {
    'fuels': format_chartjs(fuels),
    'transmissions': format_chartjs(transmissions),
    'colors': format_chartjs(colors),
    'titles': format_chartjs(titles),
    'model_years': format_chartjs(model_years),
    'registereds': format_chartjs(registereds),
}

with io.open(path.join('..', 'overview_encar.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(output, ensure_ascii=False))

