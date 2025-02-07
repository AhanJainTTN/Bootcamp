import json


def extract_package(line, extracted_data):

    filtered_string = ""

    if line.startswith("from "):
        filtered_string = line[5:]
        stop_index = filtered_string.find(" import ")
        filtered_string = (
            filtered_string[:stop_index:] if stop_index != -1 else filtered_string
        )

    elif line.startswith("import "):
        filtered_string = line[7:]

    else:
        return

    # handling aliases and commas
    for part in filtered_string.split(","):
        package = part.split(" as ")[0]
        extracted_data["package"].add(package.strip())


def extract_function(line, extracted_data):

    filtered_string = ""

    if line.startswith("def "):
        filtered_string = line[4:]
        stop_index = filtered_string.find("(")
        filtered_string = (
            filtered_string[:stop_index:] if stop_index != -1 else filtered_string
        )
        extracted_data["function"].add(filtered_string.strip())

    else:
        return


def extract_class(line, extracted_data):

    filtered_string = ""

    if line.startswith("class "):
        filtered_string = line[6:]
        stop_index = filtered_string.find("(")
        filtered_string = (
            filtered_string[:stop_index:] if stop_index != -1 else filtered_string
        )
        stop_at = ("(", ":")

        if filtered_string.find(stop_at[0]) != -1:
            stop_at_char = stop_at[0]

        else:
            stop_at_char = stop_at[1]

        stop_index = filtered_string.find(stop_at_char)
        filtered_string = (
            filtered_string[:stop_index:] if stop_index != -1 else filtered_string
        )
        extracted_data["class"].add(filtered_string.strip())


# only works with PEP8 suggested spacing for variable assignments
# implement ast for more robust variable extraction
def extract_variable(line, extracted_data):

    curr_string = " = "
    curr_index = line.find(curr_string)

    if curr_index != -1:
        filtered_string = line[:curr_index:]

        # account for type annotations
        filtered_string = filtered_string.split(":")[0]

        # handle aliases and commas
        for variable in filtered_string.split(","):
            extracted_data["variable"].add(variable.strip())
    else:
        return


extracted_data = {
    "package": set(),
    "function": set(),
    "class": set(),
    "variable": set(),
}

with open(
    "Python Basics/Input-Output and File Handling/main-2/files/python_script.py", "r"
) as script_file, open(
    "Python Basics/Input-Output and File Handling/main-2/files/script_info.json", "w"
) as script_info_json:

    for line in script_file:
        line = line.strip()  # Remove indentation or leading blank spaces
        extract_package(line, extracted_data)
        extract_function(line, extracted_data)
        extract_class(line, extracted_data)
        extract_variable(line, extracted_data)

    for key in extracted_data:
        extracted_data[key] = list(extracted_data[key])

    json.dump(extracted_data, script_info_json)
