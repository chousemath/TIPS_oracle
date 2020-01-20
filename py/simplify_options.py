import pandas as pd
import os
root = os.getcwd()


df = pd.read_csv(os.path.join(root, 'all_options.csv'))
s = df['options'].map(lambda x: str(x))
s = s.map(lambda x: x.split('\n')[0])
print(type(s))
s_with_commas = s[s.str.contains(',')]
print(s_with_commas.size)
for x in s_with_commas.head(100).tolist():
    print(x)
