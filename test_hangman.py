import pytest

from hangman import Hangman


@pytest.fixture
def hangman():
    return Hangman("The Godfather", 5)


def test_show_initial_placeholders(hangman):
    assert hangman.show_initial_placeholders() == "___ _________"


@pytest.mark.parametrize("correct_letter, expected", [
    ({"h", "e", "g", "o", "d", "f", "a", "r"}, "_he Godfa_her"),
    ({"t", "h", "e", "g", "o", "d", "f", "a", "r"}, "The Godfather"),
])
def test_display_progression(hangman, correct_letter, expected):
    hangman.correct_letter = correct_letter
    assert hangman.display_progression() == expected
