"""
Debugging file for testing the wordle filter.  This file does not use unit tests.  See other test files for unit tests.

This file changes to test random functions during development. Do not use to verify code functionality.
"""

# Import package
import wordle_filter.WordleFilter as wf
import wordle_filter.WordleGuess as wg


def main():
    test_filter = wf.WordleFilter()

    guess_seres = wg.WordleGuess("seres", [wg.LetterColor(1), wg.LetterColor(2), wg.LetterColor(1),
                                           wg.LetterColor(2), wg.LetterColor(0)])

    guess_arars = wg.WordleGuess("arars", [wg.LetterColor(2), wg.LetterColor(0), wg.LetterColor(0),
                                           wg.LetterColor(2), wg.LetterColor(0)])
    guess_brass = wg.WordleGuess("brass", [wg.LetterColor(2), wg.LetterColor(0), wg.LetterColor(0),
                                           wg.LetterColor(0), wg.LetterColor(0)])

    test_filter.add_guess(guess_seres)
    test_filter.add_guess(guess_arars)
    test_filter.add_guess(guess_brass)
    print(test_filter.get_best_guess())
    print(len(test_filter.remaining_word_list))


if __name__ == "__main__":
    main()
