from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit)

from blame_file import Blame

class BlameDocument(QWidget):
    def __init__(self, toBlame):
        QWidget.__init__(self)

        self.fileContent = QPlainTextEdit()
        self.commitInfo = QPlainTextEdit()

        # run the blame command and capture the output
        blamer = Blame(toBlame)
        output = blamer.run()
        self.fileContent.setPlainText(output)
        self.commitInfo.setPlainText(output)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.commitInfo)
        self.layout.addWidget(self.fileContent)
        self.setLayout(self.layout)


