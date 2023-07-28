"""
Module to test wordle game.
Author: Aidan Sims
"""

import wordle
import pytest


def test_valid_word():
    """Tests the code to validate if a word is real."""
    assert wordle.valid_word("dream".upper())
    assert not wordle.valid_word("ssere".upper())


def test_colors():
    """Tests the letter colorer."""
    pass


def test_not_rest_same():
    pass


test_valid_word()
