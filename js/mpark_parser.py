import os
import re
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from bs4 import BeautifulSoup, Comment

# input : html files
# output : csv 파일 (단, 테이블 헤더(칼럼)는 포함하지 않음)


def cleanNum(x: str):
    if(x):
        return re.sub("\D+", "", x)
    else:
        return ''


def export_csv(_from: str, _to: str):
    file_list = os.listdir(_from)
    results = []  # csv 파일로 출력할 배열. (차량을 파싱한 데이터)
    for html in file_list:
        with open(_from+'/'+html) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # 주석 제거하는 코드  (필수! => 옵션정보 얻어올 때. 주석이 읽하는 경우 있음.)
        for comments in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comments.extract()

        # html 파일명으로부터 파일생성 time_stamp 추출 // 파일명 형태 : (UnixTimeStamp_ms-랜덤숫자)
        # OR time_stamp = int(int(html.split('-')[0])/1000)
        time_stamp = html.split('-')[0][0:-3]

        # 타이틀 정보 (브랜드/모델/세대)
        title = soup.find('h4', class_='tit').text

        # 가격형성에 기준이 되는 기종명 찾을 때 까지 보류. 일단 전체 수집.
        # generation = title.find('em').text
        # make = title.text.split(' ')[0]
        # model = title.text.rstrip(generation).split(' ')[1]

        # 차량 정보
        all_table = soup.find_all('table')
        info_headers = [header.text.strip()
                        for header in all_table[0].find_all('th')]
        info = {info_headers[i]: cell.text.strip()
                for i, cell in enumerate(all_table[0].find_all('td'))}

        mileage = cleanNum(info.get('주행거리', ''))
        color = info.get('색상', '').strip()
        model_year = cleanNum(info.get('연식', ''))
        price = cleanNum(soup.find('p', class_='price').text)
        plate_num = info.get('차량번호', '')
        fuel = info.get('연료', '')
        transmission = info.get('변속기', '')

        # 성능검사 정보
        check_headers = [header.text.strip()
                         for header in all_table[2].find_all('th')]
        check = {check_headers[i]: cell.text.strip()
                 for i, cell in enumerate(all_table[2].find_all('td'))}

        accident = True if check.get('사고유무 (단순수리제외)', '유') == '유' else False

        # 옵션정보
        options = [opt.find(text=True).strip()
                   for opt in soup.select('div.op_cont li.on')]

        # 출력 순서
        # time_stamp: int (seconds)
        # 제목 : str (브랜드 모델 세대 세부모델 ... )
        # 번호판 : str
        # 가격 : int
        # 주행거리 : int
        # 컬러 : str
        # 형식년도 : int
        # 사고유무 : boolean
        # 연료 : str             ### 항목명 추후 협의
        # 변속기 : str            ### 항목명 추후 협의
        # 옵션 : list [str]      ### 항목명 추후 협의

        # result =[time_stamp, title,plate_num, price, mileage, color, model_year, accident, fuel, transmission, options if len(options)>0 else None]
        result = [time_stamp, title, plate_num, price, mileage,
                  color, model_year, accident, fuel, transmission, options]
        results.append(result)

    # csv 파일로 출력
    file_stamp = datetime.today().strftime("%Y-%m-%d_%H:%M")  # 파일 만든날짜 기입
    file_name = _to+'/mpark_'+file_stamp+'.csv'
    dataframe = pd.DataFrame(results)
    dataframe.to_csv(file_name, header=None, index=False)
    print('Done. => '+file_name)
