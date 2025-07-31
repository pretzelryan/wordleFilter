######################################
#
# WordleGuess - Class responsible for storing guess information for a Wordle game.
# LetterColor - Enumeration class to represent correctness of a letter in a guess.
#
# author - Ryan Muetzel (@pretzelryan)
#

# Imports
from enum import Enum


# Project Imports
from .Word import Word
from .Word import LETTERS_IN_WORD


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
    def __init__(self, word: Word, color_list: list[LetterColor]):
        """
        Constructor. List must be of length 5, otherwise raises value error.

        :param word: word used in guess
        :type word: Word
        :param color_list: list of LetterColor enumerations, must be length 5.
        :type color_list: list[LetterColor]
        """
        if not isinstance(word, Word):
            raise ValueError(f"Word must be of type Word. Got type {type(word)}.")
        elif len(color_list) != LETTERS_IN_WORD:
            raise ValueError(f"List must be of length 5. Got length {len(color_list)}.")

        self.word = word
        self.color_list = color_list

        # determine where green, yellow, and grey letters are located. This simplifies the filtering function.
        self.location_dict = self._create_location_dict()

    def _create_location_dict(self) -> dict[LetterColor, list[int]]:
        """
        Creates a dictionary that describes the location of colors within the guess.

        :return: Dictionary of length three, with elements "green", "yellow", and "grey" enumeration corresponding
        to integer lists that describe the locations of the colored elements.
        """
        # Decision to format color_list into dict to make the filtering function simpler.
        # example dict = {green: [1, 2], yellow: [4], grey: [3, 5]}
        location_dict = {LetterColor(0): [],
                         LetterColor(1): [],
                         LetterColor(2): []}

        # add the index of the color to the corresponding list in the color dictionary
        for i in range(len(self.color_list)):
            location_dict[self.color_list[i]].append(i)

        return location_dict

    def __repr__(self):
        """
        String representation of the guess object.

        :return: word and color list
        :rtype: str
        """
        return f"WordleGuess(word={self.word.get_string()}, colors={self.color_list})"
