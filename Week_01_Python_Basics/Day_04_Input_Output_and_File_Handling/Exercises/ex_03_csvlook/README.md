# csvlook

A Python command-line utility to display CSV data in a clean, tabular format — built without using Python's built-in `csv` module.

This tool is inspired by the `csvlook` command from `csvkit`, and supports flexible options such as delimiter detection, column filtering, and row slicing.

## Features

- Automatically **detects the delimiter** if not specified (`-d`).
- Supports parsing fields **enclosed in a quote character** (`-q`, default is `"`).
- Nicely formatted tabular output with **aligned column widths**.
- Filter output using:
  - Specific columns: `-f 1,3,4`
  - Skip rows: `--skip-row N`
  - Show first N rows: `--head N`
  - Show last N rows: `--tail N`

## Usage

```bash
python csvlook.py path/to/file.csv [OPTIONS]
```

### Required Argument

- `csvpath`: Path to the input CSV file.

### Optional Arguments

| Option         | Description                                                                       |
| -------------- | --------------------------------------------------------------------------------- |
| `-d DELIMITER` | Specify a custom delimiter (e.g. `,`, `;`, `\t`, `⏐`). If omitted, it's guessed.  |
| `-q QUOTECHAR` | Quote character for wrapping fields (default is `"`)                              |
| `-f COLUMNS`   | Comma-separated **1-based** column indices to include in output (e.g. `-f 1,3,5`) |
| `--skip-row N` | Skip the first N rows (excluding the header)                                      |
| `--head N`     | Display only the first N data rows                                                |
| `--tail N`     | Display only the last N data rows                                                 |

> Note: In case both options are present, `--head` is applied before `--tail`.

## Example

### Display full CSV with auto-detected delimiter:

```bash
python csvlook.py data.csv
```

### Display only selected columns:

```bash
python csvlook.py data.csv -f 1,3,5
```

### Skip first 2 rows and show top 5 records:

```bash
python csvlook.py data.csv --skip-row 2 --head 5
```

### Use semicolon delimiter and single quote as quotechar:

```bash
python csvlook.py data.csv -d ';' -q "'"
```

## Implementation Notes

- The script does **not use the `csv` module**.
- Assumes all data can be read into memory (not designed for very large files).

## Limitations

- Assumes well-formed CSV data.
- Does not support multiline fields inside quotes.
- Only handles one type of quote character per file.

## License

MIT License
