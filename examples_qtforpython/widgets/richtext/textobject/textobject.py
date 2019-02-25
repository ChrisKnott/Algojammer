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

"""PySide2 port of the widgets/richtext/textobject example from Qt v5.x"""

from PySide2 import QtCore, QtGui, QtWidgets, QtSvg


class SvgTextObject(QtCore.QObject, QtGui.QTextObjectInterface):

    def intrinsicSize(self, doc, posInDocument, format):
        renderer = QtSvg.QSvgRenderer(format.property(Window.SvgData).toByteArray())
        size = renderer.defaultSize()

        if size.height() > 25:
            size *= 25.0 / size.height()

        return QtCore.QSizeF(size)

    def drawObject(self, painter, rect, doc, posInDocument, format):
        renderer = QtSvg.QSvgRenderer(format.property(Window.SvgData).toByteArray())
        renderer.render(painter, rect)


class Window(QtWidgets.QWidget):

    SvgTextFormat = QtGui.QTextFormat.UserObject + 1

    SvgData = 1

    def __init__(self):
        super(Window, self).__init__()

        self.setupGui()
        self.setupTextObject()

        self.setWindowTitle(self.tr("Text Object Example"))

    def insertTextObject(self):
        fileName = self.fileNameLineEdit.text()
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QIODevice.ReadOnly):
            QtWidgets.QMessageBox.warning(self, self.tr("Error Opening File"),
                    self.tr("Could not open '%1'").arg(fileName))

        svgData = file.readAll()

        svgCharFormat = QtGui.QTextCharFormat()
        svgCharFormat.setObjectType(Window.SvgTextFormat)
        svgCharFormat.setProperty(Window.SvgData, svgData)

        cursor = self.textEdit.textCursor()
        cursor.insertText(u"\uFFFD", svgCharFormat)
        self.textEdit.setTextCursor(cursor)

    def setupTextObject(self):
        svgInterface = SvgTextObject(self)
        self.textEdit.document().documentLayout().registerHandler(Window.SvgTextFormat, svgInterface)

    def setupGui(self):
        fileNameLabel = QtWidgets.QLabel(self.tr("Svg File Name:"))
        self.fileNameLineEdit = QtWidgets.QLineEdit()
        insertTextObjectButton = QtWidgets.QPushButton(self.tr("Insert Image"))

        self.fileNameLineEdit.setText('./files/heart.svg')
        QtCore.QObject.connect(insertTextObjectButton, QtCore.SIGNAL('clicked()'), self.insertTextObject)

        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.addWidget(fileNameLabel)
        bottomLayout.addWidget(self.fileNameLineEdit)
        bottomLayout.addWidget(insertTextObjectButton)

        self.textEdit = QtWidgets.QTextEdit()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.textEdit)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
