import pymongo
import dotenv
import pathlib
import os
import sys
import json
import csv
import io
from normalize import normalize

known_options = set()
with open ('options.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        opt = row[2].strip()
        if opt:
            known_options.add(normalize(opt))

# load in credentials for mongodb
env_path = pathlib.Path('..') / 'js' / '.env'
dotenv.load_dotenv(dotenv_path=env_path)
client = pymongo.MongoClient(os.environ['MONGODB_URI'])

collection = client.oracle.encar
options = collection.distinct('options')

unknown_options = set()
for option_str in options:
    option_list = [normalize(x.strip()) for x in option_str.split(',')]
    option_list = [x for x in option_list if normalize('만원') not in x]
    for option in option_list:
        if option not in known_options:
            unknown_options.add(option)

with open('unknown_options.csv', mode='w') as out:
    writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for option in unknown_options:
        writer.writerow([option, '???'])

