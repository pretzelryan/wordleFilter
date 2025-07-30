######################################
#
# WordleFilter - Class representing individual .
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import subprocess
import csv
import pickle

# Globals
SOURCE_WORD_LIST_TXT = "words.txt"
STORED_WORDS_FILE = "word_objects.pkl"


class Word:
    """
    Represents a word object in context of a wordle game.

    """

    def __init__(self, word: str, level: int, entropy_vec: list[float], percentile_vec: list[int],
                 expected_entropy: float, expected_words_remaining: float, max_words_remaining: int,
                 number_of_groups: int, prior: int, precomputed_average: list[float],
                 expected_additional_guesses: float):
        """
        Constructor.

        :param word: string word
        :type word: str
        :param level: integer level
        :type level: int
        :param entropy_vec: entropy vector of floats
        :type entropy_vec: list[float]
        :param percentile_vec: percentile vector of floats
        :type percentile_vec: list[float]
        :param expected_entropy: float entropy score
        :type expected_entropy: float
        :param expected_words_remaining: integer number of expected words remaining
        :type expected_words_remaining: int
        :param max_words_remaining: integer maximum number of words remaining
        :type max_words_remaining: int
        :param number_of_groups: integer number of groups
        :type number_of_groups: int
        :param prior: integer prior
        :type prior: int
        :param precomputed_average: list of floats precomputed averages
        :type precomputed_average: list[float]
        :param expected_additional_guesses: float expected additional guesses
        :type expected_additional_guesses: float
        """

        self.word = word
        self.level = level
        self.entropy_vec = entropy_vec
        self.percentile_vec = percentile_vec
        self.expected_entropy = expected_entropy
        self.expected_words_remaining = expected_words_remaining
        self.max_words_remaining = max_words_remaining
        self.number_of_groups = number_of_groups
        self.prior = prior
        self.precomputed_average = precomputed_average
        self.expected_additional_guesses = expected_additional_guesses


def _open_raw_word_list() -> list[str]:
    """
    Opens the raw text file of words.

    Raises:
        FileNotFoundError if txt file does not exist or cannot be found.

    :return: list of words as strings
    :rtype: list[str]
    """
    with open(SOURCE_WORD_LIST_TXT, "r") as f:
        return f.read().splitlines()

def _convert_string_to_num(val: str | list[str]) -> int | float | str | list:
    """
    Converts a string to an int or float or list of ints or floats.
    If conversion fails, returns original string.

    :param val: string to convert
    :type val: str
    :return: converted type
    :rtype: int | float | str | list
    """
    # if we have a list, then recursively call to convert all datatypes within the list
    if isinstance(val, list):
        return [_convert_string_to_num(v) for v in val]

    # if it's a string
    elif isinstance(val, str):
        # floats have a dot in the string
        if "." in val:
            return float(val)
        # otherwise it's probably an int
        elif val.isdigit():
            return int(val)
        # edge case, where the number is neither float nor int
        else:
            return val

    # if it's not a string then return the object itself.
    else:
        return val

def get_raw_word_list() -> list[str]:
    """
    Gets the list of words from the word list file.

    :return: list of words as strings
    :rtype: list[str]
    """
    try:
        return _open_raw_word_list()

    except FileNotFoundError as e:
        import_word_list()
        return _open_raw_word_list()

def import_word_list():
    """
    Retrieves the word list from nytimes word list file.

    """
    # set up the subprocess to get the word list from GitHub repo
    command = "curl -s https://static01.nytimes.com/newsgraphics/wordlebot/_big_assets/words.txt"
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    # if successfully got the response, parse into a list
    if result.returncode == 0:
        words = result.stdout.splitlines()
    # otherwise throw error
    else:
        raise subprocess.SubprocessError(result.returncode, command, result.stderr)

    # store returned word list to a local .txt file, delimited by tabs and returns
    with open(SOURCE_WORD_LIST_TXT, "w", newline="") as file:
        file.write(result.stdout)

def generate_words_file():
    """
    Processes word list text file into word objects, then stores them.

    """
    # Get the list of strings
    word_string_list = get_raw_word_list()

    # Preallocate object list size. The first line is the header and will be ignored
    word_object_list = [None] * (len(word_string_list) - 1)

    # looping through the list of strings, ignoring the header
    for i, word in enumerate(word_string_list[1:]):
        # take the string and spit it into the fields, delimited on tabs
        fields = word.split("\t")

        # some entries are lists with comma delimiter, so process those strings into lists
        for j, entry in enumerate(fields):
            if "," in entry:
                fields[j] = [_convert_string_to_num(x.strip()) for x in entry.split(",")]
            else:
                fields[j] = _convert_string_to_num(entry)

        # use the fields list to create the Word object (*args)
        word_object_list[i] = Word(*fields)

    # store the words file
    with open(STORED_WORDS_FILE, 'wb') as file:
        pickle.dump(word_object_list, file)

def get_words_file() -> list[Word]:
    """
    Get the list of word objects.

    If list of objects does not yet exist, it will be created.

    :return:
    :rtype: list[Word]
    """
    pass
