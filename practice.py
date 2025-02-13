l1 = [1, 2, 3]
l2 = [4, 5, 6]

# possible

t = (l1, l2)
print(t)

# possible

l1[0] = 4
print(t)

# possible

t[0][0] = 9
print(t)

# possible

t[0].append(11)
print(t)

# possible

t[0].pop()
print(t)

# not possible

# t[0] = [1, 4, 7]

# a list inside a tuple can be modified, however the tuple structure should remain the same i.e. tuple level modifications like adding a new list or modifying an entire list since it is a tuple element is not allowed

# possible

t[0].pop()
print(t)


# A shallow copy only copies the outer structure, retaining references to the nested objects. In this case, the inner lists are shared between original and shallow_copied.
my_list = [1, 2, 3, [4, 5, 6]]
my_list_copy = my_list.copy()
my_list_copy[3].append(7)
my_list.append(8)

print(my_list)
print(my_list_copy)

list_squares = [x**2 for x in range(10)]
print(list_squares)

nested_list = [[x for x in range(y)] for y in range(1, 10)]
print(nested_list)

my_set = {"a", "b", "c"}
print("a" in my_set)

# empty set
# my_set = {} creates an empty dictionary
my_set = set()

# reduce
from functools import reduce


def add(x, y):
    return x + y


a = [1, 2, 3, 4, 5]
res = reduce(add, a)
print(res)


b = "Hello ABC XYZ"
res = reduce(add, b.split(" "))

# PYTHONPATH is used to set the path for the user-defined modules so that it can be directly imported into a Python program.
# sys.path is a built-in variable within the sys module. It contains a list of directories that the interpreter will search in for the required module.

"""
sys.path is initialized from these locations:
The directory containing the input script (or the current directory when no file is specified).

PYTHONPATH (a list of directory names, with the same syntax as the shell variable PATH).

The installation-dependent default (by convention including a site-packages directory, handled by the site module).
"""

# Python program creating a
# context manager


class ContextManager:
    def __init__(self):
        print("init method called")

    def __enter__(self):
        print("enter method called")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("exit method called")


with ContextManager() as manager:
    print("with statement block")

# The with statement is used to wrap the execution of a block with methods defined by a context manager
# Context managers allow you to allocate and release resources precisely when you want to.
"""
Steps: 
1. ContextManager object initialised - if __init__ defined, it runs first
2. Then __enter__ of context manager is executed
3. Code inside with is executed
4. The context manager’s __exit__() method is invoked. If an exception caused the exit, its type, value, and traceback are passed as arguments to __exit__(). Otherwise, three None arguments are supplied.
"""

# Generators: In Python, a generator is a function that returns an iterator that produces a sequence of values when iterated over. Generators are useful when we want to produce a large sequence of values, but we don't want to store all of them in memory at once.
# When the generator function is called, it does not execute the function body immediately. Instead, it returns a generator object that can be iterated over to produce the values.
# The yield keyword is used to produce a value from the generator and pause the generator function's execution until the next value is requested.

# my_tuple = (1, 2, 3, [4, 5, 6])
# my_tuple[3].append(7)
# print(my_tuple)

# my_tuple = tuple([[1, 2, 3]])
# print(my_set)
# print(len(my_tuple))

data = [[1, 2, 3], [4, 5, 6]]
print(data[0])
data = [[1, 2, 3], [4, 5, 6]]
print(data[0])

my_dict = {"a": 1, "b": 2, "c": 3}
for key in my_dict.keys():
    print(key)

# works
list = [1, 2, 3, 4, 5]
print(list)


def class_in_fun(fval):

    class InsideFun:
        def __init__(self, ival):
            self.cval = ival

    obj = InsideFun(fval)
    print(obj.cval)


mval = 22
class_in_fun(mval)
