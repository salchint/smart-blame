#!python
# -*- coding: utf-8 -*- 

""" User stories

I try to write this module's/application's documentation in user stories. This
way the list of requirements is transparent and can evolve during development.

(/) As Bob I want git-blame to be printed to the BlameDocument widget.
(/) As Bob I want the file to be blamed specified as a command line argument.
(/) As Bob I want the BlameDocument widget splitted in order to have the commit info
separated from the content.
() As Bob I want the commit info and the content scroll simultaneously.
() As Bob I want the content to be syntactically highlighted.
() As Werner I want to get and process the commit info in its porcelain format
in order to get the full information about the commit.
"""

import sys
import random

from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit)
from PySide2.QtCore import Slot, Qt

from blameViewer import BlameViewer


        # self.hello = ["Hallo Welt", "你好，世界", "Hei maailma", "Hola Mundo"]

        # self.button = QPushButton("Click me!")
        # self.text = QLabel("Hello World")
        # self.text.setAlignment(Qt.AlignCenter)

        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)
        # self.setLayout(self.layout)

        # # Connecting the signal
        # self.button.clicked.connect(self.magic)

    # @Slot()
    # def magic(self):
        # self.text.setText(random.choice(self.hello))


class MyWidget(QWidget):
    def __init__(self, toBlame):
        QWidget.__init__(self)

        # For now there is only this one document
        self.blameView = BlameViewer(toBlame)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.blameView)
        self.setLayout(self.layout)


class ArgumentWarning(SyntaxWarning):
    pass


def main(argv):
    app = QApplication(argv)
    #print(app.arguments())

    if 1 < len(app.arguments()):
        widget = MyWidget(app.arguments()[1])
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec_())
    else:
        sys.exit("No file to be blamed given.")


if __name__ == "__main__":
    main(sys.argv)

