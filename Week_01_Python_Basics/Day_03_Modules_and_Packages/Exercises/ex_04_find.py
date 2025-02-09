"""
Write a `find.py` script which implemnts Linux `find` command Implemnt below options: `-name` `-atime` `-type` `-maxdepth` Example use: To find all ".py" files (not folders) in home directory and 2 level sub-directories which where created recently in last 7 days write find.py ~/ -name "*.py" -type f -atime -7
"""

import os
import time
import argparse
from typing import List, Optional


def valid_dir(directory: str) -> bool:
    """
    Checks if the given directory path is valid.
    """
    return os.path.isdir(directory)


def valid_atime(filepath: str, atime: Optional[int]) -> bool:
    """
    Checks if the file's last access time is within the given threshold.

    Args:
        filepath (str): The path to the file.
        atime (Optional[int]): Access time filtering criteria.

    Returns:
        bool: True if the file meets the access time criteria, False otherwise.
    """
    if atime is None:
        return True
    atime_seconds = atime * 86400  # Convert days to seconds
    return time.time() - os.path.getatime(filepath) <= atime_seconds


def is_match(filename: str, search_pattern: Optional[str]) -> bool:
    """
    Checks if a filename matches a search pattern.

    Args:
        filename (str): The filename to check.
        search_pattern (Optional[str]): The pattern to match against.

    Returns:
        bool: True if the filename matches the pattern, False otherwise.
    """
    if not search_pattern or search_pattern == "*.*" or filename == search_pattern:
        return True

    file_base, file_ext = os.path.splitext(filename)
    search_base, search_ext = os.path.splitext(search_pattern)

    if search_pattern.endswith(".*") and file_base == search_base:
        return True
    if search_pattern.startswith("*.") and file_ext == search_ext:
        return True

    return False


def find_file(
    search_pattern: Optional[str],
    search_type: Optional[str],
    atime: Optional[int],
    directory: str,
    depth: int,
    matches: List[str],
) -> None:
    """
    Recursively searches for files or directories matching the given criteria.

    Args:
        search_pattern (Optional[str]): The pattern to match filenames.
        search_type (Optional[str]): The type of file to search for ('d' for directories, 'f' for files).
        atime (Optional[int]): The access time filter in days.
        directory (str): The directory to search in.
        depth (int): The maximum depth to search.
        matches (List[str]): A list to store matching file paths.
    """
    if depth < 0:
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


def main() -> None:
    """
    Entry point of the script. Parses command-line arguments and searches for files based on criteria.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-name", default=None)
    parser.add_argument("-type", choices=["d", "f"], default=None)
    parser.add_argument("-maxdepth", type=int, default=2)
    parser.add_argument("-atime", type=int, default=None)
    parser.add_argument("directory", type=str, default=os.getcwd(), nargs="?")
    args = parser.parse_args()

    directory: str = args.directory
    search_pattern: Optional[str] = args.name
    max_depth: int = args.maxdepth
    atime: Optional[int] = args.atime
    file_type: Optional[str] = args.type

    matches: List[str] = []

    if valid_dir(directory):
        find_file(search_pattern, file_type, atime, directory, max_depth, matches)
    else:
        print("Not a valid directory.")

    if matches:
        for match in matches:
            print(match)
    else:
        print("No matches found.")


if __name__ == "__main__":
    main()
