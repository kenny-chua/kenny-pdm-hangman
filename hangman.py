import random
import re


def secret_movie_list():
    with open("movies.txt", "r") as file:
        secret_movie_list = list({re.sub(r"^\d+\.\s+|(\(\d{4}\))", "", line).strip() for line in file})
        return secret_movie_list


class Hangman:
    # Psuedo code
    # def play(self):
    #     1. Display a welcome message and rules (optional, user-friendly step).
    #     2. Show the initial progression of the word (e.g., "_ _ _ _").
    #     3. While the game is not over:
    #         a. Prompt the user for a guess (single letter).
    #         b. Check if the letter has already been guessed.
    #         c. If it's a new guess:
    #             i. Update correct or incorrect guesses based on the letter.
    #             ii. Update the progression of the word (reveal correct letters).
    #             iii. Track the number of guesses remaining.
    #         d. Check if the game has been won or lost.
    #     4. Display the final result (win/loss) and reveal the full word.

    def __init__(self):
        self.secret_movie_proper = random.choice(secret_movie_list())
        self.secret_movie = self.secret_movie_proper.lower()
        self.guesses = 0
        self.max_guesses = 10
        self.already_guessed = set()
        self.correct_letter = set()

    def show_initial_placeholders(self):
        initial_placeholder = ""
        for char in self.secret_movie:
            if char != " ":
                initial_placeholder += "_"
            else:
                initial_placeholder += " "
        return initial_placeholder

    def guess_a_letter(self):
        while True:
            userguess = input("Guess a letter.\n").strip().lower()
            if len(userguess) != 1 or not userguess.isalpha():
                print("Invalid input. Please enter a single letter.")
            elif userguess in self.already_guessed:
                print("You’ve already guessed that letter. Try again.")
            else:
                self.already_guessed.add(userguess)
                return userguess

    def display_progression(self):
        placeholder = ""
        for char in self.secret_movie:
            if char in self.correct_letter:
                placeholder += char
            elif char == " ":
                placeholder += " "
            else:
                placeholder += "_"
        return placeholder

    def check_status(self):
        if self.display_progression() == self.secret_movie:
            print(f"Congratulations, you have won! The movie is:\n{self.secret_movie_proper}")
            return True
        elif self.guesses >= self.max_guesses:
            print(f"You have run out of guesses. The movie was:\n{self.secret_movie_proper}")
            return True
        return False

    def play(self):
        print("Welcome to Hangman! Try to guess the movie title before you run out of guesses.")
        input("Hit enter for your first movie.")
        print("This is your movie")
        print(self.show_initial_placeholders())

        while not self.check_status():
            guess = self.guess_a_letter()
            if guess in self.secret_movie:
                self.correct_letter.add(guess)
                print(f"Good Guess {guess}!")
            else:
                self.guesses += 1
                print(f"Sorry, incorrect guess. You have {self.max_guesses - self.guesses} left before you hang")

            print(self.display_progression())


hangman = Hangman()
hangman.play()
