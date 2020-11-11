from os import path
import csv
import sys
import pandas as pd
from pandas import DataFrame
from time import time

if __name__ == '__main__':
    path_csv_details = sys.argv[1]
    path_csv_accidents = sys.argv[2]
    dir_output = sys.argv[3]
    details = pd.read_csv(path_csv_details, header=None)
    details.columns = ['carid', 'timestamp', 'brand+model', 'car_number', 'price', 'mileage',
                       'color', 'model_year', 'registered_at', 'fuel', 'transmission', 'options', 'accident']
    details = details.drop(['options'], axis=1)
    accidents = pd.read_csv(path_csv_accidents, header=None)
    accidents.columns = ['carid', 'accident', 'vin']
    merged = pd.merge(accidents, details, on=['carid'], how='right')
    merged = merged.fillna('')
    merged['accident'] = merged[['accident_x', 'accident_y']].apply(
        lambda x: ''.join([str(y) for y in x]), axis=1)
    merged = merged.drop(['accident_x', 'accident_y'], axis=1)
    fname = f'encar-combined-{int(time())}.csv'
    dataframe = pd.DataFrame(merged)
    dataframe.to_csv(path.join(dir_output, fname), index=False)
