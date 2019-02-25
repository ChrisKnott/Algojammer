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

"""PySide2 port of the corelib/threads/mandelbrot example from Qt v5.x, originating from PyQt"""

from PySide2.QtCore import (Signal, QMutex, QMutexLocker, QPoint, QSize, Qt,
        QThread, QWaitCondition)
from PySide2.QtGui import QColor, QImage, QPainter, QPixmap, qRgb
from PySide2.QtWidgets import QApplication, QWidget


DefaultCenterX = -0.647011
DefaultCenterY = -0.0395159
DefaultScale = 0.00403897

ZoomInFactor = 0.8
ZoomOutFactor = 1 / ZoomInFactor
ScrollStep = 20


class RenderThread(QThread):
    ColormapSize = 512

    renderedImage = Signal(QImage, float)

    def __init__(self, parent=None):
        super(RenderThread, self).__init__(parent)

        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.centerX = 0.0
        self.centerY = 0.0
        self.scaleFactor = 0.0
        self.resultSize = QSize()
        self.colormap = []

        self.restart = False
        self.abort = False

        for i in range(RenderThread.ColormapSize):
            self.colormap.append(self.rgbFromWaveLength(380.0 + (i * 400.0 / RenderThread.ColormapSize)))

    def stop(self):
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()

        self.wait(2000)

    def render(self, centerX, centerY, scaleFactor, resultSize):
        locker = QMutexLocker(self.mutex)

        self.centerX = centerX
        self.centerY = centerY
        self.scaleFactor = scaleFactor
        self.resultSize = resultSize

        if not self.isRunning():
            self.start(QThread.LowPriority)
        else:
            self.restart = True
            self.condition.wakeOne()

    def run(self):
        while True:
            self.mutex.lock()
            resultSize = self.resultSize
            scaleFactor = self.scaleFactor
            centerX = self.centerX
            centerY = self.centerY
            self.mutex.unlock()

            halfWidth = resultSize.width() // 2
            halfHeight = resultSize.height() // 2
            image = QImage(resultSize, QImage.Format_RGB32)

            NumPasses = 8
            curpass = 0

            while curpass < NumPasses:
                MaxIterations = (1 << (2 * curpass + 6)) + 32
                Limit = 4
                allBlack = True

                for y in range(-halfHeight, halfHeight):
                    if self.restart:
                        break
                    if self.abort:
                        return

                    ay = 1j * (centerY + (y * scaleFactor))

                    for x in range(-halfWidth, halfWidth):
                        c0 = centerX + (x * scaleFactor) + ay
                        c = c0
                        numIterations = 0

                        while numIterations < MaxIterations:
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break

                        if numIterations < MaxIterations:
                            image.setPixel(x + halfWidth, y + halfHeight,
                                           self.colormap[numIterations % RenderThread.ColormapSize])
                            allBlack = False
                        else:
                            image.setPixel(x + halfWidth, y + halfHeight, qRgb(0, 0, 0))

                if allBlack and curpass == 0:
                    curpass = 4
                else:
                    if not self.restart:
                        self.renderedImage.emit(image, scaleFactor)
                    curpass += 1

            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()

    def rgbFromWaveLength(self, wave):
        r = 0.0
        g = 0.0
        b = 0.0

        if wave >= 380.0 and wave <= 440.0:
            r = -1.0 * (wave - 440.0) / (440.0 - 380.0)
            b = 1.0
        elif wave >= 440.0 and wave <= 490.0:
            g = (wave - 440.0) / (490.0 - 440.0)
            b = 1.0
        elif wave >= 490.0 and wave <= 510.0:
            g = 1.0
            b = -1.0 * (wave - 510.0) / (510.0 - 490.0)
        elif wave >= 510.0 and wave <= 580.0:
            r = (wave - 510.0) / (580.0 - 510.0)
            g = 1.0
        elif wave >= 580.0 and wave <= 645.0:
            r = 1.0
            g = -1.0 * (wave - 645.0) / (645.0 - 580.0)
        elif wave >= 645.0 and wave <= 780.0:
            r = 1.0

        s = 1.0
        if wave > 700.0:
            s = 0.3 + 0.7 * (780.0 - wave) / (780.0 - 700.0)
        elif wave < 420.0:
            s = 0.3 + 0.7 * (wave - 380.0) / (420.0 - 380.0)

        r = pow(r * s, 0.8)
        g = pow(g * s, 0.8)
        b = pow(b * s, 0.8)

        return qRgb(r*255, g*255, b*255)


class MandelbrotWidget(QWidget):
    def __init__(self, parent=None):
        super(MandelbrotWidget, self).__init__(parent)

        self.thread = RenderThread()
        self.pixmap = QPixmap()
        self.pixmapOffset = QPoint()
        self.lastDragPos = QPoint()

        self.centerX = DefaultCenterX
        self.centerY = DefaultCenterY
        self.pixmapScale = DefaultScale
        self.curScale = DefaultScale

        self.thread.renderedImage.connect(self.updatePixmap)

        self.setWindowTitle("Mandelbrot")
        self.setCursor(Qt.CrossCursor)
        self.resize(550, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        if self.pixmap.isNull():
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter,
                    "Rendering initial image, please wait...")
            return

        if self.curScale == self.pixmapScale:
            painter.drawPixmap(self.pixmapOffset, self.pixmap)
        else:
            scaleFactor = self.pixmapScale / self.curScale
            newWidth = int(self.pixmap.width() * scaleFactor)
            newHeight = int(self.pixmap.height() * scaleFactor)
            newX = self.pixmapOffset.x() + (self.pixmap.width() - newWidth) / 2
            newY = self.pixmapOffset.y() + (self.pixmap.height() - newHeight) / 2

            painter.save()
            painter.translate(newX, newY)
            painter.scale(scaleFactor, scaleFactor)
            exposed, _ = painter.matrix().inverted()
            exposed = exposed.mapRect(self.rect()).adjusted(-1, -1, 1, 1)
            painter.drawPixmap(exposed, self.pixmap, exposed)
            painter.restore()

        text = "Use mouse wheel or the '+' and '-' keys to zoom. Press and " \
                "hold left mouse button to scroll."
        metrics = painter.fontMetrics()
        textWidth = metrics.width(text)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 127))
        painter.drawRect((self.width() - textWidth) / 2 - 5, 0, textWidth + 10,
                metrics.lineSpacing() + 5)
        painter.setPen(Qt.white)
        painter.drawText((self.width() - textWidth) / 2,
                metrics.leading() + metrics.ascent(), text)

    def resizeEvent(self, event):
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.zoom(ZoomInFactor)
        elif event.key() == Qt.Key_Minus:
            self.zoom(ZoomOutFactor)
        elif event.key() == Qt.Key_Left:
            self.scroll(-ScrollStep, 0)
        elif event.key() == Qt.Key_Right:
            self.scroll(+ScrollStep, 0)
        elif event.key() == Qt.Key_Down:
            self.scroll(0, -ScrollStep)
        elif event.key() == Qt.Key_Up:
            self.scroll(0, +ScrollStep)
        else:
            super(MandelbrotWidget, self).keyPressEvent(event)

    def wheelEvent(self, event):
        numDegrees = event.angleDelta().y() / 8
        numSteps = numDegrees / 15.0
        self.zoom(pow(ZoomInFactor, numSteps))

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.lastDragPos = QPoint(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QPoint(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QPoint()

            deltaX = (self.width() - self.pixmap.width()) / 2 - self.pixmapOffset.x()
            deltaY = (self.height() - self.pixmap.height()) / 2 - self.pixmapOffset.y()
            self.scroll(deltaX, deltaY)

    def updatePixmap(self, image, scaleFactor):
        if not self.lastDragPos.isNull():
            return

        self.pixmap = QPixmap.fromImage(image)
        self.pixmapOffset = QPoint()
        self.lastDragPosition = QPoint()
        self.pixmapScale = scaleFactor
        self.update()

    def zoom(self, zoomFactor):
        self.curScale *= zoomFactor
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale,
                self.size())

    def scroll(self, deltaX, deltaY):
        self.centerX += deltaX * self.curScale
        self.centerY += deltaY * self.curScale
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale,
                self.size())


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    widget = MandelbrotWidget()
    widget.show()
    r = app.exec_()
    widget.thread.stop()
    sys.exit(r)
