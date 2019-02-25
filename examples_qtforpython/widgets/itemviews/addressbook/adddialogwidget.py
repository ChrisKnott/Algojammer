#!/usr/bin/python

#############################################################################
##
## Copyright (C) 2011 Arun Srinivasan <rulfzid@gmail.com>
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

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QDialog, QLabel, QTextEdit, QLineEdit,
                               QDialogButtonBox, QGridLayout, QVBoxLayout)

class AddDialogWidget(QDialog):
    """ A dialog to add a new address to the addressbook. """

    def __init__(self, parent=None):
        super(AddDialogWidget, self).__init__(parent)

        nameLabel = QLabel("Name")
        addressLabel = QLabel("Address")
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel)

        self.nameText = QLineEdit()
        self.addressText = QTextEdit()

        grid = QGridLayout()
        grid.setColumnStretch(1, 2)
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.nameText, 0, 1)
        grid.addWidget(addressLabel, 1, 0, Qt.AlignLeft | Qt.AlignTop)
        grid.addWidget(self.addressText, 1, 1, Qt.AlignLeft)

        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

        self.setWindowTitle("Add a Contact")

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # These properties make using this dialog a little cleaner. It's much
    # nicer to type "addDialog.address" to retrieve the address as compared
    # to "addDialog.addressText.toPlainText()"
    @property
    def name(self):
        return self.nameText.text()

    @property
    def address(self):
        return self.addressText.toPlainText()


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = AddDialogWidget()
    if (dialog.exec_()):
        name = dialog.name
        address = dialog.address
        print("Name:" + name)
        print("Address:" + address)
