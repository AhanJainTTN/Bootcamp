import csv
import json


class CSVtoJSON:

    def __init__(self, delimiter, quotechar, csv_path, json_path):
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.csv_path = csv_path
        self.json_path = json_path

    def process_row(self, csv_row):
        pass

    def process_csv(self):

        headers = list()
        data = list()

        with open(
            self.csv_path,
            "r",
        ) as csv_file:
            csv_file_reader = csv.reader(
                csv_file, delimiter=self.delimiter, quotechar=self.quotechar
            )

    def extract_headers(self, csv_row):
        headers = row

    def dump_to_json(self, data):
        with open(self.json_path, "w") as json_output_file:
            json.dump(data, json_output_file)


headers = list()
data = list()

with open(
    "/home/ahan/Documents/Bootcamp/Week_03/Exercises/ex_03/files/sample.csv", "r"
) as csv_file:

    csv_file_reader = csv.reader(csv_file, delimiter=",", quotechar='"')

    row_one = True
    for row in csv_file_reader:
        if row_one:
            headers = row
            row_one = False
        else:
            row_dict = dict()
            for i, item in enumerate(row):
                row_dict[headers[i]] = item
            data.append(row_dict)

    json_path = (
        "/home/ahan/Documents/Bootcamp/Week_03/Exercises/ex_03/files/sample.json"
    )

    with open(json_path, "w") as json_output_file:
        json.dump(data, json_output_file)
