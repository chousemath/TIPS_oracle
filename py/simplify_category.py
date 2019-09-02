import csv
import os
import io
import json
from normalize import normalize

val = 1
mapping = {}
with open(os.path.join(os.getcwd(), 'categories.csv')) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        if len(row) < 1:
            continue
        fuel = normalize(row[0])
        mapping[fuel] = val
        val += 1

print(mapping)

with io.open('category_map.json', 'w') as output:
    output.write(json.dumps(mapping, ensure_ascii=False))




