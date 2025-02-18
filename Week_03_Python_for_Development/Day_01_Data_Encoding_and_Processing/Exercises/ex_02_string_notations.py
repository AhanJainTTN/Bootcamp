"""
What is  u"", r"" and "", f"" string notations in Python. Give example?
"""
# Unicode is essential because it enables text representation for all languages and symbols across different platforms and operating systems. Without Unicode, handling multilingual text, special characters, and emojis would be problematic. Unicode is a universal character encoding standard that assigns a unique number i.e code point to every character in every language, symbol, and emoji. Before Unicode, different languages used different encoding standards like ASCII, Latin-1, Shift-JIS, etc. which caused compatibility issues. Python automatically uses Unicode for all strings since Python 2.
# rstrings
windows_path = "C:\Users\Ahan\Documents\GitHub\Bootcamp/©, π, ß, €"
print(windows_path)
# The backslashes in the string cause escape sequence issues (escape sequence is a special character combination that starts with a backslash (\) and is used to represent characters that cannot be typed directly in a string)
windows_path = r"C:\Users\Ahan\Documents\GitHub\Bootcamp/©, π, ß, €"
print(windows_path)

s = "Hello, π 😊"  # Includes Unicode characters
print(s)

# Python 2 did support Unicode, but not by default. Instead, it primarily used ASCII strings (str type) unless explicitly told to use Unicode. ASCII only supports 128 characters (A-Z, a-z, 0-9, punctuation).
# It breaks when handling non-English characters (ä, ñ, π, ©, ß, €, emojis etc.) resulting in UnicodeDecodeError.

# Regular Strings - Default string type in Python. Used when no special processing is required.
# f"" Formatted Strings (f-strings) Allows inline variable interpolation in strings (introduced in Python 3.6+). Used for dynamic string formatting.

