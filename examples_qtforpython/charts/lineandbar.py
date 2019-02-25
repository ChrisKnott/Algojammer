#!/usr/bin/python

#############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
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

"""PySide2 port of the line/bar example from Qt v5.x"""

import sys
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCharts import QtCharts


class TestChart(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.set0 = QtCharts.QBarSet("Jane")
        self.set1 = QtCharts.QBarSet("John")
        self.set2 = QtCharts.QBarSet("Axel")
        self.set3 = QtCharts.QBarSet("Mary")
        self.set4 = QtCharts.QBarSet("Sam")

        self.set0.append([1, 2, 3, 4, 5, 6])
        self.set1.append([5, 0, 0, 4, 0, 7])
        self.set2.append([3, 5, 8, 13, 8, 5])
        self.set3.append([5, 6, 7, 3, 4, 5])
        self.set4.append([9, 7, 5, 3, 1, 2])

        self.barSeries = QtCharts.QBarSeries()
        self.barSeries.append(self.set0)
        self.barSeries.append(self.set1)
        self.barSeries.append(self.set2)
        self.barSeries.append(self.set3)
        self.barSeries.append(self.set4)

        self.lineSeries = QtCharts.QLineSeries()
        self.lineSeries.setName("trend")
        self.lineSeries.append(QPoint(0, 4))
        self.lineSeries.append(QPoint(1, 15))
        self.lineSeries.append(QPoint(2, 20))
        self.lineSeries.append(QPoint(3, 4))
        self.lineSeries.append(QPoint(4, 12))
        self.lineSeries.append(QPoint(5, 17))

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.barSeries)
        self.chart.addSeries(self.lineSeries)
        self.chart.setTitle("Line and barchart example")

        self.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        self.axisX = QtCharts.QBarCategoryAxis()
        self.axisX.append(self.categories)
        self.chart.setAxisX(self.axisX, self.lineSeries)
        self.chart.setAxisX(self.axisX, self.barSeries)
        self.axisX.setRange("Jan", "Jun")

        self.axisY = QtCharts.QValueAxis()
        self.chart.setAxisY(self.axisY, self.lineSeries)
        self.chart.setAxisY(self.axisY, self.barSeries)
        self.axisY.setRange(0, 20)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self.chartView)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TestChart()
    window.show()
    window.resize(440, 300)

    sys.exit(app.exec_())
