######################################
#
# WordleFilter - Class responsible for filtering word list down based on provided guesses.
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import string
import subprocess
import csv

# local package imports
from .WordleGuess import WordleGuess, LetterColor, LETTERS_IN_WORD

# Global variables
WORD_LIST_FILENAME = "word_list.csv"
POSITION_FREQUENCY_WEIGHT = 3
GENERAL_FREQUENCY_WEIGHT = 1


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

    # store returned word list to a local .csv file
    with open(WORD_LIST_FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(words[0:])


def get_word_list():
    """
    Gets the list of possible word list from the local csv file.  If a local csv file is not present, a new one will be
    generated by calling store_word_list().

    :return: list of all possible words
    """
    # open the local file to get the words.
    try:
        return _open_word_list()

    # if no file, then send the API request to generate the file, then return it.
    except FileNotFoundError as e:
        store_word_list()
        return _open_word_list()


def _open_word_list():
    """
    Opens the locally stored csv file with all possible wordle words.

    Raises:
        FileNotFoundError if csv file does not exist or cannot be found.

    :return: List of all possible words
    """
    with open(WORD_LIST_FILENAME, "r") as file:
        reader = csv.reader(file)
        words = [row for row in reader][0]

    return words


def _calculate_letter_frequency(word_list: list[str]) -> dict:
    """
    Creates a dictionary corresponding to letter counts in each position.

    :param word_list: List of words.
    :return: Dictionary of positions corresponding with letter frequency.
    """
    letter_frequency = _initialize_letter_frequency_dict()

    for word in word_list:
        if len(word) != LETTERS_IN_WORD:
            raise ValueError("Invalid word length.")

        # Add one to the count for each letter and position.
        for i in letter_frequency:
            letter_frequency[i][word[i]] += 1

    return letter_frequency


def _initialize_letter_frequency_dict() -> dict:
    """
    Creates a blank dictionary to store letter counts for each position.

    :return: Blank dictionary of positions corresponding with letter frequency.
    """
    letter_frequency = {}
    for i in range(5):
        new_alphabet_dict = {letter: 0 for letter in string.ascii_lowercase}
        letter_frequency[i] = new_alphabet_dict

    return letter_frequency


def _get_best_guess_hashing(word_list: list[str]) -> str:
    """
    Determines the best guess based on the dynamic hashing method. This method uses the frequency and location
    of letters to select a guess that has the highest quantity of shared letters with other words.

    :return:
    """
    letter_frequency = _calculate_letter_frequency(word_list)

    # assume the first word is the best word, until we find a better one
    best_word = word_list[0]
    best_score = 0

    for word in word_list:
        score = _get_hash_score(word, letter_frequency)
        if score > best_score:
            best_word = word
            best_score = score

    return best_word


def _get_hash_score(word: str, letter_frequency: dict) -> int:
    """
    Calculates the hash score based on the frequency of letters in specific locations and general frequency.

    :param word: Word to be evaluated.
    :param letter_frequency: Dictionary of positions corresponding with letter frequency.
    :return: Integer hash score for the word.
    """
    score = 0

    # iterate through the indexes of the word
    for i, letter in enumerate(word):
        # determine the position specific score
        position_score = letter_frequency[i][letter] * POSITION_FREQUENCY_WEIGHT

        # determine the position independent score, excluding the current index
        general_score = 0
        for j in range(len(word)):
            if j != i:
                general_score += letter_frequency[j][letter] * GENERAL_FREQUENCY_WEIGHT

        score += (position_score + general_score)

    return score


class WordleFilter:
    """
    Handles narrowing down the words for a Wordle game based on provided guesses.

    """
    def __init__(self):
        """
        Constructor.

        """
        self.remaining_word_list = get_word_list()
        self.guess_list = []

    def add_guess(self, guess: WordleGuess):
        """
        Adds the next guess to the guessed word list, then filters the remaining word list based on information from
        the guess.

        :param guess: WordleGuess used in game.
        :return: None
        """
        self.guess_list.append(guess)
        self._filter_word_list(guess)

    def get_remaining_words(self):
        """
        Returns the remaining words for the given wordle game.

        :return: List of remaining words.
        """
        return self.remaining_word_list

    def _filter_word_list(self, guess: WordleGuess):
        """
        Filters out words from the remaining word list based on information from the guess.

        :param guess: WordleGuess used in game.
        :return: None
        """
        green_index_list = guess.location_dict[LetterColor.GREEN]
        yellow_index_list = guess.location_dict[LetterColor.YELLOW]
        grey_index_list = guess.location_dict[LetterColor.GREY]

        # Use a copy of the word list during iteration to avoid runtime errors.
        for word in self.remaining_word_list.copy():
            # Remove words that do not contain green letters in position.
            for i in green_index_list:
                if word[i] != guess.word[i]:
                    self.remaining_word_list.remove(word)
                    break

            # If the word was not yet removed:
            # Remove words that do not contain yellow letters in position other than the location given.
            else:
                for i in yellow_index_list:
                    # Remove the word if it does not contain the yellow letter.
                    if guess.word[i] not in word:
                        self.remaining_word_list.remove(word)
                        break
                    # Remove the word if it contains the yellow letter in the yellow index.
                    if word[i] == guess.word[i]:
                        self.remaining_word_list.remove(word)
                        break

                # If the word was not yet removed:
                # Remove words that contain grey letters that are not repeated in the green list.
                else:
                    # Since green letters can "consume" repeated letters, filter them out so they are not considered
                    available_letters = [word[j] for j in range(len(word)) if j not in green_index_list]
                    for i in grey_index_list:
                        if guess.word[i] in available_letters:
                            self.remaining_word_list.remove(word)
                            break

    def get_best_guess(self, hashing=True) -> str:
        """
        Gets the best guess for the Wordle puzzle using the current possible remaining words.

        :return: String best word to guess.
        """
        pass

        # If hashing is true, then use the dynamic hash method.
        if hashing:
            return _get_best_guess_hashing(self.remaining_word_list)

        # If hashing is false, then use the entropy method.
