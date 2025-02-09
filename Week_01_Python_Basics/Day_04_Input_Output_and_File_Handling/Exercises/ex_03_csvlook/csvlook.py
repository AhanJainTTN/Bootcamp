"""
Without using Python CSV module write a "csvlook` command csvlook should have following features: * [-d DELIMITER] if -`d` option not paased script should be able to guess a seperator * [-q QUOTECHAR] used to parsed colum value parenthesised within QUOTECHAR, if the value not passed should assume default value dboult quote `csvlook` should display data nicely on console in uniform width To project the data `csvlook` script should accept comma seprated colum numbers, e.g -f 3,5,7 should print only column 3, 5 7 --skip-row N to skil first N rows --head N to display only first N rows --tail N to display last N rows
"""

import argparse
from typing import List, Optional


def guess_delimiter(data: List[str]) -> str:
    """
    Determines the most frequently occurring delimiter in the given data.

    Args:
        data (List[str]): A list of CSV lines.

    Returns:
        str: The most frequently used delimiter.
    """
    delimiters = (",", "\t", " ", ";", "|")
    delimiter_counts = {delimiter: 0 for delimiter in delimiters}

    for line in data:
        for delimiter in delimiters:
            delimiter_counts[delimiter] += line.count(delimiter)

    return max(delimiter_counts, key=delimiter_counts.get)


def parse_csv_line(line: str, delimiter: str, quotechar: str = '"') -> List[str]:
    """
    Parses a single CSV line into a list of values, handling quoted values.

    Args:
        line (str): The CSV line to parse.
        delimiter (str): The delimiter used in the CSV file.
        quotechar (str): The character used to quote values.

    Returns:
        List[str]: A list of parsed values.
    """
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


def format_and_display(data: List[List[str]]) -> None:
    """
    Formats and prints the CSV data in a readable tabular format.

    Args:
        data (List[List[str]]): The parsed CSV data.
    """
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

    formatted_data = formatted_data = [formatted_headers, separator]

    for row in actual_data:
        formatted_row = " | ".join(
            str(value).ljust(column_widths[i]) for i, value in enumerate(row)
        )
        formatted_data.append(formatted_row)

    for row in formatted_data:
        print(row)


def skip_nrows(data: List[List[str]], n: int = 0) -> List[List[str]]:
    """
    Skips the first N rows of the data.

    Args:
        data (List[List[str]]): The input data.
        n (int, optional): The number of rows to skip. Defaults to 0.

    Returns:
        List[List[str]]: The filtered data.
    """
    return data[n:] if n else data


def head_nrows(data: List[List[str]], n: Optional[int] = None) -> List[List[str]]:
    """
    Returns the first N rows of the data.

    Args:
        data (List[List[str]]): The input data.
        n (Optional[int], optional): The number of rows to return. Defaults to None.

    Returns:
        List[List[str]]: The filtered data.
    """
    return data[:n] if n else data


def tail_nrows(data: List[List[str]], n: Optional[int] = None) -> List[List[str]]:
    """
    Returns the last N rows of the data.

    Args:
        data (List[List[str]]): The input data.
        n (Optional[int], optional): The number of rows to return. Defaults to None.

    Returns:
        List[List[str]]: The filtered data.
    """
    return data[-n:] if n else data


def main() -> None:
    """
    Entry point of the script. Parses command-line arguments and processes the CSV file.
    """
    print("\n")

    parser = argparse.ArgumentParser(
        description="Process a CSV file with filtering options."
    )

    # Required argument
    parser.add_argument("csvpath", type=str, help="Path to the CSV file.")

    # Optional arguments
    parser.add_argument("-f", type=str, default=None)
    parser.add_argument("-d", default=None)
    parser.add_argument("--skip-row", type=int, default=None)
    parser.add_argument("--head", type=int, default=None)
    parser.add_argument("--tail", type=int, default=None)
    parser.add_argument("-q", "--quotechar", type=str, default='"')

    args = parser.parse_args()

    csvpath: str = args.csvpath
    skip_row: Optional[int] = args.skip_row
    head: Optional[int] = args.head
    tail: Optional[int] = args.tail
    quotechar: str = args.quotechar
    delimiter: Optional[str] = args.d
    selected_cols: Optional[List[int]] = (
        [int(x) for x in args.f.split(",")] if args.f else None
    )

    # Debug print
    print(f"CSV Path: {csvpath}")
    print(f"Selected Columns: {selected_cols}")
    print(f"Skip Rows: {skip_row}")
    print(f"Head: {head}")
    print(f"Tail: {tail}")
    print(f"Quote Character: {quotechar}")
    print(f"Delimiter: {delimiter}")

    with open(csvpath, "r") as csv_file:

        raw_data = [line.rstrip("\n") for line in csv_file]

        if not delimiter:
            delimiter = guess_delimiter(raw_data)

        cleaned_data = [parse_csv_line(row, delimiter, quotechar) for row in raw_data]

        data_headers = cleaned_data[0]
        row_data = cleaned_data[1:]

        row_data = skip_nrows(row_data, skip_row)
        row_data = head_nrows(row_data, head)
        row_data = tail_nrows(row_data, tail)

        filtered_data = [data_headers] + row_data

        if selected_cols:
            final_data = [
                [row[col] for col in selected_cols if col < len(row)]
                for row in filtered_data
            ]
        else:
            final_data = filtered_data

        format_and_display(final_data)
        print("\n")


if __name__ == "__main__":
    main()
