import pytest

from hangman import Hangman


# ---------------------- FIXTURES ---------------------- `#
@pytest.fixture
def hangman():
    """
    Provides a Hangman instance with a fixed movie title and max guesses.
    """
    return Hangman("Pirates of the Caribbean: Dead Man's Chest", 5)


@pytest.fixture
def mock_movie_file(mocker):
    mock_data = """
    1. The Godfather (1972)
    2. Wall-E! (2008)
    3. Up (2009)
    4. Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1964)
    5. The Godfather Part II (1974)
    6. Pirates of the Caribbean: Dead Man's Chest (2006)
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data))


# ---------------------- TEST HANGMAN ---------------------- #
def test_initialization(hangman):
    """
    Test Hangman initialization with a fixed title and guesses
    """
    assert hangman.secret_movie_proper == "Pirates of the Caribbean: Dead Man's Chest"
    assert hangman.secret_movie == "pirates of the caribbean: dead man's chest"
    assert hangman.max_guesses == 5
    assert hangman.wrong_guesses == 0
    assert hangman.already_guessed == set()
    assert hangman.correct_letter == set()


@pytest.mark.parametrize(
    "movie_title, expected_placeholder",
    [
        (
            "Pirates of the Caribbean: Dead Man's Chest",
            "_______ __ ___ _________: ____ ___'_ _____",
        ),
        ("Wall-E!", "____-_!"),
        ("Up", "__"),
    ],
)
def test_show_initial_placeholders(movie_title, expected_placeholder):
    """
    Test that placeholders are generated correctly for different movie titles.
    """
    game = Hangman(movie_title, 5)
    assert game.show_initial_placeholders() == expected_placeholder


@pytest.mark.parametrize(
    "movie_title, correct_letters, expected_progression",
    [
        (
            "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
            set(),
            "__. ___________ __: ___ _ _______ __ ____ ________ ___ ____ ___ ____",
        ),
        (
            "Pirates of the Caribbean: Dead Man's Chest",
            {"d", "r", "s", "t", "l"},
            "__r_t_s __ t__ __r______: D__d ___'s ___st",
        ),
        (
            "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
            set("drstrangeloveorhowilearnedtostopworryingandlovethebomb"),
            "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
        ),
        (
            "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
            {"x", "q", "z", "f"},
            "__. ___________ __: ___ _ _______ __ ____ ________ ___ ____ ___ ____",
        ),
    ],
    ids=[
        "no_letters_guessed",
        "partially_guessed_letters",
        "fully_guessed_title",
        "wrong_letters",
    ]
)
def test_display_game_progression(movie_title, correct_letters, expected_progression):
    """
    Test that the progression display works for complicated movie titles.
    """
    hangman = Hangman(movie_title, 5)
    hangman.correct_letters = correct_letters
    assert hangman.display_game_progression() == expected_progression


@pytest.mark.parametrize(
    "userguess, expected",
    [
        ("t", (True, None)),  # Valid guess
        (
            "1",
            (False, "Invalid input. Please enter a single letter.\n"),
        ),  # Invalid input
        (
            "tt",
            (False, "Invalid input. Please enter a single letter.\n"),
        ),  # Multiple letters
        ("g1", (False, "Invalid input. Please enter a single letter.\n")),
    ],
)
def test_is_valid_guess(hangman, userguess, expected):
    """
    Test validation of user guesses.
    """
    assert hangman.is_valid_guess(userguess) == expected


def test_process_correct_guess(hangman):
    """
    Test processing a correct guess.
    """
    assert hangman.process_guess("t") is True
    assert "t" in hangman.correct_letter
    assert hangman.wrong_guesses == 0


def test_process_incorrect_guess(hangman):
    """
    Test processing an incorrect guess.
    """
    assert hangman.process_guess("x") is False
    assert hangman.wrong_guesses == 1


def test_valid_guess_a_letter(hangman, mocker):
    """
    Test guessing a valid letter with mocked input.
    """
    mocker.patch("builtins.input", return_value="t")
    guess = hangman.guess_a_letter()
    assert guess == "t"


def test_invalid_guess_a_letter(hangman, mocker):
    """
    Test guessing an invalid letter with mocked input.
    """
    mocker.patch("builtins.input", side_effect=["1", "t"])
    guess = hangman.guess_a_letter()
    assert guess == "t"


@pytest.mark.parametrize(
    "correct_letter, wrong_guesses, expected",
    [
        (set("piratesofthecaribbeandeadmanschest"), 0, True),  # Win condition
        (set(), 5, True),  # Lose condition
        (set(), 0, False),  # Game still in progress
    ],
)
def test_check_win_or_lose(hangman, correct_letter, wrong_guesses, expected):
    """
    Test win/lose conditions.
    """
    hangman.correct_letter = correct_letter
    hangman.wrong_guesses = wrong_guesses
    assert hangman.check_win_or_lose() == expected


# ---------------------- TEST EDGE CASES ---------------------- #
def test_movie_with_special_characters():
    """
    Test handling of special characters in the movie title.
    """
    game = Hangman("Wall-E!", 5)
    assert game.show_initial_placeholders() == "____-_!"


def test_max_guesses(hangman):
    """
    Test behavior when max guesses are exceeded.
    """
    hangman.wrong_guesses = 5
    assert hangman.check_win_or_lose() is True
