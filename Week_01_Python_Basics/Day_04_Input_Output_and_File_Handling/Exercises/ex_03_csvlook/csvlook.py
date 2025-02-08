"""
Without using Python CSV module write a "csvlook` command csvlook should have following features: * [-d DELIMITER] if -`d` option not paased script should be able to guess a seperator * [-q QUOTECHAR] used to parsed colum value parenthesised within QUOTECHAR, if the value not passed should assume default value dboult quote `csvlook` should display data nicely on console in uniform width To project the data `csvlook` script should accept comma seprated colum numbers, e.g -f 3,5,7 should print only column 3, 5 7 --skip-row N to skil first N rows --head N to display only first N rows --tail N to display last N rows
"""

import argparse


def guess_delimiter(data):
    delimiters = (",", "\t", " ", ";", "|")
    delimiter_counts = {delimiter: 0 for delimiter in delimiters}

    for line in data:
        for delimiter in delimiters:
            delimiter_counts[delimiter] += line.count(delimiter)

    return max(delimiter_counts, key=delimiter_counts.get)


def parse_csv_line(line, delimiter, quotechar='"'):
    values = []
    current_value = []
    in_quotes = False

    for char in line:
        if char == quotechar:  # Toggle quote status
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:  # If not inside quotes, split here
            values.append("".join(current_value).strip())
            current_value = []
        else:
            current_value.append(char)

    values.append("".join(current_value).strip())  # Add last column
    return values


def format_and_display(data):

    print("\n")

    column_widths = [0] * len(data[0])
    for row in range(len(data)):
        for col in range(len(data[0])):
            curr_length = len(data[row][col])
            column_widths[col] = max(curr_length, column_widths[col])

    headers = data[0]
    actual_data = data[1:]

    formatted_headers = " | ".join(
        str(header).upper().ljust(column_widths[i]) for i, header in enumerate(headers)
    )
    separator = "-*-".join("-" * column_widths[i] for i in range(len(headers)))

    formatted_data = list()
    formatted_data.append(formatted_headers)
    formatted_data.append(separator)

    for row in actual_data:
        formatted_row = " | ".join(
            str(value).ljust(column_widths[i]) for i, value in enumerate(row)
        )
        formatted_data.append(formatted_row)

    for row in formatted_data:
        print(row)


def skip_nrows(data, n=0):
    return data[n:]


def head_nrows(data, n=None):
    return data[:n] if n else data


def tail_nrows(data, n=None):
    return data[-n:] if n else data


if __name__ == "__main__":

    print("\n")

    parser = argparse.ArgumentParser(
        description="Process a CSV file with filtering options."
    )

    # Required argument
    parser.add_argument("csvpath", type=str, help="Path to the CSV file.")

    # Optional arguments
    parser.add_argument("-f", type=str, default=None)
    parser.add_argument("-d", default=None)
    parser.add_argument("--skip-row", type=int, default=0)
    parser.add_argument("--head", type=int, default=None)
    parser.add_argument("--tail", type=int, default=None)
    parser.add_argument("-q", "--quotechar", type=str, default='"')

    args = parser.parse_args()

    csvpath = args.csvpath
    skip_row = args.skip_row
    head = args.head
    tail = args.tail
    quotechar = args.quotechar
    selected_cols = list(map(int, args.f.split(",").strip())) if args.f else None
    delimiter = args.d

    # Debug print
    print(f"CSV Path: {csvpath}")
    print(f"Selected Columns: {selected_cols}")
    print(f"Skip Rows: {skip_row}")
    print(f"Head: {head}")
    print(f"Tail: {tail}")
    print(f"Quote Character: {quotechar}")
    print(f"Delimiter: {delimiter}")

    with open(csvpath, "r") as csv_file:

        raw_data = list()
        for line in csv_file:
            line = line.rstrip("\n")
            raw_data.append(line)

        if not delimiter:
            delimiter = guess_delimiter(raw_data)

        cleaned_data = [parse_csv_line(row, delimiter, quotechar) for row in raw_data]

        data_headers = cleaned_data[0]
        row_data = cleaned_data[1:]

        row_data = skip_nrows(row_data, skip_row)
        row_data = head_nrows(row_data, head)
        row_data = tail_nrows(row_data, tail)

        filtered_data = list()
        filtered_data.append(data_headers)
        for row in row_data:
            filtered_data.append(row)

        final_data = list()
        if selected_cols:
            for row in filtered_data:
                filtered_row = [row[col] for col in selected_cols if col < len(row)]
                final_data.append(filtered_row)
        else:
            final_data = filtered_data

        format_and_display(final_data)
        print("\n")
