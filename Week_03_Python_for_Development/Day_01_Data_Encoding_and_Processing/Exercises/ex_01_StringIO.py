"""
What is StringIO library for? explain with an example
"""

"""
Source: https://stackoverflow.com/questions/7996479/what-is-stringio-in-python-used-for-in-reality

StringIO gives you file-like access to strings, so you can use an existing module that deals with a file and change almost nothing and make it work with strings. We can also avoid creating temporary files since it works like a file but stays in memory. Also faster than writing to files on disk due to no need of system calls by OS to kernel.
"""
import csv
from io import StringIO

data = {
    "Login email": "mary@example.com",
    "Identifier": "9346",
    "One-time password": "14ju73",
    "Recovery code": "mj9346",
    "First name": "Mary",
    "Last name": "Jenkins",
    "Department": "Engineering, HR",
    "Location": "Manchester",
}
# creating an in memory file object
output_file = StringIO()
# now we can interact it with just like any other file object
headers = data.keys() if data else []
writer = csv.DictWriter(output_file, fieldnames=headers, delimiter=";", quotechar='"')
writer.writeheader()
writer.writerow(data)
# blank output because seek pointer is set to end of file
# i.e. place of last write
# since StringIO works like a file opened in write mode
# print(output_file.read())
output_file.seek(0)
print(output_file.read())
# in memory file so .close() not necessary and garbage collector automatically cleans up - use .close() to explicitly free up memory
