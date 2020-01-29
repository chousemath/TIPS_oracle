from typing import List, Tuple
from cdecompose import decompose
from random import shuffle
from time import sleep

Route = Tuple[str, str]

routes: List[Route] = [
    ('pages_detail', 'html_src_encar'),
    ('pages_detail_encar_domestic', 'html_src_encar'),
    ('pages_detail_mpark', 'html_src_mpark'),
    ('pages_detail_aj', 'html_src_aj'),
    ('encar_accident_reports', 'html_src_encar_accidents'),
]
shuffle(routes)

if __name__ == '__main__':
    while True:
        for route in routes:
            decompose(route)
            sleep(5)
        print('Finished with a round of decomposition')
