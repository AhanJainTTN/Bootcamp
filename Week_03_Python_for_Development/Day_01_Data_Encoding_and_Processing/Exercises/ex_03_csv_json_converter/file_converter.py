"""
Part-1:

Write a simple script to tranlate CSV file into JSON file 

Input: example CSV file
Output: .json file - each line is valid JSON equvilent to a row in CSV file

Part-2:
Write a script to tranlate a simple JSON file (white each line is a valid JSON) into .CSV file

Assume that JSONs are not nested

Part-3:
Write a simple function using StringIO which can transalte a "dict" into a comma-seprated string 
"""

import csv
import json
from io import StringIO
from typing import Dict, Any


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Reads a CSV file and converts it into a JSON file, where each line is a valid JSON equivalent to a row in CSV.
    """
    # newline="" because on Windows newlines are stored as \r\n (and just \n on Mac and Linux).
    # As a result, if a file is opened without specifying newline, open() translates \r\n into \n\n,
    # making csvreader think there is an extra line when in fact it is just a blank line.
    # This blank line gets processed as a blank object in our JSON.
    # newline="" prevents open() from translating \r\n to \n\n.
    # It passes the file as it is to the csv module.
    with open(csv_path, "r", newline="") as csv_file, open(
        json_path, "w"
    ) as json_output_file:
        # The csv.DictReader returns a generator that yields dictionaries row by row.
        # This approach first loads the entire file as a list into memory after which it is dumped to JSON.
        # A more memory-focused approach would be to iterate through the dictreader generator object
        # and append to JSON one line at a time - however, JSONs are more suitable to be dumped at once.
        json.dump(
            list(csv.DictReader(csv_file, delimiter=",", quotechar='"')),
            json_output_file,
        )


def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Reads a JSON file where each line is a valid JSON and converts it into a CSV file.
    Assumes JSON objects are not nested.
    """
    with open(json_path, "r") as json_input_file, open(
        csv_path, "w", newline=""
    ) as csv_file:
        data = json.load(json_input_file)
        headers = data[0].keys() if data else []

        # writer is an object which operates like a regular writer but maps dictionaries onto output rows.
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # using fieldnames specified at the time of csvwriter object creation,
        # writes the first row in the CSV file, which contains the column headers.
        writer.writeheader()

        # Writes multiple rows at once from a list of dictionaries.
        writer.writerows(data)


def dict_to_csv_string(data: Dict[Any, Any]) -> str:
    """
    Converts a dictionary into a comma-separated string using StringIO.
    """
    # Creating an in-memory file object
    output_file = StringIO()
    # now we can interact with it just like any other file object
    headers = data.keys() if data else []
    # The quotechar only comes into play if the delimiter is the same as one of the multi value separators
    writer = csv.DictWriter(
        output_file, fieldnames=headers, delimiter=";", quotechar='"'
    )
    writer.writeheader()
    # writerow vs writerows:
    # writerow writes one dictionary row at a time.
    # writerows writes a list of dictionaries all at once.
    writer.writerow(data)
    # Equivalent in this context:
    # writer.writerows([data])
    # Blank output because seek pointer is set to end of file i.e. place of last write
    # since StringIO works like a file opened in write mode
    output_file.seek(0)  # Move to the start of the StringIO buffer
    result = output_file.read()
    # In-memory file so .close() not necessary and garbage collector automatically cleans up.
    # Use .close() to explicitly free up memory.
    output_file.close()

    return result


def main() -> None:
    # File paths
    csv_path_1 = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_01_Data_Encoding_and_Processing/Exercises/ex_03_csv_json_converter/files/sample.csv"
    json_path_1 = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_01_Data_Encoding_and_Processing/Exercises/ex_03_csv_json_converter/files/csv_to_json.json"
    csv_path_2 = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_01_Data_Encoding_and_Processing/Exercises/ex_03_csv_json_converter/files/json_to_csv.csv"
    json_path_2 = "/Users/ahan/Documents/GitHub/Bootcamp/Week_03_Python_for_Development/Day_01_Data_Encoding_and_Processing/Exercises/ex_03_csv_json_converter/files/sample.json"

    # Convert CSV to JSON
    csv_to_json(csv_path_1, json_path_1)
    # Convert JSON to CSV
    json_to_csv(json_path_2, csv_path_2)

    # Convert Dictionary to CSV String
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
    csv_string = dict_to_csv_string(data)
    print(csv_string)


if __name__ == "__main__":
    main()
