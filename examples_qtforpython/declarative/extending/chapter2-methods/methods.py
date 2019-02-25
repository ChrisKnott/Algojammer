#!/usr/bin/python

#############################################################################
##
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

from __future__ import print_function

"""PySide2 port of the qml/tutorials/extending-qml/chapter2-methods example from Qt v5.x"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'utils'))
from utils import text_type

from PySide2.QtCore import Property, Signal, Slot, QUrl, Qt
from PySide2.QtGui import QGuiApplication, QPen, QPainter, QColor
from PySide2.QtQml import qmlRegisterType
from PySide2.QtQuick import QQuickPaintedItem, QQuickView

class PieChart (QQuickPaintedItem):
    def __init__(self, parent = None):
        QQuickPaintedItem.__init__(self, parent)
        self._name = u''

    def paint(self, painter):
        pen = QPen(self.color, 2)
        painter.setPen(pen);
        painter.setRenderHints(QPainter.Antialiasing, True);
        painter.drawPie(self.boundingRect().adjusted(1,1,-1,-1), 90 * 16, 290 * 16);

    def getColor(self):
        return self._color

    def setColor(self, value):
        self._color = value

    def getName(self):
        return self._name

    def setName(self, value):
        self._name = value

    color = Property(QColor, getColor, setColor)
    name = Property(text_type, getName, setName)
    chartCleared = Signal()

    @Slot() # This should be something like @Invokable
    def clearChart(self):
        self.setColor(Qt.transparent)
        self.update()
        self.chartCleared.emit()

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    qmlRegisterType(PieChart, 'Charts', 1, 0, 'PieChart');

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qmlFile = os.path.join(os.path.dirname(__file__), 'app.qml')
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qmlFile)))
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()
    res = app.exec_()
    # Deleting the view before it goes out of scope is required to make sure all child QML instances
    # are destroyed in the correct order.
    del view
    sys.exit(res)
