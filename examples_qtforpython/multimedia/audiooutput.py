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

"""PySide2 port of the multimedia/audiooutput example from Qt v5.x, originating from PyQt"""

from math import pi, sin
from struct import pack

from PySide2.QtCore import QByteArray, QIODevice, Qt, QTimer, qWarning
from PySide2.QtMultimedia import (QAudio, QAudioDeviceInfo, QAudioFormat,
        QAudioOutput)
from PySide2.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
        QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget)


class Generator(QIODevice):

    def __init__(self, format, durationUs, sampleRate, parent):
        super(Generator, self).__init__(parent)

        self.m_pos = 0
        self.m_buffer = QByteArray()

        self.generateData(format, durationUs, sampleRate)

    def start(self):
        self.open(QIODevice.ReadOnly)

    def stop(self):
        self.m_pos = 0
        self.close()

    def generateData(self, format, durationUs, sampleRate):
        pack_format = ''

        if format.sampleSize() == 8:
            if format.sampleType() == QAudioFormat.UnSignedInt:
                scaler = lambda x: ((1.0 + x) / 2 * 255)
                pack_format = 'B'
            elif format.sampleType() == QAudioFormat.SignedInt:
                scaler = lambda x: x * 127
                pack_format = 'b'
        elif format.sampleSize() == 16:
            if format.sampleType() == QAudioFormat.UnSignedInt:
                scaler = lambda x: (1.0 + x) / 2 * 65535
                pack_format = '<H' if format.byteOrder() == QAudioFormat.LittleEndian else '>H'
            elif format.sampleType() == QAudioFormat.SignedInt:
                scaler = lambda x: x * 32767
                pack_format = '<h' if format.byteOrder() == QAudioFormat.LittleEndian else '>h'

        assert(pack_format != '')

        channelBytes = format.sampleSize() // 8
        sampleBytes = format.channelCount() * channelBytes

        length = (format.sampleRate() * format.channelCount() * (format.sampleSize() // 8)) * durationUs // 100000

        self.m_buffer.clear()
        sampleIndex = 0
        factor = 2 * pi * sampleRate / format.sampleRate()

        while length != 0:
            x = sin((sampleIndex % format.sampleRate()) * factor)
            packed = pack(pack_format, int(scaler(x)))

            for _ in range(format.channelCount()):
                self.m_buffer.append(packed)
                length -= channelBytes

            sampleIndex += 1

    def readData(self, maxlen):
        data = QByteArray()
        total = 0

        while maxlen > total:
            chunk = min(self.m_buffer.size() - self.m_pos, maxlen - total)
            data.append(self.m_buffer.mid(self.m_pos, chunk))
            self.m_pos = (self.m_pos + chunk) % self.m_buffer.size()
            total += chunk

        return data.data()

    def writeData(self, data):
        return 0

    def bytesAvailable(self):
        return self.m_buffer.size() + super(Generator, self).bytesAvailable()


class AudioTest(QMainWindow):

    PUSH_MODE_LABEL = "Enable push mode"
    PULL_MODE_LABEL = "Enable pull mode"
    SUSPEND_LABEL = "Suspend playback"
    RESUME_LABEL = "Resume playback"

    DurationSeconds = 1
    ToneSampleRateHz = 600
    DataSampleRateHz = 44100

    def __init__(self):
        super(AudioTest, self).__init__()

        self.m_device = QAudioDeviceInfo.defaultOutputDevice()
        self.m_output = None

        self.initializeWindow()
        self.initializeAudio()

    def initializeWindow(self):
        layout = QVBoxLayout()

        self.m_deviceBox = QComboBox()
        self.m_deviceBox.activated[int].connect(self.deviceChanged)
        for deviceInfo in QAudioDeviceInfo.availableDevices(QAudio.AudioOutput):
            self.m_deviceBox.addItem(deviceInfo.deviceName(), deviceInfo)

        layout.addWidget(self.m_deviceBox)

        self.m_modeButton = QPushButton()
        self.m_modeButton.clicked.connect(self.toggleMode)
        self.m_modeButton.setText(self.PUSH_MODE_LABEL)

        layout.addWidget(self.m_modeButton)

        self.m_suspendResumeButton = QPushButton(
                clicked=self.toggleSuspendResume)
        self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)

        layout.addWidget(self.m_suspendResumeButton)

        volumeBox = QHBoxLayout()
        volumeLabel = QLabel("Volume:")
        self.m_volumeSlider = QSlider(Qt.Horizontal, minimum=0, maximum=100,
                singleStep=10)
        self.m_volumeSlider.valueChanged.connect(self.volumeChanged)

        volumeBox.addWidget(volumeLabel)
        volumeBox.addWidget(self.m_volumeSlider)

        layout.addLayout(volumeBox)

        window = QWidget()
        window.setLayout(layout)

        self.setCentralWidget(window)

    def initializeAudio(self):
        self.m_pullTimer = QTimer(self)
        self.m_pullTimer.timeout.connect(self.pullTimerExpired)
        self.m_pullMode = True

        self.m_format = QAudioFormat()
        self.m_format.setSampleRate(self.DataSampleRateHz)
        self.m_format.setChannelCount(1)
        self.m_format.setSampleSize(16)
        self.m_format.setCodec('audio/pcm')
        self.m_format.setByteOrder(QAudioFormat.LittleEndian)
        self.m_format.setSampleType(QAudioFormat.SignedInt)

        info = QAudioDeviceInfo(QAudioDeviceInfo.defaultOutputDevice())
        if not info.isFormatSupported(self.m_format):
            qWarning("Default format not supported - trying to use nearest")
            self.m_format = info.nearestFormat(self.m_format)

        self.m_generator = Generator(self.m_format,
                self.DurationSeconds * 1000000, self.ToneSampleRateHz, self)

        self.createAudioOutput()

    def createAudioOutput(self):
        self.m_audioOutput = QAudioOutput(self.m_device, self.m_format)
        self.m_audioOutput.notify.connect(self.notified)
        self.m_audioOutput.stateChanged.connect(self.handleStateChanged)

        self.m_generator.start()
        self.m_audioOutput.start(self.m_generator)
        self.m_volumeSlider.setValue(self.m_audioOutput.volume() * 100)

    def deviceChanged(self, index):
        self.m_pullTimer.stop()
        self.m_generator.stop()
        self.m_audioOutput.stop()
        self.m_device = self.m_deviceBox.itemData(index)

        self.createAudioOutput()

    def volumeChanged(self, value):
        if self.m_audioOutput is not None:
            self.m_audioOutput.setVolume(value / 100.0)

    def notified(self):
        qWarning("bytesFree = %d, elapsedUSecs = %d, processedUSecs = %d" % (
                self.m_audioOutput.bytesFree(),
                self.m_audioOutput.elapsedUSecs(),
                self.m_audioOutput.processedUSecs()))

    def pullTimerExpired(self):
        if self.m_audioOutput is not None and self.m_audioOutput.state() != QAudio.StoppedState:
            chunks = self.m_audioOutput.bytesFree() // self.m_audioOutput.periodSize()
            for _ in range(chunks):
                data = self.m_generator.read(self.m_audioOutput.periodSize())
                if data is None or len(data) != self.m_audioOutput.periodSize():
                    break

                self.m_output.write(data)

    def toggleMode(self):
        self.m_pullTimer.stop()
        self.m_audioOutput.stop()

        if self.m_pullMode:
            self.m_modeButton.setText(self.PULL_MODE_LABEL)
            self.m_output = self.m_audioOutput.start()
            self.m_pullMode = False
            self.m_pullTimer.start(20)
        else:
            self.m_modeButton.setText(self.PUSH_MODE_LABEL)
            self.m_pullMode = True
            self.m_audioOutput.start(self.m_generator)

        self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)

    def toggleSuspendResume(self):
        if self.m_audioOutput.state() == QAudio.SuspendedState:
            qWarning("status: Suspended, resume()")
            self.m_audioOutput.resume()
            self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)
        elif self.m_audioOutput.state() == QAudio.ActiveState:
            qWarning("status: Active, suspend()")
            self.m_audioOutput.suspend()
            self.m_suspendResumeButton.setText(self.RESUME_LABEL)
        elif self.m_audioOutput.state() == QAudio.StoppedState:
            qWarning("status: Stopped, resume()")
            self.m_audioOutput.resume()
            self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)
        elif self.m_audioOutput.state() == QAudio.IdleState:
            qWarning("status: IdleState")

    stateMap = {
        QAudio.ActiveState: "ActiveState",
        QAudio.SuspendedState: "SuspendedState",
        QAudio.StoppedState: "StoppedState",
        QAudio.IdleState: "IdleState"}

    def handleStateChanged(self, state):
        qWarning("state = " + self.stateMap.get(state, "Unknown"))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Audio Output Test")

    audio = AudioTest()
    audio.show()

    sys.exit(app.exec_())
