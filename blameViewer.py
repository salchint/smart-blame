from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget,
        QPlainTextEdit)
from PySide2.QtCore import (Slot, Qt, QRect)
from PySide2.QtGui import (QPainter, QTextBlock)

from commitInfoArea import CommitInfoArea
from blame_file import Blame

class BlameViewer(QPlainTextEdit):
    def __init__(self, toBlame):
        QPlainTextEdit.__init__(self)

        # The UI part
        self.commitInfoArea = CommitInfoArea(self)
        self.blockCountChanged.connect(self.updateCommitInfoAreaWidth)
        self.updateRequest.connect(self.updateCommitInfoArea)
        self.updateCommitInfoAreaWidth(0)

        # Run the blame command and capture the output
        blamer = Blame(toBlame)
        output = blamer.run()
        self.setPlainText(output)

    def commitInfoAreaWidth(self):
        digits = 7

        space = 3 + self.fontMetrics().width('9') * digits
        return space

    @Slot()
    def updateCommitInfoAreaWidth(self, w):
        self.setViewportMargins(self.commitInfoAreaWidth(), 0, 0, 0)

    @Slot()
    def updateCommitInfoArea(self, rect, dy):
        if dy:
            self.commitInfoArea.scroll(0, dy)
        else:
            self.commitInfoArea.update(0, rect.y(),
                    self.commitInfoArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.commitInfoAreaWidth()

    def resizeEvent(self, e):
        # print('Resize the blame viewer')
        QPlainTextEdit.resizeEvent(self, e)

        cr = self.contentsRect()
        self.commitInfoArea.setGeometry(QRect(cr.left(), cr.top(),
            self.commitInfoAreaWidth(), cr.height()))

    def commitInfoAreaPaintEvent(self, e):
        painter = QPainter(self.commitInfoArea)
        painter.fillRect(e.rect(), Qt.darkCyan)

        block = self.firstVisibleBlock()
        blocknumber = block.blockNumber()
        top = (int)(self.blockBoundingGeometry(block).translated(
                self.contentOffset()).top())
        bottom = top + (int)(self.blockBoundingRect(block).height())

        while block.isValid()  and  top <= e.rect().bottom:
            if block.isVisible()  and  bottom >= e.rect().top:
                number = str(blocknumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, commitInfoArea.width(),
                        self.fontMetrics.height(), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + (int)(blockBoundingRect(block).height())
            blocknumber = blocknumber + 1