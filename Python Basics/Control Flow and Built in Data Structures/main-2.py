astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""
my_dict1 = {}

# .get(key, default value if key does not exist)
for word in astring.split():
    my_dict1[word] = my_dict1.get(word, 0) + 1

print(my_dict1)

# TC: O(n) where n is the length of the string
# SC: O(n) additional space used by astring.split()

from collections import Counter

my_dict2 = {}

my_dict2 = Counter(word for word in astring.split())
print(my_dict2)

# TC: O(n) where n is the length of the string
# SC: No additional space because of the use of generator expression for astring.split()
