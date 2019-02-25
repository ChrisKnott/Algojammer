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
from PySide2.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        button = QPushButton(self)
        button.setGeometry(QRect(100, 100, 100, 100))

        machine = QStateMachine(self)
        s1 = QState()
        s1.assignProperty(button, 'text', 'Outside')
        s2 = QState()
        s2.assignProperty(button, 'text', 'Inside')

        enterTransition = QEventTransition(button, QEvent.Enter)
        enterTransition.setTargetState(s2)
        s1.addTransition(enterTransition)

        leaveTransition = QEventTransition(button, QEvent.Leave)
        leaveTransition.setTargetState(s1)
        s2.addTransition(leaveTransition)

        s3 = QState()
        s3.assignProperty(button, 'text', 'Pressing...')

        pressTransition = QEventTransition(button, QEvent.MouseButtonPress)
        pressTransition.setTargetState(s3)
        s2.addTransition(pressTransition)

        releaseTransition = QEventTransition(button, QEvent.MouseButtonRelease)
        releaseTransition.setTargetState(s2)
        s3.addTransition(releaseTransition)

        machine.addState(s1)
        machine.addState(s2)
        machine.addState(s3)

        machine.setInitialState(s1)
        machine.start()

        self.setCentralWidget(button)
        self.show()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
