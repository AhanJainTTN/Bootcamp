import os, sys
import encodings, time as t
import aifc as ai, ast
import weakref as w, zipapp as z, argparse as arg
from array import array


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


class MyClass:
    """A simple example class"""

    i = 12345

    def f(self):
        return "hello world"


class YourClass(MyClass):
    pass


a = 5
b = 6
c = 7
d = 8
e, f = 10, 20
name = "Python"
count: int = 100
_list = [1, 2, 3]
_data = {"key": "value"}
