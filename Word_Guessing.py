import random

def get_word(difficulty):
    """
    Returns a random word based on the selected difficulty.
    """
    words = {
        "easy": ["cat", "dog", "sun", "book", "tree"],
        "medium": ["python", "kotlin", "planet", "orange", "window"],
        "hard": ["javascript", "algorithm", "difficult", "mysterious", "framework"]
    }
    return random.choice(words[difficulty])

def get_attempts(difficulty):
    """
    Returns the number of attempts allowed based on difficulty.
    """
    return {"easy": 10, "medium": 8, "hard": 6}[difficulty]

def display_status(hidden_word, guesses, attempts, score):
    """
    Displays the current status of the game:
    - The word with guessed letters revealed
    - The list of guessed letters
    - Remaining attempts and current score
    """
    print("\nCurrent word:", hidden_word)
    print("Guessed letters:", " ".join(sorted(guesses)))
    print(f"Attempts left: {attempts} | Score: {score}")

def play_game(name):
    """
    Runs a single round of the word guessing game for the given player name.
    Handles difficulty selection, guessing loop, scoring, and end-of-round messages.
    """
    print("\nChoose difficulty: easy / medium / hard")
    while True:
        difficulty = input("Enter difficulty: ").lower()
        if difficulty in ["easy", "medium", "hard"]:
            break
        print("Invalid difficulty. Please choose easy, medium, or hard.")

    word = get_word(difficulty)  # Select a random word
    attempts = get_attempts(difficulty)  # Set attempts based on difficulty
    hidden_word = "-" * len(word)  # Initialize hidden word display
    guesses = set()  # Store guessed letters
    score = 0  # Initialize score for this round

    while attempts > 0:
        display_status(hidden_word, guesses, attempts, score)
        guess = input("Enter a letter: ").lower()

        # Validate input: must be a single alphabetical character
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetical character.")
            continue

        # Check if letter was already guessed
        if guess in guesses:
            print("You already guessed that letter.")
            continue

        guesses.add(guess)  # Add guess to the set

        if guess in word:
            # Reveal guessed letters in the hidden word
            hidden_word = ''.join([c if c in guesses else '-' for c in word])
            print("Good job! You guessed a letter.")
            score += 10  # Award points for correct guess
        else:
            attempts -= 1  # Deduct attempt for wrong guess
            print(f"Sorry, {guess} is not in the word.")

        # Check if the word has been completely guessed
        if hidden_word == word:
            print(f"\nCongratulations, {name}! You've guessed the word: {word}")
            score += 50  # Bonus for guessing the whole word
            break
    else:
        # Ran out of attempts
        print(f"\nSorry, {name}. You've run out of attempts. The word was: {word}")

    print(f"Your final score: {score}")
    return score  # Return score for this round

def main():
    """
    Main function to start the game, handle player name, and manage multiple rounds.
    """
    name = input("Enter your name: ")
    print(f"Hello, {name}! Welcome to the Word Guessing Game.")

    total_score = 0  # Track total score across rounds
    while True:
        total_score += play_game(name)  # Play a round and add to total score
        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != 'y':
            break

    print(f"\nThanks for playing, {name}! Your total score: {total_score}")

# Start the game
if __name__ == "__main__":
    main()
