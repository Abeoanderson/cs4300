from src import task3

def test_check_number_positive():
    assert task3.check_number(5) == "positive"

def test_check_number_negative():
    assert task3.check_number(-5) == "negative"

def test_check_number_zero():
    assert task3.check_number(0) == "zero"

def test_first_10_primes():
    assert task3.print_first_10_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum_1_to_100():
    assert task3.sum_1_to_100() == 5050