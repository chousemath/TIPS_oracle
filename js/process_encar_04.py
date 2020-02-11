from typing import List, Sequence, Tuple, Dict
from scipy.stats import linregress
import pandas as pd
import numpy as np
from os import listdir, path
import json
import io
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from encar_helper_one import norm, clean_price, clean_title, clean_plate, clean_fuel, clean_transmission, clean_color, clean_registered, clean_mileage, clean_model_year, format_chartjs

font_name = 'NotoSansKR-Regular.otf'
fontprop = fm.FontProperties(fname=font_name, size=10)


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

# Plot timestamp vs price
#fig, ax = plt.subplots(3)
#fig.tight_layout()
#for i, name in enumerate(names[:3]):
#    df_vals = df_encar[df_encar.name == name[0]]
#    ax[i].scatter(df_vals.timestamp, df_vals.price)
#    coef = np.polyfit(df_vals.timestamp, df_vals.price, 1)
#    poly1d_fn = np.poly1d(coef) 
#    ax[i].plot(df_vals.timestamp, df_vals.price, 'yo', df_vals.timestamp, poly1d_fn(df_vals.timestamp), '--k')
#    reg = linregress(df_vals.timestamp, df_vals.price)
#    rvalue = f'r: {round(reg.rvalue, 4)}'
#    pvalue = f'p: {round(reg.pvalue, 4)}'
#    stderr = f'err: {round(reg.stderr, 4)}'
#    ax[i].set_title(f'{name[0]}, ({rvalue}, {pvalue}, {stderr})', fontproperties=fontprop)
#    ax[i].set_xticks([])
#    ax[i].set_xlabel('Unix Timestamp (S)')
#    ax[i].set_yticks([])
#    ax[i].set_ylabel('Price (KRW)')
#
#plt.savefig(path.join('experiments', 'process_encar_04', 'timestamp-price.png'), bbox_inches="tight")

# Plot mileage vs price
fig, ax = plt.subplots(3)
fig.tight_layout()
for i, name in enumerate(names[:3]):
    df_vals = df_encar[df_encar.name == name[0]]
    ax[i].scatter(df_vals.mileage, df_vals.price)
    coef = np.polyfit(df_vals.mileage, df_vals.price, 1)
    poly1d_fn = np.poly1d(coef) 
    ax[i].plot(df_vals.mileage, df_vals.price, 'yo', df_vals.mileage, poly1d_fn(df_vals.mileage), '--k')
    reg = linregress(df_vals.mileage, df_vals.price)
    rvalue = f'r: {round(reg.rvalue, 4)}'
    pvalue = f'p: {round(reg.pvalue, 4)}'
    stderr = f'err: {round(reg.stderr, 4)}'
    ax[i].set_title(f'{name[0]}, ({rvalue}, {pvalue}, {stderr})', fontproperties=fontprop)
    ax[i].set_xticks([])
    ax[i].set_xlabel('Mileage (KM)')
    ax[i].set_yticks([])
    ax[i].set_ylabel('Price (KRW)')

plt.savefig(path.join('experiments', 'process_encar_04', 'mileage-price.png'), bbox_inches="tight")
