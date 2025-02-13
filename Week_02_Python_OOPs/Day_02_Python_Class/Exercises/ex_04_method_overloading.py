"""
Python does not support method overloading directly. Implement a class MathOperations with a method add() that can handle both two and three arguments.
"""

from typing import Optional


class MathOperations:

    def add_v1(
        self, a: Optional[int] = 0, b: Optional[int] = 0, c: Optional[int] = 0
    ) -> int:
        return a + b + c

    def add_v2(self, *args: int) -> int:
        return sum(args)

    def add_v3(self, **kwargs: int) -> int:
        return sum(kwargs.values())


mathobj = MathOperations()

# Using Optional Arguments
print(f"Three Arguments (v1): {mathobj.add_v1(1, 2, 3)}")
print(f"Two Arguments (v1): {mathobj.add_v1(1, 3)}")
print(f"Single Argument (v1): {mathobj.add_v1(3)}")

# Using *args
print(f"Three Arguments (v2): {mathobj.add_v2(1, 2, 3)}")
print(f"Two Arguments (v2): {mathobj.add_v2(1, 3)}")
print(f"Single Argument (v2): {mathobj.add_v2(3)}")

# Using **kwargs
print(f"Three Arguments (v3): {mathobj.add_v3(a=1, b=2, c=3)}")
print(f"Two Arguments (v3): {mathobj.add_v3(a=1, b=3)}")
print(f"Single Argument (v3): {mathobj.add_v3(a=3)}")
