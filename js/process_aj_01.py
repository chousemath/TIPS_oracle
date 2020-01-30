from typing import List, Sequence, Tuple, Dict
import pandas as pd
from os import listdir, path


def clean_price(in_val: str) -> int:
    in_val = in_val.replace(',', '').strip()
    return int(in_val) * 10_000


def clean_color(in_val: str) -> str:
    return in_val.replace('(변경)', '').strip()


def clean_displacement(in_val: str) -> int:
    in_val = in_val.replace(',', '').replace('cc', '').strip()
    return int(in_val)


def clean_mileage(in_val: str) -> int:
    in_val = in_val.replace('(불분명)', '').strip()
    return int(in_val)


def clean_registered_at(in_val: str) -> str:
    """Output a `registered at` value that conforms to Seula's and Jiyeon's format"""
    # 2016 (20150717)
    words = in_val.replace(')', '').strip().split(' (')
    if len(words) != 2 or len(words[1]) != 8:
        return ''
    return f'{words[1][:4]}.{words[1][4:6]}'


def format_chartjs(in_val: Sequence[Tuple[str, int]]) -> Dict:
    data: List[int] = []
    labels: List[str] = []
    for x in in_val:
        labels.append(x[0])
        data.append(x[1])
    return {'data': data, 'labels': labels}


root = 'csv_aj'
latest = sorted([x for x in listdir(root) if '.csv' in x])[-1]
df = pd.read_csv(path.join(root, latest))
df = df.drop(df.columns[[3, 10, 11, 12, 13, 15]], axis=1)
columns = list(range(len(df.columns)))
df.columns = [
    'plate',
    'vin',
    'registered',
    'fuel',
    'mileage',
    'displacement',
    'category',
    'transmission',
    'color',
    'title',
    'price',


]
df.registered = df.registered.map(clean_registered_at)
df.mileage = df.mileage.map(clean_mileage)
df.color = df.color.map(clean_color)
df.price = df.price.map(clean_price)
df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
df = df[(df.registered != '') & (df.price > 0)]
df_aj = df.drop_duplicates(subset='vin', keep='last', inplace=False)
fuels = [(x, len(df_aj[df_aj.fuel == x].index)) for x in df_aj.fuel.unique()]
categories = [(x, len(df_aj[df_aj.category == x].index))
              for x in df_aj.category.unique()]
transmissions = [(x, len(df_aj[df_aj.transmission == x].index))
                 for x in df_aj.transmission.unique()]
colors = [(x, len(df_aj[df_aj.color == x])) for x in df_aj.color.unique()]
titles = [(x, len(df_aj[df_aj.title == x])) for x in df_aj.title.unique()]
output = {
    'fuels': format_chartjs(fuels),
    'categories': format_chartjs(categories),
    'transmissions': format_chartjs(transmissions),
    'colors': format_chartjs(colors),
    'titles': format_chartjs(titles),
}
