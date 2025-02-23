l1 = [1, 2, 3]
l2 = [4, 5, 6]

# possible
t = (l1, l2)
print(t)

# possible
l1[0] = 4
print(t)

# possible
l1 += [8, 9]
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

# A shallow copy only copies the outer structure, retaining references to the nested objects. In this case, the inner lists are shared between original and shallow_copied. Shallow copies copy references to nested objects, meaning my_list_copy[3] still refers to the same inner list [4, 5, 6] as my_list[3]. Adding 7 to my_list_copy[3] also affects my_list[3]. Appending 8 to my_list does not affect my_list_copy because it is modifying the outer list, not a shared reference.
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

"""
Implement a singleton class `Database` that ensures only one instance of the class can be created. Testing reference deletions and garbage collector.
"""

import sys
import gc


class Database:
    curr_obj = None

    def __new__(cls):
        if cls.curr_obj is None:
            cls.curr_obj = super().__new__(cls)
        return cls.curr_obj

    def __init__(self):
        self.db_connect = "<connection_string>"

    @classmethod
    def __delref__(cls):
        cls.curr_obj = None


db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# 4 because 2 are from db_1 and db_2, 1 from curr_obj and 1 from sys.getrefcount()
print(sys.getrefcount(db_1))

del db_1
del db_2

print(sys.getrefcount(Database.curr_obj))
Database.__delref__()
print(sys.getrefcount(Database.curr_obj))  # garbage value since object does not exist

gc.collect()

db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# print(sys.getrefcount(Database.curr_obj))
# print(sys.getrefcount(db_1))
# print(sys.getrefcount(db_2))

# Printing memory addressed using id()
# print(f"Memory Address (db_1): {id(db_1)}")
# print(f"Memory Address (db_2): {id(db_2)}")
# print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# Note: weakref are references not accounted for by the garbage collector

# if single item - no separator present
print("-*-".join(["abc"]))


def funcvar(x):
    x = x * 2


def funclist(x):
    x = [i * i for i in x]
    x.append(4)
    # x = [i * i for i in x]


var = 5
print(var)
funcvar(5)
print(var)

l = [1, 2, 3]
print(l)
funclist(l)
print(l)


class Car:

    def __init__(self, w):
        self.wheels = w


c1 = Car(4)
c2 = Car(4)

print(id(c1) == id(c2))

x = 4
y = 4

print(id(x) == id(y))

print(dir(__builtins__))

my_list = [1, 2, 3, 4, 5, 6, 7, 8]
print(my_list[:])


# int, floats, bool etc. stored as PyObject
x = 1
# collections stored as PyVarObject which has a value field which points to storage location of memory location with addresses to actual objects - why not store the actual objects - because for indexing to work all elements should have the same size - this can be solved using memory location addresses since they will always be the same size - this also allows collections to hold different types of data in the same list/tuple/set etc. - this allocation is also contiguous in nature - if this array becomes full python allocates new memory, usually twice the size of exisitng array and moves item i.e. addresses to new array - pyvarobject value pointer is updated to point ar start of this array and previous memory is freed - pyvarobject address never changes
my_list = [1, 2, 3, 4, 5, 6, 7, 8]
# True
print(id(my_list[0]) == id(x))

# works
my_list = [1, 2, 3, 4, 5, 6, 7, 8]
print(f"{my_list = }")

x = "abcjfdgjdjgj_dfgdfjgjdhgjdfs"
y = "abcjfdgjdjgj_dfgdfjgjdhgjdfs"

print(id(x) == id(y))

# # Running directly in interpreter
# >>> x = 56789
# >>> y = 56789
# >>> print(id(x) == id(y))
# False
# >>> x = "my string"
# >>> y = "my string"
# >>> print(id(x) == id(y))
# False
# >>> x = "my_string"
# >>> y = "my_string"
# >>> print(id(x) == id(y))
# True
# >>> x = 256
# >>> y = 256
# >>> print(id(x) == id(y))
# True
# >>> x = 257
# >>> y = 257
# >>> print(id(x) == id(y))
# False

# Running in .py file
x = 56789
y = 56789
print(id(x) == id(y))
# True
x = "my string"
y = "my string"
print(id(x) == id(y))
# True
x = "my_string"
y = "my_string"
print(id(x) == id(y))
# True
x = 256
y = 256
print(id(x) == id(y))
# True
x = 257
y = 257
print(id(x) == id(y))
# True

x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]
print(id(x) == id(y))
# False


def fun(x):
    x = [1, 2, 3]


x = [3, 4, 5]
fun(x)
print(x)
# [3, 4, 5]

x = [1, 2, 3, 4, 5]
y = x
y = [1, 3, 3]
print(x, y)
# [1, 2, 3, 4, 5] [1, 3, 3]


# default function arguments are evaluated only once at definition - here my_list is bound to funnction object as a default under __defaults__ and same my_list is appended to at each function call - solution use None as default and check for None inside function or use an immutable object like a tuple
def add_two_to_list(my_list=[]):
    my_list.append(2)
    return my_list


x = add_two_to_list()
print(x)
# [2]
y = add_two_to_list()
print(y)
# [2, 2]

# += calls iadd method of list object of y and returns a list object
x = [1, 2]
y = x
y += [3, 4]
print(x, y)
# [1, 2, 3, 4] [1, 2, 3, 4]

x = [1, 2]
y = x
y = y + [3, 4]
print(x, y)
# [1, 2] [1, 2, 3, 4]

# can initialise tuples without parentheses - it is the commas which are necessary
t = 1, 2, 3, 4
print(type(t))

t = 1, 2, [3, 4]
print(t)

# does not work
# t[2] = [3, 4]

# works - why - because when the tuple is created memory is allocated for the objects it contains i.e. memory addresses of PyObject 1,2 and PyVarObject [3,4] which is a list
# when we say a tuple is immutable we refer to the actual memory addresses representing the tuple i.e. the contiguos block of memory starting at the address as sepcified by the value attribute of the PyVarObject
# as long as these addresses remain the same - we can modify the objects they are pointing to
t[2].extend([5, 6])
print(t)

# different ids since new tuple is being created using the __iadd__ method of tuple class - similar for all immutable objects in python
t = 1, 2, [3, 4]
print(t, id(t))
t += 7, 8
print(t, id(t))

# raises TypeError in script
t = 1, 2, [3, 4]
print(t)
# t[2] += [7, 8]
print(t)

# works in real time interpreter - why - += invokes __iadd__ method of the list which extends the existing list. However this __iadd__ returns self i.e. the calling objects instance and t[2] gets the same address it originally had but an error is raised as this is still an attempt to modify the memoey address even if it is the same address
# >>> t = 1, 2, [3, 4]
# >>> print(t)
# (1, 2, [3, 4])
# >>> t[2] += [7, 8]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: 'tuple' object does not support item assignment
# >>> print(t)
# (1, 2, [3, 4, 7, 8])


# why no change in tuple value - at initialisation every tuple element points to object 12
# x also points to 12
# when value of x changes a new object 34 is created and x points to it
# however the 12 object is still pointed to by the tuple and we get the same values
# However, if Python allowed direct memory manipulation (like in C with pointers), one could theoretically modify the value at the memory address where 12 was stored, forcing all references to 12 (including the tuple’s references) to reflect the new value. But Python does not allow this due to its memory safety rules.
x = 12
t = (x, x, x)
print(t)
# (12, 12, 12)
x = 34
print(t)
# (12, 12, 12)

t1 = (1, 2, 3, 4, 5, 6, 7, 8)
t2 = (1, 2, 3, 4, 5, 6, 7, 8)
print(t1 is t2)
# True

t1 = (1, 2, 3, 4, 5, 6, [7, 8])
t2 = (1, 2, 3, 4, 5, 6, [7, 8])
print(t1 is t2)
# False

# using del with lists
a = [-1, 1, 66.25, 333, 333, 1234.5]
del a[0]
print(a)
[1, 66.25, 333, 333, 1234.5]
del a[2:4]
print(a)
[1, 66.25, 1234.5]
del a[:]
print(a)

# single item tuple
# A special problem is the construction of tuples containing 0 or 1 items: the syntax has some extra quirks to accommodate these. Empty tuples are constructed by an empty pair of parentheses; a tuple with one item is constructed by following a value with a comma (it is not sufficient to enclose a single value in parentheses). Ugly, but effective.
empty = ()
print(type(empty))
singleton = ("hello",)  # <-- note trailing comma
print(len(empty))
print(len(singleton))
print(type(singleton))
print(singleton)

# filter
my_list = filter(lambda x: x % 2 == 0, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(list(my_list))

# reduce
from functools import reduce


def add(x, y, z):
    return x + y + z


x = reduce(add, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(x)

# sum
x = sum({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
print(x)

# map
x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
my_list = [x for x in map(str, x)]
print(my_list)

# generator expression
gen_exp = (x for x in range(10))
print(list(gen_exp))
print(list(gen_exp))  # [] (blank) - why -
print(gen_exp)


# fibonacci
def fibo(n):

    first = 0
    second = 1

    while n:
        curr_num = first + second
        first = second
        second = curr_num
        print(curr_num)
        n -= 1


fibo(10)

my_dict = {"a": 1, "b": 2, "c": 3}
print(type(my_dict.items()))  # <class 'dict_items'>
print(type(my_dict.keys()))  # <class 'dict_keys'>
print(type(my_dict.values()))  # <class 'dict_values'>
print(type(my_dict.keys))  # <class 'builtin_function_or_method'>

my_list = [1, 2, 3, 4, 5]
my_list *= 3  # same as my_list + my_list + my_list
print(my_list)

# my_list = [1, 2, 3, 4, 5]
# my_list *= [4, 5, 6]  # TypeError: can't multiply sequence by non-int of type 'list'
# print(my_list)

# doesnt work for normal or frozenset since values in a set must be immutable for hash calculations and lookups - frozensets are themselves immutable and can be used as dictionary keys
x = [7, 8, 9]
my_set = frozenset({1, 2, 3, 4, 5, 6, x})
print(my_set)


def hello():
    pass


class A:

    def hello():
        pass


a = A()
# In Python, __main__ is the name of the module that is being run as the main program. If a script is executed directly, Python assigns __name__ = "__main__", meaning that the module itself is being run. Thus, any class, function, or variable defined in the main script is inside the __main__ namespace. Python displays <class '__main__.A'> to indicate that A belongs to __main__.
print(type(a))  # <class '__main__.A'>
print(type(a.hello))  # <class 'method'>
print(type(hello))  # <class 'function'>


class A:
    _x = 24
    __y = 48


a = A()
print(a._x)
# doesnt work because Python mangles private attributes using _ClassName__attribute to prevent accidental access.
print(a.__y)
# however still accessible through _ClassName__attribute
print(a._A__y)

(x := 5)
print(x)


class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        print("B")


class C(A):
    def show(self):
        print("C")


class D(B, C):  # Multiple Inheritance
    pass


d = D()
d.show()  # Output: "B"


class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        print("B")
        super().show()


class C(A):
    def show(self):
        print("C")
        super().show()


class D(B, C):
    def show(self):
        print("D")
        super().show()


d = D()
d.show()

# D -> B -> C -> A
# Why not D -> B -> A -> C -> A - C3 linearisation algorithm used my MRO does not allow duplicate calls to parent
# super().super() is not valid


class A:
    x = 5

    def show(self):
        print(B.y)


class B(A):
    y = 5


b = B()
super(B, b).show()


# Since parent class has no way to know about child classes, if the parent has to access some data from child class, child needs to call the parent's method and pass the child object as parameter which can then be used by the parent to access the child attributes
class Parent:
    parent = 25

    def showa(self):
        print("Child Value: ", self.child)


class Child(Parent):
    child = 10

    def show(self):
        Parent.showa(self)


c = Child()
c.show()


class A:
    def show(self):
        print("A.show()")


class B(A):
    def show(self):
        print("B.show()")
        super().show()


B.show(B())

"""
Implement a singleton class `Database` that ensures only one instance of the class can be created.
"""

import sys


class Database:
    curr_obj = None

    def __new__(cls):
        if cls.curr_obj is None:
            cls.curr_obj = super().__new__(cls)
        return cls.curr_obj

    def __init__(self):
        self.db_connect = "<connection_string>"

    @classmethod
    def __delref__(cls):
        cls.curr_obj = None


db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# print(sys.getrefcount(Database.curr_obj))

del db_1
del db_2

# print(sys.getrefcount(Database.curr_obj))

Database.__delref__()
import gc

gc.collect()

db_1 = Database()
db_2 = Database()

# Printing memory addressed using id()
print(f"Memory Address (db_1): {id(db_1)}")
print(f"Memory Address (db_2): {id(db_2)}")
print(f"Same Memory Address: {id(db_1) == id(db_2)}")

# print(sys.getrefcount(Database.curr_obj))
# print(sys.getrefcount(db_1))
# print(sys.getrefcount(db_2))

# Printing memory addressed using id()
# print(f"Memory Address (db_1): {id(db_1)}")
# print(f"Memory Address (db_2): {id(db_2)}")
# print(f"Same Memory Address: {id(db_1) == id(db_2)}")


class A:
    my_str = "I belong to class."

    def __init__(self):
        self.my_str = "I belong to object."
        pass


a = A()
print(A.my_str)
print(a.my_str)  # if no my_str for instance, refers to class my_str

my_list = [1, 2, 3]
a = 1
c = 1
print(a is c)

# To-Do: Custom decorator for program execution time

# No two threads from the same process are ever executed at the same time. They can jump around on the CPU cores but are never executed simultaneously. This is ensured by the Global Interpreter Lock (GIL) which locks the interpreter for other threads of the process when a thread from the process is currently accessing it.
# All threads in a process share the memory space allocated to the process by the OS for code, data etc. but the threads have their own registers and stack memory.
# IO operations are blocking i.e. once a thread makes an IO request, the thread must wait for the return value. During this wait, the GIL is released and another thread from the same process can access it.
