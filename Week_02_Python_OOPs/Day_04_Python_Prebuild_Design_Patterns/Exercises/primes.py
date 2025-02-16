"""
Implement a Prime class which should have following functionality:

- Ability to test if a number is prime or not.
- Generate prime numbers.
- Generate prime numbers greater than a number N.
- Generate prime numbers less than a number N.
- Generate all prime numbers between N, to M.
- implement __len__() to tell number of primes between N and M where N < M.
- overload +, += operators to generate prime numbers with respect to current 
prime number  e.g.
"""

from math import sqrt
from typing import List, Optional


class Prime:
    """
    A class for generating and working with prime numbers.
    """

    def __init__(self, start: int, stop: int):
        self.start = start
        self.stop = stop

    def is_prime(self, num: int) -> bool:
        """
        Checks if a number is prime.
        """
        if num == 1 or num == 0 or num < 0:
            return False

        for i in range(2, (int(sqrt(num))) + 1):
            if num % i == 0:
                return False

        return True

    def primes_after(self, n: int) -> List[int]:
        """
        Returns a list of first n prime numbers after start.
        """
        start = self.start + 2 if self.is_prime(self.start) else self.start
        primes = list()
        while len(primes) < n:
            if self.is_prime(start):
                primes.append(start)
            start += 1

        return primes

    def primes_before(self, num: int) -> List[int]:
        """
        Returns a list of all prime numbers before start.
        """
        stop = self.start
        primes = list()
        for i in range(stop):
            if self.is_prime(i):
                primes.append(i)

        return primes

    def primes_between(self) -> List[int]:
        """
        Returns all prime numbers between start and stop.
        """
        primes = list()
        return [i for i in range(self.start + 1, self.stop) if self.is_prime(i)]

    def __len__(self) -> int:
        return len(self.primes_between())

    def __add__(self, next_prime: int) -> int:
        curr_prime = (
            self.start if self.is_prime(self.start) else self.primes_after(1)[0]
        )

        start = curr_prime + 2
        while next_prime > 0:
            if self.is_prime(start):
                next_prime -= 1
                curr_prime = start
            start += 2

        return curr_prime

    def __iadd__(self, next_prime: int):
        self.start = self.__add__(next_prime)
        return self

    def __str__(self) -> str:
        return f"Prime({self.start}, {self.stop})"

    def __repr__(self) -> str:
        return f"Prime(start={self.start}, stop={self.stop})"


def main():
    """
    Entry points of the script.
    """
    obj = Prime(47, 101)

    print(f"Number of Prime Numbers Between {obj.start} and {obj.stop}: {len(obj)}")
    print(f"Prime Numbers Before {obj.start}: {obj.primes_before(100)}")

    n = 25
    print(f"First {n} Prime Numbers After {obj.start}: {obj.primes_after(n)}")
    print(
        f"Prime Numbers Between Between {obj.start} and {obj.stop}: {obj.primes_between()}"
    )

    print(str(obj))
    print(obj + 3)
    obj += 3
    print(repr(obj))


if __name__ == "__main__":
    main()
