def calculate_scrabble_score(word):
    letter_scores = {
        "aeioulnrst": 1,
        "dg": 2,
        "bcmp": 3,
        "fhvwy": 4,
        "k": 5,
        "jx": 8,
        "qz": 10
    }

    score = 0
    for letter in word:
        for key in letter_scores:
            if letter in key:
                score += letter_scores[key]
                break  # Break the loop once the letter is found
    return score


def main():
    user_word = raw_input("Enter a word: ").lower()  # Convert the input word to lowercase
    score = calculate_scrabble_score(user_word)
    print("The Scrabble score for '{}' is: {}".format(user_word, score))

if __name__ == "__main__":
    main()
