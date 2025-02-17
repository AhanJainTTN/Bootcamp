import json


def append_quotechar(item, quotechar):
    return quotechar + item + quotechar


def extract_headers(obj):
    delimiter = ","
    quotechar = '"'
    return ",".join(
        item if delimiter not in item else append_quotechar(item, quotechar)
        for item in obj.keys()
    )


def extract_data(obj):
    delimiter = ","
    quotechar = '"'
    return ",".join(
        item if delimiter not in item else append_quotechar(item, quotechar)
        for item in obj.values()
    )


with open(
    "/home/ahan/Documents/Bootcamp/Week_03/Exercises/ex_03/files/sample.json", "r"
) as json_file, open(
    "/home/ahan/Documents/Bootcamp/Week_03/Exercises/ex_03/files/sample_csv_json.csv",
    "w",
) as csv_file:
    data = json.load(json_file)
    # csv_file.write(extract_headers(data) + "\n")
    first_row = True
    for row in data:
        if first_row:
            csv_file.write(extract_headers(row) + "\n")
            first_row = False
        else:
            csv_file.write(extract_data(row) + "\n")
