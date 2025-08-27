######################################
#
# WordleScorer - Class responsible for giving guesses a score to determine best guess.
#
# author - Ryan Muetzel (@pretzelryan)
#

# local package imports
from .Word import Word


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
    the solution space. This approach is less efficient, but more generally more initiative.

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
    raise NotImplementedError("Heuristic scorer is not yet implemented.")
    # first construct a data structure of what letters exist where for the provided word list.
    # then use that data structure to score each word (_calculate_heuristic_score)
    # then normalize the score from 0-99


def _calculate_heuristic_score(word: Word) -> None:
    """
    Calculates the score for a word using heuristic method. Directly modifies word object.

    :param word: Word to calculate score for.
    :type word: Word
    :return: None
    :rtype: NoneType
    """
    pass
    # This function might get removed or mechanically changed
    # depends on implementation of the scoring algorithm

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
        new_score = ((old_score - existing_min_score) / existing_range) \
                    + target_range + existing_min_score
        word.set_score(new_score)
