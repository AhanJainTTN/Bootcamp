"""
From a multi-words and multi-line string, prepare a dict with key as "word" and value as occureance of word.

Example:
----------
Input = Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.

Output (Partial): {'the': 5, 'to': 4, 'Python': 3, 'quotes': 3, 'one': 3, 'and': 3, 'a': 3, 'multiline': 3, 'Using': 2, 'triple': 2, 'string.': 2, 'at': 2, 'Multiline': 1, 'String': 1, 'Triple-Quotes': 1, 'style': 1, 'is': 1, 'of': 1, 'easiest': 1, 'most': 1, 'common': 1, 'ways': 1, 'split': 1, 'large': 1, 'string': 1, 'into': 1, 'Triple': 1, "('''": 1, 'or': 1...

Complexity Analysis
-------------------
TC: O(n) where n is the length of the string
SC: O(n) additional space used by astring.split()
"""

from typing import Dict


def word_frequency_counter(text: str) -> Dict[str, int]:
    """
    Counts the occurrences of each word in the given text using a dictionary.

    Args:
        text (str): The input string.

    Returns:
        dict[str, int]: A dictionary with words as keys and their frequencies as values.
    """
    word_count: Dict[str, int] = {}
    for word in text.split():
        word_count[word] = (
            word_count.get(word, 0) + 1
        )  # .get(key, default value if key does not exist)
    return word_count


def main() -> None:
    """
    Entry point of the script. Computes and prints word frequency using dictionary.
    """
    astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""
    print(word_frequency_counter(astring))


if __name__ == "__main__":
    main()
