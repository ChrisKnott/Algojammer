#!/usr/bin/env python

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

"""PySide2 port of the Model Data example from Qt v5.x"""

import sys
from random import randrange

from PySide2.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import (QApplication, QGridLayout, QHeaderView,
    QTableView, QWidget)
from PySide2.QtCharts import QtCharts

class CustomTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.input_data = []
        self.mapping = {}
        self.column_count = 4
        self.row_count = 15

        for i in range(self.row_count):
            data_vec = [0]*self.column_count
            for k in range(len(data_vec)):
                if k % 2 == 0:
                    data_vec[k] = i * 50 + randrange(30)
                else:
                    data_vec[k] = randrange(100)
            self.input_data.append(data_vec)

    def rowCount(self, parent=QModelIndex()):
        return len(self.input_data)

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section % 2 == 0:
                return "x"
            else:
                return "y"
        else:
            return "{}".format(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for color, rect in self.mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(color)
            # cell not mapped return white color
            return QColor(Qt.white);
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.input_data[index.row()][index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def add_mapping(self, color, area):
        self.mapping[color] = area

    def clear_mapping(self):
        self.mapping = {}



class TableWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.model = CustomTableModel()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.chart = QtCharts.QChart()
        self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

        self.series = QtCharts.QLineSeries()
        self.series.setName("Line 1")
        self.mapper = QtCharts.QVXYModelMapper(self)
        self.mapper.setXColumn(0)
        self.mapper.setYColumn(1)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        # for storing color hex from the series
        seriesColorHex = "#000000"

        # get the color of the series and use it for showing the mapped area
        seriesColorHex = "{}".format(self.series.pen().color().name())
        self.model.add_mapping(seriesColorHex, QRect(0, 0, 2, self.model.rowCount()))

        # series 2
        self.series = QtCharts.QLineSeries()
        self.series.setName("Line 2")

        self.mapper = QtCharts.QVXYModelMapper(self)
        self.mapper.setXColumn(2)
        self.mapper.setYColumn(3)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        # get the color of the series and use it for showing the mapped area
        seriesColorHex = "{}".format(self.series.pen().color().name())
        self.model.add_mapping(seriesColorHex, QRect(2, 0, 2, self.model.rowCount()));

        self.chart.createDefaultAxes()
        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumSize(640, 480)

        # create main layout
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.table_view, 1, 0)
        self.main_layout.addWidget(self.chart_view, 1, 1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(0, 0)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TableWidget()
    w.show()
    sys.exit(app.exec_())
