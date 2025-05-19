"""
Write a `find.py` script which implemnts Linux `find` command Implemnt below options: `-name` `-atime` `-type` `-maxdepth` Example use: To find all ".py" files (not folders) in home directory and 2 level sub-directories which where created recently in last 7 days write find.py ~/ -name "*.py" -type f -atime -7
"""

import os
import time
import argparse
import fnmatch
from typing import List, Optional


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
    Checks if filename matches the given wildcard pattern using fnmatch.

    Args:
        filename (str): The name of the file.
        pattern (Optional[str]): The wildcard pattern.

    Returns:
        bool: True if pattern matches or pattern is None.
    """
    if not search_pattern:
        return True

    return fnmatch.fnmatch(filename, search_pattern)


def find_files(
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
            find_files(
                search_pattern, search_type, atime, full_path, depth - 1, matches
            )


def main() -> None:
    """
    Entry point of the script. Emulates Linux `find` with basic filters:
    - Name pattern match
    - File type: file or directory
    - Access time filtering (in days)
    - Max depth of recursion
    """
    parser = argparse.ArgumentParser(
        description="Replicates basic functionality of the Linux `find` command."
    )
    parser.add_argument("directory", type=str, nargs="?", default=os.getcwd())
    parser.add_argument("-name", type=str, help="Wildcard pattern to match file names.")
    parser.add_argument(
        "-type", choices=["f", "d"], help="File type: f (file), d (directory)."
    )
    parser.add_argument(
        "-atime",
        type=str,
        help="Access time filter in days.",
    )
    parser.add_argument(
        "-maxdepth", type=int, default=2, help="Max depth of directory traversal."
    )
    args = parser.parse_args()

    matches: List[str] = []

    if os.path.isdir(args.directory):
        find_files(
            args.name, args.type, args.atime, args.directory, args.maxdepth, matches
        )
    else:
        print("Not a valid directory.")

    if matches:
        for match in matches:
            print(match)
    else:
        print("No matches found.")


if __name__ == "__main__":
    main()
