"""
Debugging file for testing the wordle filter.  This file does not use unit tests.  See other test files for unit tests.
"""

# Import package
import wordle_filter.WordleFilter as wf
import wordle_filter.WordleGuess as wg


def main():
    words = wf.get_word_list()
    print(words)


if __name__ == "__main__":
    main()
