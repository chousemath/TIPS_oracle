from typing import List, Sequence, Tuple, Dict
import unicodedata as ud


def norm(in_val: str) -> str:
    return ud.normalize('NFC', str(in_val)).strip()


def clean_price(in_val: str) -> int:
    return int(in_val) * 10_000


def clean_title(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()


def clean_plate(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()


def clean_fuel(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()


def clean_transmission(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()


def clean_color(in_val: str) -> str:
    return in_val.replace('자세히보기', '').strip()


def clean_registered(in_val: str) -> str:
    return str(in_val).replace('자세히보기', '').strip()


def clean_mileage(in_val: str) -> int:
    return int(in_val)


def clean_model_year(in_val: str) -> str:
    return str(in_val)


def format_chartjs(in_val: Sequence[Tuple[str, int]]) -> Dict:
    data: List[int] = []
    labels: List[str] = []
    for x in in_val:
        labels.append(x[0])
        data.append(x[1])
    return {'data': data, 'labels': labels}
