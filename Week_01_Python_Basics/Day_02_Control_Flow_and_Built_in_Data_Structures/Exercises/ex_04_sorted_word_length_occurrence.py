"""
From a multi-words and multi-line string, display list of words and word's length with occurence more than 1 in sorted order.

Example:
----------
Input: astring = Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.

Output: Word Length Occurrence Python 6 3 Using 5 2 the 3 5 triple 6 2 quotes 6 3 one 3 3 and 3 3 to 2 4 a 1 3 multiline 9 3 string. 7 2 at 2 2
"""

from collections import Counter

astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""

my_dict = Counter(word for word in astring.split())
filtered_list = [(k, len(k), my_dict[k]) for k in my_dict if my_dict[k] > 1]
filtered_list = sorted(filtered_list, key=lambda x: x[2])
print(filtered_list)

# TC: O(n) where n is the length of the string
# SC: # SC: O(n) additional space taken by my_dict
