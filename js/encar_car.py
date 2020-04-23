from typing import Type, List
import sys
from bs4 import BeautifulSoup
import codecs
import csv
import os
import re
from time import time
import shutil
from random import shuffle

_from = sys.argv[1]  # source directory for html files
_to = sys.argv[2]  # destination directory for csv file


files = os.listdir(_from)
shuffle(files)

for file in files:
    if file.endswith('.html'):
        try:
            with open(_from+file) as f:
                bs_obj = BeautifulSoup(f.read(), 'lxml')
                elem_brand = bs_obj.find('span', {'class': 'brand'})
                if elem_brand is not None:
                    brand = elem_brand.text.strip()
                    if '5시리즈' in brand and 'BMW' in brand:
                        print(brand)
                        to_path = os.path.join(_to, file)
                        if os.path.exists(to_path):
                            print('\t * already exists, skipping...')
                        shutil.copy(os.path.join(_from, file), to_path)
        except Exception as e:
            print(str(e))
