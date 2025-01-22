######################################
#
# TODO: documentation
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import subprocess
import csv

# local package imports
# from .WordleGuess import WordleGuess


def store_word_list():
    """
    Gets and stores the list of possible words to a local csv file.

    """
    # set up the subprocess to get the word list from github repo
    command = "curl -s https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    # if successfully got the response, parse into a list
    if result.returncode == 0:
        words = result.stdout.splitlines()
    # otherwise throw error
    else:
        raise subprocess.SubprocessError(result.returncode, command, result.stderr)

    print(words)

    # store returned word list to a local .csv file
    with open("word_list.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(words[0:])


class WordleFilter:
    """
    Handles narrowing down the words for a Wordle game based on provided guesses.

    """
    def __init__(self):
        # TODO: docstring
        pass


def main():
    store_word_list()


if __name__ == "__main__":
    main()
