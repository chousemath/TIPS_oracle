import pandas as pd
from os import listdir, path

root = 'csv_aj'
latest = sorted([x for x in listdir(root) if '.csv' in x])[-1]
df = pd.read_csv(path.join(root, latest))
df = df.drop(df.columns[[1, 3, 12, 13, 15]], axis=1)

print(df.head())
