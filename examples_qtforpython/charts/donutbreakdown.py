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

"""PySide2 port of the Donut Chart Breakdown example from Qt v5.x"""


import sys
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QFont, QPainter
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCharts import QtCharts

class MainSlice(QtCharts.QPieSlice):
    def __init__(self, breakdown_series, parent=None):
        super(MainSlice, self).__init__(parent)

        self.breakdown_series = breakdown_series
        self.name = None

        self.percentageChanged.connect(self.update_label)

    def get_breakdown_series(self):
        return self.breakdown_series

    def setName(self, name):
        self.name = name

    def name(self):
        return self.name

    def update_label(self):
        self.setLabel("{} {:.2f}%".format(self.name,
            self.percentage() * 100))


class DonutBreakdownChart(QtCharts.QChart):
    def __init__(self, parent=None):
        super(DonutBreakdownChart, self).__init__(QtCharts.QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        self.main_series = QtCharts.QPieSeries()
        self.main_series.setPieSize(0.7)
        self.addSeries(self.main_series)

    def add_breakdown_series(self, breakdown_series, color):
        font = QFont("Arial", 8)

        # add breakdown series as a slice to center pie
        main_slice = MainSlice(breakdown_series)
        main_slice.setName(breakdown_series.name())
        main_slice.setValue(breakdown_series.sum())
        self.main_series.append(main_slice)

        # customize the slice
        main_slice.setBrush(color)
        main_slice.setLabelVisible()
        main_slice.setLabelColor(Qt.white)
        main_slice.setLabelPosition(QtCharts.QPieSlice.LabelInsideHorizontal)
        main_slice.setLabelFont(font)

        # position and customize the breakdown series
        breakdown_series.setPieSize(0.8)
        breakdown_series.setHoleSize(0.7)
        breakdown_series.setLabelsVisible()

        for pie_slice in breakdown_series.slices():
            color = QColor(color).lighter(115)
            pie_slice.setBrush(color)
            pie_slice.setLabelFont(font)

        # add the series to the chart
        self.addSeries(breakdown_series)

        # recalculate breakdown donut segments
        self.recalculate_angles()

        # update customize legend markers
        self.update_legend_markers()

    def recalculate_angles(self):
        angle = 0
        slices = self.main_series.slices();
        for pie_slice in slices:
            breakdown_series = pie_slice.get_breakdown_series()
            breakdown_series.setPieStartAngle(angle)
            angle += pie_slice.percentage() * 360.0 # full pie is 360.0
            breakdown_series.setPieEndAngle(angle)

    def update_legend_markers(self):
        # go through all markers
        for series in self.series():
            markers = self.legend().markers(series)
            for marker in markers:
                if series == self.main_series:
                    # hide markers from main series
                    marker.setVisible(False)
                else:
                    # modify markers from breakdown series
                    marker.setLabel("{} {:.2f}%".format(
                        marker.slice().label(),
                        marker.slice().percentage() * 100, 0))
                    marker.setFont(QFont("Arial", 8))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Graph is based on data of:
    #    'Total consumption of energy increased by 10 per cent in 2010'
    # Statistics Finland, 13 December 2011
    # http://www.stat.fi/til/ekul/2010/ekul_2010_2011-12-13_tie_001_en.html
    series1 = QtCharts.QPieSeries()
    series1.setName("Fossil fuels")
    series1.append("Oil", 353295)
    series1.append("Coal", 188500)
    series1.append("Natural gas", 148680)
    series1.append("Peat", 94545)

    series2 = QtCharts.QPieSeries()
    series2.setName("Renewables")
    series2.append("Wood fuels", 319663)
    series2.append("Hydro power", 45875)
    series2.append("Wind power", 1060)

    series3 = QtCharts.QPieSeries()
    series3.setName("Others")
    series3.append("Nuclear energy", 238789)
    series3.append("Import energy", 37802)
    series3.append("Other", 32441)

    donut_breakdown = DonutBreakdownChart()
    donut_breakdown.setAnimationOptions(QtCharts.QChart.AllAnimations)
    donut_breakdown.setTitle("Total consumption of energy in Finland 2010")
    donut_breakdown.legend().setAlignment(Qt.AlignRight)
    donut_breakdown.add_breakdown_series(series1, Qt.red)
    donut_breakdown.add_breakdown_series(series2, Qt.darkGreen)
    donut_breakdown.add_breakdown_series(series3, Qt.darkBlue)

    window = QMainWindow()
    chart_view = QtCharts.QChartView(donut_breakdown)
    chart_view.setRenderHint(QPainter.Antialiasing)
    window.setCentralWidget(chart_view)
    available_geometry = app.desktop().availableGeometry(window)
    size = available_geometry.height() * 0.75
    window.resize(size, size * 0.8)
    window.show()

    sys.exit(app.exec_())
