import pymongo
import dotenv
import pathlib
import os
import unicodedata
import json
import io

def normalize(input: str) -> str:
    return unicodedata.normalize('NFC', input)

# load in colors that have already been mapped
mapping_path = pathlib.Path('..') / 'mappings' / 'colors_to_numbers.json'
with open(mapping_path) as mapped_colors_file:
    mapped_colors = json.load(mapped_colors_file)
# load in credentials for mongodb
env_path = pathlib.Path('..') / 'js' / '.env'
dotenv.load_dotenv(dotenv_path=env_path)
client = pymongo.MongoClient(os.environ['MONGODB_URI'])

collection = client.oracle.encar
colors = collection.distinct('color')

unmapped_colors = {'colors': []}
for color in colors:
    color = normalize(color)
    skip = False
    for key in mapped_colors:
        if normalize(key) in color:
            skip = True
            break
    if not skip:
        unmapped_colors['colors'].append(color)

with io.open('unmapped_colors.json', 'w') as output:
    output.write(json.dumps(unmapped_colors, ensure_ascii=False))
    

