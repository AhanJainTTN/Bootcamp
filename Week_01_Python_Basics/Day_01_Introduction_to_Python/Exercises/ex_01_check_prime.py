"""
Write a Python script to test if a number is prime or not? 
- The script name: primes.py 
- Add a function is_prime() which returns a boolean True or False 
- The program should accept a number from the console.
"""


def is_prime(num):
    # 1 is neither prime nor composite
    # since we are checking for primes, we will simply return false
    if num == 1:
        return False

    for i in range(2, (num // 2) + 1):
        if num % i == 0:
            return False

    return True


if __name__ == "__main__":
    num = int(input("Enter a Number: "))
    print(is_prime(num))
