import unicodedata
import json

def normalize(input: str) -> str:
    return unicodedata.normalize('NFC', input)

with open('category_map.json') as json_file:
    categories = json.load(json_file)

with open('fuel_map.json') as json_file:
    fuels = json.load(json_file)

with open('transmission_map.json') as json_file:
    transmissions = json.load(json_file)

with open('color_map.json') as json_file:
    colors = json.load(json_file)

def expand_year(year: str) -> str:
    year = int(year)
    if year > 75:
        return f'19{year}'
    else:
        if year < 10:
            year = f'0{year}'
        return f'20{year}'

def simplify_year(year: str) -> str:
    year = year.split('(')
    if len(year) == 1:
        year = year[0].split(normalize('년'))
        year[1] = year[1].replace(normalize('월식'), '')
    else:
        year_front = year[0].split(normalize('년'))
        year_front[1] = year_front[1].replace(normalize('월식'), '')
        year = year_front + [year[1].replace(normalize('년형)'), '')]
        year[2] = expand_year(year[2])

    year[0] = expand_year(year[0])
    return '_'.join(year)

def simplify_fuel(fuel: str) -> int:
    if fuel in fuels:
        return fuels[fuel]
    return 0

def simplify_transmission(transmission: str) -> int:
    if transmission in transmissions:
        return transmissions[transmission]
    return 0

def simplify_category(category: str) -> int:
    if category in categories:
        return categories[category]
    return 0

def simplify_color(color: str) -> int:
    if color in colors:
        return colors[color]
    return 0


def simplify_displacement(displacement: str) -> int:
    if 'cc' in displacement:
        return int(displacement.replace('cc', ''))
    return 0
