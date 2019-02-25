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

from PySide2 import QtCore, QtGui, QtWidgets, QtXmlPatterns

import schema_rc
from ui_schema import Ui_SchemaMainWindow


try:
    # Python v2.
    unicode

    def encode_utf8(ba):
        return unicode(ba, encoding='utf8')

    def decode_utf8(qs):
        return QtCore.QByteArray(str(qs))

except NameError:
    # Python v3.

    def encode_utf8(ba):
        return str(ba.data(), encoding='utf8')

    def decode_utf8(qs):
        return QtCore.QByteArray(bytes(qs, encoding='utf8'))


class XmlSyntaxHighlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(XmlSyntaxHighlighter, self).__init__(parent)

        self.highlightingRules = []

        # Tag format.
        format = QtGui.QTextCharFormat()
        format.setForeground(QtCore.Qt.darkBlue)
        format.setFontWeight(QtGui.QFont.Bold)
        pattern = QtCore.QRegExp("(<[a-zA-Z:]+\\b|<\\?[a-zA-Z:]+\\b|\\?>|>|/>|</[a-zA-Z:]+>)")
        self.highlightingRules.append((pattern, format))

        # Attribute format.
        format = QtGui.QTextCharFormat()
        format.setForeground(QtCore.Qt.darkGreen)
        pattern = QtCore.QRegExp("[a-zA-Z:]+=")
        self.highlightingRules.append((pattern, format))

        # Attribute content format.
        format = QtGui.QTextCharFormat()
        format.setForeground(QtCore.Qt.red)
        pattern = QtCore.QRegExp("(\"[^\"]*\"|'[^']*')")
        self.highlightingRules.append((pattern, format))

        # Comment format.
        self.commentFormat = QtGui.QTextCharFormat()
        self.commentFormat.setForeground(QtCore.Qt.lightGray)
        self.commentFormat.setFontItalic(True)

        self.commentStartExpression = QtCore.QRegExp("<!--")
        self.commentEndExpression = QtCore.QRegExp("-->")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = text.length() - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.commentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength)


class MessageHandler(QtXmlPatterns.QAbstractMessageHandler):

    def __init__(self):
        super(MessageHandler, self).__init__()

        self.m_description = ""
        self.m_sourceLocation = QtXmlPatterns.QSourceLocation()

    def statusMessage(self):
        return self.m_description

    def line(self):
        return self.m_sourceLocation.line()

    def column(self):
        return self.m_sourceLocation.column()

    def handleMessage(self, type, description, identifier, sourceLocation):
        self.m_description = description
        self.m_sourceLocation = sourceLocation


class MainWindow(QtWidgets.QMainWindow, Ui_SchemaMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setupUi(self)

        XmlSyntaxHighlighter(self.schemaView.document())
        XmlSyntaxHighlighter(self.instanceEdit.document())

        self.schemaSelection.addItem("Contact Schema")
        self.schemaSelection.addItem("Recipe Schema")
        self.schemaSelection.addItem("Order Schema")

        self.instanceSelection.addItem("Valid Contact Instance")
        self.instanceSelection.addItem("Invalid Contact Instance")

        self.schemaSelection.currentIndexChanged[int].connect(self.schemaSelected)
        self.instanceSelection.currentIndexChanged[int].connect(self.instanceSelected)
        self.validateButton.clicked.connect(self.validate)
        self.instanceEdit.textChanged.connect(self.textChanged)

        self.validationStatus.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.schemaSelected(0)
        self.instanceSelected(0)

    def schemaSelected(self, index):
        self.instanceSelection.clear()

        if index == 0:
            self.instanceSelection.addItem("Valid Contact Instance")
            self.instanceSelection.addItem("Invalid Contact Instance")
        elif index == 1:
            self.instanceSelection.addItem("Valid Recipe Instance")
            self.instanceSelection.addItem("Invalid Recipe Instance")
        elif index == 2:
            self.instanceSelection.addItem("Valid Order Instance")
            self.instanceSelection.addItem("Invalid Order Instance")

        self.textChanged()

        schemaFile = QtCore.QFile(':/schema_%d.xsd' % index)
        schemaFile.open(QtCore.QIODevice.ReadOnly)
        schemaData = schemaFile.readAll()
        self.schemaView.setPlainText(encode_utf8(schemaData))

        self.validate()

    def instanceSelected(self, index):
        if index is -1:
            return

        index += 2 * self.schemaSelection.currentIndex()
        instanceFile = QtCore.QFile(':/instance_%d.xml' % index)
        instanceFile.open(QtCore.QIODevice.ReadOnly)
        instanceData = instanceFile.readAll()
        self.instanceEdit.setPlainText(encode_utf8(instanceData))

        self.validate()

    def validate(self):
        schemaData = decode_utf8(self.schemaView.toPlainText())
        instanceData = decode_utf8(self.instanceEdit.toPlainText())

        messageHandler = MessageHandler()

        schema = QtXmlPatterns.QXmlSchema()
        schema.setMessageHandler(messageHandler)
        schema.load(schemaData, QtCore.QUrl())

        errorOccurred = False
        if not schema.isValid():
            errorOccurred = True
        else:
            validator = QtXmlPatterns.QXmlSchemaValidator(schema)
            if not validator.validate(instanceData):
                errorOccurred = True

        if errorOccurred:
            self.validationStatus.setText(messageHandler.statusMessage())
            self.moveCursor(messageHandler.line(), messageHandler.column())
            background = QtCore.Qt.red
        else:
            self.validationStatus.setText("validation successful")
            background = QtCore.Qt.green

        styleSheet = 'QLabel {background: %s; padding: 3px}' % QtGui.QColor(background).lighter(160).name()
        self.validationStatus.setStyleSheet(styleSheet)

    def textChanged(self):
        self.instanceEdit.setExtraSelections([])

    def moveCursor(self, line, column):
        self.instanceEdit.moveCursor(QtGui.QTextCursor.Start)

        for i in range(1, line):
            self.instanceEdit.moveCursor(QtGui.QTextCursor.Down)

        for i in range(1, column):
            self.instanceEdit.moveCursor(QtGui.QTextCursor.Right)

        extraSelections = []
        selection = QtWidgets.QTextEdit.ExtraSelection()

        lineColor = QtGui.QColor(QtCore.Qt.red).lighter(160)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.instanceEdit.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)

        self.instanceEdit.setExtraSelections(extraSelections)

        self.instanceEdit.setFocus()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
