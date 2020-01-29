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

root = 'csv_aj'
latest = sorted([x for x in listdir(root) if '.csv' in x])[-1]
df = pd.read_csv(path.join(root, latest))
df = df.drop(df.columns[[1, 3, 10, 11, 12, 13, 15]], axis=1)
df.columns = list(range(len(df.columns)))
df[1] = df[1].map(clean_registered_at)
df[3] = df[3].map(clean_mileage)
df[7] = df[7].map(clean_color)
df[9] = df[9].map(clean_price)
df_aj = df.drop_duplicates(subset=[0])
print(df_aj.head())

# organize cars by plate number
#for plate_num in df[0].unique():
#    df_temp = df.loc[df[0] == plate_num]
#    print(df_temp.head())
