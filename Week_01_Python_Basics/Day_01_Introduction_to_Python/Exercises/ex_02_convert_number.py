"""
Write a code to print the binary, octal, or hexadecimal representation of a number. Do not use any third-party library.
"""


def to_binary(num: int) -> int:
    """
    Converts given integer base 10 10 number to binary.

    Args:
        num (int): The base 10 number to be converted.

    Returns:
        int: COnverted binary number.
    """
    ans = ""

    while num:
        ans = str(num % 2) + ans
        num = num // 2

    return int(ans)


def to_octal(num: int) -> int:
    """
    Converts given integer base 10 number to octal.

    Args:
        num (int): The base 10 number to be converted.

    Returns:
        int: COnverted octal number.
    """
    ans = ""

    while num:
        ans = str(num % 8) + ans
        num = num // 8

    return int(ans)


def to_hexadecimal(num: int) -> int:
    """
    Converts given integer base 10 number to hexadecimal.

    Args:
        num (int): The base 10 number to be converted.

    Returns:
        int: COnverted hexadecimal number.
    """
    # for equivalent hexadecimal lookup
    hexa_map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]

    ans = ""

    while num:
        ans = str(hexa_map[num % 16]) + ans
        num = num // 16

    return ans


def main():
    """
    Entry point for the script. Converts an integer to binary, octal and hexadecimal equivalents.
    """
    num = int(input("Enter a Number: "))
    print("Binary: ", to_binary(num))
    print("Octal: ", to_octal(num))
    print("Hexadecimal: ", to_hexadecimal(num))


if __name__ == "__main__":
    main()
