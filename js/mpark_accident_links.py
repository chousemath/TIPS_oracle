from bs4 import BeautifulSoup
from typing import List
from os import listdir, path

target = 'openCarPerformance'
root = 'html_src_mpark'
links: List[str] = []
for fpath in [path.join(root, fname) for fname in listdir(root) if '.html' in fname]:
    with open(fpath, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        nums = [a.get('href').replace(';', '').replace('javascript:openCarPerformance', '').replace('(', '').replace(')', '').replace("'", '') for a in soup.find_all('a', href=True) if target in a.get('href')]
        links.extend([f'http://www.m-park.co.kr/car_popup/CarCheck_180702.asp?CheckNo={num}' for num in nums])
with open('mpark_accident_links.txt', 'w') as writer:
    for link in links:
        writer.write(f'{link}\n')
