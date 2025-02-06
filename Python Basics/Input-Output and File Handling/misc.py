import os

print(os.getcwd())

with open("number.txt", encoding="utf-8") as file:
    read_data = file.read()
    print(read_data)

# this skips a line since for line in file
# for line in file:
#     line = file.readline()
#     print(line)
