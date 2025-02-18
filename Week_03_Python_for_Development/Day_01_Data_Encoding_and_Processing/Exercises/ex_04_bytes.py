"""
In Python, what is bytes and bytearray? What is use of both and when to use both explain with a use-case code example. How to covert a string literal to bytes and and bytes to string?
"""

"""bytes and bytearrays are built-in data types used for storing raw binary data. bytes is immuatble while bytearrays are mutable."""

# shows ascii equivalents if they exist else hex representation
b = bytes([1, 2, 3, 4, 5, 6, 97, 98, 99, 100])
print(b)  # b'\x01\x02\x03\x04\x05\x06abcd'

# immutable
# b[0] = 65  # TypeError: 'bytes' object does not support item assignment

# possible to modify bytearrays
ba = bytearray([1, 2, 3, 4, 5, 6, 97, 98, 99, 100])
print(ba)  # bytearray(b'\x01\x02\x03\x04\x05\x06abcd')
ba[0] = 65
print(ba)  # bytearray(b'A\x02\x03\x04\x05\x06abcd')

# why use bytes - Reading and writing images, audio, videos, executables - where we want to ensure non corruption/no modification of data.
# for network communication - Network protocols expect raw binary data (bytes), not strings.
# bytearray can be used for memory optimisation for large datasets since it uses less memory than lists

# encoding and decoding
my_string = "Hello, World!"
print(my_string)  # Hello, World!
my_byte = my_string.encode("utf-8")
print(my_byte)  # b'Hello, World!'
my_string = my_byte.decode("utf-8")
print(my_string)  # Hello, World!
