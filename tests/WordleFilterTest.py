"""
Test file for WordleFilter class.

Functionality of the WordleFilter is dependent upon a functioning WordleGuess class.
"""

# Standard imports.
import unittest

# Package imports.
from wordle_filter.WordleGuess import LetterColor
from wordle_filter.WordleGuess import WordleGuess
from wordle_filter.WordleFilter import WordleFilter


class FilterTest(unittest.TestCase):
    def test_filter_constructor(self):
        """
        Test the filter constructor.

        :return:
        """
        new_filter = WordleFilter()

        self.assertIsNotNone(new_filter, "WordleFilter failed to initialize.")
        self.assertIsNotNone(new_filter.remaining_word_list, "WordleFilter remaining word list failed to initialize.")
        self.assertIsNotNone(new_filter.guess_list, "WordleFilter guess list failed to initialize.")

        self.assertGreater(len(new_filter.remaining_word_list), 1, "WordleFilter initialized remaining word "
                                                                   "list to an incorrect size.")
        self.assertEqual(len(new_filter.guess_list), 0, "WordleFilter initialized guess list to incorrect size.")

    def test_filter_perfect(self):
        """
        Test the filter function by adding a word with only one green letter.

        :return: None
        """
        word = "SHARK"
        int_color_list = [0, 0, 0, 0, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        new_guess = WordleGuess(word, enumeration_list)
        new_filter = WordleFilter()

        new_filter.add_guess(new_guess)

        self.assertEqual(["shark"], new_filter.remaining_word_list, "Filter did not find correct word.")
