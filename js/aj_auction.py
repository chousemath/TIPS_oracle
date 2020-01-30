from typing import List
from bs4 import BeautifulSoup as BS
from os import listdir, path
from sys import argv, exit
from csv import writer
from time import time


headers = ['title', 'model_year', 'mileage', 'transmission', 'fuel', 'color', 'submission_number', 'plate', 'parking_location', 'lane', 'registered', 'rating', 'category', 'starting_price', 'status', 'result', 'final_price']
removed = ['관심물품등록', '후상담 신청', '부재자 응찰', '자동차등록증']
if __name__ == '__main__':
    if len(argv) != 3:
        print('\nYou are using this script incorrectly')
        print('Instructions: python aj_auction.py <SOURCE_DIR> <DESTINATION_DIR>')
        print('Example usage: python aj_auction.py html_src_aj csv_aj_auction\n')
        exit()
    full_data: List[List] = []
    for fpath in [path.join(argv[1], x) for x in listdir(argv[1]) if '.html' in x]:
        try:
            with open(fpath, 'r') as f:
                soup = BS(f, 'lxml')
                cars = soup.find_all('div', class_='car-details')
                for car in cars:
                    t = car.text
                    if '경매결과' not in t:
                        continue
                    data = [x.strip() for x in t.replace('  ', '').replace('\t', '').split('\n') if x.strip()]
                    data = [x for x in data if x not in removed]
                    result = data[:15] + data[16:]
                    if len(result) < 17:
                        result.append('0')
                    result[0] = ' '.join(result[0].split(' ')[1:]).strip() # clean up the title
                    result[1] = int(result[1])
                    result[2] = int(result[2].replace(',', '').replace('km', '').strip())
                    result[6] = result[6].replace('출품번호 :', '').strip()
                    result[7] = result[7].replace('차량번호 :', '').strip()
                    result[8] = result[8].replace('주차구역 :', '').strip()
                    result[9] = result[9].replace('레인 :', '').strip()
                    result[10] = result[10].replace('최초등록일 :', '').strip()
                    result[11] = result[11].replace('평가점 :', '').strip()
                    result[12] = result[12].replace('경력 :', '').strip()
                    result[13] = int(result[13].replace(',', '').replace('"', '').replace('시작가 :', '').strip())
                    result[14] = result[14].replace('진행상태 :', '').strip()
                    result[16] = int(result[16].replace(',', '').replace('희망가 :', '').replace('(', '').replace(')', '').strip())
                    full_data.append(result)
        except Exception as e:
            print(str(e))
    name = f'ajauction-{int(time())}.csv'
    with open(path.join(argv[2], name), 'w', newline='') as f:
        wr = writer(f)
        full_data.insert(0, headers)
        wr.writerows(full_data)
