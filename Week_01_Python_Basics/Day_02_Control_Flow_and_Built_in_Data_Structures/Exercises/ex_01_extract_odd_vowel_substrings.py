"""
Write a code to filter all sub-strings which have even number of vowels.

Example:
----------
Input: "I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo"

Output: "I an string which contains and odd of aaa aeo"

Complexity Analysis
-------------------
input_str.split(): O(n) where n is the length of the string
count_vowels(word): O(k) where k is the length of a word
generator expression: O(s.k) = O(n) where s is the number of words

TC: O(n) + O(n) == O(n) where n is the length of the string
SC: No additional space because of the use of generator expression for input_str.split()
"""

from typing import Set


def count_vowels(word: str) -> int:
    """
    Counts the number of vowels in a given word.

    Args:
        word (str): The input word to check for vowels.

    Returns:
        int: The count of vowels in the word.

    Note:
        Why use set instead of list for storing the vowels: The "in" keyword has different time complexities depending on the container type. Using a set provides O(1) average time complexity for lookups, whereas a list would be O(n).
    """
    return sum(
        1 for char in word if char in {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    )


def extract_odd_vowel_substring(text: str) -> str:
    """
    Extracts and returns a space separated string of words that contain odd number of vowels.

    Args:
        input_str (str): The input string containing multiple words.

    Returns:
        str: A new string containing only words with an odd number of vowels.
    """
    return " ".join(word for word in text.split() if count_vowels(word) % 2 != 0)


def main() -> None:
    """
    Entry point of the script. Extracts odd vowel words from the input string.

    Note:
        Defined separately to avoid polluting the global scope because everything inside if __name__ == "__main__" remains in memory unnecessarily if defined globally.
    """
    input_str = "I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo"
    print(extract_odd_vowel_substring(input_str))


if __name__ == "__main__":
    main()
