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

"""PySide2 Multimedia player example"""

import sys
from PySide2.QtCore import SLOT, QStandardPaths, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import (QAction, qApp, QApplication, QDialog, QFileDialog,
    QMainWindow, QMenu, QMenuBar, QSlider, QStyle, QToolBar)
from PySide2.QtMultimedia import QMediaPlayer, QMediaPlaylist
from PySide2.QtMultimediaWidgets import QVideoWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.playlist = QMediaPlaylist()
        self.player = QMediaPlayer()

        toolBar = QToolBar()
        self.addToolBar(toolBar)

        fileMenu = self.menuBar().addMenu("&File")
        openAction = QAction(QIcon.fromTheme("document-open"),
                             "&Open...", self, shortcut=QKeySequence.Open,
                             triggered=self.open)
        fileMenu.addAction(openAction)
        exitAction = QAction(QIcon.fromTheme("application-exit"), "E&xit",
                             self, shortcut="Ctrl+Q", triggered=self.close)
        fileMenu.addAction(exitAction)

        playMenu = self.menuBar().addMenu("&Play")
        playIcon = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.playAction = toolBar.addAction(playIcon, "Play")
        self.playAction.triggered.connect(self.player.play)
        playMenu.addAction(self.playAction)

        previousIcon = self.style().standardIcon(QStyle.SP_MediaSkipBackward)
        self.previousAction = toolBar.addAction(previousIcon, "Previous")
        self.previousAction.triggered.connect(self.previousClicked)
        playMenu.addAction(self.previousAction)

        pauseIcon = self.style().standardIcon(QStyle.SP_MediaPause)
        self.pauseAction = toolBar.addAction(pauseIcon, "Pause")
        self.pauseAction.triggered.connect(self.player.pause)
        playMenu.addAction(self.pauseAction)

        nextIcon = self.style().standardIcon(QStyle.SP_MediaSkipForward)
        self.nextAction = toolBar.addAction(nextIcon, "Next")
        self.nextAction.triggered.connect(self.playlist.next)
        playMenu.addAction(self.nextAction)

        stopIcon = self.style().standardIcon(QStyle.SP_MediaStop)
        self.stopAction = toolBar.addAction(stopIcon, "Stop")
        self.stopAction.triggered.connect(self.player.stop)
        playMenu.addAction(self.stopAction)

        self.volumeSlider = QSlider()
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setFixedWidth(app.desktop().availableGeometry(self).width() / 10)
        self.volumeSlider.setValue(self.player.volume())
        self.volumeSlider.setTickInterval(10)
        self.volumeSlider.setTickPosition(QSlider.TicksBelow)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.valueChanged.connect(self.player.setVolume)
        toolBar.addWidget(self.volumeSlider)

        aboutMenu = self.menuBar().addMenu("&About")
        aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)
        aboutMenu.addAction(aboutQtAct)

        self.videoWidget = QVideoWidget()
        self.setCentralWidget(self.videoWidget)
        self.player.setPlaylist(self.playlist)
        self.player.stateChanged.connect(self.updateButtons)
        self.player.setVideoOutput(self.videoWidget)

        self.updateButtons(self.player.state())

    def open(self):
        fileDialog = QFileDialog(self)
        supportedMimeTypes = QMediaPlayer.supportedMimeTypes()
        if not supportedMimeTypes:
            supportedMimeTypes.append("video/x-msvideo") # AVI
        fileDialog.setMimeTypeFilters(supportedMimeTypes)
        moviesLocation = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        fileDialog.setDirectory(moviesLocation)
        if fileDialog.exec_() == QDialog.Accepted:
            self.playlist.addMedia(fileDialog.selectedUrls()[0])
            self.player.play()

    def previousClicked(self):
        # Go to previous track if we are within the first 5 seconds of playback
        # Otherwise, seek to the beginning.
        if self.player.position() <= 5000:
            self.playlist.previous()
        else:
            player.setPosition(0)

    def updateButtons(self, state):
        mediaCount = self.playlist.mediaCount()
        self.playAction.setEnabled(mediaCount > 0
            and state != QMediaPlayer.PlayingState)
        self.pauseAction.setEnabled(state == QMediaPlayer.PlayingState)
        self.stopAction.setEnabled(state != QMediaPlayer.StoppedState)
        self.previousAction.setEnabled(self.player.position() > 0)
        self.nextAction.setEnabled(mediaCount > 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    availableGeometry = app.desktop().availableGeometry(mainWin)
    mainWin.resize(availableGeometry.width() / 3, availableGeometry.height() / 2)
    mainWin.show()
    sys.exit(app.exec_())
