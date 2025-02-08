"""
Code to generate first n prime numbers.
"""


def is_prime(n):

    if n == 1:
        return False

    for i in range(2, (n // 2) + 1):
        if n % i == 0:
            return False

    return True


def n_primes(n):
    prime_count = 0
    i = 2
    primes = []

    while prime_count < n:
        if is_prime(i):
            primes.append(i)
            prime_count += 1

        i += 1 if i == 2 else 2

    return primes


print(n_primes(25))
