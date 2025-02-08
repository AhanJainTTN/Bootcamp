"""
You have a number.txt, with each line a real number. Write a code to split this file into 3 files as follows: even.txt -- contain all even numbers odd.txt -- all odd number float.txt -- all floating point number. Use with() clause for file handling
"""

import os


def number_splitter(input_file_path, output_dir=os.getcwd()):

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, "r") as numbers_file, open(
        os.path.join(output_dir, "even.txt"), "w"
    ) as even_file, open(os.path.join(output_dir, "odd.txt"), "w") as odd_file, open(
        os.path.join(output_dir, "float.txt"), "w"
    ) as float_file:

        for line in numbers_file:
            curr_line = line.rstrip("\n")

            try:
                num = float(curr_line)
                if "." in curr_line:
                    float_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to float.txt")
                elif num % 2 == 0:
                    even_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to even.txt")
                elif num % 2 == 1:
                    odd_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to odd.txt")
            except ValueError:
                print(f"{curr_line} is not a number")


if __name__ == "__main__":

    input_file_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_01_split_numbers/files/numbers.txt"
    output_dir = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_01_split_numbers/files"

    number_splitter(input_file_path, output_dir)


# Why not just check for '.' in string - this fails if we are reading something other than a numeric value - only works if our file consists of purely real numbers
# Why not a simple odd/even check i.e. num % 2 == 1/0 - If a number like 0.0 or 1.0 is encountered, even though it is technically a float, it is written to odd/even file.

# To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been reached, f.read() will return an empty string ('').
