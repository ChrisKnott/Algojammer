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

"""PySide2 port of the Legend example from Qt v5.x"""

import sys
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QBrush, QColor, QPainter, QPen
from PySide2.QtWidgets import (QApplication, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QPushButton, QWidget)
from PySide2.QtCharts import QtCharts

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.chart = QtCharts.QChart()
        self.series = QtCharts.QBarSeries()

        self.main_layout = QGridLayout()
        self.button_layout = QGridLayout()
        self.font_layout = QFormLayout()

        self.font_size = QDoubleSpinBox()

        self.legend_posx = QDoubleSpinBox()
        self.legend_posy = QDoubleSpinBox()
        self.legend_width = QDoubleSpinBox()
        self.legend_height = QDoubleSpinBox()

        self.detach_legend_button = QPushButton("Toggle attached")
        self.detach_legend_button.clicked.connect(self.toggle_attached)
        self.button_layout.addWidget(self.detach_legend_button, 0, 0)

        self.add_set_button = QPushButton("add barset")
        self.add_set_button.clicked.connect(self.add_barset)
        self.button_layout.addWidget(self.add_set_button, 2, 0)

        self.remove_barset_button = QPushButton("remove barset")
        self.remove_barset_button.clicked.connect(self.remove_barset)
        self.button_layout.addWidget(self.remove_barset_button, 3, 0)

        self.align_button = QPushButton("Align (Bottom)")
        self.align_button.clicked.connect(self.set_legend_alignment)
        self.button_layout.addWidget(self.align_button, 4, 0)

        self.bold_button = QPushButton("Toggle bold")
        self.bold_button.clicked.connect(self.toggle_bold)
        self.button_layout.addWidget(self.bold_button, 8, 0)

        self.italic_button = QPushButton("Toggle italic")
        self.italic_button.clicked.connect(self.toggle_italic)
        self.button_layout.addWidget(self.italic_button, 9, 0)

        self.legend_posx.valueChanged.connect(self.update_legend_layout)
        self.legend_posy.valueChanged.connect(self.update_legend_layout)
        self.legend_width.valueChanged.connect(self.update_legend_layout)
        self.legend_height.valueChanged.connect(self.update_legend_layout)

        legend_layout = QFormLayout()
        legend_layout.addRow("HPos", self.legend_posx)
        legend_layout.addRow("VPos", self.legend_posy)
        legend_layout.addRow("Width", self.legend_width)
        legend_layout.addRow("Height", self.legend_height)

        self.legend_settings = QGroupBox("Detached legend")
        self.legend_settings.setLayout(legend_layout)
        self.button_layout.addWidget(self.legend_settings)
        self.legend_settings.setVisible(False)

        # Create chart view with the chart
        self.chart_view = QtCharts.QChartView(self.chart, self)

        # Create spinbox to modify font size
        self.font_size.setValue(self.chart.legend().font().pointSizeF())
        self.font_size.valueChanged.connect(self.font_size_changed)

        self.font_layout.addRow("Legend font size", self.font_size)

        # Create layout for grid and detached legend
        self.main_layout.addLayout(self.button_layout, 0, 0)
        self.main_layout.addLayout(self.font_layout, 1, 0)
        self.main_layout.addWidget(self.chart_view, 0, 1, 3, 1)
        self.setLayout(self.main_layout)

        self.create_series()

    def create_series(self):
        self.add_barset()
        self.add_barset()
        self.add_barset()
        self.add_barset()

        self.chart.addSeries(self.series)
        self.chart.setTitle("Legend detach example")
        self.chart.createDefaultAxes()

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view.setRenderHint(QPainter.Antialiasing)

    def show_legend_spinbox(self):
        self.legend_settings.setVisible(True)
        chart_viewrect = self.chart_view.rect()

        self.legend_posx.setMinimum(0)
        self.legend_posx.setMaximum(chart_viewrect.width())
        self.legend_posx.setValue(150)

        self.legend_posy.setMinimum(0)
        self.legend_posy.setMaximum(chart_viewrect.height())
        self.legend_posy.setValue(150)

        self.legend_width.setMinimum(0)
        self.legend_width.setMaximum(chart_viewrect.width())
        self.legend_width.setValue(150)

        self.legend_height.setMinimum(0)
        self.legend_height.setMaximum(chart_viewrect.height())
        self.legend_height.setValue(75)

    def hideLegendSpinbox(self):
        self.legend_settings.setVisible(False)

    def toggle_attached(self):
        legend = self.chart.legend()
        if legend.isAttachedToChart():
            legend.detachFromChart()
            legend.setBackgroundVisible(True)
            legend.setBrush(QBrush(QColor(128, 128, 128, 128)))
            legend.setPen(QPen(QColor(192, 192, 192, 192)))

            self.show_legend_spinbox()
            self.update_legend_layout()
        else:
            legend.attachToChart()
            legend.setBackgroundVisible(False)
            self.hideLegendSpinbox()
        self.update()

    def add_barset(self):
        series_count = self.series.count()
        bar_set = QtCharts.QBarSet("set {}".format(series_count))
        delta = series_count * 0.1
        bar_set.append([1 + delta, 2 + delta, 3 + delta, 4 + delta])
        self.series.append(bar_set)

    def remove_barset(self):
        sets = self.series.barSets()
        len_sets = len(sets)
        if len_sets > 0:
            self.series.remove(sets[len_sets - 1])

    def set_legend_alignment(self):
        button = self.sender()
        legend = self.chart.legend()
        alignment = legend.alignment()

        if alignment == Qt.AlignTop:
            legend.setAlignment(Qt.AlignLeft)
            if button:
                button.setText("Align (Left)")
        elif alignment == Qt.AlignLeft:
            legend.setAlignment(Qt.AlignBottom)
            if button:
                button.setText("Align (Bottom)")
        elif alignment == Qt.AlignBottom:
            legend.setAlignment(Qt.AlignRight)
            if button:
                button.setText("Align (Right)")
        else:
            if button:
                button.setText("Align (Top)")
            legend.setAlignment(Qt.AlignTop)

    def toggle_bold(self):
        legend = self.chart.legend()
        font = legend.font()
        font.setBold(not font.bold())
        legend.setFont(font)

    def toggle_italic(self):
        legend = self.chart.legend()
        font = legend.font()
        font.setItalic(not font.italic())
        legend.setFont(font)

    def font_size_changed(self):
        legend = self.chart.legend()
        font = legend.font()
        font_size  = self.font_size.value()
        if font_size < 1:
            font_size = 1
        font.setPointSizeF(font_size)
        legend.setFont(font)

    def update_legend_layout(self):
        legend = self.chart.legend()

        rect = QRectF(self.legend_posx.value(),
            self.legend_posy.value(),
            self.legend_width.value(),
            self.legend_height.value())
        legend.setGeometry(rect)

        legend.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWidget()
    available_geometry = app.desktop().availableGeometry(w)
    size = available_geometry.height() * 0.75
    w.setFixedSize(size, size)
    w.show()
    sys.exit(app.exec_())
