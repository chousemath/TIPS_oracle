from simplify import simplify_displacement, \
    simplify_fuel, \
    simplify_category, \
    simplify_year, \
    simplify_transmission, \
    simplify_color

def test_simplify_fuel():
    assert simplify_fuel("가솔린+CNG") == 1
    assert simplify_fuel("가솔린") == 2
    assert simplify_fuel("기타") == 3
    assert simplify_fuel("가솔린+LPG") == 4

def test_simplify_category():
    assert simplify_category("승합차") == 1
    assert simplify_category("중형차") == 2
    assert simplify_category("RV") == 3
    assert simplify_category("스포츠카") == 4

def test_simplify_colors():
    assert simplify_color("검정색") == 1
    assert simplify_color("검정투톤") == 1
    assert simplify_color("아이보리") == 2
    assert simplify_color("흰색투톤") == 2


def test_simplify_transmission():
    assert simplify_transmission("오토") == 1
    assert simplify_transmission("CVT") == 2

def test_simplify_displacement():
    assert simplify_displacement('123cc') == 123
    assert simplify_displacement('0cc') == 0
    assert simplify_displacement('') == 0

def test_simplify_year():
    assert simplify_year('19년05월식(20년형)') == '2019_05_2020'
    assert simplify_year('94년09월식') == '1994_09'
    assert simplify_year('93년03월식(01년형)') == '1993_03_2001'

