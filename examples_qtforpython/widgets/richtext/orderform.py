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

"""PySide2 port of the widgets/richtext/orderform example from Qt v5.x"""

from PySide2 import QtCore, QtGui, QtWidgets, QtPrintSupport


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        fileMenu = QtWidgets.QMenu("&File", self)
        newAction = fileMenu.addAction("&New...")
        newAction.setShortcut("Ctrl+N")
        self.printAction = fileMenu.addAction("&Print...", self.printFile)
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.setEnabled(False)
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")
        self.menuBar().addMenu(fileMenu)

        self.letters = QtWidgets.QTabWidget()

        newAction.triggered.connect(self.openDialog)
        quitAction.triggered.connect(self.close)

        self.setCentralWidget(self.letters)
        self.setWindowTitle("Order Form")

    def createLetter(self, name, address, orderItems, sendOffers):
        editor = QtWidgets.QTextEdit()
        tabIndex = self.letters.addTab(editor, name)
        self.letters.setCurrentIndex(tabIndex)

        cursor = editor.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)

        textFormat = QtGui.QTextCharFormat()
        boldFormat = QtGui.QTextCharFormat()
        boldFormat.setFontWeight(QtGui.QFont.Bold)

        referenceFrameFormat = QtGui.QTextFrameFormat()
        referenceFrameFormat.setBorder(1)
        referenceFrameFormat.setPadding(8)
        referenceFrameFormat.setPosition(QtGui.QTextFrameFormat.FloatRight)
        referenceFrameFormat.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 40))
        cursor.insertFrame(referenceFrameFormat)

        cursor.insertText("A company", boldFormat)
        cursor.insertBlock()
        cursor.insertText("321 City Street")
        cursor.insertBlock()
        cursor.insertText("Industry Park")
        cursor.insertBlock()
        cursor.insertText("Another country")

        cursor.setPosition(topFrame.lastPosition())

        cursor.insertText(name, textFormat)
        for line in address.split("\n"):
            cursor.insertBlock()
            cursor.insertText(line)

        cursor.insertBlock()
        cursor.insertBlock()

        date = QtCore.QDate.currentDate()
        cursor.insertText("Date: %s" % date.toString('d MMMM yyyy'),
                textFormat)
        cursor.insertBlock()

        bodyFrameFormat = QtGui.QTextFrameFormat()
        bodyFrameFormat.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 100))
        cursor.insertFrame(bodyFrameFormat)

        cursor.insertText("I would like to place an order for the following "
                "items:", textFormat)
        cursor.insertBlock()
        cursor.insertBlock()

        orderTableFormat = QtGui.QTextTableFormat()
        orderTableFormat.setAlignment(QtCore.Qt.AlignHCenter)
        orderTable = cursor.insertTable(1, 2, orderTableFormat)

        orderFrameFormat = cursor.currentFrame().frameFormat()
        orderFrameFormat.setBorder(1)
        cursor.currentFrame().setFrameFormat(orderFrameFormat)

        cursor = orderTable.cellAt(0, 0).firstCursorPosition()
        cursor.insertText("Product", boldFormat)
        cursor = orderTable.cellAt(0, 1).firstCursorPosition()
        cursor.insertText("Quantity", boldFormat)

        for text, quantity in orderItems:
            row = orderTable.rows()

            orderTable.insertRows(row, 1)
            cursor = orderTable.cellAt(row, 0).firstCursorPosition()
            cursor.insertText(text, textFormat)
            cursor = orderTable.cellAt(row, 1).firstCursorPosition()
            cursor.insertText(str(quantity), textFormat)

        cursor.setPosition(topFrame.lastPosition())

        cursor.insertBlock()

        cursor.insertText("Please update my records to take account of the "
                "following privacy information:")
        cursor.insertBlock()

        offersTable = cursor.insertTable(2, 2)

        cursor = offersTable.cellAt(0, 1).firstCursorPosition()
        cursor.insertText("I want to receive more information about your "
                "company's products and special offers.", textFormat)
        cursor = offersTable.cellAt(1, 1).firstCursorPosition()
        cursor.insertText("I do not want to receive any promotional "
                "information from your company.", textFormat)

        if sendOffers:
            cursor = offersTable.cellAt(0, 0).firstCursorPosition()
        else:
            cursor = offersTable.cellAt(1, 0).firstCursorPosition()

        cursor.insertText('X', boldFormat)

        cursor.setPosition(topFrame.lastPosition())
        cursor.insertBlock()
        cursor.insertText("Sincerely,", textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(name)

        self.printAction.setEnabled(True)

    def createSample(self):
        dialog = DetailsDialog('Dialog with default values', self)
        self.createLetter('Mr Smith',
                '12 High Street\nSmall Town\nThis country',
                dialog.orderItems(), True)

    def openDialog(self):
        dialog = DetailsDialog("Enter Customer Details", self)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.createLetter(dialog.senderName(), dialog.senderAddress(),
                    dialog.orderItems(), dialog.sendOffers())

    def printFile(self):
        editor = self.letters.currentWidget()
        printer = QtPrintSupport.QPrinter()

        dialog = QtPrintSupport.QPrintDialog(printer, self)
        dialog.setWindowTitle("Print Document")

        if editor.textCursor().hasSelection():
            dialog.addEnabledOption(QtPrintSupport.QAbstractPrintDialog.PrintSelection)

        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        editor.print_(printer)


class DetailsDialog(QtWidgets.QDialog):
    def __init__(self, title, parent):
        super(DetailsDialog, self).__init__(parent)

        self.items = ("T-shirt", "Badge", "Reference book", "Coffee cup")

        nameLabel = QtWidgets.QLabel("Name:")
        addressLabel = QtWidgets.QLabel("Address:")
        addressLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.nameEdit = QtWidgets.QLineEdit()
        self.addressEdit = QtWidgets.QTextEdit()
        self.offersCheckBox = QtWidgets.QCheckBox("Send information about "
                "products and special offers:")

        self.setupItemsTable()

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameEdit, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0)
        mainLayout.addWidget(self.addressEdit, 1, 1)
        mainLayout.addWidget(self.itemsTable, 0, 2, 2, 1)
        mainLayout.addWidget(self.offersCheckBox, 2, 1, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle(title)

    def setupItemsTable(self):
        self.itemsTable = QtWidgets.QTableWidget(len(self.items), 2)

        for row, item in enumerate(self.items):
            name = QtWidgets.QTableWidgetItem(item)
            name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.itemsTable.setItem(row, 0, name)
            quantity = QtWidgets.QTableWidgetItem('1')
            self.itemsTable.setItem(row, 1, quantity)

    def orderItems(self):
        orderList = []

        for row in range(len(self.items)):
            text = self.itemsTable.item(row, 0).text()
            quantity = int(self.itemsTable.item(row, 1).data(QtCore.Qt.DisplayRole))
            orderList.append((text, max(0, quantity)))

        return orderList

    def senderName(self):
        return self.nameEdit.text()

    def senderAddress(self):
        return self.addressEdit.toPlainText()

    def sendOffers(self):
        return self.offersCheckBox.isChecked()

    def verify(self):
        if self.nameEdit.text() and self.addressEdit.toPlainText():
            self.accept()
            return

        answer = QtWidgets.QMessageBox.warning(self, "Incomplete Form",
                "The form does not contain all the necessary information.\n"
                "Do you want to discard it?",
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if answer == QtWidgets.QMessageBox.Yes:
            self.reject()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    window.createSample()
    sys.exit(app.exec_())
