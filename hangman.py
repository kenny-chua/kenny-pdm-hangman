import random
import re


def secret_movie_list():
    with open("movies.txt", "r") as file:
        secret_movie_list = list({re.sub(r"^\d+\.\s+(.*)\s\(\d{4}\)", r"\1", line).strip() for line in file})
        return secret_movie_list


class Hangman:
    def __init__(self, secret_movie=None, max_guesses=10):
        if secret_movie is not None:
            self.secret_movie_proper = secret_movie
        else:
            self.secret_movie_proper = random.choice(secret_movie_list())
        self.secret_movie = self.secret_movie_proper.lower()
        self.guesses = 0
        self.max_guesses = max_guesses
        self.already_guessed = set()
        self.correct_letter = set()

    def show_initial_placeholders(self):
        initial_placeholder = ""
        for char in self.secret_movie:
            if char == "'":
                initial_placeholder += "'"
            elif char == ".":
                initial_placeholder += "."
            elif char == ":":
                initial_placeholder += ":"
            elif char != " ":
                initial_placeholder += "_"
            else:
                initial_placeholder += " "
        return initial_placeholder

    def guess_a_letter(self):
        while True:
            userguess = input("\nGuess a letter.\n").strip().lower()
            if len(userguess) != 1 or not userguess.isalpha():
                print("Invalid input. Please enter a single letter.\n")
                print(self.display_progression())
            elif userguess in self.already_guessed:
                print("You’ve already guessed that letter. Try again.\n")
                print(self.display_progression())
            else:
                self.already_guessed.add(userguess)
                return userguess

    def display_progression(self):
        placeholder = ""
        for char in self.secret_movie_proper:
            if char.lower() in self.correct_letter:
                placeholder += char
            elif char == " ":
                placeholder += " "
            elif char == "'":
                placeholder += "'"
            elif char == ".":
                placeholder += "."
            elif char == ":":
                placeholder += ":"
            else:
                placeholder += "_"
        return placeholder

    def check_win_or_lose(self):
        if self.display_progression() == self.secret_movie_proper:
            print(f"Congratulations, you have won! The movie is:\n\n{self.secret_movie_proper}")
            return True
        elif self.guesses >= self.max_guesses:
            print(f"You have run out of guesses. The movie was:\n\n{self.secret_movie_proper}")
            return True
        return False

    def play(self):
        print("Welcome to Hangman! Try to guess the movie title before you run out of guesses.")
        input("Hit any key for your first movie.\n")
        print("\nTHIS IS YOUR MOVIE\n")
        print(self.show_initial_placeholders())

        while not self.check_win_or_lose():
            guess = self.guess_a_letter()
            if guess in self.secret_movie:
                self.correct_letter.add(guess)
                print(f"Good Guess {guess}!\n")
            else:
                self.guesses += 1
                print(f"Sorry, incorrect guess. You have {self.max_guesses - self.guesses} left before you hang\n")

            print(f"{self.display_progression()}\n")


if __name__ == "__main__":
    hangman = Hangman("My: adf")
    hangman.play()
