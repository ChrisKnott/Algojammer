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

"""PySide2 port of the xml/dombookmarks example from Qt v5.x"""

from PySide2 import QtCore, QtGui, QtWidgets, QtXml


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.xbelTree = XbelTree()
        self.setCentralWidget(self.xbelTree)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("DOM Bookmarks")
        self.resize(480, 320)

    def open(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                "Open Bookmark File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "DOM Bookmarks",
                    "Cannot read file %s:\n%s." % (fileName, inFile.errorString()))
            return

        if self.xbelTree.read(inFile):
            self.statusBar().showMessage("File loaded", 2000)

    def saveAs(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save Bookmark File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        outFile = QtCore.QFile(fileName)
        if not outFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "DOM Bookmarks",
                    "Cannot write file %s:\n%s." % (fileName, outFile.errorString()))
            return

        if self.xbelTree.write(outFile):
            self.statusBar().showMessage("File saved", 2000)

    def about(self):
       QtWidgets.QMessageBox.about(self, "About DOM Bookmarks",
            "The <b>DOM Bookmarks</b> example demonstrates how to use Qt's "
            "DOM classes to read and write XML documents.")

    def createActions(self):
        self.openAct = QtWidgets.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveAsAct = QtWidgets.QAction("&Save As...", self, shortcut="Ctrl+S",
                triggered=self.saveAs)

        self.exitAct = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtWidgets.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtWidgets.QAction("About &Qt", self,
                triggered=QtWidgets.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)


class XbelTree(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(XbelTree, self).__init__(parent)

        self.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.setHeaderLabels(("Title", "Location"))

        self.domDocument = QtXml.QDomDocument()

        self.domElementForItem = {}

        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()

        self.folderIcon.addPixmap(self.style().standardPixmap(QtWidgets.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(self.style().standardPixmap(QtWidgets.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(self.style().standardPixmap(QtWidgets.QStyle.SP_FileIcon))

    def read(self, device):
        ok, errorStr, errorLine, errorColumn = self.domDocument.setContent(device, True)
        if not ok:
            QtWidgets.QMessageBox.information(self.window(), "DOM Bookmarks",
                    "Parse error at line %d, column %d:\n%s" % (errorLine, errorColumn, errorStr))
            return False

        root = self.domDocument.documentElement()
        if root.tagName() != 'xbel':
            QtWidgets.QMessageBox.information(self.window(), "DOM Bookmarks",
                    "The file is not an XBEL file.")
            return False
        elif root.hasAttribute('version') and root.attribute('version') != '1.0':
            QtWidgets.QMessageBox.information(self.window(), "DOM Bookmarks",
                    "The file is not an XBEL version 1.0 file.")
            return False

        self.clear()

        # It might not be connected.
        try:
            self.itemChanged.disconnect(self.updateDomElement)
        except:
            pass

        child = root.firstChildElement('folder')
        while not child.isNull():
            self.parseFolderElement(child)
            child = child.nextSiblingElement('folder')

        self.itemChanged.connect(self.updateDomElement)

        return True

    def write(self, device):
        indentSize = 4

        out = QtCore.QTextStream(device)
        self.domDocument.save(out, indentSize)
        return True

    def updateDomElement(self, item, column):
        element = self.domElementForItem.get(id(item))
        if not element.isNull():
            if column == 0:
                oldTitleElement = element.firstChildElement('title')
                newTitleElement = self.domDocument.createElement('title')

                newTitleText = self.domDocument.createTextNode(item.text(0))
                newTitleElement.appendChild(newTitleText)

                element.replaceChild(newTitleElement, oldTitleElement)
            else:
                if element.tagName() == 'bookmark':
                    element.setAttribute('href', item.text(1))

    def parseFolderElement(self, element, parentItem=None):
        item = self.createItem(element, parentItem)

        title = element.firstChildElement('title').text()
        if not title:
            title = "Folder"

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setIcon(0, self.folderIcon)
        item.setText(0, title)

        folded = (element.attribute('folded') != 'no')
        self.setItemExpanded(item, not folded)

        child = element.firstChildElement()
        while not child.isNull():
            if child.tagName() == 'folder':
                self.parseFolderElement(child, item)
            elif child.tagName() == 'bookmark':
                childItem = self.createItem(child, item)

                title = child.firstChildElement('title').text()
                if not title:
                    title = "Folder"

                childItem.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                childItem.setIcon(0, self.bookmarkIcon)
                childItem.setText(0, title)
                childItem.setText(1, child.attribute('href'))
            elif child.tagName() == 'separator':
                childItem = self.createItem(child, item)
                childItem.setFlags(item.flags() & ~(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable))
                childItem.setText(0, 30 * "\xb7")

            child = child.nextSiblingElement()

    def createItem(self, element, parentItem=None):
        item = QtWidgets.QTreeWidgetItem()

        if parentItem is not None:
            item = QtWidgets.QTreeWidgetItem(parentItem)
        else:
            item = QtWidgets.QTreeWidgetItem(self)

        self.domElementForItem[id(item)] = element
        return item


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    sys.exit(app.exec_())
