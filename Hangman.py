
import random
from pathlib import Path

# Load words from the provided text file
def load_words():
    word_file = Path(__file__).with_name("wordslist.txt.txt")

    try:
        with open(word_file, "r", encoding="utf-8") as file:
            words = [
                line.strip().lower()
                for line in file
                if line.strip().isascii()
                and line.strip().isalpha()
                and len(line.strip()) >= 3
            ]

    except FileNotFoundError:
        print("Error: wordslist.txt.txt was not found!")
        print("Keep wordslist.txt.txt in the same folder as Hangman.py.")
        raise SystemExit(1)

    if not words:
        print("Error: No valid words found in the text file.")
        raise SystemExit(1)

    return words


WORDS = load_words()


# ASCII Hangman stages: 0 to 6 incorrect guesses
HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =========
    """
]


def display_word(secret_word, guessed_letters):
    """Show guessed letters and hide the remaining letters."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_hangman():
    """Run one complete Hangman game."""
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    print("=" * 35)
    print("     HANGMAN WORD GUESSING GAME")
    print("=" * 35)
    print("Guess the hidden word one letter at a time!")
    print(f"You have {max_attempts} incorrect guesses allowed.")
    print(f"Words loaded from file: {len(WORDS)}")

    while wrong_guesses < max_attempts:
        print(HANGMAN_PICS[wrong_guesses])
        print("\nWord:", display_word(secret_word, guessed_letters))
        print(
            "Guessed letters:",
            " ".join(sorted(guessed_letters)) or "None"
        )
        print("Attempts remaining:", max_attempts - wrong_guesses)

        guess = input("\nEnter a letter: ").strip().lower()

        # Validate the input
        if (
            len(guess) != 1
            or not guess.isalpha()
            or not guess.isascii()
        ):
            print("Invalid input! Please enter one English letter.")
            continue

        # Prevent duplicate guesses
        if guess in guessed_letters:
            print("You already guessed that letter. Try another!")
            continue

        guessed_letters.add(guess)

        # Check whether the letter exists in the word
        if guess in secret_word:
            print("Correct guess!")
        else:
            wrong_guesses += 1
            print("Wrong guess!")

        # Check for victory
        if all(letter in guessed_letters for letter in secret_word):
            print("\nWord:", display_word(secret_word, guessed_letters))
            print("\nCongratulations! You guessed the word!")
            print("Secret word:", secret_word.upper())
            print("Incorrect guesses:", wrong_guesses)
            return

    # Display the final Hangman drawing and defeat message
    print(HANGMAN_PICS[max_attempts])
    print("\nGame Over! You have used all six incorrect guesses.")
    print("The secret word was:", secret_word.upper())


if __name__ == "__main__":
    play_hangman()
