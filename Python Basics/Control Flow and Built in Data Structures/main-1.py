def count_vowels(word):

    # vowel_list = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    # time complexity of the 'in' keyword in python is dependent on the type of container it is used in
    # sets have better average time complexities than lists so a set makes more sense in this case

    vowel_set = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    vowel_count = 0

    for char in word:
        if char in vowel_set:
            vowel_count += 1

    return vowel_count


input_str = "I have an input string which contains even and odd numbers of vowels aA aa aaa ae aeo"

ans = " ".join(word for word in input_str.split() if count_vowels(word) % 2 != 0)
print(ans)

# input_str.split(): O(n) where n is the length of the string
# count_vowels(word): O(k) where k is the length of a word
# generator expression: O(s.k) = O(n) where s is the number of words

# TC: O(n) + O(n) == O(n)
# SC: No additional space because of the use of generator expression for input_str.split()
