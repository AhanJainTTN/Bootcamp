"""
From a multi-words and multi-line string, display list of words and word's length with occurence more than 1 in sorted order.

Example:
----------
Input: astring = Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it.

Output: Word Length Occurrence Python 6 3 Using 5 2 the 3 5 triple 6 2 quotes 6 3 one 3 3 and 3 3 to 2 4 a 1 3 multiline 9 3 string. 7 2 at 2 2

Complexity Analysis
-------------------
TC: O(n) where n is the length of the string
SC: O(n) additional space taken by word_count
"""

from typing import Dict, List, Tuple


def get_sorted_frequent_words(
    text: str, frequency: int = 2
) -> List[Tuple[str, int, int]]:
    """
     Identifies words that appear at least 'frequency' times in the given text and returns them sorted by frequency.

    Args:
        text (str): The input string.
        frequency (int): The minimum number of occurrences required to include a word in the result.

    Returns:
        list[(str, int, int)]: A list of tuples where each tuple contains:
            - The word (str)
            - The word length (int)
            - The frequency (int)
        The list is sorted by frequency in ascending order.
    """
    word_count: Dict[str, int] = {}
    for word in text.split():
        word_count[word] = (
            word_count.get(word, 0) + 1
        )  # .get(key, default value if key does not exist)

    filtered_list = [
        (k, len(k), word_count[k]) for k in word_count if word_count[k] >= frequency
    ]

    return sorted(filtered_list, key=lambda x: x[2])


def main() -> None:
    """
    Entry point of the script. Computes and prints words, word length and frequency with multiple occurrences in the input string.
    """
    astring = """Python Multiline String Using Triple-Quotes Using the triple quotes style is one of the easiest and most common ways to split a large string into a multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows you to format text over many lines and include line breaks. Put two triple quotes around the multiline Python string, one at the start and one at the end, to define it."""
    print(get_sorted_frequent_words(astring, 2))


if __name__ == "__main__":
    main()
