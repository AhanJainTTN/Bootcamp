"""
Code to generate first n prime numbers.
"""

from typing import List


def is_prime(num: int) -> bool:
    """
    Determines whether a given number is prime.

    Args:
        num (int): The number to check for primality.

    Returns:
        bool: True if the number is prime, False otherwise.
    """

    if num == 1:
        return False

    for i in range(2, (num // 2) + 1):
        if num % i == 0:
            return False

    return True


def n_primes(n: int) -> List[int]:
    """
    Generates the first 'n' prime numbers.

    Args:
        n (int): The number of prime numbers to generate.

    Returns:
        list[int]: A list of the first 'n' prime numbers.
    """
    prime_count = 0
    i = 2
    primes = []

    while prime_count < n:
        if is_prime(i):
            primes.append(i)
            prime_count += 1

        i += 1 if i == 2 else 2  # skip even numbers after 2

    return primes


def main() -> None:
    """
    Entry point of the script. Generates and prints the first n prime numbers.
    """
    n = 25
    print(n_primes(n))


if __name__ == "__main__":
    main()
