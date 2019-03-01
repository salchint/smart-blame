import sys
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QWidget, QPlainTextEdit)
from PySide2.QtCore import Slot, Qt

class MyColumn(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo"]

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
    def __init__(self):
        QWidget.__init__(self)

        self.hello = MyColumn()
        self.plainText = QPlainTextEdit()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.hello)
        self.layout.addWidget(self.plainText)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
