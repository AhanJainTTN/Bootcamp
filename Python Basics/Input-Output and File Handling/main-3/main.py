# traverses rows matrix to find greatest length in each column - used to calculate maxwidth
def calc_column_width(rows):

    max_width = list(0 for i in range(len(rows[0])))

    for row in range(len(rows)):
        for col in range(len(rows[0])):
            curr_length = len(rows[row][col])
            max_width[col] = max(curr_length, max_width[col])

    print(max_width)
    return max_width


def display_csv(rows):
    pass


delimiter = ";"

with open(
    "Python Basics/Input-Output and File Handling/main-3/files/sample.csv", "r"
) as csv_file:

    rows = []
    for line in csv_file:
        line = line.rstrip("\n")
        rows.append(line.split(delimiter))

    print(rows)
    col_width = calc_column_width(rows)
