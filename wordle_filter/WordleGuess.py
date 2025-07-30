######################################
#
# WordleGuess - Class responsible for storing guess information for a Wordle game.
# LetterColor - Enumeration class to represent correctness of a letter in a guess.
#
# author - Ryan Muetzel (@pretzelryan)
#

# Imports
from enum import Enum


# Global Variables
LETTERS_IN_WORD = 5


class LetterColor(Enum):
    """
    Enumeration to represent the correctness of each letter in a guess.

    """
    GREEN = 0
    YELLOW = 1
    GREY = 2


class WordleGuess:
    """
    Handles data storage for each individual guessing round.

    """
    def __init__(self, word: str, color_list: list[LetterColor]):
        """
        Constructor. Arguments must be length of 5, otherwise raises ValueError.

        :param word: five-letter word used in guess.
        :param color_list: List of letter color enumerations in guess.
        """
        if len(word) != LETTERS_IN_WORD or len(color_list) != LETTERS_IN_WORD:
            raise ValueError("Guess arguments must be of length " + str(LETTERS_IN_WORD) + ".")

        self.word = word.lower()
        self.color_list = color_list

        # determine where green, yellow, and grey letters are located to simplify the filtering function.
        self.location_dict = self._create_location_dict()

    def _create_location_dict(self):
        """
        Creates a dictionary that describes the location of colors within the guess.

        :return: Dictionary of length three, with elements "green", "yellow", and "grey" enumeration corresponding
        to integer lists that describe the locations of the colored elements.
        """
        # example dict = {green: [1, 2], yellow: [4], grey: [3, 5]}
        location_dict = {LetterColor(0): [],
                         LetterColor(1): [],
                         LetterColor(2): []}

        # add the index of the color to the corresponding list in the color dictionary
        for i in range(len(self.color_list)):
            location_dict[self.color_list[i]].append(i)

        return location_dict
