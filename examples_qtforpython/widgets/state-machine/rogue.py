#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2010 velociraptor Genjix <aphidia@hotmail.com>
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class MovementTransition(QEventTransition):
    def __init__(self, window):
        super(MovementTransition, self).__init__(window, QEvent.KeyPress)
        self.window = window
    def eventTest(self, event):
        if event.type() == QEvent.StateMachineWrapped and \
          event.event().type() == QEvent.KeyPress:
            key = event.event().key()
            return key == Qt.Key_2 or key == Qt.Key_8 or \
                key == Qt.Key_6 or key == Qt.Key_4
        return False
    def onTransition(self, event):
        key = event.event().key()
        if key == Qt.Key_4:
            self.window.movePlayer(self.window.Left)
        if key == Qt.Key_8:
            self.window.movePlayer(self.window.Up)
        if key == Qt.Key_6:
            self.window.movePlayer(self.window.Right)
        if key == Qt.Key_2:
            self.window.movePlayer(self.window.Down)

class Custom(QState):
    def __init__(self, parent, mw):
        super(Custom, self).__init__(parent)
        self.mw = mw

    def onEntry(self, e):
        print(self.mw.status)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.pX = 5
        self.pY = 5
        self.width = 35
        self.height = 20
        self.statusStr = ''

        database = QFontDatabase()
        font = QFont()
        if 'Monospace' in database.families():
            font = QFont('Monospace', 12)
        else:
            for family in database.families():
                if database.isFixedPitch(family):
                    font = QFont(family, 12)
        self.setFont(font)

        self.setupMap()
        self.buildMachine()
        self.show()
    def setupMap(self):
        self.map = []
        qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))
        for x in range(self.width):
            column = []
            for y in range(self.height):
                if x == 0 or x == self.width - 1 or y == 0 or \
                  y == self.height - 1 or qrand() % 40 == 0:
                    column.append('#')
                else:
                    column.append('.')
            self.map.append(column)

    def buildMachine(self):
        machine = QStateMachine(self)

        inputState = Custom(machine, self)
        # this line sets the status
        self.status = 'hello!'
        # however this line does not
        inputState.assignProperty(self, 'status', 'Move the rogue with 2, 4, 6, and 8')

        machine.setInitialState(inputState)
        machine.start()

        transition = MovementTransition(self)
        inputState.addTransition(transition)

        quitState = QState(machine)
        quitState.assignProperty(self, 'status', 'Really quit(y/n)?')

        yesTransition = QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_Y)
        self.finalState = QFinalState(machine)
        yesTransition.setTargetState(self.finalState)
        quitState.addTransition(yesTransition)

        noTransition = QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_N)
        noTransition.setTargetState(inputState)
        quitState.addTransition(noTransition)

        quitTransition = QKeyEventTransition(self, QEvent.KeyPress, Qt.Key_Q)
        quitTransition.setTargetState(quitState)
        inputState.addTransition(quitTransition)

        machine.setInitialState(inputState)
        machine.finished.connect(qApp.quit)
        machine.start()

    def sizeHint(self):
        metrics = QFontMetrics(self.font())
        return QSize(metrics.width('X') * self.width, metrics.height() * (self.height + 1))
    def paintEvent(self, event):
        metrics = QFontMetrics(self.font())
        painter = QPainter(self)
        fontHeight = metrics.height()
        fontWidth = metrics.width('X')

        painter.fillRect(self.rect(), Qt.black)
        painter.setPen(Qt.white)

        yPos = fontHeight
        painter.drawText(QPoint(0, yPos), self.status)
        for y in range(self.height):
            yPos += fontHeight
            xPos = 0
            for x in range(self.width):
                if y == self.pY and x == self.pX:
                    xPos += fontWidth
                    continue
                painter.drawText(QPoint(xPos, yPos), self.map[x][y])
                xPos += fontWidth
        painter.drawText(QPoint(self.pX * fontWidth, (self.pY + 2) * fontHeight), '@')
    def movePlayer(self, direction):
        if direction == self.Left:
            if self.map[self.pX - 1][self.pY] != '#':
                self.pX -= 1
        elif direction == self.Right:
            if self.map[self.pX + 1][self.pY] != '#':
                self.pX += 1
        elif direction == self.Up:
            if self.map[self.pX][self.pY - 1] != '#':
                self.pY -= 1
        elif direction == self.Down:
            if self.map[self.pX][self.pY + 1] != '#':
                self.pY += 1
        self.repaint()
    def getStatus(self):
        return self.statusStr
    def setStatus(self, status):
        self.statusStr = status
        self.repaint()
    status = Property(str, getStatus, setStatus)
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    Width = 35
    Height = 20

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
