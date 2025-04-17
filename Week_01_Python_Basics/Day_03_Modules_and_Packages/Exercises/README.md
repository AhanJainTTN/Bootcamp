# find.py

A Python script that mimics the basic functionality of the Linux `find` command. This utility recursively searches for files and directories in a given directory, supporting filters such as name pattern, file type, access time, and maximum search depth.

## Features

- Filter files or directories by **name pattern** using wildcards (e.g. `*.py`)
- Filter by **file type**: regular files (`-type f`) or directories (`-type d`)
- Filter based on **access time** in days (`-atime`)
- Restrict search using **maximum directory depth** (`-maxdepth`)

## Usage

```bash
python find.py [directory] [OPTIONS]
```

### Positional Argument

- `directory`: The root directory to search from. Defaults to the current working directory.

### Options

| Option      | Description                                                           |
| ----------- | --------------------------------------------------------------------- |
| `-name`     | Wildcard pattern to match filenames (e.g. `"*.txt"`, `"data_*.csv"`). |
| `-type`     | File type: `f` for files, `d` for directories.                        |
| `-atime`    | Access time in days. Finds files accessed within the last N days.     |
| `-maxdepth` | Maximum depth of directory traversal. Default is `2`.                 |

> Note: The `-atime` option only supports filtering files accessed **within** the last N days.

## Examples

### 1. Find all `.py` files accessed in the last 7 days (up to 2 levels deep):

```bash
python find.py ~/ -name "*.py" -type f -atime 7 -maxdepth 2
```

### 2. Find directories with names starting with `test`:

```bash
python find.py ./projects -name "test*" -type d
```

### 3. Find all files at any depth:

```bash
python find.py /var/logs -type f -maxdepth 10
```

## Notes

- The script uses `fnmatch` for shell-style wildcard matching.
- Access time is calculated using the `os.path.getatime()` function.
- File system permission errors are not currently handled; unreadable directories may raise exceptions.
- Access time is compared to the current time and converted to whole days (24-hour periods).

## Limitations

- Only supports access time filtering as "within N days".
- Does not support modification time or more complex expressions like `+N` or `-N`.
- No support for symbolic link resolution or advanced file attributes.

## License

MIT License
