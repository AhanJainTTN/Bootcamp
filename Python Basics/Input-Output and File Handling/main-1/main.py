def is_int(string):

    if string[0] == "-":

        if string[1::].isdigit():
            return True
        else:
            return False

    return string.isdigit()


def is_float(string):

    try:
        float(string)
        return True
    except ValueError:
        return False


with open(
    "Python Basics/Input-Output and File Handling/main-1/files/numbers.txt", "r"
) as numbers_file, open(
    "Python Basics/Input-Output and File Handling/main-1/files/even.txt", "w"
) as even_file, open(
    "Python Basics/Input-Output and File Handling/main-1/files/odd.txt", "w"
) as odd_file, open(
    "Python Basics/Input-Output and File Handling/main-1/files/float.txt", "w"
) as float_file:

    for line in numbers_file:
        curr_line = line.rstrip("\n")

        if is_int(curr_line):
            curr_val = int(curr_line)

            if curr_val % 2 == 0:
                even_file.write(curr_line + "\n")
                print(f"Wrote {curr_val} to even.txt")
            else:
                odd_file.write(curr_line + "\n")
                print(f"Wrote {curr_val} to odd.txt")

        # explicit check takes care of non numeric values
        # if float is checked first, it retunrs ints as floats as well
        elif is_float(curr_line):
            curr_val = float(curr_line)
            float_file.write(curr_line + "\n")
            print(f"Wrote {curr_val} to float.txt")

# alternative to read files without \n
# lines = file.read().splitlines()
# print(lines)

# To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been reached, f.read() will return an empty string ('').
