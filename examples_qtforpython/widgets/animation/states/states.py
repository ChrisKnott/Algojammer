#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
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

from PySide2 import QtCore, QtGui, QtWidgets

import states_rc


class Pixmap(QtWidgets.QGraphicsObject):
    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.p = QtGui.QPixmap(pix)

    def paint(self, painter, option, widget):
        painter.drawPixmap(QtCore.QPointF(), self.p)

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(self.p.size()))


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    # Text edit and button.
    edit = QtWidgets.QTextEdit()
    edit.setText("asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
                 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
                 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy "
                 "asdf lkjha yuoiqwe asd iuaysd u iasyd uiy!")

    button = QtWidgets.QPushButton()
    buttonProxy = QtWidgets.QGraphicsProxyWidget()
    buttonProxy.setWidget(button)
    editProxy = QtWidgets.QGraphicsProxyWidget()
    editProxy.setWidget(edit)

    box = QtWidgets.QGroupBox()
    box.setFlat(True)
    box.setTitle("Options")

    layout2 = QtWidgets.QVBoxLayout()
    box.setLayout(layout2)
    layout2.addWidget(QtWidgets.QRadioButton("Herring"))
    layout2.addWidget(QtWidgets.QRadioButton("Blue Parrot"))
    layout2.addWidget(QtWidgets.QRadioButton("Petunias"))
    layout2.addStretch()

    boxProxy = QtWidgets.QGraphicsProxyWidget()
    boxProxy.setWidget(box)

    # Parent widget.
    widget = QtWidgets.QGraphicsWidget()
    layout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical, widget)
    layout.addItem(editProxy)
    layout.addItem(buttonProxy)
    widget.setLayout(layout)

    p1 = Pixmap(QtGui.QPixmap(':/digikam.png'))
    p2 = Pixmap(QtGui.QPixmap(':/akregator.png'))
    p3 = Pixmap(QtGui.QPixmap(':/accessories-dictionary.png'))
    p4 = Pixmap(QtGui.QPixmap(':/k3b.png'))
    p5 = Pixmap(QtGui.QPixmap(':/help-browser.png'))
    p6 = Pixmap(QtGui.QPixmap(':/kchart.png'))

    scene = QtWidgets.QGraphicsScene(0, 0, 400, 300)
    scene.setBackgroundBrush(scene.palette().window())
    scene.addItem(widget)
    scene.addItem(boxProxy)
    scene.addItem(p1)
    scene.addItem(p2)
    scene.addItem(p3)
    scene.addItem(p4)
    scene.addItem(p5)
    scene.addItem(p6)

    machine = QtCore.QStateMachine()
    state1 = QtCore.QState(machine)
    state2 = QtCore.QState(machine)
    state3 = QtCore.QState(machine)
    machine.setInitialState(state1)

    # State 1.
    state1.assignProperty(button, 'text', "Switch to state 2")
    state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
    state1.assignProperty(box, 'geometry', QtCore.QRect(-200, 150, 200, 150))
    state1.assignProperty(p1, 'pos', QtCore.QPointF(68, 185))
    state1.assignProperty(p2, 'pos', QtCore.QPointF(168, 185))
    state1.assignProperty(p3, 'pos', QtCore.QPointF(268, 185))
    state1.assignProperty(p4, 'pos', QtCore.QPointF(68 - 150, 48 - 150))
    state1.assignProperty(p5, 'pos', QtCore.QPointF(168, 48 - 150))
    state1.assignProperty(p6, 'pos', QtCore.QPointF(268 + 150, 48 - 150))
    state1.assignProperty(p1, 'rotation', 0.0)
    state1.assignProperty(p2, 'rotation', 0.0)
    state1.assignProperty(p3, 'rotation', 0.0)
    state1.assignProperty(p4, 'rotation', -270.0)
    state1.assignProperty(p5, 'rotation', -90.0)
    state1.assignProperty(p6, 'rotation', 270.0)
    state1.assignProperty(boxProxy, 'opacity', 0.0)
    state1.assignProperty(p1, 'opacity', 1.0)
    state1.assignProperty(p2, 'opacity', 1.0)
    state1.assignProperty(p3, 'opacity', 1.0)
    state1.assignProperty(p4, 'opacity', 0.0)
    state1.assignProperty(p5, 'opacity', 0.0)
    state1.assignProperty(p6, 'opacity', 0.0)

    # State 2.
    state2.assignProperty(button, 'text', "Switch to state 3")
    state2.assignProperty(widget, 'geometry', QtCore.QRectF(200, 150, 200, 150))
    state2.assignProperty(box, 'geometry', QtCore.QRect(9, 150, 190, 150))
    state2.assignProperty(p1, 'pos', QtCore.QPointF(68 - 150, 185 + 150))
    state2.assignProperty(p2, 'pos', QtCore.QPointF(168, 185 + 150))
    state2.assignProperty(p3, 'pos', QtCore.QPointF(268 + 150, 185 + 150))
    state2.assignProperty(p4, 'pos', QtCore.QPointF(64, 48))
    state2.assignProperty(p5, 'pos', QtCore.QPointF(168, 48))
    state2.assignProperty(p6, 'pos', QtCore.QPointF(268, 48))
    state2.assignProperty(p1, 'rotation', -270.0)
    state2.assignProperty(p2, 'rotation', 90.0)
    state2.assignProperty(p3, 'rotation', 270.0)
    state2.assignProperty(p4, 'rotation', 0.0)
    state2.assignProperty(p5, 'rotation', 0.0)
    state2.assignProperty(p6, 'rotation', 0.0)
    state2.assignProperty(boxProxy, 'opacity', 1.0)
    state2.assignProperty(p1, 'opacity', 0.0)
    state2.assignProperty(p2, 'opacity', 0.0)
    state2.assignProperty(p3, 'opacity', 0.0)
    state2.assignProperty(p4, 'opacity', 1.0)
    state2.assignProperty(p5, 'opacity', 1.0)
    state2.assignProperty(p6, 'opacity', 1.0)

    # State 3.
    state3.assignProperty(button, 'text', "Switch to state 1")
    state3.assignProperty(p1, 'pos', QtCore.QPointF(0, 5))
    state3.assignProperty(p2, 'pos', QtCore.QPointF(0, 5 + 64 + 5))
    state3.assignProperty(p3, 'pos', QtCore.QPointF(5, 5 + (64 + 5) + 64))
    state3.assignProperty(p4, 'pos', QtCore.QPointF(5 + 64 + 5, 5))
    state3.assignProperty(p5, 'pos', QtCore.QPointF(5 + 64 + 5, 5 + 64 + 5))
    state3.assignProperty(p6, 'pos', QtCore.QPointF(5 + 64 + 5, 5 + (64 + 5) + 64))
    state3.assignProperty(widget, 'geometry', QtCore.QRectF(138, 5, 400 - 138, 200))
    state3.assignProperty(box, 'geometry', QtCore.QRect(5, 205, 400, 90))
    state3.assignProperty(p1, 'opacity', 1.0)
    state3.assignProperty(p2, 'opacity', 1.0)
    state3.assignProperty(p3, 'opacity', 1.0)
    state3.assignProperty(p4, 'opacity', 1.0)
    state3.assignProperty(p5, 'opacity', 1.0)
    state3.assignProperty(p6, 'opacity', 1.0)

    t1 = state1.addTransition(button.clicked, state2)
    animation1SubGroup = QtCore.QSequentialAnimationGroup()
    animation1SubGroup.addPause(250)
    animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, b'geometry', state1))
    t1.addAnimation(animation1SubGroup)
    t1.addAnimation(QtCore.QPropertyAnimation(widget, b'geometry', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p1, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p2, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p3, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p4, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p5, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p6, b'pos', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p1, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p2, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p3, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p4, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p5, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p6, b'rotation', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p1, b'opacity', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p2, b'opacity', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p3, b'opacity', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p4, b'opacity', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p5, b'opacity', state1))
    t1.addAnimation(QtCore.QPropertyAnimation(p6, b'opacity', state1))

    t2 = state2.addTransition(button.clicked, state3)
    t2.addAnimation(QtCore.QPropertyAnimation(box, b'geometry', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(widget, b'geometry', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p1, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p2, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p3, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p4, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p5, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p6, b'pos', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p1, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p2, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p3, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p4, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p5, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p6, b'rotation', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p1, b'opacity', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p2, b'opacity', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p3, b'opacity', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p4, b'opacity', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p5, b'opacity', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(p6, b'opacity', state2))

    t3 = state3.addTransition(button.clicked, state1)
    t3.addAnimation(QtCore.QPropertyAnimation(box, b'geometry', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(widget, b'geometry', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p1, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p2, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p3, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p4, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p5, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p6, b'pos', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p1, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p2, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p3, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p4, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p5, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p6, b'rotation', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p1, b'opacity', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p2, b'opacity', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p3, b'opacity', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p4, b'opacity', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p5, b'opacity', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(p6, b'opacity', state3))

    machine.start()

    view = QtWidgets.QGraphicsView(scene)
    view.show()

    sys.exit(app.exec_())
