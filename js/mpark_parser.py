from typing import Dict
import os
import re
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from bs4 import BeautifulSoup, Comment

# input : html files
# output : csv 파일 (단, 테이블 헤더(칼럼)는 포함하지 않음)


def cleanNum(x: str) -> str:
    return re.sub('\D+', '', x) if (x) else ''


accident_codes = {
    '유': 1,
    '무': 2,
}


def get_check_details(root: str):  # 성능점검표에서 차대번호, 최초등록일 파싱
    try:
        with open(root) as fp2:
            record_soup = BeautifulSoup(fp2, 'lxml')
            # table로 조회시 차대번호 누락되는 문제 있음.
            record_tr = record_soup.find_all('tr')
            vin = record_tr[3].find('td').text
            registered_at = record_tr[2].find('td').text
            return vin, registered_at
    except FileNotFoundError as e:
        # print (e)
        return '', ''


def get_info(is_certified: bool, tables: Dict):
    if (is_certified):
        info_headers = [header.text.strip()
                        for header in tables[1].find_all('th')]
        return {info_headers[i]: cell.text.strip()
                for i, cell in enumerate(tables[1].find_all('td'))}
    else:
        info_headers = [header.text.strip()
                        for header in tables[0].find_all('th')]
        return {info_headers[i]: cell.text.strip()
                for i, cell in enumerate(tables[0].find_all('td'))}


def get_check(is_certified: bool, tables: Dict):
    if (is_certified):
        check_headers = [header.text.strip()
                         for header in tables[3].find_all('th')]
        return {check_headers[i]: cell.text.strip()
                for i, cell in enumerate(tables[3].find_all('td'))}
    else:
        check_headers = [header.text.strip()
                         for header in tables[2].find_all('th')]
        return {check_headers[i]: cell.text.strip()
                for i, cell in enumerate(tables[2].find_all('td'))}


def export_csv(_from: str, _to: str):
    file_list = os.listdir(_from)
    results = []  # csv 파일로 출력할 배열. (차량을 파싱한 데이터)
    for html in file_list:
        with open(_from+'/'+html) as fp:
            soup = BeautifulSoup(fp, 'lxml')

        # 주석 제거하는 코드  (필수! => 옵션정보 얻어올 때. 주석이 읽하는 경우 있음.)
        for comments in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comments.extract()

        try:
            # html 파일명으로부터 파일생성 time_stamp 추출 // 파일명 형태 : (UnixTimeStamp_ms-랜덤숫자)
            time_stamp = html.split('-')[0][0:-3]

            # 타이틀 정보 (브랜드/모델/세대/상세정보)
            title = soup.find('h4', class_='tit').text
            # 전체 수집 후 특정 학습할 모델별로 필터링 하여 전처리 할 예정.
            # generation = title.find('em').text
            # make = title.text.split(' ')[0]
            # model = title.text.rstrip(generation).split(' ')[1]

            # [일반매물 vs 인증매물 구분] 및 테이블 데이터 수집.
            certified_car = True if soup.find(
                'h4', class_='blind', string='인증 중고차') else False
            tables = soup.find_all('table')

            # 차량정보
            info = get_info(certified_car, tables)
            mileage = cleanNum(info.get('주행거리', ''))
            color = info.get('색상', '').strip()
            model_year = cleanNum(info.get('연식', ''))
            price = cleanNum(soup.find('p', class_='price').text)
            plate_num = info.get('차량번호', '')
            fuel = info.get('연료', '')
            transmission = info.get('변속기', '')

            # 성능검사 정보
            check = get_check(certified_car, tables)
            accident = accident_codes.get(check.get('사고유무 (단순수리제외)', ''), 3)

            # 성능점검표 페이지에서 차대번호(vin), 최초등록일 (registered_at) 가져오기.
            check_source = soup.find(
                'a', class_='btn btn_ty05', string='성능·상태 점검기록부 보기').get('href', '')
            check_num = check_source.split("'")[1] if check_source else ''
            root = os.path.join('mpark_accident_reports', f'{check_num}.html')
            check_details = get_check_details(root)

            vin = check_details[0]
            registered_at = check_details[1]

            # 옵션정보
            options = [opt.find(text=True).strip()
                       for opt in soup.select('div.op_cont li.on')]

            # 출력 순서
            # time_stamp: int (seconds)
            # 제목 : str (브랜드 모델 세대 세부모델 ... )
            # 번호판 : str
            # 차대번호 : str
            # 가격 : int
            # 주행거리 : int
            # 컬러 : str
            # 형식년도 : int
            # 최초등록일 : str
            # 사고유무 : int (사고 있음 1 / 없음 2 / 모름 3)
            # 연료 : str             ### 항목명 추후 협의
            # 변속기 : str            ### 항목명 추후 협의
            # 옵션 : list [str]      ### 항목명 추후 협의

            #result =[time_stamp, title,plate_num, vin, price, mileage, color, model_year, accident, fuel, transmission, options if len(options)>0 else None]
            result = [time_stamp, title, plate_num, vin, price, mileage, color, model_year,
                      registered_at, accident, fuel, transmission, options]
            results.append(result)
        except Exception as e:
            print(' :: error :: ', type(e), e, ' at '+html)

    # csv 파일로 출력
    file_stamp = datetime.today().strftime('%Y-%m-%d_%H:%M')  # 파일 만든날짜 기입
    file_name = os.path.join(_to, f'mpark_{file_stamp}.csv')
    dataframe = pd.DataFrame(results)
    dataframe.to_csv(file_name, header=None, index=False)
    print('Done. => '+file_name)
