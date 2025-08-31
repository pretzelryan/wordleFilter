######################################
#
# WordleFilter - Class representing individual words. Also handles importing list of word objects.
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import subprocess
import pickle

# Globals
SOURCE_WORD_LIST_TXT = "words.txt"
STORED_WORD_LIST_PKL = "word_objects.pkl"
LETTERS_IN_WORD = 5


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

        self._set_string(word)
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
        self.score = int(0)

    def _set_string(self, word_str: str) -> None:
        """
        Set the string of word. Should only be called from word object constructor.

        :param word_str: String of word object.
        :type word_str: str
        :return: None
        :rtype: NoneType
        """
        if len(word_str) != LETTERS_IN_WORD:
            raise ValueError(f"Word string must have length equal to word length. "
                             f"Expected {LETTERS_IN_WORD}, but got {len(word_str)}.")
        self.word = word_str

    def get_string(self) -> str:
        """
        Returns the string word.

        :return: word string
        :rtype: str
        """
        return self.word

    def get_level(self) -> int:
        """
        Returns the level of the word. Level corresponds to if a word is a common word, thus likely to
        be a possible solution. Level 0 represents common words.

        :return: int level of word
        :rtype: int
        """
        return self.level

    def get_score(self) -> int:
        """
        Returns the score of the word. Score corresponds to the efficiency of the word as a guess.
        Words that should find the solution faster have a higher score.

        :return: int score of word
        :rtype: int
        """
        return self.score

    def get_letter(self, index) -> str:
        """
        Returns the letter in the i-th position in the word.

        :return: string letter
        :rtype: str
        """
        if not (0 <= index < LETTERS_IN_WORD):
            raise ValueError(f"Index must be between 0 and {LETTERS_IN_WORD}. Got {index}.")
        return self.word[index]

    def set_score(self, score: int | float) -> None:
        """
        Sets the score of the word. Score corresponds to the efficiency of the word as a guess.
        Words that should find the solution faster have a higher score.

        :param score: int score
        :type score: int | float
        :return: None
        :rtype: NoneType
        """
        self.score = score

    def __repr__(self) -> str:
        """
        String representation of the word.

        :return: word string
        :rtype: str
        """
        return self.get_string()

    def __eq__(self, other: object | str) -> bool:
        """
        Equality operator. Compares the string of other to string of this word.

        :param other: other word object or string
        :type other: Word
        :return: true if self and other are equal, false otherwise
        :rtype: bool
        """
        if isinstance(other, Word):
            return self.get_string() == other.get_string()
        elif isinstance(other, str):
            return self.get_string() == other
        return NotImplemented


def _open_word_list_txt() -> list[str]:
    """
    Opens the raw text file of words.

    Raises:
        FileNotFoundError if txt file does not exist or cannot be found.

    :return: list of words as strings
    :rtype: list[str]
    """
    with open(SOURCE_WORD_LIST_TXT, "r") as f:
        return f.read().splitlines()

def _open_word_list_pkl() -> list[Word]:
    """
    Opens pickle file of word objects.

    Raises:
        FileNotFoundError if pickle file does not exist or cannot be found.

    :return: list of word objects
    :rtype: list[Word]
    """
    with open(STORED_WORD_LIST_PKL, "rb") as f:
        return pickle.load(f)

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
        return _open_word_list_txt()

    except FileNotFoundError as e:
        import_word_list()
        return _open_word_list_txt()

def import_word_list():
    """
    Retrieves the word list from nytimes remote word list file.

    :return: None
    :rtype: NoneType
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

    :return: None
    :rtype: NoneType
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
    with open(STORED_WORD_LIST_PKL, 'wb') as file:
        pickle.dump(word_object_list, file)

def get_words_file() -> list[Word]:
    """
    Get the list of word objects.

    If list of objects does not yet exist, it will be created.

    :return: list of word objects
    :rtype: list[Word]
    """
    try:
        return _open_word_list_pkl()
    except FileNotFoundError as e:
        generate_words_file()
        return _open_word_list_pkl()

def find_word_from_string(word_list: list[Word], target_string: str) -> Word | None:
    """
    Finds the first Word object in the word list provided.

    :param word_list: list of word objects to be searched
    :type word_list: list[Word]
    :param target_string: string of word to search for
    :type target_string: str
    :return: Word object with matching string to target string if found, otherwise None
    :rtype: Word | None
    """
    return next((word for word in word_list if word == target_string), None)
