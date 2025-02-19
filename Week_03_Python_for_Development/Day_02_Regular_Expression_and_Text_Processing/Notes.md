Regex Notes

r'^((\d)|(\d\d))[A-Za-z]{3,}\.{0,3}$' vs.
r'^(\d)|(\d\d)[A-Za-z]{3,}\.{0,3}$' vs.
r'^\d{1,2}[A-Za-z]{3,}\.{0,3}$'

r'^(\d)|(\d\d)[A-Za-z]{3,}\.{0,3}$' only considers anchor for the first \d i.e. either look for string starting with a single digit only or any string with two consecutive digits and the remaining pattern.

^((\d)|(\d\d))[A-Za-z]{3,}\.{0,3}$ makes the grouping explicit i.e. either the first char is a digit or the first two chars are digits (followed by the rest of the pattern in both cases).
