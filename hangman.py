import random
import re
from typing import Generator

DEFAULT_MOVIE = "Default Movie"


def secret_movie_generator(filepath: str = "movies.txt") -> Generator[str, None, None]:
    try:
        with open(filepath, "r") as file:
            for line in file:
                movie = re.sub(r"^\d+\.\s+(.*)\s\(\d{4}\)", r"\1", line).strip()
                if movie:
                    yield movie
    except FileNotFoundError:
        print(f"Error: Files {filepath} not found.")
        return [DEFAULT_MOVIE]
    except ValueError as e:
        print(f"Error: {e}")
        return [DEFAULT_MOVIE]
    except Exception as e:
        print(f"Error: {e}")
        return [DEFAULT_MOVIE]


class Hangman:
    def __init__(self, secret_movie=None, max_guesses=10) -> None:
        movie_list = list(secret_movie_generator())
        self.secret_movie_proper = secret_movie or (
            random.choice(movie_list) if movie_list else DEFAULT_MOVIE
        )
        self.secret_movie = self.secret_movie_proper.lower()
        self.wrong_guesses = 0
        self.max_guesses = max_guesses
        self.already_guessed = set()
        self.correct_letter = set()

    def get_placeholder(self, reveal_correct: bool = False) -> str:
        return "".join(
            char if char.lower() in self.correct_letter or not char.isalpha() else "_"
            for char in self.secret_movie_proper
        )

    def show_initial_placeholders(self) -> str:
        return self.get_placeholder(reveal_correct=False)

    def display_game_progression(self) -> str:
        return self.get_placeholder(reveal_correct=True)

    def is_valid_guess(self, userguess: str) -> tuple[bool, str | None]:
        if len(userguess) != 1 or not userguess.isalpha():
            return False, "Invalid input. Please enter a single letter.\n"
        if userguess in self.already_guessed:
            return False, "You’ve already guessed that letter. Try again.\n"
        return True, None

    def process_guess(self, guess: str) -> bool:
        if guess.lower() in self.secret_movie:
            self.correct_letter.add(guess.lower())
            return True
        else:
            self.wrong_guesses += 1
            return False

    def guess_a_letter(self) -> str:
        while True:
            userguess = input("\nGuess a letter.\n").strip().lower()
            is_valid, message = self.is_valid_guess(userguess)
            if not is_valid:
                print(message)
                print(self.display_game_progression())
            else:
                self.already_guessed.add(userguess)
                return userguess

    def check_win_or_lose(self) -> bool:
        if self.display_game_progression() == self.secret_movie_proper:
            print(
                f"Congratulations, you have won! The movie is:\n\n{self.secret_movie_proper}"
            )
            return True
        elif self.wrong_guesses >= self.max_guesses:
            print(
                f"You have run out of guesses. The movie was:\n\n{self.secret_movie_proper}"
            )
            return True
        return False

    def play(self) -> None:
        print(
            "Welcome to Hangman! Try to guess the movie title before you run out of guesses."
        )
        input("Hit any key for your first movie.\n")
        print("\nTHIS IS YOUR MOVIE\n")
        print(self.show_initial_placeholders())
        while not self.check_win_or_lose():
            guess = self.guess_a_letter()
            is_correct = self.process_guess(guess)
            if is_correct:
                print(f"Good Guess {guess}!\n")
            else:
                print(
                    f"Sorry, incorrect guess. You have {self.max_guesses - self.wrong_guesses} left before you hang\n"
                )

            print(f"{self.display_game_progression()}\n")


if __name__ == "__main__":
    # hangman = Hangman(secret_movie="Love & Mercy, Oh Brother!! Where? Art:Thou?")
    hangman = Hangman()
    hangman.play()
