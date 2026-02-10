def check_number(num):
    """checks if num is positive, negative, or zero """
    if num > 0:
        return "positive"
    elif num < 0: 
        return "negative"
    else:
        return "zero"

def print_first_10_primes():
    """return the first 10 prime numbers."""
    primes = []
    num = 2

    while len(primes) < 10:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1

    return primes

def sum_1_to_100():
    """return the sum of numbers from 1 to 100"""
    sum = 0
    i = 1

    while i <= 100:
        sum += i
        i += 1

    return sum