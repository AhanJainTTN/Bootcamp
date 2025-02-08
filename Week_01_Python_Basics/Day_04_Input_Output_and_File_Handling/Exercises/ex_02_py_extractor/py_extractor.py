"""
Write a code to read a "Python_script.py" as input file and extract following information to prepare a JSON * all package name which the input Python script use * all function name which the input Python script define * all class name which the input Python script define * all the variable name which the input Python script define example output: { "package": ["os", "itertools"], "function": ["function1", "function2"], "class": ["classA", "classB"], "variable": ["num", "i", "j"] }
"""

import os
import json


def extract_package(line, extracted_data):

    filtered_string = ""

    if line.startswith("from "):
        filtered_string = line[5:].split(" import ")[0]
    elif line.startswith("import "):
        filtered_string = line[7:]
    else:
        return
    # handling aliases and commas
    for part in filtered_string.split(","):
        package = part.split(" as ")[0].split(".")[0]
        extracted_data["package"].add(package.strip())


def extract_function(line, extracted_data):
    if line.startswith("def "):
        filtered_string = line[4:].split("(")[0]
        extracted_data["function"].add(filtered_string.strip())


def extract_class(line, extracted_data):
    if line.startswith("class "):
        filtered_string = line[6:].split("(")[0].split(":")[0]
        extracted_data["class"].add(filtered_string.strip())


# only works with PEP8 suggested spacing for variable assignments
# implement ast for more robust variable extraction
def extract_variable(line, extracted_data):
    index = line.find(" = ")

    if index != -1:
        filtered_string = line[:index:]
        # account for type annotations
        filtered_string = filtered_string.split(":")[0]
        # handle commas
        for variable in filtered_string.split(","):
            extracted_data["variable"].add(variable.strip())


def extract_metadata(input_file_path, output_dir=os.getcwd()):

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file_path, "r") as script_file, open(
        os.path.join(output_dir, "script_info.json"), "w"
    ) as script_info_json:

        extracted_data = {
            "package": set(),
            "function": set(),
            "class": set(),
            "variable": set(),
        }

        for line in script_file:
            line = line.strip()  # Remove indentation or leading blank spaces
            if not line.startswith("#"):  # ignore comments
                extract_package(line, extracted_data)
                extract_function(line, extracted_data)
                extract_class(line, extracted_data)
                extract_variable(line, extracted_data)

        for key in extracted_data:
            extracted_data[key] = list(extracted_data[key])

        json.dump(extracted_data, script_info_json)


if __name__ == "__main__":

    input_file_path = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_02_py_extractor/files/python_script.py"
    output_dir = "/Users/ahan/Documents/GitHub/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_02_py_extractor/files/"

    extract_metadata(input_file_path, output_dir)
