"""
Write a Python script to test if a number is prime or not? 
- The script name: primes.py 
- Add a function is_prime() which returns a boolean True or False 
- The program should accept a number from the console.
"""

from math import sqrt


def is_prime(num: int) -> bool:
    """
    Checks whether a given numer is prime or not.

    Args:
        num (int): The input number to be checked.

    Returns:
        bool: Prime or not.

    Note:
        How 1 is handled: 1 is neither prime nor composite and since we are checking for primes, we will simply return False.
    """
    if num == 1:
        return False

    for i in range(2, (int(sqrt(num))) + 1):
        if num % i == 0:
            return False

    return True


def main():
    """
    Entry point for the script.
    """
    num = int(input("Enter a Number: "))
    print(is_prime(num))


if __name__ == "__main__":
    main()
