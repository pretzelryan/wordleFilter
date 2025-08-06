"""
Debugging file for testing the wordle filter.  This file does not use unit tests.  See other test files for unit tests.
"""

# Import package
import wordle_filter.WordleFilter as wf
import wordle_filter.Word as w
import wordle_filter.WordleGuess as wg
from wordle_filter.Word import get_words_file


def main():
    """
    debug

    :return:
    :rtype:
    """
    w.import_word_list()
    words = get_words_file()

    new_color_list = [wg.LetterColor.GREEN, wg.LetterColor.GREY, wg.LetterColor.GREY, wg.LetterColor.GREY, wg.LetterColor.GREY]
    new_guess = wg.WordleGuess(words[0], new_color_list)


if __name__ == "__main__":
    main()
