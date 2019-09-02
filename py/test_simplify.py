from simplify import simplify_displacement, simplify_fuel

def test_simplify_fuel():
    assert simplify_fuel("가솔린+CNG") == 1
    assert simplify_fuel("가솔린") == 2
    assert simplify_fuel("기타") == 3
    assert simplify_fuel("가솔린+LPG") == 4

# {"가솔린+LPG": 4, "CNG": 5, "LNG": 6, "가솔린+전기": 7, "LPG(일반인구입)": 8, "전기": 9, "수소": 10, "디젤+전기": 11, "LPG+전기": 12, "디젤": 13}

def test_simplify_displacement():
    assert simplify_displacement('123cc') == 123
    assert simplify_displacement('0cc') == 0
