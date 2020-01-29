import pandas as pd
from os import listdir, path

def clean_registered_at(in_val: str) -> str:
    """Output a `registered at` value that conforms to Seula's and Jiyeon's format"""
    # 2016 (20150717)
    words = in_val.replace(')', '').strip().split(' (')
    if len(words) != 2 or len(words[1]) != 8:
        return ''
    return f'{words[1][:4]}.{words[1][4:6]}'

root = 'csv_aj'
latest = sorted([x for x in listdir(root) if '.csv' in x])[-1]
df = pd.read_csv(path.join(root, latest))
df = df.drop(df.columns[[1, 3, 10, 11, 12, 13, 15]], axis=1)
df.columns = list(range(len(df.columns)))
df[1] = df[1].map(clean_registered_at)
print(df.head())
print(len(df.columns))
