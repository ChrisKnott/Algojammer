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

"""PySide2 port of the widgets/dialogs/extension example from Qt v5.x"""

from PySide2 import QtCore, QtWidgets


class FindDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)

        label = QtWidgets.QLabel("Find &what:")
        lineEdit = QtWidgets.QLineEdit()
        label.setBuddy(lineEdit)

        caseCheckBox = QtWidgets.QCheckBox("Match &case")
        fromStartCheckBox = QtWidgets.QCheckBox("Search from &start")
        fromStartCheckBox.setChecked(True)

        findButton = QtWidgets.QPushButton("&Find")
        findButton.setDefault(True)

        moreButton = QtWidgets.QPushButton("&More")
        moreButton.setCheckable(True)
        moreButton.setAutoDefault(False)

        buttonBox = QtWidgets.QDialogButtonBox(QtCore.Qt.Vertical)
        buttonBox.addButton(findButton, QtWidgets.QDialogButtonBox.ActionRole)
        buttonBox.addButton(moreButton, QtWidgets.QDialogButtonBox.ActionRole)

        extension = QtWidgets.QWidget()

        wholeWordsCheckBox = QtWidgets.QCheckBox("&Whole words")
        backwardCheckBox = QtWidgets.QCheckBox("Search &backward")
        searchSelectionCheckBox = QtWidgets.QCheckBox("Search se&lection")

        moreButton.toggled.connect(extension.setVisible)

        extensionLayout = QtWidgets.QVBoxLayout()
        extensionLayout.setContentsMargins(0, 0, 0, 0)
        extensionLayout.addWidget(wholeWordsCheckBox)
        extensionLayout.addWidget(backwardCheckBox)
        extensionLayout.addWidget(searchSelectionCheckBox)
        extension.setLayout(extensionLayout)

        topLeftLayout = QtWidgets.QHBoxLayout()
        topLeftLayout.addWidget(label)
        topLeftLayout.addWidget(lineEdit)

        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addLayout(topLeftLayout)
        leftLayout.addWidget(caseCheckBox)
        leftLayout.addWidget(fromStartCheckBox)
        leftLayout.addStretch(1)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(buttonBox, 0, 1)
        mainLayout.addWidget(extension, 1, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Extension")
        extension.hide()


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = FindDialog()
    sys.exit(dialog.exec_())
