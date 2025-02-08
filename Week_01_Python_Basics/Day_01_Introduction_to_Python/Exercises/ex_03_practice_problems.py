"""
1. Given the string my_string = 'Hello Python!',
reverse the string using slicing, print '!' using indexing.
"""

str = "Hello Python!"
str_rev = str[::-1]

print("Original String: ", str)
print("Reversed String (After Slicing): ", str_rev)
print("Indexed Character: ", str_rev[0])

"""
2. Use slicing to get the word "frain" from "information".
"""

str = "information"
str_slice = str[2::2]

print("Original String: ", str)
print("Sliced String: ", str_slice)

"""
3. Using examples, explain string.format() and f-strings.
"""

# using positional aeguments
str = "My name is {} and I am {} years old.".format("Ahan", 23)
print(str)

# using indexed placeholders
str = "My name is {1} and I am {0} years old.".format(23, "Ahan")
print(str)

# using named placeholders
str = "My name is {name} and I am {age} years old.".format(name="Ahan", age=23)
print(str)

# using dictionaries
d1 = {"name": "Ahan", "age": 23}
# **d1 unpacks dictionary keys as named arguments
# name variable gets assigned value 'Ahan' and age gets assigned '23'
str = "My name is {name} and I am {age} years old.".format(**d1)
print(str)

name = "Ahan"
age = 23

# using direct expressions
str = f"My name is {name} and I am {age} years old."
print(str)

# evaluating expressions
str = f"My name is {name} and I am {19 + 4} years old."
print(str)

# using dictionaries
d1 = {"name": "Ahan", "age": 23}
str = f"My name is {d1['name']} and I am {d1['age']} years old.".format(**d1)
print(str)

"""
4. Can we sort a dictionary? Why or why not?
"""

my_dict = {"b": 5, "a": 7, "c": 3}
print("Original Dictionary: ", my_dict)

# Sort by keys
sorted_dict_bykey = dict(sorted(my_dict.items()))
print("Sorted by Key: ", sorted_dict_bykey)

# Sort by values
sorted_dict_byvalue = dict(sorted(my_dict.items(), key=lambda x: x[1]))
print("Sorted by Value", sorted_dict_byvalue)

from collections import OrderedDict

# Using OrderedDict from collections
ordered_dict = OrderedDict()
ordered_dict["b"] = 3
ordered_dict["a"] = 5
ordered_dict["c"] = 2

print("OrderedDict Before Modification:", ordered_dict)

ordered_dict["b"] = 10
print("After Modification:", ordered_dict)

"""
5. Using keys and indexing, grab the 'hello' from the following dictionaries:

    d = {'simple_key': 'hello'}
    d = {'k1': {'k2': 'hello'}}
    d = {'k1': [{'nest_key': ['this is deep', ['hello']]}]}
    d = {'k1': [1, 2, {'k2': ['this is tricky', {'tough': [1, 2, ['hello']]}]}]}
"""

d1 = {"simple_key": "hello"}
d2 = {"k1": {"k2": "hello"}}
d3 = {"k1": [{"nest_key": ["this is deep", ["hello"]]}]}
d4 = {"k1": [1, 2, {"k2": ["this is tricky", {"tough": [1, 2, ["hello"]]}]}]}

print("From d1: ", d1["simple_key"])
print("From d2: ", d2["k1"]["k2"])
print("From d3: ", d3["k1"][0]["nest_key"][1][0])
print("From d4: ", d4["k1"][2]["k2"][1]["tough"][2][0])

"""
6. Reassign 'hello' in this nested list to say 'goodbye' instead: 
    list3 = [1, 2, [3, 4, 'hello']
"""

list3 = [1, 2, [3, 4, "hello"]]
print("List Before Modification: ", list3)

list3[2][2] = "goodbye"
print("List After Modification: ", list3)

"""
7. From the given list list5, create a set: 
    list5 = [1, 2, 2, 33, 4, 4, 11, 22, 3, 3, 2]
"""

list5 = [1, 2, 2, 33, 4, 4, 11, 22, 3, 3, 2]
set5 = set(list5)

print(type(set5), set5)

"""
8. In the string "information", count the total number of occurrences of 'i'.
"""

str = "information"
i_count = 0

for k in str:
    if k == "i":
        i_count += 1

print("String: ", str)
print("Using Loop: ", i_count)
print("Using str.count()", str.count("i"))
