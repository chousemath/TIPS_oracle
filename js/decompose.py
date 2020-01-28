from typing import List, Tuple
from cdecompose import decompose
from random import shuffle

Route = Tuple[str, str]

routes: List[Route] = [
    ('pages_detail', 'html_src_encar'),
    ('pages_detail_encar_domestic', 'html_src_encar'),
    ('pages_detail_mpark', 'html_src_mpark'),
    ('pages_detail_aj', 'html_src_aj'),
]
shuffle(routes)

if __name__ == '__main__':
    while True:
        for route in routes:
            decompose(route)
        print('Finished with a round of decomposition')