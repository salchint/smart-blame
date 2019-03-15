from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QSize

class CommitInfoArea(QWidget):
    """A widget left to the file content. It contains the commit information of
    the blamed file.
    """
    def __init__(self, viewer):
        QWidget.__init__(self)
        self._viewer = viewer

    def sizeHint(self):
        return QSize(self._viewer.commitInfoAreaWidth(), 0)

    def paintEvent(self, e):
        print ('Paint the commit info area')
        # QWidget.paintEvent(self, e)
        self._viewer.commitInfoAreaPaintEvent(e)
