"""
From a multi-word and multi-line string, filter and list only words
that occur multiple times.

Example:
----------
Input = Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.

Output: Python Using the triple quotes one and to a multiline string. at

Complexity Analysis
-------------------
TC: O(n) where n is the length of the string
SC: O(n) additional space taken by word_count
"""

from typing import Dict, List


def get_frequent_words(text: str, frequency: int = 2) -> List[str]:
    """
    Identifies words that appear at least 'frequency' times in the given text.

    Args:
        text (str): The input string.
        frequency (int): The minimum number of occurrences required to include a word in the result.

    Returns:
        list[str]: A list of words that appear at least 'frequency' times.
    """
    word_count: Dict[str, int] = {}
    for word in text.split():
        word_count[word] = (
            word_count.get(word, 0) + 1
        )  # .get(key, default value if key does not exist)

    filtered_list = [k for k in word_count if word_count[k] >= frequency]

    return filtered_list


def main() -> None:
    """
    Entry point of the script. Computes and prints words with multiple occurrences in the input string.
    """
    astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""
    print(" ".join(get_frequent_words(astring, 2)))


if __name__ == "__main__":
    main()
