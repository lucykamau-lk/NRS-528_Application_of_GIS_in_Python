def count_words_occurrences(sentence):
    # Split the string into words
    words = sentence.split()

    # Create a dictionary to store word count of each word
    word_count = {}
    for word in words:
        # if the word is already in the dictionary, increment its count
        if word in word_count:
            word_count[word] += 1
        # if the word is already in the dictionary, add it with count 1
        else:
            word_count[word] = 1

    # print each word along with its count
    for word, count in word_count.items():
        print(word + ": " + str(count))


# Given string
given_string = 'hi dee hi how are you mr dee'

# call the function with the given string
count_words_occurrences(given_string)
