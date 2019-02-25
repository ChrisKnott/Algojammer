#!/usr/bin/python

#############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
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

"""PySide2 QtDataVisualization example"""

import os
import sys
from PySide2.QtCore import QRect, QSize, QProcess, Qt
from PySide2.QtGui import QGuiApplication, QScreen, QWindow
from PySide2.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget
from PySide2.QtDataVisualization import QtDataVisualization

def dataToBarDataRow(data):
    return list(QtDataVisualization.QBarDataItem(d) for d in data)

def dataToBarDataArray(data):
    return list(dataToBarDataRow(row) for row in data)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Qt DataVisualization 3D Bars')

        self.bars = QtDataVisualization.Q3DBars()

        self.columnAxis = QtDataVisualization.QCategory3DAxis()
        self.columnAxis.setTitle('Columns')
        self.columnAxis.setTitleVisible(True)
        self.columnAxis.setLabels(['Column1', 'Column2'])
        self.columnAxis.setLabelAutoRotation(30)

        self.rowAxis = QtDataVisualization.QCategory3DAxis()
        self.rowAxis.setTitle('Rows')
        self.rowAxis.setTitleVisible(True)
        self.rowAxis.setLabels(['Row1', 'Row2'])
        self.rowAxis.setLabelAutoRotation(30)

        self.valueAxis = QtDataVisualization.QValue3DAxis()
        self.valueAxis.setTitle('Values')
        self.valueAxis.setTitleVisible(True)
        self.valueAxis.setRange(0, 5)

        self.bars.setRowAxis(self.rowAxis)
        self.bars.setColumnAxis(self.columnAxis)
        self.bars.setValueAxis(self.valueAxis)

        self.series = QtDataVisualization.QBar3DSeries()
        self.arrayData = [[1, 2], [3, 4]]
        self.series.dataProxy().addRows(dataToBarDataArray(self.arrayData))

        self.bars.setPrimarySeries(self.series)

        self.container = QWidget.createWindowContainer(self.bars)

        if not self.bars.hasContext():
            print("Couldn't initialize the OpenGL context.")
            sys.exit(-1)

        camera = self.bars.scene().activeCamera()
        camera.setYRotation(22.5)

        geometry = QGuiApplication.primaryScreen().geometry()
        size = geometry.height() * 3 / 4
        self.container.setMinimumSize(size, size)

        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.setCentralWidget(self.container)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
