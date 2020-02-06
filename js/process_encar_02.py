from typing import List, Sequence, Tuple, Dict
import pandas as pd
from os import listdir, path
import json
import unicodedata as ud
import io
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_name = 'NotoSansKR-Regular.otf'
fontprop = fm.FontProperties(fname=font_name, size=10)


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


def clean_model_year(in_val: str) -> str:
    return str(in_val)


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
df.columns = ['car_id', 'timestamp', 'title', 'plate', 'price', 'mileage', 'color',
              'model_year', 'registered', 'fuel', 'transmission', 'options', 'accident']

df_encar = df.drop_duplicates(subset='plate', keep='last', inplace=False)
df_encar.title = df_encar.title.map(clean_title)
df_encar.plate = df_encar.plate.map(clean_plate)
df_encar.price = df_encar.price.map(clean_price)
df_encar.mileage = df_encar.mileage.map(clean_mileage)
df_encar.color = df_encar.color.map(clean_color)
df_encar.model_year = df_encar.model_year.map(clean_model_year)
df_encar.registered = df_encar.registered.map(clean_registered)
df_encar.fuel = df_encar.fuel.map(clean_fuel)
df_encar.transmission = df_encar.transmission.map(clean_transmission)
df_encar = df_encar[(df_encar.plate != '') & (
    df_encar.price > 0) & (df_encar.timestamp > 0)]
df_encar['name'] = df_encar['title'].astype(
    str) + df_encar['model_year'].astype(str)

names = [(norm(x), len(df_encar[df_encar.name == x]))
         for x in df_encar.name.unique()]

names.sort(key=itemgetter(1), reverse=True)

# select the top 4 most numerous car models
fig, ax = plt.subplots(4)
fig.tight_layout()
for i, name in enumerate(names[:4]):
    df_vals = df_encar[df_encar.name == name[0]]
    ax[i].scatter(df_vals.timestamp, df_vals.price)
    ax[i].set_title(name[0], fontproperties=fontprop)
    ax[i].set_xticks([])
    ax[i].set_yticks([])


plt.savefig(path.join('experiments', 'process_encar_02',
                      'timeseries.png'), bbox_inches="tight")
