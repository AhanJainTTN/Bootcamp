import os
import time
import argparse
import fnmatch


def valid_dir(dir):

    if not os.path.isdir(dir):
        return False
    else:
        return True


def valid_atime(filepath, atime):

    if atime is None:
        return True

    atime_seconds = atime * 86400
    current_time = time.time()
    file_atime = os.path.getatime(filepath)

    return current_time - file_atime <= atime_seconds


def find_file(file, type, atime, filepath, depth, matches):

    if depth <= 0:
        return

    for f in os.listdir(filepath):

        full_path = os.path.join(filepath, f)

        # if file is not None or fnmatch.fnmatch(f,file):

        if f == file and valid_atime(full_path, atime):

            file_type = "Directory" if os.path.isdir(full_path) else "File"

            if type == None:
                matches.append(f"{file_type}: {full_path}")
            elif type == "d" and os.path.isdir(full_path):
                matches.append(f"{file_type}: {full_path}")
            elif type == "f" and not os.path.isdir(full_path):
                matches.append(f"{file_type}: {full_path}")

        if os.path.isdir(full_path):
            find_file(file, type, atime, full_path, depth - 1, matches)


if __name__ == "__main__":

    matches = list()

    parser = argparse.ArgumentParser()
    parser.add_argument("-name")
    parser.add_argument("-type")
    parser.add_argument("-maxdepth", type=int)
    parser.add_argument("-atime", type=int)
    parser.add_argument("directory", type=str)
    args = parser.parse_args()

    dir = args.directory if dir else os.getcwd()
    file = args.name
    depth = args.maxdepth
    atime = args.atime
    type = args.type

    if valid_dir(dir):
        find_file(file, type, atime, dir, depth, matches)
    else:
        print("Not a valid directory.")

    if matches:
        for match in matches:
            print(match)
    else:
        print("No matches found.")
