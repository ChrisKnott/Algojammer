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

class PingEvent(QEvent):
    def __init__(self):
        super(PingEvent, self).__init__(QEvent.Type(QEvent.User+2))
class PongEvent(QEvent):
    def __init__(self):
        super(PongEvent, self).__init__(QEvent.Type(QEvent.User+3))

class Pinger(QState):
    def __init__(self, parent):
        super(Pinger, self).__init__(parent)
    def onEntry(self, e):
        self.p = PingEvent()
        self.machine().postEvent(self.p)
        print('ping?')

class PongTransition(QAbstractTransition):
    def eventTest(self, e):
        return e.type() == QEvent.User+3
    def onTransition(self, e):
        self.p = PingEvent()
        machine.postDelayedEvent(self.p, 500)
        print('ping?')
class PingTransition(QAbstractTransition):
    def eventTest(self, e):
        return e.type() == QEvent.User+2
    def onTransition(self, e):
        self.p = PongEvent()
        machine.postDelayedEvent(self.p, 500)
        print('pong!')

if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)

    machine = QStateMachine()
    group = QState(QState.ParallelStates)
    group.setObjectName('group')

    pinger = Pinger(group)
    pinger.setObjectName('pinger')
    pinger.addTransition(PongTransition())

    ponger = QState(group)
    ponger.setObjectName('ponger')
    ponger.addTransition(PingTransition())

    machine.addState(group)
    machine.setInitialState(group)
    machine.start()

    sys.exit(app.exec_())
