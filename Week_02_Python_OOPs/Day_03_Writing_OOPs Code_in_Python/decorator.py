def wrapper(func):

    def modify_func(*args):
        res = func(*args)
        res = res**2

        return res

    return modify_func


@wrapper
def add(x, y):
    return x + y


# res = add(5, 6)
# print(res)

# my_list = [1, 2, 3]
# i = iter(my_list)

# for count in len(my_list):
#     print(i.__next__)

# for itr in my_list:
#     print(itr)

import time


def execution_time(func):

    def inner_func():
        start = time.time()
        func()
        end = time.time()
        return f"Execution Time: {end - start}"

    return inner_func


@execution_time
def say_hello_n():
    return [f"Hello: {i}" for i in range(1, 50)]


fun = execution_time(say_hello_n)
print(fun)  # function object reference
print(fun())
