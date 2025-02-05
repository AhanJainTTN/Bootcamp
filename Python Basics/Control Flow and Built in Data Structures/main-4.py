from collections import Counter

astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""

my_dict = Counter(word for word in astring.split())
filtered_list = [(k, len(k), my_dict[k]) for k in my_dict if my_dict[k] > 1]
print(filtered_list)

# TC: O(n) where n is the length of the string
# SC: # SC: O(n) additional space taken by my_dict
