import random
import re
from typing import Generator

DEFAULT_MOVIE = "No Movie Provide, Default Movie Title"


def clean_movie_title(raw_title: str) -> str:
    """
    Cleans any movie title by removing numbering, years, and extra spaces.

    Args:
        raw_title (str): The raw, unclean movie title.

    Returns:
        str: The cleaned movie title.
    """
    return re.sub(r"^\d+\.\s+(.*)\s\(\d{4}\)", r"\1", raw_title).strip()


def secret_movie_generator(filepath: str = "movies.txt") -> Generator[str, None, None]:
    """
    Generates movie titles from a file.

    This function reads a file line by line, extracts the movie title
    using a regular expression, and yields it as a string. If the file
    is not found or an error occurs, it yields a default movie title.

    Args:
        filepath (str): Path to the file containing movie titles. Defaults to 'movies.txt'.

    Yields:
        str: A movie title extracted from the file.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If an error occurs during movie title extraction.
        Exception: For any other unexpected errors.
    """
    try:
        with open(filepath, "r") as file:
            for line in file:
                movie_from_file = clean_movie_title(line)
                if movie_from_file:
                    yield movie_from_file
    except FileNotFoundError:
        print(f"Error: Files {filepath} not found.")
        yield [DEFAULT_MOVIE]
    except Exception as e:
        print(f"Error: {e}")
        yield [DEFAULT_MOVIE]


class Hangman:
    """
    A Hangman game for guessing movie titles.

    Attributes:
        secret_movie_proper (str): The actual movie title being guessed.
        secret_movie (str): The lowercased version of the movie title for matching guesses.
        wrong_guesses (int): The number of incorrect guesses made.
        max_guesses (int): The maximum allowed incorrect guesses.
        already_guessed (set): A set of letters already guessed by the player.
        correct_letter (set): A set of correctly guessed letters.
    """

    def __init__(self, secret_movie=None, max_guesses=10) -> None:
        """
        Initializes the Hangman game.

        Args:
            secret_movie (str, optional): A predefined movie title. If not provided,
                                          a random movie is chosen.
            max_guesses (int): The maximum number of incorrect guesses allowed. Defaults to 10.
        """
        movie_list = list(secret_movie_generator())
        self.secret_movie_proper = (
            clean_movie_title(secret_movie)
            if secret_movie
            else random.choice(movie_list)
        )
        self.secret_movie = self.secret_movie_proper.lower()
        self.wrong_guesses = 0
        self.max_guesses = max_guesses
        self.already_guessed = set()
        self.correct_letter = set()

    def get_placeholder(self, reveal_correct: bool = False) -> str:
        """
        Generates a masked version of the movie title.

        Args:
            reveal_correct (bool): If True, includes correctly guessed letters.
                                   If False, shows only placeholders. Defaults to False.

        Returns:
            str: The masked movie title.
        """
        return "".join(
            char if char.lower() in self.correct_letter or not char.isalpha() else "_"
            for char in self.secret_movie_proper
        )

    def show_initial_placeholders(self) -> str:
        """
        Displays the initial masked version of the movie title.

        Returns:
            str: The initial placeholder string.
        """
        return self.get_placeholder(reveal_correct=False)

    def display_game_progression(self) -> str:
        """
        Displays the current progress of the game, including correctly guessed letters.

        Returns:
            str: The current state of the movie title.
        """
        return self.get_placeholder(reveal_correct=True)

    def is_valid_guess(self, userguess: str) -> tuple[bool, str | None]:
        """
        Validates a user's guess.

        Args:
            userguess (str): The letter guessed by the user.

        Returns:
            tuple[bool, str | None]: A tuple where the first element indicates if the guess is valid,
                                     and the second element is an error message (if invalid).
        """
        if len(userguess) != 1 or not userguess.isalpha():
            return False, "Invalid input. Please enter a single letter.\n"
        if userguess in self.already_guessed:
            return False, "You’ve already guessed that letter. Try again.\n"
        return True, None

    def process_guess(self, guess: str) -> bool:
        """
        Processes a user's guess and updates the game state.

        Args:
            guess (str): The letter guessed by the user.

        Returns:
            bool: True if the guess is correct, False otherwise.
        """
        if guess.lower() in self.secret_movie:
            self.correct_letter.add(guess.lower())
            return True
        else:
            self.wrong_guesses += 1
            return False

    def guess_a_letter(self) -> str:
        """
        Prompts the user to guess a letter.

        Returns:
            str: The valid guessed letter.
        """
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
        """
        Checks if the user has won or lost the game.

        Returns:
            bool: True if the game is over (win or lose), False otherwise.
        """
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
        """
        Starts and runs the Hangman game.
        """
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
