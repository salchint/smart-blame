#!python
# -*- coding: utf-8 -*- 

""" User stories

I try to write this module's/application's documentation in user stories. This
way the list of requirements is transparent and can evolve during development.

(/) As Bob I want git-blame to be printed to the BlameDocument widget.
(/) As Bob I want the file to be blamed specified as a command line argument.
(/) As Bob I want the BlameDocument widget split in order to have the commit info
    separated from the content.
(/) As Bob I want the commit info and the content scroll simultaneously.
(/) As Werner I want to get and process the commit info in its porcelain format
    in order to get the full information about the commit.
(/) As Bob I want the commitId to be clickable.
(/) As Bob I want to click on the commitId to reblame the file at that very
    commit.
(/) As Bob I want to have the reblamed file displayed in a separate BlameViewer.
(/) As Bob I want the commitIds be shortened to safe space for the code.
() As Bob I want the same commitIds be grouped colorfully.
() As Bob I want to get a balloon displaying all the commit details, when
    hovering over the commitId.
() As Bob I want the content to be syntactically highlighted.
() As Bob I want to close BlameViewers individually.
"""

import sys

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
    """This is my main widget.

    The main widget represents the container for the one or more blameViewer
    widgets, each displaying one version of the given file.
    """

    def __init__(self, toBlame):
        QWidget.__init__(self)

        self.toBlame = toBlame
        self.viewers = []
        self.layout = QHBoxLayout()

        # Add the initial viewer, displaying working copy version of the given
        # file.
        blameView = BlameViewer(toBlame)
        self.addViewer(blameView)

    @Slot()
    def reblameCommit(self, commitId):
        print("  Reblame {} at {}".format(self.toBlame, commitId))
        blameView = BlameViewer(self.toBlame, commitId)
        self.addViewer(blameView)

    def addViewer(self, viewer):
        # oldViewers = self.viewers
        # print("Reinserting {} old viewers".format(len(oldViewers)))
        # self.clearViewers()

        # # New viewers are displayed left to the current ones
        # self.viewers.insert(0, viewer)
        # self.viewers += oldViewers

        # for v in self.viewers:
            # print("Add {} to main layout".format(v))
            # self.layout.addWidget(v)

        self.layout.addWidget(viewer)

        self.setLayout(self.layout)

        # Make the viewer sensitive to reblaming events
        viewer.commitIdClicked.connect(self.reblameCommit)

    # def clearViewers(self):
        # """Remove all the viewers from the main widgets layout."""

        # while 0 < len(self.viewers):
            # item = self.layout.takeAt(0)
            # self.viewers.pop(0)

            # # Don't really delete the viewer as it is going to be reinserted
            # # item.widget().deleteLater()
            # item.widget().setParent(None)


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
        sys.exit("No file to be blamed specified.")


if __name__ == "__main__":
    main(sys.argv)

