import csv
import os
from normalize import normalize

def expand_year(year: str) -> str:
    year = int(year)
    if year > 75:
        return f'19{year}'
    else:
        if year < 10:
            year = f'0{year}'
        return f'20{year}'

def convert_year(year: str) -> str:
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


with open(os.path.join(os.getcwd(), 'year_examples.csv')) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for row in csv_reader:
        print(convert_year(normalize(row[0])))





