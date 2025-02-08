"""
Write a `find.py` script which implemnts Linux `find` command Implemnt below options: `-name` `-atime` `-type` `-maxdepth` Example use: To find all ".py" files (not folders) in home directory and 2 level sub-directories which where created recently in last 7 days write find.py ~/ -name "*.py" -type f -atime -7
"""

import os
import time
import argparse


def valid_dir(directory):
    return os.path.isdir(directory)


def valid_atime(filepath, atime):
    if atime is None:
        return True
    atime_seconds = atime * 86400
    return time.time() - os.path.getatime(filepath) <= atime_seconds


def is_match(filename, search_pattern):

    if not search_pattern or filename == search_pattern or search_pattern == "*.*":
        return True

    base_name, extension = os.path.splitext(filename)

    if (
        search_pattern.endswith(".*")
        and base_name == os.path.splitext(search_pattern)[0]
    ):
        return True
    if (
        search_pattern.startswith("*.")
        and extension == os.path.splitext(search_pattern)[1]
    ):
        return True

    return False


def find_file(search_pattern, search_type, atime, directory, depth, matches):

    if depth <= 0:
        return

    for filename in os.listdir(directory):

        full_path = os.path.join(directory, filename)

        if valid_atime(full_path, atime) and is_match(filename, search_pattern):

            file_type = "Directory" if os.path.isdir(full_path) else "File"

            if search_type == None:
                matches.append(f"{file_type}: {full_path}")
            elif search_type == "d" and file_type == "Directory":
                matches.append(f"{file_type}: {full_path}")
            elif search_type == "f" and file_type == "File":
                matches.append(f"{file_type}: {full_path}")

        if os.path.isdir(full_path):
            find_file(search_pattern, search_type, atime, full_path, depth - 1, matches)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-name", default=None)
    parser.add_argument("-type", choices=["d", "f"], default=None)
    parser.add_argument("-maxdepth", type=int, default=float("inf"))
    parser.add_argument("-atime", type=int, default=None)
    parser.add_argument("directory", type=str, default=os.getcwd(), nargs="?")
    args = parser.parse_args()

    directory = args.directory
    search_pattern = args.name
    max_depth = args.maxdepth
    atime = args.atime
    file_type = args.type

    matches = list()

    if valid_dir(directory):
        find_file(search_pattern, file_type, atime, directory, max_depth, matches)
    else:
        print("Not a valid directory.")

    if matches:
        for match in matches:
            print(match)
    else:
        print("No matches found.")
