######################################
#
# WordleWindow - GUI Window to interact nice
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import sys
import numpy as np
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Import package
from wordle_filter.WordleFilter import WordleFilter
from wordle_filter.WordleGuess import WordleGuess, LetterColor
from wordle_filter.Word import Word, LETTERS_IN_WORD

# Default Global Variable
MAX_GUESS_COUNT = 6


# class implementation
class WordleWindow(QMainWindow):
    """
    Window GUI for Wordle Filter.

    """

    def __init__(self, max_guesses=MAX_GUESS_COUNT):
        """
        Constructor.

        """
        super().__init__()

        # Instantiate Local Wordle Filter
        self.wordle_filter = WordleFilter()
        self.max_guesses = max_guesses

        # Set window properties
        self.setWindowTitle("Wordle Filter")

        # Settings menu widget (subwindow)
        # TODO

        # Guess entry, dropdown, and console widgets
        self._instantiate_guess_entry_interface()
        self._instantiate_guess_drop_down_interface()
        self._instantiate_guess_console()
        self._instantiate_guess_history_grid()

        # Instantiate layouts
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        # Add individual layouts to left side
        self.left_layout.addLayout(self.guess_line_layout)
        self.left_layout.addLayout(self.guess_drop_down_layout)
        self.left_layout.addWidget(self.guess_console)
        self.left_layout.addLayout(self.guess_history_grid)

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def _instantiate_guess_entry_interface(self) -> None:
        """
        Instantiates widgets and local layouts associated with guess entry interface.

        :return: None
        :rtype: NoneType
        """
        self.guess_line_edit_label = QLabel("Guess:")

        self.guess_line_edit = QLineEdit()
        self.guess_line_edit.setMaxLength(LETTERS_IN_WORD)
        self.guess_line_edit.returnPressed.connect(self.add_guess)

        self.submit_button = QPushButton("Submit Guess", self)
        self.submit_button.clicked.connect(self.add_guess)

        self.guess_line_layout = QHBoxLayout()
        self.guess_line_layout.addWidget(self.guess_line_edit_label)
        self.guess_line_layout.addWidget(self.guess_line_edit)
        self.guess_line_layout.addWidget(self.submit_button)

    def _instantiate_guess_drop_down_interface(self) -> None:
        """
        Instantiates widgets and local layouts associated with guess drop down interface.

        :return: None
        :rtype: NoneType
        """
        # Create container layout for this subsection
        self.guess_drop_down_layout = QHBoxLayout()

        # create list of color enums
        self.color_enums = [color for color in LetterColor]
        # Reverse so the order is GREY -> YELLOW -> GREEN
        self.color_enums.reverse()

        # Create list of dropdowns and populate
        self.guess_drop_down_list = [QComboBox() for _ in range(LETTERS_IN_WORD)]
        for drop_down in self.guess_drop_down_list:
            # add color selections to dropdown
            # TODO: use icons to populate with color instead of text
            for color in self.color_enums:
                drop_down.addItem(color.name.capitalize())
            # add dropdown to layout
            self.guess_drop_down_layout.addWidget(drop_down)

    def _instantiate_guess_console(self) -> None:
        """
        Instantiates widgets and local layouts associated with guess console.

        :return: None
        :rtype: NoneType
        """
        self.guess_console = QLabel("")
        # For some reason PyCharm is giving a warning 'cannot find reference AlignCenter', but works correctly.
        self.guess_console.setAlignment(Qt.AlignCenter)
        # TODO: Formatting (changing text color)

    def _instantiate_guess_history_grid(self):
        """
        Instantiates widgets and local layouts associated with guess history grid.

        :return: None
        :rtype: NoneType
        """
        self.guess_history_grid = QGridLayout()

        # Populate the grid with graphics text items.
        # each line needs a graphics simple text item for each letter and a resubmit button
        self.guess_array = [["" for _ in range(LETTERS_IN_WORD)] for _ in range(self.max_guesses)]
        self.resubmit_button_list = [QPushButton("Resubmit") for _ in range(self.max_guesses)]
        # TODO: Link buttons to actions

        for guess_index in range(self.max_guesses):
            for letter_index in range(LETTERS_IN_WORD):
                # Store the graphic text items to the storage array
                new_graphic_letter = QLabel(f"{guess_index, letter_index}")
                self.guess_array[guess_index][letter_index] = new_graphic_letter
                # TODO: figure out how to display the letters prettily and with corresponding color background.

                # Then add it to the grid layout
                self.guess_history_grid.addWidget(new_graphic_letter, guess_index, letter_index, Qt.AlignCenter)

            # We also want to place all the resubmit buttons at the end of their corresponding line
            self.guess_history_grid.addWidget(self.resubmit_button_list[guess_index], guess_index, LETTERS_IN_WORD)

        # Reset button should span the entire horizontal grid
        self.reset_button = QPushButton("Reset Guesses", self)
        self.guess_history_grid.addWidget(self.reset_button, self.max_guesses, 0, 1, LETTERS_IN_WORD)

    def add_guess(self) -> None:
        """
        Creates a new Wordle Guess object.

        :return: None
        :rtype: NoneType
        """
        print(f"Got: {self.guess_line_edit.text()}")
        self.guess_console.setText("Guess Entered: " + self.guess_line_edit.text())

        pass

    def filter_words(self):
        """
        Filters the word list based on input guesses.

        :return: None
        :rtype: NoneType
        """
        print("TODO: filter_words not yet implemented")

    def calculate_scores(self):
        """
        Calculates the score for words.

        :return: None
        :rtype: NoneType
        """
        print("TODO: calculate_scores not yet implemented")

