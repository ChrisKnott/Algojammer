#!/usr/bin/env python

############################################################################
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

"""PySide2 port of the widgets/layouts/dynamiclayouts example from Qt v5.x"""

from PySide2.QtCore import Qt, QSize
from PySide2.QtWidgets import (QApplication, QDialog, QLayout, QGridLayout,
                               QMessageBox, QGroupBox, QSpinBox, QSlider,
                               QProgressBar, QDial, QDialogButtonBox,
                               QComboBox, QLabel)

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.rotableWidgets = []

        self.createRotableGroupBox()
        self.createOptionsGroupBox()
        self.createButtonBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.rotableGroupBox, 0, 0)
        mainLayout.addWidget(self.optionsGroupBox, 1, 0)
        mainLayout.addWidget(self.buttonBox, 2, 0)
        mainLayout.setSizeConstraint(QLayout.SetMinimumSize)

        self.mainLayout = mainLayout
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Dynamic Layouts")

    def rotateWidgets(self):
        count = len(self.rotableWidgets)
        if count % 2 == 1:
            raise AssertionError("Number of widgets must be even")

        for widget in self.rotableWidgets:
            self.rotableLayout.removeWidget(widget)

        self.rotableWidgets.append(self.rotableWidgets.pop(0))

        for i in range(count//2):
            self.rotableLayout.addWidget(self.rotableWidgets[count - i - 1], 0, i)
            self.rotableLayout.addWidget(self.rotableWidgets[i], 1, i)


    def buttonsOrientationChanged(self, index):
        self.mainLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.setMinimumSize(0, 0)

        orientation = Qt.Orientation(int(self.buttonsOrientationComboBox.itemData(index)))

        if orientation == self.buttonBox.orientation():
            return

        self.mainLayout.removeWidget(self.buttonBox)

        spacing = self.mainLayout.spacing()

        oldSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing)
        self.buttonBox.setOrientation(orientation)
        newSizeHint = self.buttonBox.sizeHint() + QSize(spacing, spacing)

        if orientation == Qt.Horizontal:
            self.mainLayout.addWidget(self.buttonBox, 2, 0)
            self.resize(self.size() + QSize(-oldSizeHint.width(), newSizeHint.height()))
        else:
            self.mainLayout.addWidget(self.buttonBox, 0, 3, 2, 1)
            self.resize(self.size() + QSize(newSizeHint.width(), -oldSizeHint.height()))

        self.mainLayout.setSizeConstraint(QLayout.SetDefaultConstraint)

    def show_help(self):
        QMessageBox.information(self, "Dynamic Layouts Help",
                            "This example shows how to change layouts "
                            "dynamically.")

    def createRotableGroupBox(self):
        self.rotableGroupBox = QGroupBox("Rotable Widgets")

        self.rotableWidgets.append(QSpinBox())
        self.rotableWidgets.append(QSlider())
        self.rotableWidgets.append(QDial())
        self.rotableWidgets.append(QProgressBar())
        count = len(self.rotableWidgets)
        for i in range(count):
            self.rotableWidgets[i].valueChanged[int].\
                connect(self.rotableWidgets[(i+1) % count].setValue)

        self.rotableLayout = QGridLayout()
        self.rotableGroupBox.setLayout(self.rotableLayout)

        self.rotateWidgets()

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QGroupBox("Options")

        buttonsOrientationLabel = QLabel("Orientation of buttons:")

        buttonsOrientationComboBox = QComboBox()
        buttonsOrientationComboBox.addItem("Horizontal", Qt.Horizontal)
        buttonsOrientationComboBox.addItem("Vertical", Qt.Vertical)
        buttonsOrientationComboBox.currentIndexChanged[int].connect(self.buttonsOrientationChanged)

        self.buttonsOrientationComboBox = buttonsOrientationComboBox

        optionsLayout = QGridLayout()
        optionsLayout.addWidget(buttonsOrientationLabel, 0, 0)
        optionsLayout.addWidget(self.buttonsOrientationComboBox, 0, 1)
        optionsLayout.setColumnStretch(2, 1)
        self.optionsGroupBox.setLayout(optionsLayout)

    def createButtonBox(self):
        self.buttonBox = QDialogButtonBox()

        closeButton = self.buttonBox.addButton(QDialogButtonBox.Close)
        helpButton = self.buttonBox.addButton(QDialogButtonBox.Help)
        rotateWidgetsButton = self.buttonBox.addButton("Rotate &Widgets", QDialogButtonBox.ActionRole)

        rotateWidgetsButton.clicked.connect(self.rotateWidgets)
        closeButton.clicked.connect(self.close)
        helpButton.clicked.connect(self.show_help)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec_()
