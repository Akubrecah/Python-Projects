# Super Enhanced Hangman Game with categories, hints, scoring, leaderboard, and more!

import random
import sys

# ANSI color codes for fun output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Dictionary of categories, words by difficulty, and hints
categories = {
    "fruits": {
        "easy": {
            "apple": "Keeps the doctor away.",
            "banana": "A yellow fruit, monkeys love it.",
            "lemon": "Very sour, yellow citrus.",
            "grape": "Small, round, can be made into wine.",
        },
        "medium": {
            "pineapple": "Spiky outside, sweet inside.",
            "apricot": "Small, orange, and fuzzy.",
            "coconut": "Brown, hairy, and full of water.",
            "peach": "Fuzzy skin, sweet and juicy.",
        },
        "hard": {
            "watermelon": "Green outside, red inside, black seeds.",
            "strawberry": "Red, heart-shaped, and has seeds outside.",
            "muskmelon": "Net-like skin, orange flesh.",
            "lychee": "White flesh, red shell, Asian fruit.",
        }
    },
    "animals": {
        "easy": {
            "lion": "King of the jungle.",
            "panda": "Black and white bear, eats bamboo.",
            "rabbit": "Long ears, loves carrots.",
            "tiger": "Big cat with stripes.",
        },
        "medium": {
            "giraffe": "Tallest animal, long neck.",
            "zebra": "Horse-like, black and white stripes.",
            "dolphin": "Intelligent sea mammal.",
            "penguin": "Bird that cannot fly, lives in Antarctica.",
        },
        "hard": {
            "elephant": "Largest land animal.",
            "kangaroo": "Jumps and has a pouch.",
        }
    }
}

# In-memory leaderboard
leaderboard = {}

def choose_category():
    """Prompt user to choose a category or all categories."""
    print(Colors.HEADER + "Categories available:" + Colors.ENDC)
    cats = list(categories.keys())
    for idx, cat in enumerate(cats, 1):
        print(f"{idx}. {cat.capitalize()}")
    print(f"{len(cats)+1}. All Categories (random)")
    while True:
        choice = input("Choose a category by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(cats)+1:
            if int(choice) == len(cats)+1:
                return "all"
            return cats[int(choice)-1]
        else:
            print(Colors.WARNING + "Invalid choice. Please enter a valid number." + Colors.ENDC)

def choose_difficulty(category):
    """Prompt user to choose a difficulty level."""
    print(Colors.HEADER + "Difficulty levels:" + Colors.ENDC)
    levels = ["easy", "medium", "hard"]
    for idx, lvl in enumerate(levels, 1):
        print(f"{idx}. {lvl.capitalize()}")
    print(f"{len(levels)+1}. Random")
    while True:
        choice = input("Choose difficulty by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(levels)+1:
            if int(choice) == len(levels)+1:
                return random.choice(levels)
            return levels[int(choice)-1]
        else:
            print(Colors.WARNING + "Invalid choice. Please enter a valid number." + Colors.ENDC)

def get_word_and_hint(category, difficulty):
    """Get a random word and hint from the chosen category and difficulty."""
    if category == "all":
        category = random.choice(list(categories.keys()))
    if difficulty == "random":
        difficulty = random.choice(list(categories[category].keys()))
    word, hint = random.choice(list(categories[category][difficulty].items()))
    return category, difficulty, word, hint

def display_word(word, letterGuessed):
    """Display the current state of the guessed word."""
    display = ''
    for char in word:
        if char in letterGuessed:
            display += Colors.OKGREEN + char + Colors.ENDC + ' '
        else:
            display += Colors.FAIL + '_ ' + Colors.ENDC
    print(display.strip())

def hangman_graphic(chances, total_chances):
    """Display a simple hangman graphic based on remaining chances."""
    stages = [
        "",
        " O ",
        " O \n | ",
        " O \n/| ",
        " O \n/|\\",
        " O \n/|\\\n/  ",
        " O \n/|\\\n/ \\"
    ]
    idx = total_chances - chances
    idx = min(idx, len(stages)-1)
    print(Colors.OKBLUE + stages[idx] + Colors.ENDC)

def show_leaderboard():
    """Display the leaderboard."""
    print(Colors.BOLD + "\nLeaderboard:" + Colors.ENDC)
    if not leaderboard:
        print("No scores yet!")
        return
    sorted_scores = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(sorted_scores, 1):
        print(f"{i}. {name}: {score}")

def play_game(player_name):
    """Main game logic for one round."""
    category = choose_category()
    difficulty = choose_difficulty(category)
    category, difficulty, word, hint = get_word_and_hint(category, difficulty)
    print(Colors.OKCYAN + f"\nCategory: {category.capitalize()} | Difficulty: {difficulty.capitalize()}" + Colors.ENDC)
    print(Colors.OKCYAN + f"Hint: {hint}" + Colors.ENDC)
    print(f"The word has {len(word)} letters.")

    letterGuessed = set()
    total_chances = max(6, len(word) + 2)
    chances = total_chances
    score = 0
    used_hint = False
    bought_chance = False

    try:
        while chances > 0:
            print("\nWord: ", end='')
            display_word(word, letterGuessed)
            print(f"Guessed letters: {' '.join(sorted(letterGuessed)) if letterGuessed else 'None'}")
            print(f"Chances left: {chances} | Score: {score}")
            hangman_graphic(chances, total_chances)

            print(Colors.OKCYAN + "Options: [hint] (-5 pts), [buy] extra chance (-10 pts), [quit]" + Colors.ENDC)
            guess = input('Enter a letter or option: ').lower().strip()
            if guess == "hint":
                if used_hint:
                    print(Colors.WARNING + "You already used your hint!" + Colors.ENDC)
                else:
                    print(Colors.OKCYAN + f"Hint: {hint}" + Colors.ENDC)
                    score -= 5
                    used_hint = True
                continue
            if guess == "buy":
                if bought_chance:
                    print(Colors.WARNING + "You can only buy one extra chance per game!" + Colors.ENDC)
                else:
                    chances += 1
                    score -= 10
                    bought_chance = True
                    print(Colors.OKGREEN + "You bought an extra chance!" + Colors.ENDC)
                continue
            if guess == "quit":
                print(Colors.WARNING + "You quit the round!" + Colors.ENDC)
                break

            # Input validation
            if not guess.isalpha():
                print(Colors.WARNING + 'Enter only a LETTER.' + Colors.ENDC)
                continue
            elif len(guess) != 1:
                print(Colors.WARNING + 'Enter only a SINGLE letter.' + Colors.ENDC)
                continue
            elif guess in letterGuessed:
                print(Colors.WARNING + 'You have already guessed that letter.' + Colors.ENDC)
                continue

            letterGuessed.add(guess)

            if guess in word:
                print(Colors.OKGREEN + f"Good job! '{guess}' is in the word." + Colors.ENDC)
                score += 10
            else:
                print(Colors.FAIL + f"Sorry, '{guess}' is not in the word." + Colors.ENDC)
                chances -= 1
                score -= 2

            # Check if all letters are guessed
            if all(char in letterGuessed for char in word):
                print(Colors.BOLD + "\nCongratulations, You won!" + Colors.ENDC)
                print(f"The word was: {Colors.OKGREEN}{word}{Colors.ENDC}")
                score += 50
                break
        else:
            print(Colors.FAIL + "\nYou lost! Try again.." + Colors.ENDC)
            print(f"The word was: {Colors.OKGREEN}{word}{Colors.ENDC}")

        print(f"Your final score for this round: {Colors.BOLD}{score}{Colors.ENDC}")
        leaderboard[player_name] = max(score, leaderboard.get(player_name, 0))
        return score

    except KeyboardInterrupt:
        print('\nBye! Try again.')
        sys.exit()

def main():
    print(Colors.HEADER + Colors.BOLD + 'Welcome to the Super Enhanced Hangman Game!' + Colors.ENDC)
    player_name = input("Enter your name: ").strip()
    print(f"Hello, {Colors.OKGREEN}{player_name}{Colors.ENDC}! Let's play Hangman!\n")

    while True:
        play_game(player_name)
        show_leaderboard()
        again = input(Colors.OKCYAN + "\nDo you want to play again? (y/n): " + Colors.ENDC).lower()
        if again != 'y':
            break

    print(Colors.BOLD + f"\nThanks for playing, {player_name}! See you next time!" + Colors.ENDC)
    show_leaderboard()

if __name__ == '__main__':
    main()