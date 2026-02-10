from src import task4

def test_int_price_int_discount():
    assert task4.calculate_discount(100, 20) == 80

def test_float_price_int_discount():
    assert task4.calculate_discount(99.99, 10) == 89.991

def test_int_price_float_discount():
    assert task4.calculate_discount(200, 12.5) == 175.0

def test_float_prie_fload_discount():
    assert task4.calculate_discount(150.5, 7.5) == 139.2125

def test_zero_discount():
    assert task4.calculate_discount(100,0) == 100