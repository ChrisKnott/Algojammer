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

"""PySide2 Charts example: Simple memory usage viewer"""

import os
import sys
from PySide2.QtCore import QRect, QSize, QProcess
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCharts import QtCharts

def runProcess(command, arguments):
    process = QProcess()
    process.start(command, arguments)
    process.waitForFinished()
    std_output = process.readAllStandardOutput().data().decode('utf-8')
    return std_output.split('\n')

def getMemoryUsage():
    result = []
    if sys.platform == 'win32':
        # Windows: Obtain memory usage in KB from 'tasklist'
        for line in runProcess('tasklist', [])[3:]:
            if len(line) >= 74:
                command = line[0:23].strip()
                if command.endswith('.exe'):
                    command = command[0:len(command) - 4]
                memoryUsage = float(line[64:74].strip().replace(',', '').replace('.', ''))
                legend = ''
                if memoryUsage > 10240:
                    legend = '{} {}M'.format(command, round(memoryUsage / 1024))
                else:
                    legend = '{} {}K'.format(command, round(memoryUsage))
                result.append([legend, memoryUsage])
    else:
        # Unix: Obtain memory usage percentage from 'ps'
        psOptions = ['-e', 'v']
        memoryColumn = 8
        commandColumn = 9
        if sys.platform == 'darwin':
            psOptions = ['-e', '-v']
            memoryColumn = 11
            commandColumn = 12
        for line in runProcess('ps', psOptions):
            tokens = line.split(None)
            if len(tokens) > commandColumn and "PID" not in tokens: # Percentage and command
                command = tokens[commandColumn]
                if not command.startswith('['):
                    command = os.path.basename(command)
                    memoryUsage = round(float(tokens[memoryColumn].replace(',', '.')))
                    legend = '{} {}%'.format(command, memoryUsage)
                    result.append([legend, memoryUsage])

    result.sort(key = lambda x: x[1], reverse=True)
    return result

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('Memory Usage')

        memoryUsage = getMemoryUsage()
        if len(memoryUsage) > 5:
            memoryUsage = memoryUsage[0:4]

        self.series = QtCharts.QPieSeries()
        for item in memoryUsage:
            self.series.append(item[0], item[1]);

        slice = self.series.slices()[0]
        slice.setExploded();
        slice.setLabelVisible();
        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.series);
        self.chartView = QtCharts.QChartView(self.chart)
        self.setCentralWidget(self.chartView)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    size = availableGeometry.height() * 3 / 4
    mainWin.resize(size, size)
    mainWin.show()
    sys.exit(app.exec_())
