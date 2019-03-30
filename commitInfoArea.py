from PySide2.QtWidgets import QWidget
from PySide2.QtCore import (QSize, Signal, Qt)

class CommitInfoArea(QWidget):
    """A widget left to the file content. It contains the commit information of
    the blamed file.
    """

    # Our own clicked signal
    clicked = Signal(int)

    def __init__(self, parent=None):
        super(CommitInfoArea, self).__init__(parent)
        #QWidget.__init__(viewer)
        self._viewer = parent

    def sizeHint(self):
        return QSize(self._viewer.commitInfoAreaWidth(), 0)

    def paintEvent(self, e):
        #print ('Paint the commit info area')
        self._viewer.commitInfoAreaPaintEvent(e)

    def mousePressEvent(self, e):
        super(CommitInfoArea, self).mousePressEvent(e)
        self.clicked.emit(e.y())
