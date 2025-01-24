######################################
#
# TODO: documentation
#
# author - Ryan Muetzel (@pretzelryan)
#

# Imports
from enum import Enum


class LetterColors(Enum):
    """
    Enumeration to represent the correctness of each letter in a guess.

    """
    GREY = 0
    YELLOW = 1
    GREEN = 2


class WordleGuess:
    """
    Handles data storage for each individual guessing round.

    """
    def __init__(self, character_list: list[str], color_list: list[LetterColors]):
        """
        Constructor. List arguments must be length of 5, otherwise throws ValueError.

        :param character_list: list of characters in the guess.
        :param color_list: List of letter color enumerations in guess.
        """
        pass
