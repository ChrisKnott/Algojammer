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

"""PySide2 port of the network/blockingfortunclient example from Qt v5.x, originating from PyQt"""

from PySide2.QtCore import (Signal, QDataStream, QMutex, QMutexLocker,
        QThread, QWaitCondition)
from PySide2.QtGui import QIntValidator
from PySide2.QtWidgets import (QApplication, QDialogButtonBox, QGridLayout,
        QLabel, QLineEdit, QMessageBox, QPushButton, QWidget)
from PySide2.QtNetwork import (QAbstractSocket, QHostAddress, QNetworkInterface,
        QTcpSocket)


class FortuneThread(QThread):
    newFortune = Signal(str)

    error = Signal(int, str)

    def __init__(self, parent=None):
        super(FortuneThread, self).__init__(parent)

        self.quit = False
        self.hostName = ''
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.port = 0

    def __del__(self):
        self.mutex.lock()
        self.quit = True
        self.cond.wakeOne()
        self.mutex.unlock()
        self.wait()

    def requestNewFortune(self, hostname, port):
        locker = QMutexLocker(self.mutex)
        self.hostName = hostname
        self.port = port
        if not self.isRunning():
            self.start()
        else:
            self.cond.wakeOne()

    def run(self):
        self.mutex.lock()
        serverName = self.hostName
        serverPort = self.port
        self.mutex.unlock()

        while not self.quit:
            Timeout = 5 * 1000

            socket = QTcpSocket()
            socket.connectToHost(serverName, serverPort)

            if not socket.waitForConnected(Timeout):
                self.error.emit(socket.error(), socket.errorString())
                return

            while socket.bytesAvailable() < 2:
                if not socket.waitForReadyRead(Timeout):
                    self.error.emit(socket.error(), socket.errorString())
                    return

            instr = QDataStream(socket)
            instr.setVersion(QDataStream.Qt_4_0)
            blockSize = instr.readUInt16()

            while socket.bytesAvailable() < blockSize:
                if not socket.waitForReadyRead(Timeout):
                    self.error.emit(socket.error(), socket.errorString())
                    return

            self.mutex.lock()
            fortune = instr.readQString()
            self.newFortune.emit(fortune)

            self.cond.wait(self.mutex)
            serverName = self.hostName
            serverPort = self.port
            self.mutex.unlock()


class BlockingClient(QWidget):
    def __init__(self, parent=None):
        super(BlockingClient, self).__init__(parent)

        self.thread = FortuneThread()
        self.currentFortune = ''

        hostLabel = QLabel("&Server name:")
        portLabel = QLabel("S&erver port:")

        for ipAddress in QNetworkInterface.allAddresses():
            if ipAddress != QHostAddress.LocalHost and ipAddress.toIPv4Address() != 0:
                break
        else:
            ipAddress = QHostAddress(QHostAddress.LocalHost)

        ipAddress = ipAddress.toString()

        self.hostLineEdit = QLineEdit(ipAddress)
        self.portLineEdit = QLineEdit()
        self.portLineEdit.setValidator(QIntValidator(1, 65535, self))

        hostLabel.setBuddy(self.hostLineEdit)
        portLabel.setBuddy(self.portLineEdit)

        self.statusLabel = QLabel(
                "This example requires that you run the Fortune Server example as well.")
        self.statusLabel.setWordWrap(True)

        self.getFortuneButton = QPushButton("Get Fortune")
        self.getFortuneButton.setDefault(True)
        self.getFortuneButton.setEnabled(False)

        quitButton = QPushButton("Quit")

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.getFortuneButton, QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QDialogButtonBox.RejectRole)

        self.getFortuneButton.clicked.connect(self.requestNewFortune)
        quitButton.clicked.connect(self.close)
        self.hostLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.portLineEdit.textChanged.connect(self.enableGetFortuneButton)
        self.thread.newFortune.connect(self.showFortune)
        self.thread.error.connect(self.displayError)

        mainLayout = QGridLayout()
        mainLayout.addWidget(hostLabel, 0, 0)
        mainLayout.addWidget(self.hostLineEdit, 0, 1)
        mainLayout.addWidget(portLabel, 1, 0)
        mainLayout.addWidget(self.portLineEdit, 1, 1)
        mainLayout.addWidget(self.statusLabel, 2, 0, 1, 2)
        mainLayout.addWidget(buttonBox, 3, 0, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("Blocking Fortune Client")
        self.portLineEdit.setFocus()

    def requestNewFortune(self):
        self.getFortuneButton.setEnabled(False)
        self.thread.requestNewFortune(self.hostLineEdit.text(),
                int(self.portLineEdit.text()))

    def showFortune(self, nextFortune):
        if nextFortune == self.currentFortune:
            self.requestNewFortune()
            return

        self.currentFortune = nextFortune
        self.statusLabel.setText(self.currentFortune)
        self.getFortuneButton.setEnabled(True)

    def displayError(self, socketError, message):
        if socketError == QAbstractSocket.HostNotFoundError:
            QMessageBox.information(self, "Blocking Fortune Client",
                    "The host was not found. Please check the host and port "
                    "settings.")
        elif socketError == QAbstractSocket.ConnectionRefusedError:
            QMessageBox.information(self, "Blocking Fortune Client",
                    "The connection was refused by the peer. Make sure the "
                    "fortune server is running, and check that the host name "
                    "and port settings are correct.")
        else:
            QMessageBox.information(self, "Blocking Fortune Client",
                    "The following error occurred: %s." % message)

        self.getFortuneButton.setEnabled(True)

    def enableGetFortuneButton(self):
        self.getFortuneButton.setEnabled(self.hostLineEdit.text() != '' and
                self.portLineEdit.text() != '')


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    client = BlockingClient()
    client.show()
    sys.exit(app.exec_())
