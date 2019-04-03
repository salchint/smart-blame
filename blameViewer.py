from PySide2.QtWidgets import (QVBoxLayout, QHBoxLayout, QWidget,
                               QPlainTextEdit)
from PySide2.QtCore import (Signal, Slot, Qt, QRect)
from PySide2.QtGui import (QPainter, QTextBlock)

from commitInfoArea import CommitInfoArea
from blame_file import Blame


class BlameViewer(QPlainTextEdit):
    """The text widget that prints the file content and the annotation info."""

    # Signal the commitId to be reblamed
    commitIdClicked = Signal(int)

    def __init__(self, toBlame, commit=0):
        QPlainTextEdit.__init__(self)

        # The UI part
        self.commitInfoArea = CommitInfoArea(self)
        self.blockCountChanged.connect(self.updateCommitInfoAreaWidth)
        self.updateRequest.connect(self.updateCommitInfoArea)
        self.commitInfoArea.clicked.connect(self.reblameAtCommit)
        self.updateCommitInfoAreaWidth(0)

        self.toBlame = toBlame
        self.printSelf(toBlame, commit)

    def printSelf(self, toBlame, commit=0):
        print("Blaming {} at commit {}....".format(toBlame, commit))
        # Run the blame command and capture the output
        blamer = Blame(toBlame, commit=commit)
        #output = blamer.run()
        #self.setPlainText(output.decode())
        self._commitLines = [(b.sourceLine(), b.commitId(), b.lineNumber()) for b in blamer.iterBlocks()]
        print("Collected {} lines at commit {}".format(len(self._commitLines),
               commit))
        self.setPlainText('\n'.join((l[0] for l in self._commitLines)))

    def commitInfoAreaWidth(self):
        digits = 44
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
            self.updateCommitInfoAreaWidth(0)

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

        while block.isValid()  and  top <= e.rect().bottom():
            if block.isVisible()  and  bottom >= e.rect().top():
                commitId = self._commitLines[blocknumber][1]
                lineNumber = self._commitLines[blocknumber][2]
                number = commitId + " " + lineNumber
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.commitInfoArea.width(),
                        self.fontMetrics().height(), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + (int)(self.blockBoundingRect(block).height())
            blocknumber = blocknumber + 1


    @Slot()
    def reblameAtCommit(self, y):
        #print("Clicked at {}".format(y))

        block = self.firstVisibleBlock()
        blocknumber = block.blockNumber()
        top = (int)(self.blockBoundingGeometry(block).translated(
                self.contentOffset()).top())
        bottom = top + (int)(self.blockBoundingRect(block).height())

        commitId = 0
        while block.isValid()  and  top <= y:
            commitId = self._commitLines[blocknumber][1]

            block = block.next()
            top = bottom
            bottom = top + (int)(self.blockBoundingRect(block).height())
            blocknumber = blocknumber + 1

        # print ("Clicked on {}".format(commitId))
        # self.printSelf(self.toBlame, commitId)
        self.commitIdClicked.emit(commitId)
