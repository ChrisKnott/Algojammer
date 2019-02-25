#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
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


def createItem(minimum, preferred, maximum, name):
    w = QtWidgets.QGraphicsProxyWidget()

    w.setWidget(QtWidgets.QPushButton(name))
    w.setMinimumSize(minimum)
    w.setPreferredSize(preferred)
    w.setMaximumSize(maximum)
    w.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

    return w


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    scene = QtWidgets.QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 480)

    minSize = QtCore.QSizeF(30, 100)
    prefSize = QtCore.QSizeF(210, 100)
    maxSize = QtCore.QSizeF(300, 100)

    a = createItem(minSize, prefSize, maxSize, "A")
    b = createItem(minSize, prefSize, maxSize, "B")
    c = createItem(minSize, prefSize, maxSize, "C")
    d = createItem(minSize, prefSize, maxSize, "D")
    e = createItem(minSize, prefSize, maxSize, "E")
    f = createItem(QtCore.QSizeF(30, 50), QtCore.QSizeF(150, 50), maxSize, "F")
    g = createItem(QtCore.QSizeF(30, 50), QtCore.QSizeF(30, 100), maxSize, "G")

    l = QtWidgets.QGraphicsAnchorLayout()
    l.setSpacing(0)

    w = QtWidgets.QGraphicsWidget(None, QtCore.Qt.Window)
    w.setPos(20, 20)
    w.setLayout(l)

    # Vertical.
    l.addAnchor(a, QtCore.Qt.AnchorTop, l, QtCore.Qt.AnchorTop)
    l.addAnchor(b, QtCore.Qt.AnchorTop, l, QtCore.Qt.AnchorTop)

    l.addAnchor(c, QtCore.Qt.AnchorTop, a, QtCore.Qt.AnchorBottom)
    l.addAnchor(c, QtCore.Qt.AnchorTop, b, QtCore.Qt.AnchorBottom)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, d, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, e, QtCore.Qt.AnchorTop)

    l.addAnchor(d, QtCore.Qt.AnchorBottom, l, QtCore.Qt.AnchorBottom)
    l.addAnchor(e, QtCore.Qt.AnchorBottom, l, QtCore.Qt.AnchorBottom)

    l.addAnchor(c, QtCore.Qt.AnchorTop, f, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorVerticalCenter, f, QtCore.Qt.AnchorBottom)
    l.addAnchor(f, QtCore.Qt.AnchorBottom, g, QtCore.Qt.AnchorTop)
    l.addAnchor(c, QtCore.Qt.AnchorBottom, g, QtCore.Qt.AnchorBottom)

    # Horizontal.
    l.addAnchor(l, QtCore.Qt.AnchorLeft, a, QtCore.Qt.AnchorLeft)
    l.addAnchor(l, QtCore.Qt.AnchorLeft, d, QtCore.Qt.AnchorLeft)
    l.addAnchor(a, QtCore.Qt.AnchorRight, b, QtCore.Qt.AnchorLeft)

    l.addAnchor(a, QtCore.Qt.AnchorRight, c, QtCore.Qt.AnchorLeft)
    l.addAnchor(c, QtCore.Qt.AnchorRight, e, QtCore.Qt.AnchorLeft)

    l.addAnchor(b, QtCore.Qt.AnchorRight, l, QtCore.Qt.AnchorRight)
    l.addAnchor(e, QtCore.Qt.AnchorRight, l, QtCore.Qt.AnchorRight)
    l.addAnchor(d, QtCore.Qt.AnchorRight, e, QtCore.Qt.AnchorLeft)

    l.addAnchor(l, QtCore.Qt.AnchorLeft, f, QtCore.Qt.AnchorLeft)
    l.addAnchor(l, QtCore.Qt.AnchorLeft, g, QtCore.Qt.AnchorLeft)
    l.addAnchor(f, QtCore.Qt.AnchorRight, g, QtCore.Qt.AnchorRight)

    scene.addItem(w)
    scene.setBackgroundBrush(QtCore.Qt.darkGreen)

    view = QtWidgets.QGraphicsView(scene)
    view.show()

    sys.exit(app.exec_())
