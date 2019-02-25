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

"""PySide2 port of the charts/audio example from Qt v5.x"""

import os
import sys
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPointF, QRect, QSize
from PySide2.QtMultimedia import (QAudio, QAudioDeviceInfo, QAudioFormat,
        QAudioInput)
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox

sampleCount = 2000
resolution = 4

class MainWindow(QMainWindow):
    def __init__(self, device):
        super(MainWindow, self).__init__()

        self.series = QtCharts.QLineSeries()
        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series)
        self.axisX = QtCharts.QValueAxis()
        self.axisX.setRange(0, sampleCount)
        self.axisX.setLabelFormat("%g")
        self.axisX.setTitleText("Samples")
        self.axisY = QtCharts.QValueAxis()
        self.axisY.setRange(-1, 1)
        self.axisY.setTitleText("Audio level")
        self.chart.setAxisX(self.axisX, self.series)
        self.chart.setAxisY(self.axisY, self.series)
        self.chart.legend().hide()
        self.chart.setTitle("Data from the microphone ({})".format(device.deviceName()))

        formatAudio = QAudioFormat()
        formatAudio.setSampleRate(8000)
        formatAudio.setChannelCount(1)
        formatAudio.setSampleSize(8)
        formatAudio.setCodec("audio/pcm")
        formatAudio.setByteOrder(QAudioFormat.LittleEndian)
        formatAudio.setSampleType(QAudioFormat.UnSignedInt)

        self.audioInput = QAudioInput(device, formatAudio, self)
        self.ioDevice = self.audioInput.start()
        self.ioDevice.readyRead.connect(self._readyRead)

        self.chartView = QtCharts.QChartView(self.chart)
        self.setCentralWidget(self.chartView)

        self.buffer = [QPointF(x, 0) for x in range(sampleCount)]
        self.series.append(self.buffer)

    def closeEvent(self, event):
        if self.audioInput is not None:
            self.audioInput.stop()
        event.accept()

    def _readyRead(self):
        data = self.ioDevice.readAll()
        availableSamples = data.size() // resolution
        start = 0
        if (availableSamples < sampleCount):
            start = sampleCount - availableSamples
            for s in range(start):
                self.buffer[s].setY(self.buffer[s + availableSamples].y())

        dataIndex = 0
        for s in range(start, sampleCount):
            value = (ord(data[dataIndex]) - 128) / 128
            self.buffer[s].setY(value)
            dataIndex = dataIndex + resolution
        self.series.replace(self.buffer)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    inputDevice = QAudioDeviceInfo.defaultInputDevice()
    if (inputDevice.isNull()):
        QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)

    mainWin = MainWindow(inputDevice)
    mainWin.setWindowTitle("audio")
    availableGeometry = app.desktop().availableGeometry(mainWin)
    size = availableGeometry.height() * 3 / 4
    mainWin.resize(size, size)
    mainWin.show()
    sys.exit(app.exec_())
