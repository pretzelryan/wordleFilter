######################################
#
# WordleFilter - Class responsible for filtering word list down based on provided guesses.
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import copy
import warnings

# local package imports
from .WordleGuess import WordleGuess, LetterColor
from .Word import Word, get_words_file


class WordleFilter:
    """
    Handles narrowing down the words for a Wordle game based on provided guesses.

    """
    def __init__(self):
        """
        Constructor.

        """
        self.total_word_list = get_words_file()
        self.guess_list = None
        self.remaining_word_list = None

        self.reset_guess_list()

    def reset_guess_list(self):
        """
        Reset guess list and remaining word list to start of game.

        :return: None
        :rtype: NoneType
        """
        self.remaining_word_list = copy.deepcopy(self.total_word_list)
        self.guess_list = []

    def add_guess(self, guess: WordleGuess):
        """
        Adds the next guess to the guessed word list, then filters the remaining word list based on
        information from the guess.

        :param guess: wordle guess object to add
        :type guess: WordleGuess
        :return: None
        :rtype: NoneType
        """
        if guess not in self.guess_list:
            self.guess_list.append(guess)
            self._filter_word_list(guess)
        else:
            warnings.warn("Guess already exists in the guess list.", UserWarning)

    def get_remaining_words(self):
        """
        Returns the remaining words for the given wordle game.

        :return: list of remaining words.
        """
        return self.remaining_word_list

    def _filter_green(self, word: Word, word_string: str,
                      guess_string: str, index_list: list[int]) -> bool:
        """
        Determine if a word is still valid based on the green index list.

        :param word: Word object to check
        :type word: Word
        :param word_string: String of word object
        :type word_string: str
        :param guess_string: String of guess
        :type guess_string: str
        :param index_list: list of index of green letters in guess
        :type index_list: list[int]
        :return: True if word is removed, False otherwise.
        :rtype: bool
        """
        for i in index_list:
            # Remove words that do not contain green letters in position.
            if word_string[i] != guess_string[i]:
                self.remaining_word_list.remove(word)
                return True

        # word is not removed, return false
        return False

    def _filter_yellow(self, word: Word, word_string: str,
                       guess_string: str, index_list: list[int]) -> bool:
        """
        Determine if a word is still valid based on the yellow index list.

        :param word: Word object to check
        :type word: Word
        :param word_string: String of word object
        :type word_string: str
        :param guess_string: String of guess
        :type guess_string: str
        :param index_list: list of index of yellow letters in guess
        :type index_list: list[int]
        :return: True if word is removed, False otherwise.
        :rtype: bool
        """
        for i in index_list:
            # Remove the word if it does not contain the yellow letter.
            if guess_string[i] not in word_string:
                self.remaining_word_list.remove(word)
                return True

            # Remove the word if it contains the yellow letter in the yellow index.
            if word_string[i] == guess_string[i]:
                self.remaining_word_list.remove(word)
                return True

        # word is not removed, return false
        return False

    def _filter_grey(self, word: Word, word_string: str, guess_string: str,
                     available_letters: set[str], index_list: list[int]) -> bool:
        """
        Determine if a word is still valid based on the grey index list.

        :param word: Word object to check
        :type word: Word
        :param word_string: String of word object
        :type word_string: str
        :param guess_string: String of guess
        :type guess_string: str
        :param available_letters: list of grey letters in guess that are not used in the solution elsewhere
        :type available_letters: set[str]
        :param index_list: list of index of grey letters in guess
        :type index_list: list[int]
        :return: True if word is removed, False otherwise.
        :rtype: bool
        """
        for i in index_list:
            # if the word contains a letter that is guaranteed to not be part of the solution, remove it
            if word_string[i] in available_letters:
                self.remaining_word_list.remove(word)
                return True

            # for cases of repeated letters where the duplicate letter is in green/yellow list
            # remove words that have that letter in the grey position
            elif guess_string[i] == word_string[i]:
                self.remaining_word_list.remove(word)
                return True

        # word is not removed, return false
        return False

    def _filter_word_list(self, guess: WordleGuess):
        """
        Filters out words from the remaining word list based on information from the guess.

        :param guess: Guess object to check the word list against
        :type guess: WordleGuess
        :return: None
        :rtype: NoneType
        """
        green_index_list = guess.location_dict[LetterColor.GREEN]
        yellow_index_list = guess.location_dict[LetterColor.YELLOW]
        grey_index_list = guess.location_dict[LetterColor.GREY]

        guess_string = guess.get_word().get_string()

        # grey letters should only be considered if they are not in the green or yellow letter sets
        green_letters = {guess_string[i] for i in green_index_list}
        yellow_letters = {guess_string[i] for i in yellow_index_list}
        grey_letters = {guess_string[i] for i in grey_index_list
                        if guess_string[i] not in green_letters and guess_string[i] not in yellow_letters}

        # Use a copy of the word list during iteration
        for word in self.remaining_word_list.copy():
            word_string = word.get_string()
            # example dict = {green: [1, 2], yellow: [4], grey: [3, 5]}

            # check against each color enum to determine if the word should be eliminated
            # if the word is eliminated, then the function will return true and trigger loop continue
            if self._filter_green(word, word_string, guess_string, green_index_list):
                continue
            if self._filter_yellow(word, word_string, guess_string, yellow_index_list):
                continue
            if self._filter_grey(word, word_string, guess_string, grey_letters, grey_index_list):
                continue
            # if a word was not removed, it is still a valid guess
