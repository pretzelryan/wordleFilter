######################################
#
# WordleScorer - Class responsible for giving guesses a score to determine best guess.
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
from string import ascii_lowercase
from typing import Optional

# local package imports
from .Word import Word, LETTERS_IN_WORD


class LetterTracker:
    """
    Tracks the frequency of letters in a list of words by letter index.

    """

    def __init__(self, word_list: list[Word], word_length: int):
        """
        Constructor.

        :param word_list: list of word objects.
        :type word_list: list[Word]
        """
        # initialize data structure for letter storage
        self.indexed_letter_counts = [_create_letter_dict() for letter in range(word_length)]
        self.total_letter_counts = _create_letter_dict()

        # count the letters for each word
        for word in word_list:
            self._add_indexed_letter_count(word)

        # update the total letter count at the end
        self._add_total_letter_count()

    def _add_indexed_letter_count(self, word: Word) -> None:
        """
        Updates the indexed letter count for a word.

        :param word: word object to be counted.
        :type word: Word
        :return: None
        :rtype: NoneType
        """
        word_str = word.get_string()
        for index in range(len(word_str)):
            letter = word_str[index]
            self.indexed_letter_counts[index][letter] += 1

    def _add_total_letter_count(self):
        """
        Updates the total letter count based on the indexed letter counts.

        :return: None
        :rtype: NoneType
        """
        for letter in self.total_letter_counts:
            for index in range(len(self.indexed_letter_counts)):
                self.total_letter_counts[letter] += self.indexed_letter_counts[index][letter]

    def get_letter_count(self, letter: str, index: Optional[int] = None) -> int:
        """
        Returns the number of times a letter appears in the all the remaining words.
        When the optional index parameter is supplied, the count returned refers only to that index.
        Otherwise, returns the count for all indexes.

        :param letter: target letter to look up count.
        :type letter: str
        :param index: Optional, index to look up count.
        :type index: int
        :return: count of times the letter appears in word list.
        :rtype: int
        """
        # if no index is provided then return the total  count for that letter
        if index is None:
            return self.total_letter_counts[letter]

        # otherwise return the count for the letter at the specified index
        return self.indexed_letter_counts[index][letter]


def filter_level_zero_words(word_list: list[Word]) -> list[Word]:
    """
    Returns the word list to only contain words with level = 0.
    Words that are level zero are considered common words, so they are able to be a possible solution.

    :param word_list: List of words objects to filter
    :type word_list: list[Word]
    :return: List of filtered words with level 0.
    :rtype: list[Word]
    """
    return [word for word in word_list if word.get_level() == 0]


def sort_word_list_by_score(word_list: list[Word]) -> None:
    """
    Sorts the word list by score in decreasing order (high to low). This function mutates the list itself,
    so nothing is returned.

    :param word_list: Word list to sort
    :type word_list: list[Word]
    :return: None
    :rtype: NoneType
    """
    word_list.sort(key=lambda word: word.get_score(), reverse=True)


def score_words(word_list: list[Word], use_entropy=False) -> None:
    """
    Updates the word attributes to calculate the score. This function mutates the objects in the list,
    rather than returning a new list.

    One of two methods can be used to calculate score, either entropy or heuristic.

    Entropy attempts to find the word that splits the remaining words into as many groups as possible.
    The more groups generated, the less guesses taken to find the solution. This grouping approach imitates
    a search tree.

    Heuristic attempts to find the word that has the most common letters based on the words left in the
    word list. This chooses guesses that will gain information about the most common letters, thus narrowing
    the solution space. This approach is less efficient, but more generally more intuitive.

    :param use_entropy: Optional. True if entropy scorer should be used, false if heuristic scorer should be used.
                        Defaults to false.
    :type use_entropy: bool
    :param word_list: List of word objects to score
    :type word_list: list[Word]
    :return: None
    :rtype: NoneType
    """
    if use_entropy:
        _score_words_entropy(word_list)
    else:
        _score_words_heuristic(word_list)


def _score_words_entropy(word_list: list[Word]) -> None:
    """
    Calculates the entropy scores for a list of words. Directly mutates word objects in list,
    so no list is returned.
    
    :param word_list: list of word objects to score
    :type word_list: list[Word]
    :return: None
    :rtype: NoneType
    """
    raise NotImplementedError("Entropy scorer is not yet implemented.")


def _calculate_entropy_score(word: Word) -> None:
    """
    Calculates the score for a word using entropy method. Directly modifies word object.

    :param word: Word to calculate score for.
    :type word:
    :return:
    :rtype:
    """
    pass
    # This function might get removed or mechanically changed
    # depends on implementation of the scoring algorithm


def _score_words_heuristic(word_list: list[Word]) -> None:
    """
    Calculates the heuristic scores for a list of words. Directly mutates word objects in list,
    so no list is returned.

    :param word_list: list of word objects to score.
    :type word_list: list[Word]
    :return: None
    :rtype: NoneType
    """
    # construct a data structure of what letters exist where for the provided word list.
    tracker = _calculate_letter_frequency(word_list)

    # use data structure to score each word
    for word in word_list:
        _calculate_heuristic_score(word, tracker)

    # then normalize the score from 0-99 and sort
    _normalize_scores(word_list)
    sort_word_list_by_score(word_list)


def _calculate_letter_frequency(word_list: list[Word]) -> LetterTracker:
    """
    Calculates the frequency of letters for the words in the provided word list.
    Letters are tracked for where in the word they show up.

    :param word_list:
    :type word_list:
    :return:
    :rtype:
    """
    # simply construct and return a letter tracker object. The constructor handles the calculations here.
    return LetterTracker(word_list, LETTERS_IN_WORD)


def _calculate_heuristic_score(word: Word, tracker: LetterTracker,
                               index_weight: int=5, overall_weight: int=1) -> None:
    """
    Calculates the score for a word using heuristic method. Directly modifies word object.

    :param word: Word to calculate score for.
    :type word: Word
    :return: None
    :rtype: NoneType
    """
    # Current scoring methodology:
    # For each index of the word, get the letter in that index.
    # Then look up the number of occurrences for that letter in that indexed position and overall.
    # Add a score multiplied by weights for position specific and overall frequency.
    #
    # To not over incentivise words with the most common letters (ex: the word ARARS), the overall weight
    # will only be accounted for if that letter only appears once in the word. If a letter appears more than
    # once in the word, only consider the index specific contribution and ignore the overall frequency.

    new_score = 0

    for index in range(LETTERS_IN_WORD):
        letter = word.get_letter(index)

        # calculate the index dependant weighting
        index_count = tracker.get_letter_count(letter, index)
        new_score += index_count * index_weight

        # only do index independent weighting if there is one occurrence of the letter
        if word.get_string().count(letter) == 1:
            overall_count = tracker.get_letter_count(letter)
            new_score += overall_count * overall_weight

    word.set_score(new_score)


def _normalize_scores(word_list: list[Word], minimum: int=0, maximum: int=99) -> None:
    """
    Linearly adjusts all scores to fall within the minimum and maximum possible values.
    Function mutates existing word list, so nothing is returned.

    :param word_list: List of word objects with scores.
    :type word_list: list[Word]
    :param minimum: Lowest number to scale the scores to.
    :type minimum: int
    :param maximum: Highest number to scale the scores to.
    :type maximum: int
    :return: None
    :rtype: NoneType
    """
    # get the existing minimum and maximum scores
    existing_min_score = min(word_list, key=lambda word: word.get_score()).get_score()
    existing_max_score = max(word_list, key=lambda word: word.get_score()).get_score()
    existing_range = existing_max_score - existing_min_score
    target_range = maximum - minimum

    # scale the score of each word
    for word in word_list:
        old_score = word.get_score()
        scaled_score = ((old_score - existing_min_score) / existing_range) * target_range + existing_min_score

        # the scaled score may be a float, but we only want ints. Round it and clamp to min/max range
        new_score = _clamp_integer(scaled_score)
        word.set_score(new_score)

def _clamp_integer(score: int | float, minimum: int=0, maximum: int=99) -> int:
    """
    Rounds the score to the nearest integer, then clamps the score to ensure it falls within
    the maximum and minimum values.

    :param score: Score to round and clamp.
    :type score: int | float
    :param minimum: Minimum range.
    :type minimum: int
    :param maximum: Maximum range.
    :type maximum: int
    :return: Adjusted score.
    :rtype: int
    """
    new_score = round(score)
    return max(minimum, min(new_score, maximum))


def _create_letter_dict() -> dict[str, int]:
    """
    Creates a new dict to hold the letter frequencies. Returns a dictionary with all letters english letters
    as keys and zero as the value for all keys

    :return: dictionary with all letters english letters as keys and zero as the value.
    :rtype: dict
    """
    return {letter: 0 for letter in ascii_lowercase}
