"""
Test file for WordleGuess class.
"""

# Standard imports.
import unittest

# Package imports.
from wordle_filter.WordleGuess import LetterColor
from wordle_filter.WordleGuess import WordleGuess


class GuessTest(unittest.TestCase):
    def test_enumeration_constructor(self):
        """
        Test the LetterColor enumeration constructor.

        :return: None
        """
        self.assertEqual(LetterColor(0).name, "GREEN", "Green enumeration name did not return 'GREEN'")
        self.assertEqual(LetterColor(1).name, "YELLOW", "Green enumeration name did not return 'YELLOW'")
        self.assertEqual(LetterColor(2).name, "GREY", "Green enumeration name did not return 'GREY'")

    def test_guess_constructor_normal(self):
        """
        Test the WordleGuess constructor as intended to be used.

        :return: None
        """
        word = "RATIO"

        int_color_list = [1, 1, 2, 2, 2]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        new_guess = WordleGuess(word, enumeration_list)

        self.assertIsNotNone(new_guess, "WordleGuess did not initialize.")
        self.assertEqual(new_guess.word, "ratio", "WordleGuess assigned incorrect word.")
        self.assertEqual(new_guess.color_list, enumeration_list, "WordleGuess assigned incorrect enumeration list.")

        location_dict = {LetterColor(0): [],
                         LetterColor(1): [0, 1],
                         LetterColor(2): [2, 3, 4]}

        self.assertEqual(new_guess.location_dict, location_dict, "Location dictionary assigned incorrectly.")

    def test_guess_constructor_error(self):
        """
        Test the WordleGuess constructor for when an error should be raised.

        :return: None
        """

        word = "BEST"

        int_color_list = [1, 1, 0, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        # Attempt to use illegal arguments for the WordleGuess constructor (length 4)
        with self.assertRaises(ValueError):
            WordleGuess(word, enumeration_list)
