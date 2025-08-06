"""
Test file for WordleFilter class.

Functionality of the WordleFilter is dependent upon a functioning WordleGuess class.
"""

# Standard imports.
import unittest

# Package imports.
from wordle_filter.Word import Word, get_words_file, find_word_from_string
from wordle_filter.WordleGuess import LetterColor
from wordle_filter.WordleGuess import WordleGuess
from wordle_filter.WordleFilter import WordleFilter


class FilterTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        """
        Set up test for each run.

        :return:
        :rtype:
        """
        self.word_list = get_words_file()
        self.filter = WordleFilter()

    def test_filter_constructor(self):
        """
        Test the filter constructor.

        :return:
        :rtype:
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
        Test the filter function by adding a word that is exactly correct.

        :return:
        :rtype:
        """
        word_string = "shark"
        int_color_list = [0, 0, 0, 0, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        word_obj = find_word_from_string(self.word_list, word_string)

        new_guess = WordleGuess(word_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # make sure there are no other words in the remaining word list
        self.assertEqual([word_obj], self.filter.remaining_word_list, "Filter did not find correct word.")

    def test_filter_two_green_one_yellow(self):
        """
        Target word is Oxide, determine if Poise filters correctly

        :return:
        :rtype:
        """
        target_string = "oxide"
        target_obj = find_word_from_string(self.word_list, target_string)

        guess_string = "poise"
        int_color_list = [2, 1, 0, 2, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)

        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # make sure target word exists in the remaining word list
        self.assertEqual(True, target_obj in self.filter.remaining_word_list, "Filter removed target word.")

    def test_single_green_letter(self):
        """
        Target word is cumin, determine if Ratio filters correctly

        :return:
        :rtype:
        """
        target_string = "cumin"
        target_obj = find_word_from_string(self.word_list, target_string)

        guess_string = "ratio"
        int_color_list = [2, 2, 2, 0, 2]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)

        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # make sure target word exists in the remaining word list
        self.assertEqual(True, target_obj in self.filter.remaining_word_list, "Filter removed target word.")

    def test_single_yellow_letter_with_repetition(self):
        """
        Target word is Roomy, determine if Ratio filters correctly.

        :return:
        :rtype:
        """
        target_string = "roomy"
        target_obj = find_word_from_string(self.word_list, target_string)

        guess_string = "ratio"
        int_color_list = [0, 2, 2, 2, 1]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)

        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # make sure target word exists in the remaining word list
        self.assertEqual(True, target_obj in self.filter.remaining_word_list, "Filter removed target word.")

    def test_triple_green_letter_with_repetition(self):
        """
        Target word is Roomy, determine if Rocky filters correctly.

        :return:
        :rtype:
        """
        target_string = "roomy"
        target_obj = find_word_from_string(self.word_list, target_string)

        guess_string = "rocky"
        int_color_list = [0, 0, 2, 2, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)

        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # make sure target word exists in the remaining word list
        self.assertEqual(True, target_obj in self.filter.remaining_word_list, "Filter removed target word.")

    def test_fully_grey_elimination(self):
        """
        Target word is 'slate', guess 'rummy' should eliminate all words with 'r', 'u', 'm', and 'y'

        :return:
        :rtype:
        """
        guess_string = "rummy"
        int_color_list = [2, 2, 2, 2, 2]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)
        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        for word in self.filter.remaining_word_list:
            word_str = word.get_string()
            self.assertNotIn("r", word_str)
            self.assertNotIn("u", word_str)
            self.assertNotIn("m", word_str)
            self.assertNotIn("y", word_str)

    def test_grey_and_green_same_letter(self):
        """
        Target is 'spend', guess is 'snoop' with one 'o' green and one 'o' grey.
        Ensure filtering only removes words with 'o' in grey-indexed position.

        :return:
        :rtype:
        """
        guess_string = "snoop"
        int_color_list = [0, 2, 0, 2, 2]  # S and O at index 2 are green; N, O at index 3 is grey
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)
        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        # O is green at index 2, grey at index 3. So reject words with O at index 3
        for word in self.filter.remaining_word_list:
            self.assertNotEqual(word.get_string()[3], "o")

    def test_double_green_same_letter(self):
        """
        Target word is 'silly', guess is 'silly' (double green for Ls).

        :return:
        :rtype:
        """
        target_string = "silly"
        target_obj = find_word_from_string(self.word_list, target_string)

        guess_string = "silly"
        int_color_list = [0, 0, 0, 0, 0]
        enumeration_list = [LetterColor(num) for num in int_color_list]

        guess_obj = find_word_from_string(self.word_list, guess_string)
        new_guess = WordleGuess(guess_obj, enumeration_list)
        self.filter.add_guess(new_guess)

        self.assertEqual([target_obj], self.filter.remaining_word_list, "Filter did not isolate perfect match.")

