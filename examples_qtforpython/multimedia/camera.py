#!/usr/bin/env python

#############################################################################
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
#############################################################################

"""PySide2 Multimedia Camera Example"""

import os, sys
from PySide2.QtCore import QDate, QDir, QStandardPaths, Qt, QUrl
from PySide2.QtGui import QClipboard, QGuiApplication, QDesktopServices, QIcon
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import (QAction, qApp, QApplication, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QTabWidget, QToolBar, QVBoxLayout, QWidget)
from PySide2.QtMultimedia import QCamera, QCameraImageCapture, QCameraInfo
from PySide2.QtMultimediaWidgets import QCameraViewfinder

class ImageView(QWidget):
    def __init__(self, previewImage, fileName):
        super(ImageView, self).__init__()

        self.fileName = fileName

        mainLayout = QVBoxLayout(self)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap.fromImage(previewImage))
        mainLayout.addWidget(self.imageLabel)

        topLayout = QHBoxLayout()
        self.fileNameLabel = QLabel(QDir.toNativeSeparators(fileName))
        self.fileNameLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        topLayout.addWidget(self.fileNameLabel)
        topLayout.addStretch()
        copyButton = QPushButton("Copy")
        copyButton.setToolTip("Copy file name to clipboard")
        topLayout.addWidget(copyButton)
        copyButton.clicked.connect(self.copy)
        launchButton = QPushButton("Launch")
        launchButton.setToolTip("Launch image viewer")
        topLayout.addWidget(launchButton)
        launchButton.clicked.connect(self.launch)
        mainLayout.addLayout(topLayout)

    def copy(self):
        QGuiApplication.clipboard().setText(self.fileNameLabel.text())

    def launch(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.fileName))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.cameraInfo = QCameraInfo.defaultCamera()
        self.camera = QCamera(self.cameraInfo)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.imageCapture = QCameraImageCapture(self.camera)
        self.imageCapture.imageCaptured.connect(self.imageCaptured)
        self.imageCapture.imageSaved.connect(self.imageSaved)
        self.currentPreview = QImage()

        toolBar = QToolBar()
        self.addToolBar(toolBar)

        fileMenu = self.menuBar().addMenu("&File")
        shutterIcon = QIcon(os.path.join(os.path.dirname(__file__),
                            "shutter.svg"))
        self.takePictureAction = QAction(shutterIcon, "&Take Picture", self,
                                         shortcut="Ctrl+T",
                                         triggered=self.takePicture)
        self.takePictureAction.setToolTip("Take Picture")
        fileMenu.addAction(self.takePictureAction)
        toolBar.addAction(self.takePictureAction)

        exitAction = QAction(QIcon.fromTheme("application-exit"), "E&xit",
                             self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAction = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAction)

        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.cameraViewfinder = QCameraViewfinder()
        self.camera.setViewfinder(self.cameraViewfinder)
        self.tabWidget.addTab(self.cameraViewfinder, "Viewfinder")

        if self.camera.status() != QCamera.UnavailableStatus:
            name = self.cameraInfo.description()
            self.setWindowTitle("PySide2 Camera Example (" + name + ")")
            self.statusBar().showMessage("Starting: '" + name + "'", 5000)
            self.camera.start()
        else:
            self.setWindowTitle("PySide2 Camera Example")
            self.takePictureAction.setEnabled(False)
            self.statusBar().showMessage("Camera unavailable", 5000)

    def nextImageFileName(self):
        picturesLocation = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        dateString = QDate.currentDate().toString("yyyyMMdd")
        pattern = picturesLocation + "/pyside2_camera_" + dateString + "_{:03d}.jpg"
        n = 1
        while True:
            result = pattern.format(n)
            if not os.path.exists(result):
                return result
            n = n + 1
        return None

    def takePicture(self):
        self.currentPreview = QImage()
        self.camera.searchAndLock()
        self.imageCapture.capture(self.nextImageFileName())
        self.camera.unlock()

    def imageCaptured(self, id, previewImage):
        self.currentPreview = previewImage

    def imageSaved(self, id, fileName):
        index = self.tabWidget.count()
        imageView = ImageView(self.currentPreview, fileName)
        self.tabWidget.addTab(imageView, "Capture #{}".format(index))
        self.tabWidget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
    mainWin.show()
    sys.exit(app.exec_())
