import os
from bs4 import BeautifulSoup
import shutil

path='./pages_detail/'
destination_path='./encar_bmw5series/'
file_list = os.listdir(path)
for file in file_list:
    if file.endswith('.html'):
        with open(path+file) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            htmltext = soup.get_text()
            if htmltext.find('5시리즈') >0 and htmltext.find('BMW') >0:
                print(file)
                print('ok')
                shutil.copy(path+file, destination_path+file)


