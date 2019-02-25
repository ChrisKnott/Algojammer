#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
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
############################################################################

import sys
import math
from PySide2 import QtCore, QtGui, QtWidgets

try:
    from PySide2 import QtMacExtras
except ImportError:
    app = QtWidgets.QApplication(sys.argv)
    messageBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "QtMacExtras macpasteboardmime",
                                       "This exampe only runs on macOS and QtMacExtras must be installed to run this example.",
                                       QtWidgets.QMessageBox.Close)
    messageBox.exec_()
    sys.exit(1)

class VCardMime(QtMacExtras.QMacPasteboardMime):
    def __init__(self, t = QtMacExtras.QMacPasteboardMime.MIME_ALL):
        super(VCardMime, self).__init__(t)

    def convertorName(self):
        return "VCardMime"

    def canConvert(self, mime, flav):
        if self.mimeFor(flav) == mime:
            return True
        else:
            return False

    def mimeFor(self, flav):
        if flav == "public.vcard":
            return "application/x-mycompany-VCard"
        else:
            return ""

    def flavorFor(self, mime):
        if mime == "application/x-mycompany-VCard":
            return "public.vcard"
        else:
            return ""

    def convertToMime(self, mime, data, flav):
        all = QtCore.QByteArray()
        for i in data:
            all += i
        return all

    def convertFromMime(mime, data, flav):
        # Todo: implement!
        return []

class TestWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)
        self.vcardMime = VCardMime()
        self.setAcceptDrops(True)

        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

        self.label1.setText("Please drag a \"VCard\" from Contacts application, normally a name in the list, and drop here.")

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        e.accept()
        self.contentsDropEvent(e)

    def contentsDropEvent(self, e):
        if e.mimeData().hasFormat("application/x-mycompany-VCard"):
            s = e.mimeData().data( "application/x-mycompany-VCard" )
            # s now contains text of vcard
            self.label2.setText(str(s))
            e.acceptProposedAction()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtMacExtras.qRegisterDraggedTypes(["public.vcard"])
    wid1 = TestWidget()
    wid1.show()
    sys.exit(app.exec_())
