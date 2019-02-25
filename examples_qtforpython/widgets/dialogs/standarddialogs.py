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

"""PySide2 port of the widgets/dialogs/standarddialogs example from Qt v5.x"""

import sys
from PySide2 import QtCore, QtGui, QtWidgets


class Dialog(QtWidgets.QDialog):
    MESSAGE = "<p>Message boxes have a caption, a text, and up to three " \
            "buttons, each with standard or custom texts.</p>" \
            "<p>Click a button to close the message box. Pressing the Esc " \
            "button will activate the detected escape button (if any).</p>"

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.openFilesPath = ''

        self.errorMessageDialog = QtWidgets.QErrorMessage(self)

        frameStyle = QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel

        self.integerLabel = QtWidgets.QLabel()
        self.integerLabel.setFrameStyle(frameStyle)
        self.integerButton = QtWidgets.QPushButton("QInputDialog.get&Integer()")

        self.doubleLabel = QtWidgets.QLabel()
        self.doubleLabel.setFrameStyle(frameStyle)
        self.doubleButton = QtWidgets.QPushButton("QInputDialog.get&Double()")

        self.itemLabel = QtWidgets.QLabel()
        self.itemLabel.setFrameStyle(frameStyle)
        self.itemButton = QtWidgets.QPushButton("QInputDialog.getIte&m()")

        self.textLabel = QtWidgets.QLabel()
        self.textLabel.setFrameStyle(frameStyle)
        self.textButton = QtWidgets.QPushButton("QInputDialog.get&Text()")

        self.colorLabel = QtWidgets.QLabel()
        self.colorLabel.setFrameStyle(frameStyle)
        self.colorButton = QtWidgets.QPushButton("QColorDialog.get&Color()")

        self.fontLabel = QtWidgets.QLabel()
        self.fontLabel.setFrameStyle(frameStyle)
        self.fontButton = QtWidgets.QPushButton("QFontDialog.get&Font()")

        self.directoryLabel = QtWidgets.QLabel()
        self.directoryLabel.setFrameStyle(frameStyle)
        self.directoryButton = QtWidgets.QPushButton("QFileDialog.getE&xistingDirectory()")

        self.openFileNameLabel = QtWidgets.QLabel()
        self.openFileNameLabel.setFrameStyle(frameStyle)
        self.openFileNameButton = QtWidgets.QPushButton("QFileDialog.get&OpenFileName()")

        self.openFileNamesLabel = QtWidgets.QLabel()
        self.openFileNamesLabel.setFrameStyle(frameStyle)
        self.openFileNamesButton = QtWidgets.QPushButton("QFileDialog.&getOpenFileNames()")

        self.saveFileNameLabel = QtWidgets.QLabel()
        self.saveFileNameLabel.setFrameStyle(frameStyle)
        self.saveFileNameButton = QtWidgets.QPushButton("QFileDialog.get&SaveFileName()")

        self.criticalLabel = QtWidgets.QLabel()
        self.criticalLabel.setFrameStyle(frameStyle)
        self.criticalButton = QtWidgets.QPushButton("QMessageBox.critica&l()")

        self.informationLabel = QtWidgets.QLabel()
        self.informationLabel.setFrameStyle(frameStyle)
        self.informationButton = QtWidgets.QPushButton("QMessageBox.i&nformation()")

        self.questionLabel = QtWidgets.QLabel()
        self.questionLabel.setFrameStyle(frameStyle)
        self.questionButton = QtWidgets.QPushButton("QMessageBox.&question()")

        self.warningLabel = QtWidgets.QLabel()
        self.warningLabel.setFrameStyle(frameStyle)
        self.warningButton = QtWidgets.QPushButton("QMessageBox.&warning()")

        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.setFrameStyle(frameStyle)
        self.errorButton = QtWidgets.QPushButton("QErrorMessage.show&M&essage()")

        self.integerButton.clicked.connect(self.setInteger)
        self.doubleButton.clicked.connect(self.setDouble)
        self.itemButton.clicked.connect(self.setItem)
        self.textButton.clicked.connect(self.setText)
        self.colorButton.clicked.connect(self.setColor)
        self.fontButton.clicked.connect(self.setFont)
        self.directoryButton.clicked.connect(self.setExistingDirectory)
        self.openFileNameButton.clicked.connect(self.setOpenFileName)
        self.openFileNamesButton.clicked.connect(self.setOpenFileNames)
        self.saveFileNameButton.clicked.connect(self.setSaveFileName)
        self.criticalButton.clicked.connect(self.criticalMessage)
        self.informationButton.clicked.connect(self.informationMessage)
        self.questionButton.clicked.connect(self.questionMessage)
        self.warningButton.clicked.connect(self.warningMessage)
        self.errorButton.clicked.connect(self.errorMessage)

        self.native = QtWidgets.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)
        layout.addWidget(self.integerButton, 0, 0)
        layout.addWidget(self.integerLabel, 0, 1)
        layout.addWidget(self.doubleButton, 1, 0)
        layout.addWidget(self.doubleLabel, 1, 1)
        layout.addWidget(self.itemButton, 2, 0)
        layout.addWidget(self.itemLabel, 2, 1)
        layout.addWidget(self.textButton, 3, 0)
        layout.addWidget(self.textLabel, 3, 1)
        layout.addWidget(self.colorButton, 4, 0)
        layout.addWidget(self.colorLabel, 4, 1)
        layout.addWidget(self.fontButton, 5, 0)
        layout.addWidget(self.fontLabel, 5, 1)
        layout.addWidget(self.directoryButton, 6, 0)
        layout.addWidget(self.directoryLabel, 6, 1)
        layout.addWidget(self.openFileNameButton, 7, 0)
        layout.addWidget(self.openFileNameLabel, 7, 1)
        layout.addWidget(self.openFileNamesButton, 8, 0)
        layout.addWidget(self.openFileNamesLabel, 8, 1)
        layout.addWidget(self.saveFileNameButton, 9, 0)
        layout.addWidget(self.saveFileNameLabel, 9, 1)
        layout.addWidget(self.criticalButton, 10, 0)
        layout.addWidget(self.criticalLabel, 10, 1)
        layout.addWidget(self.informationButton, 11, 0)
        layout.addWidget(self.informationLabel, 11, 1)
        layout.addWidget(self.questionButton, 12, 0)
        layout.addWidget(self.questionLabel, 12, 1)
        layout.addWidget(self.warningButton, 13, 0)
        layout.addWidget(self.warningLabel, 13, 1)
        layout.addWidget(self.errorButton, 14, 0)
        layout.addWidget(self.errorLabel, 14, 1)
        layout.addWidget(self.native, 15, 0)
        self.setLayout(layout)

        self.setWindowTitle("Standard Dialogs")

    def setInteger(self):
        i, ok = QtWidgets.QInputDialog.getInt(self,
                "QInputDialog.getInteger()", "Percentage:", 25, 0, 100, 1)
        if ok:
            self.integerLabel.setText("%d%%" % i)

    def setDouble(self):
        d, ok = QtWidgets.QInputDialog.getDouble(self, "QInputDialog.getDouble()",
                "Amount:", 37.56, -10000, 10000, 2)
        if ok:
            self.doubleLabel.setText("$%g" % d)

    def setItem(self):
        items = ("Spring", "Summer", "Fall", "Winter")

        item, ok = QtWidgets.QInputDialog.getItem(self, "QInputDialog.getItem()",
                "Season:", items, 0, False)
        if ok and item:
            self.itemLabel.setText(item)

    def setText(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "QInputDialog.getText()",
                "User name:", QtWidgets.QLineEdit.Normal,
                QtCore.QDir.home().dirName())
        if ok and text != '':
            self.textLabel.setText(text)

    def setColor(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.green, self)
        if color.isValid():
            self.colorLabel.setText(color.name())
            self.colorLabel.setPalette(QtGui.QPalette(color))
            self.colorLabel.setAutoFillBackground(True)

    def setFont(self):
        font, ok = QtWidgets.QFontDialog.getFont(QtGui.QFont(self.fontLabel.text()), self)
        if ok:
            self.fontLabel.setText(font.key())
            self.fontLabel.setFont(font)

    def setExistingDirectory(self):
        options = QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                "QFileDialog.getExistingDirectory()",
                self.directoryLabel.text(), options)
        if directory:
            self.directoryLabel.setText(directory)

    def setOpenFileName(self):
        options = QtWidgets.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, filtr = QtWidgets.QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()",
                self.openFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)", "", options)
        if fileName:
            self.openFileNameLabel.setText(fileName)

    def setOpenFileNames(self):
        options = QtWidgets.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
        files, filtr = QtWidgets.QFileDialog.getOpenFileNames(self,
                "QFileDialog.getOpenFileNames()", self.openFilesPath,
                "All Files (*);;Text Files (*.txt)", "", options)
        if files:
            self.openFilesPath = files[0]
            self.openFileNamesLabel.setText("[%s]" % ', '.join(files))

    def setSaveFileName(self):
        options = QtWidgets.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, filtr = QtWidgets.QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",
                self.saveFileNameLabel.text(),
                "All Files (*);;Text Files (*.txt)", "", options)
        if fileName:
            self.saveFileNameLabel.setText(fileName)

    def criticalMessage(self):
        reply = QtWidgets.QMessageBox.critical(self, "QMessageBox.critical()",
                Dialog.MESSAGE,
                QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Ignore)
        if reply == QtWidgets.QMessageBox.Abort:
            self.criticalLabel.setText("Abort")
        elif reply == QtWidgets.QMessageBox.Retry:
            self.criticalLabel.setText("Retry")
        else:
            self.criticalLabel.setText("Ignore")

    def informationMessage(self):
        reply = QtWidgets.QMessageBox.information(self,
                "QMessageBox.information()", Dialog.MESSAGE)
        if reply == QtWidgets.QMessageBox.Ok:
            self.informationLabel.setText("OK")
        else:
            self.informationLabel.setText("Escape")

    def questionMessage(self):
        reply = QtWidgets.QMessageBox.question(self, "QMessageBox.question()",
                Dialog.MESSAGE,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            self.questionLabel.setText("Yes")
        elif reply == QtWidgets.QMessageBox.No:
            self.questionLabel.setText("No")
        else:
            self.questionLabel.setText("Cancel")

    def warningMessage(self):
        msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                "QMessageBox.warning()", Dialog.MESSAGE,
                QtWidgets.QMessageBox.NoButton, self)
        msgBox.addButton("Save &Again", QtWidgets.QMessageBox.AcceptRole)
        msgBox.addButton("&Continue", QtWidgets.QMessageBox.RejectRole)
        if msgBox.exec_() == QtWidgets.QMessageBox.AcceptRole:
            self.warningLabel.setText("Save Again")
        else:
            self.warningLabel.setText("Continue")

    def errorMessage(self):
        self.errorMessageDialog.showMessage("This dialog shows and remembers "
                "error messages. If the checkbox is checked (as it is by "
                "default), the shown message will be shown again, but if the "
                "user unchecks the box the message will not appear again if "
                "QErrorMessage.showMessage() is called with the same message.")
        self.errorLabel.setText("If the box is unchecked, the message won't "
                "appear again.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())
