"""
You have a number.txt, with each line a real number. Write a code to split this file into 3 files as follows: even.txt -- contain all even numbers odd.txt -- all odd number float.txt -- all floating point number. Use with() clause for file handling
"""

import os
from typing import Optional


def number_splitter(input_file_path: str, output_dir: Optional[str] = None):
    """
    Reads a file containing numbers (one per line) and categorizes them into separate files:
    - even.txt (even integers)
    - odd.txt (odd integers)
    - float.txt (floating-point numbers)

    Args:
        input_file_path (str): The path to the input file containing numbers.
        output_dir (Optional[str]): The directory where the output files will be saved.
                                    Defaults to the current working directory.

    Returns:
        None: The function writes output to files and prints status messages.
    """
    # Set output directory to current working directory if not provided
    if output_dir is None:
        output_dir = os.getcwd()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, "r") as numbers_file, open(
        os.path.join(output_dir, "even.txt"), "w"
    ) as even_file, open(os.path.join(output_dir, "odd.txt"), "w") as odd_file, open(
        os.path.join(output_dir, "float.txt"), "w"
    ) as float_file:

        for line in numbers_file:
            curr_line = line.rstrip("\n")  # Removes any trailing newlines or spaces

            try:
                num = float(curr_line)
                # Check if the number is a floating-point number
                if "." in curr_line:
                    float_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to float.txt")
                # Check if it's an even integer
                elif num % 2 == 0:
                    even_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to even.txt")
                # Check if it's an odd integer
                elif num % 2 == 1:
                    odd_file.write(curr_line + "\n")
                    print(f"Wrote {curr_line} to odd.txt")
            except ValueError:
                print(f"{curr_line} is not a number")


def main() -> None:
    """
    Entry point of the scripts.
    """
    input_file_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_01_split_numbers/files/numbers.txt"
    output_dir = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_01_split_numbers/files"

    number_splitter(input_file_path, output_dir)


if __name__ == "__main__":
    main()


# Why not just check for '.' in string - this fails if we are reading something other than a numeric value - only works if our file consists of purely real numbers
# Why not a simple odd/even check i.e. num % 2 == 1/0 - If a number like 0.0 or 1.0 is encountered, even though it is technically a float, it is written to odd/even file.
