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

"""PySide2 port of the widgets/tools/codecs example from Qt v5.x"""

from PySide2 import QtCore, QtGui, QtWidgets


def codec_name(codec):
    try:
        # Python v3.
        name = str(codec.name(), encoding='ascii')
    except TypeError:
        # Python v2.
        name = str(codec.name())

    return name


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.setCentralWidget(self.textEdit)

        self.codecs = []
        self.findCodecs()

        self.previewForm = PreviewForm(self)
        self.previewForm.setCodecList(self.codecs)

        self.saveAsActs = []
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Codecs")
        self.resize(500, 400)

    def open(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if fileName:
            inFile = QtCore.QFile(fileName)
            if not inFile.open(QtCore.QFile.ReadOnly):
                QtWidgets.QMessageBox.warning(self, "Codecs",
                        "Cannot read file %s:\n%s" % (fileName, inFile.errorString()))
                return

            data = inFile.readAll()

            self.previewForm.setEncodedData(data)
            if self.previewForm.exec_():
                self.textEdit.setPlainText(self.previewForm.decodedString())

    def save(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self)
        if fileName:
            outFile = QtCore.QFile(fileName)
            if not outFile.open(QtCore.QFile.WriteOnly|QtCore.QFile.Text):
                QtWidgets.QMessageBox.warning(self, "Codecs",
                        "Cannot write file %s:\n%s" % (fileName, outFile.errorString()))
                return

            action = self.sender()
            codecName = action.data()

            out = QtCore.QTextStream(outFile)
            out.setCodec(codecName)
            out << self.textEdit.toPlainText()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Codecs",
                "The <b>Codecs</b> example demonstrates how to read and "
                "write files using various encodings.")

    def aboutToShowSaveAsMenu(self):
        currentText = self.textEdit.toPlainText()

        for action in self.saveAsActs:
            codecName = str(action.data())
            codec = QtCore.QTextCodec.codecForName(codecName)
            action.setVisible(codec and codec.canEncode(currentText))

    def findCodecs(self):
        codecMap = []
        iso8859RegExp = QtCore.QRegExp('ISO[- ]8859-([0-9]+).*')

        for mib in QtCore.QTextCodec.availableMibs():
            codec = QtCore.QTextCodec.codecForMib(mib)
            sortKey = codec_name(codec).upper()
            rank = 0

            if sortKey.startswith('UTF-8'):
                rank = 1
            elif sortKey.startswith('UTF-16'):
                rank = 2
            elif iso8859RegExp.exactMatch(sortKey):
                if len(iso8859RegExp.cap(1)) == 1:
                    rank = 3
                else:
                    rank = 4
            else:
                rank = 5

            codecMap.append((str(rank) + sortKey, codec))

        codecMap.sort()
        self.codecs = [item[-1] for item in codecMap]

    def createActions(self):
        self.openAct = QtWidgets.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        for codec in self.codecs:
            name = codec_name(codec)

            action = QtWidgets.QAction(name + '...', self, triggered=self.save)
            action.setData(name)
            self.saveAsActs.append(action)

        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtWidgets.QAction("About &Qt", self,
                triggered=QtWidgets.qApp.aboutQt)

    def createMenus(self):
        self.saveAsMenu = QtWidgets.QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.saveAsMenu.aboutToShow.connect(self.aboutToShowSaveAsMenu)

        self.fileMenu = QtWidgets.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addMenu(self.saveAsMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QtWidgets.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.helpMenu)


class PreviewForm(QtWidgets.QDialog):
    def __init__(self, parent):
        super(PreviewForm, self).__init__(parent)

        self.encodingComboBox = QtWidgets.QComboBox()
        encodingLabel = QtWidgets.QLabel("&Encoding:")
        encodingLabel.setBuddy(self.encodingComboBox)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        self.encodingComboBox.activated.connect(self.updateTextEdit)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(encodingLabel, 0, 0)
        mainLayout.addWidget(self.encodingComboBox, 0, 1)
        mainLayout.addWidget(self.textEdit, 1, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 2, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Choose Encoding")
        self.resize(400, 300)

    def setCodecList(self, codecs):
        self.encodingComboBox.clear()
        for codec in codecs:
            self.encodingComboBox.addItem(codec_name(codec), codec.mibEnum())

    def setEncodedData(self, data):
        self.encodedData = data
        self.updateTextEdit()

    def decodedString(self):
        return self.decodedStr

    def updateTextEdit(self):
        mib = self.encodingComboBox.itemData(self.encodingComboBox.currentIndex())
        codec = QtCore.QTextCodec.codecForMib(mib)

        data = QtCore.QTextStream(self.encodedData)
        data.setAutoDetectUnicode(False)
        data.setCodec(codec)

        self.decodedStr = data.readAll()
        self.textEdit.setPlainText(self.decodedStr)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
