"""
Write a code to read a "Python_script.py" as input file and extract following information to prepare a JSON * all package name which the input Python script use * all function name which the input Python script define * all class name which the input Python script define * all the variable name which the input Python script define example output: { "package": ["os", "itertools"], "function": ["function1", "function2"], "class": ["classA", "classB"], "variable": ["num", "i", "j"] }
"""

import os
import json
from typing import Dict, Set, Optional


def extract_package(line: str, extracted_data: Dict[str, Set[str]]) -> None:
    """
    Extracts imported package names from a given line of Python code. Updates 'extracted_data' in place.

    Args:
        line (str): The line of code to analyze.
        extracted_data (Dict[str, Set[str]]): The dictionary storing extracted metadata.
    """
    filtered_string = ""

    if line.startswith("from "):
        filtered_string = line[5:].split(" import ")[0]
    elif line.startswith("import "):
        filtered_string = line[7:]
    else:
        return
    # Handling aliases and multiple imports
    for part in filtered_string.split(","):
        package = part.split(" as ")[0].split(".")[0]
        extracted_data["package"].add(package.strip())


def extract_function(line: str, extracted_data: Dict[str, Set[str]]) -> None:
    """
    Extracts function names from a given line of Python code. Updates 'extracted_data' in place.

    Args:
        line (str): The line of code to analyze.
        extracted_data (Dict[str, Set[str]]): The dictionary storing extracted metadata.
    """
    if line.startswith("def "):
        filtered_string = line[4:].split("(")[0]
        extracted_data["function"].add(filtered_string.strip())


def extract_class(line: str, extracted_data: Dict[str, Set[str]]) -> None:
    """
    Extracts class names from a given line of Python code. Updates 'extracted_data' in place.

    Args:
        line (str): The line of code to analyze.
        extracted_data (Dict[str, Set[str]]): The dictionary storing extracted metadata.
    """
    if line.startswith("class "):
        filtered_string = line[6:].split("(")[0].split(":")[0]
        extracted_data["class"].add(filtered_string.strip())


# implement ast for more robust variable extraction
def extract_variable(line: str, extracted_data: Dict[str, Set[str]]) -> None:
    """
    Extracts variable names from a given line of Python code. Updates 'extracted_data' in place.

    Args:
        line (str): The line of code to analyze.
        extracted_data (Dict[str, Set[str]]): The dictionary storing extracted metadata.

    Notes:
        Only works with PEP8 suggested spacing for variable assignments i.e. one space before and after.
    """
    index = line.find(" = ")

    if index != -1:
        filtered_string = line[:index:]
        # Account for type annotations
        filtered_string = filtered_string.split(":")[0]
        # Handle multiple variables
        for variable in filtered_string.split(","):
            extracted_data["variable"].add(variable.strip())


def extract_metadata(input_file_path: str, output_dir: Optional[str] = None) -> None:
    """
    Extracts metadata (packages, functions, classes, variables) from a Python script. Writes extracted metadata to a JSON file.

    Args:
        input_file_path (str): Path to the input Python script.
        output_dir (Optional[str]): Directory to save extracted metadata. Defaults to the current directory.
    """
    if output_dir is None:
        output_dir = os.getcwd()

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


def main() -> None:
    """
    Entry point of the script. Calls extract_metadata() with file paths.
    """
    input_file_path = "/home/ahan/Documents/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_02_py_extractor/files/python_script.py"
    output_dir = "/home/ahan/Documents/Bootcamp/Week_01_Python_Basics/Day_04_Input_Output_and_File_Handling/Exercises/ex_02_py_extractor/files/"

    extract_metadata(input_file_path, output_dir)


if __name__ == "__main__":
    main()
