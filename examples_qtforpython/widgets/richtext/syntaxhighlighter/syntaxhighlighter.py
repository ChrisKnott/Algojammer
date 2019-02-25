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

"""PySide2 port of the widgets/richtext/syntaxhighlighter example from Qt v5.x"""

import sys
import re
from PySide2 import QtCore, QtGui, QtWidgets

import syntaxhighlighter_rc


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.highlighter = Highlighter()

        self.setupFileMenu()
        self.setupEditor()

        self.setCentralWidget(self.editor)
        self.setWindowTitle(self.tr("Syntax Highlighter"))

    def newFile(self):
        self.editor.clear()

    def openFile(self, path=""):
        fileName = path

        if fileName=="":
            fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open File"), "",
                                                         "qmake Files (*.pro *.prf *.pri)")

        if fileName!="":
            inFile = QtCore.QFile(fileName)
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                self.editor.setPlainText(str(inFile.readAll()))

    def setupEditor(self):
        variableFormat = QtGui.QTextCharFormat()
        variableFormat.setFontWeight(QtGui.QFont.Bold)
        variableFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\\b[A-Z_]+\\b", variableFormat)

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setBackground(QtGui.QColor("#77ff77"))
        self.highlighter.addMapping("#[^\n]*", singleLineCommentFormat)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setBackground(QtCore.Qt.cyan)
        quotationFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\".*\"", quotationFormat)

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\\b[a-z0-9_]+\\(.*\\)", functionFormat)

        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.editor = QtWidgets.QTextEdit()
        self.editor.setFont(font)
        self.highlighter.addToDocument(self.editor.document())

    def setupFileMenu(self):
        fileMenu = QtWidgets.QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(fileMenu)

        newFileAct = QtWidgets.QAction(self.tr("&New..."), self)
        newFileAct.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+N", "File|New")))
        self.connect(newFileAct, QtCore.SIGNAL("triggered()"), self.newFile)
        fileMenu.addAction(newFileAct)

        openFileAct = QtWidgets.QAction(self.tr("&Open..."), self)
        openFileAct.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+O", "File|Open")))
        self.connect(openFileAct, QtCore.SIGNAL("triggered()"), self.openFile)
        fileMenu.addAction(openFileAct)

        fileMenu.addAction(self.tr("E&xit"), QtWidgets.qApp, QtCore.SLOT("quit()"),
                           QtGui.QKeySequence(self.tr("Ctrl+Q", "File|Exit")))


class Highlighter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)

        self.mappings = {}

    def addToDocument(self, doc):
        self.connect(doc, QtCore.SIGNAL("contentsChange(int, int, int)"), self.highlight)

    def addMapping(self, pattern, format):
        self.mappings[pattern] = format

    def highlight(self, position, removed, added):
        doc = self.sender()

        block = doc.findBlock(position)
        if not block.isValid():
            return

        if added > removed:
            endBlock = doc.findBlock(position + added)
        else:
            endBlock = block

        while block.isValid() and not (endBlock < block):
            self.highlightBlock(block)
            block = block.next()

    def highlightBlock(self, block):
        layout = block.layout()
        text = block.text()

        overrides = []

        for pattern in self.mappings:
            for m in re.finditer(pattern,text):
                range = QtGui.QTextLayout.FormatRange()
                s,e = m.span()
                range.start = s
                range.length = e-s
                range.format = self.mappings[pattern]
                overrides.append(range)

        layout.setAdditionalFormats(overrides)
        block.document().markContentsDirty(block.position(), block.length())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 512)
    window.show()
    window.openFile(":/examples/example")
    sys.exit(app.exec_())
