""" User stories

I try to write this module's/application's documentation in user stories. This
way the list of requirements is transparent and can evolve during development.

(/) As Bob I want git-blame to be printed to the MyColumn widget.
(/) As Bob I want the file to be blamed specified as a command line argument.
() As Bob I want the MyColumn widget splitted in order to have the blame info
separated from the content.
() As Bob I want the content to be syntactically highlighted.
() As Werner I want to get and process the blame info in its porcelain format
in order to get the full information about the commit.
"""

import sys
import random

from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit)
from PySide2.QtCore import Slot, Qt

import blame_file

class MyColumn(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma", "Hola Mundo"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

class MyWidget(QWidget):
    def __init__(self, toBlame):
        QWidget.__init__(self)

        self.hello = MyColumn()
        self.plainText = QPlainTextEdit()

        # run the blame command and capture the output
        blame = blame_file.Blame(toBlame)
        output = blame.run()
        self.plainText.appendPlainText(output)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.hello)
        self.layout.addWidget(self.plainText)
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
