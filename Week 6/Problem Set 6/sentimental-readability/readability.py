def main():
    # Ask user for input text
    text = input("Text: ")

    # L is the average number of letter per 100 words in the text
    L = 100 * count_letters(text) / count_words(text)

    # S is the average number of sentences per 100 words in the text
    S = 100 * count_sentences(text) / count_words(text)

    # Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8

    print(grade(index))


# Assume that any sequence of characters separated by spaces should count as a word
def count_words(text):
    '''Return number of words in a given text'''
    words = 1
    for i in text:
        if i == " ":
            words += 1
    return words


#  Assume that a letter is any lowercase character from a to z or any uppercase character from A to Z
def count_letters(text):
    '''Return number of letters in a given text'''
    alphabet = "abcdefghijklmnopqrstvuwxyz"
    letters = 0
    for i in text:
        if i.lower() in alphabet:
            letters += 1
    return letters


# Assume that any occurrence of a period, exclamation point, or question mark indicates the end of a sentence
def count_sentences(text):
    '''Return number of sentences in a given text'''
    sentences = 0
    for i in text:
        if i == "." or i == "!" or i == "?":
            sentences += 1
    return sentences


def grade(index):
    '''Return the grade level of the given text based on its difficulty'''
    if index >= 16:
        return "Grade 16+"
    elif index < 1:
        return "Before Grade 1"
    else:
        return f"Grade {round(index)}"


if __name__ == "__main__":
    main()