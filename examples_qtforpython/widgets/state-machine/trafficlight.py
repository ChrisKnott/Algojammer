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

class LightWidget(QWidget):
    def __init__(self, color):
        super(LightWidget, self).__init__()
        self.color = color
        self.onVal = False
    def isOn(self):
        return self.onVal
    def setOn(self, on):
        if self.onVal == on:
            return
        self.onVal = on
        self.update()
    @Slot()
    def turnOff(self):
        self.setOn(False)
    @Slot()
    def turnOn(self):
        self.setOn(True)
    def paintEvent(self, e):
        if not self.onVal:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 0, self.width(), self.height())

    on = Property(bool, isOn, setOn)

class TrafficLightWidget(QWidget):
    def __init__(self):
        super(TrafficLightWidget, self).__init__()
        vbox = QVBoxLayout(self)
        self.redLight = LightWidget(Qt.red)
        vbox.addWidget(self.redLight)
        self.yellowLight = LightWidget(Qt.yellow)
        vbox.addWidget(self.yellowLight)
        self.greenLight = LightWidget(Qt.green)
        vbox.addWidget(self.greenLight)
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setPalette(pal)
        self.setAutoFillBackground(True)

def createLightState(light, duration, parent=None):
    lightState = QState(parent)
    timer = QTimer(lightState)
    timer.setInterval(duration)
    timer.setSingleShot(True)
    timing = QState(lightState)
    timing.entered.connect(light.turnOn)
    timing.entered.connect(timer.start)
    timing.exited.connect(light.turnOff)
    done = QFinalState(lightState)
    timing.addTransition(timer, SIGNAL('timeout()'), done)
    lightState.setInitialState(timing)
    return lightState

class TrafficLight(QWidget):
    def __init__(self):
        super(TrafficLight, self).__init__()
        vbox = QVBoxLayout(self)
        widget = TrafficLightWidget()
        vbox.addWidget(widget)
        vbox.setContentsMargins(0, 0, 0, 0)

        machine = QStateMachine(self)
        redGoingYellow = createLightState(widget.redLight, 1000)
        redGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen = createLightState(widget.redLight, 1000)
        yellowGoingGreen.setObjectName('redGoingYellow')
        redGoingYellow.addTransition(redGoingYellow, SIGNAL('finished()'), yellowGoingGreen)
        greenGoingYellow = createLightState(widget.yellowLight, 3000)
        greenGoingYellow.setObjectName('redGoingYellow')
        yellowGoingGreen.addTransition(yellowGoingGreen, SIGNAL('finished()'), greenGoingYellow)
        yellowGoingRed = createLightState(widget.greenLight, 1000)
        yellowGoingRed.setObjectName('redGoingYellow')
        greenGoingYellow.addTransition(greenGoingYellow, SIGNAL('finished()'), yellowGoingRed)
        yellowGoingRed.addTransition(yellowGoingRed, SIGNAL('finished()'), redGoingYellow)

        machine.addState(redGoingYellow)
        machine.addState(yellowGoingGreen)
        machine.addState(greenGoingYellow)
        machine.addState(yellowGoingRed)
        machine.setInitialState(redGoingYellow)
        machine.start()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = TrafficLight()
    widget.resize(110, 300)
    widget.show()
    sys.exit(app.exec_())
