from ccompress import compress
from typing import List
from random import shuffle
from time import sleep

routes: List[str] = [
    'pages_detail_carmanager',
    'pages_list_carmanager',
    'pages_detail',
    'pages_detail_encar_domestic',
    #'pages_detail_mpark',
    'pages_detail_aj',
    'pages_detail_autoinside',
    'pages_accident_autoinside',
    #'mpark_accident_reports',
    'encar_accident_reports',
    'pages_list',
    'pages_list_aj',
    'pages_list_autoinside',
    'pages_list_encar_domestic',
    #'pages_list_mpark',
    'html_src_autoinside_accident',
    'html_src_encar_accidents',
    #'html_src_mpark_accident',
]
# shuffle(routes)

if __name__ == '__main__':
    while True:
        for route in routes:
            compress(route)
            sleep(2)
        print('Finished with a round of decomposition')
