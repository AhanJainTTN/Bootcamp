def encode_animals(input_string: str) -> str:
    """
    Takes an input string with animals and encodes as per the following pattern:

    Appends a new ascii character to the output string, starting from `a`, for every unique animal encountered.

    Args:
    input_string (str): The input string to be encoded.

    Returns:
    str: The encoded string.

    Example:
    Input: "dog cat dog dog cow rat elephant"
    Output: abaacde
    """
    output_str = ""
    curr_char = 97  # starting ascii value
    animal_mapping = dict()  # dictionary to maintain character to animal mappings
    animals = input_string.split()

    # assigns ascii character if animal already present
    # else assigns the next available character
    for animal in animals:
        if animal_mapping.get(animal) is None:
            animal_mapping[animal] = chr(curr_char)
            curr_char += 1
        output_str += animal_mapping.get(animal)

    print(animal_mapping)
    return output_str


def main():
    """Entry point of the script."""
    input_str = "dog cat dog dog cow rat elephant"
    print(encode_animals(input_str))


if __name__ == "__main__":
    main()
