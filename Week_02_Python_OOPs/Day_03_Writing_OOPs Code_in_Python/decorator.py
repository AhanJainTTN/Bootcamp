def wrapper(func):

    def modify_func(*args):
        res = func(*args)
        res = res**2

        return res

    return modify_func


@wrapper
def add(x, y):
    return x + y


res = add(5, 6)
print(res)

# my_list = [1, 2, 3]
# i = iter(my_list)

# for count in len(my_list):
#     print(i.__next__)

# for itr in my_list:
#     print(itr)
