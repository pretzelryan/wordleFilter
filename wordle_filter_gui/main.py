######################################
#
# main - entry point for wordle solver GUI app.
#
# author - Ryan Muetzel (@pretzelryan)
#

# imports
import sys
from PySide6.QtWidgets import QApplication

# Import package
from .WordleWindow import WordleWindow


def main():
    """
    Instantiates window to open Wordle GUI.

    """
    app = QApplication(sys.argv)

    window = WordleWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
   main()