def split_text(text):
    words = []
    current_word = ""
    for char in text:
        if char == " " or char == ",":
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += char
    if current_word:
        words.append(current_word)
    return words

def count_lowercase_consonant_words(text):
    vowels = "aeiou"  
    consonant_count = 0
    words = split_text(text)

    for word in words:
        if word: 
            first_letter = word[0]  
            if 'a' <= first_letter <= 'z' and first_letter not in vowels:  
                consonant_count += 1

    return consonant_count

def count_words_with_max_length(words) -> int:
    max_length = max(len(word) for word in words)
    return sum(1 for word in words if len(word) == max_length)


def words_before_punctuation(text):
    words = text.split()
    followed_by_punctuation = []
    for word in words:
        if word.endswith(",") or word.endswith("."):
            followed_by_punctuation.append(word[:-1]) 
    return followed_by_punctuation

def find_longest_word_ending_with_e(words):
    longest_ending_with_e = ""
    for word in words:
        if word.endswith("e") and len(word) > len(longest_ending_with_e):
            longest_ending_with_e = word
    return longest_ending_with_e