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

    for line in data[:5]:  # Samples from first 5 lines
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
        # If not inside quotes and delimiter encountered - split
        elif char == delimiter and not in_quotes:
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
    if not data:
        print("No data to display.")
        return

    # Transpose the data matrix: each inner tuple represents a column now
    transposed_data = list(zip(*data))

    # For each column, find the longest value (based on string length)
    column_widths = [len(max(column, key=len)) for column in transposed_data]

    headers = data[0]
    actual_data = data[1:]

    formatted_headers = " | ".join(
        str(header).upper().ljust(column_widths[i]) for i, header in enumerate(headers)
    )
    separator = "-*-".join("-" * column_widths[i] for i in range(len(headers)))

    formatted_data = [formatted_headers, separator]
    for row in actual_data:
        formatted_row = " | ".join(
            str(value).ljust(column_widths[i]) for i, value in enumerate(row)
        )
        formatted_data.append(formatted_row)

    print("\n")

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


def apply_filters(
    data: List[List[str]],
    skip: Optional[int],
    head: Optional[int],
    tail: Optional[int],
) -> List[List[str]]:
    data = skip_nrows(data, skip)
    data = head_nrows(data, head)
    data = tail_nrows(data, tail)
    return data


def main() -> None:
    """
    Main CLI entry point to parse arguments and display CSV data.

    Features:
    - Delimiter guessing
    - Quoted fields parsing
    - Column filtering
    - Head, tail, and row skipping
    """

    parser = argparse.ArgumentParser(
        description="csvlook: Display CSV files in a clean tabular format."
    )

    parser.add_argument("csvpath", type=str, help="Path to the CSV file.")
    parser.add_argument(
        "-f",
        type=str,
        default=None,
        help="Comma-separated list of 1-based column indices to display (e.g. 1,3,4).",
    )
    parser.add_argument(
        "-d",
        default=None,
        help="Specify the delimiter used in the file. If omitted, it will be guessed.",
    )
    parser.add_argument(
        "-q",
        "--quotechar",
        type=str,
        default='"',
        help='Character used to quote values (default: ").',
    )
    parser.add_argument(
        "--skip-row",
        type=int,
        default=0,
        help="Number of rows to skip from the top (excluding header).",
    )
    parser.add_argument("--head", type=int, help="Display only the first N data rows.")
    parser.add_argument("--tail", type=int, help="Display only the last N data rows.")

    args = parser.parse_args()

    selected_cols = [int(x) - 1 for x in args.f.split(",")] if args.f else None

    print(f"\nCSV Path: {args.csvpath}")
    print(
        f"Selected Columns: {None if not args.f else tuple(col + 1 for col in selected_cols)}",
    )
    print(f"Skip Rows: {args.skip_row}")
    print(f"Head: {args.head}")
    print(f"Tail: {args.tail}")
    print(f"Quote Character: {args.quotechar}")
    print(f"Delimiter: {args.d}")

    with open(args.csvpath, "r") as csv_file:

        raw_data = [line.rstrip("\n") for line in csv_file]
        delimiter = args.d if args.d else guess_delimiter(raw_data)
        cleaned_data = [
            parse_csv_line(row, delimiter, args.quotechar) for row in raw_data
        ]

        data_headers, row_data = cleaned_data[0], cleaned_data[1:]

        row_data = apply_filters(
            data=row_data, skip=args.skip_row, head=args.head, tail=args.tail
        )

        filtered_data = [data_headers] + row_data

        if selected_cols:
            filtered_data = [
                [row[col] for col in selected_cols if col < len(row)]
                for row in filtered_data
            ]

        format_and_display(filtered_data)
        print("\n")


if __name__ == "__main__":
    main()
