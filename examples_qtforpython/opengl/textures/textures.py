#!/usr/bin/env python

############################################################################
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
############################################################################

"""PySide2 port of the opengl/textures example from Qt v5.x"""

import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

try:
    from OpenGL.GL import *
except ImportError:
    app = QtWidgets.QApplication(sys.argv)
    messageBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "OpenGL textures",
                                       "PyOpenGL must be installed to run this example.",
                                       QtWidgets.QMessageBox.Close)
    messageBox.setDetailedText("Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)

import textures_rc


class GLWidget(QtOpenGL.QGLWidget):
    sharedObject = 0
    refCount = 0

    coords = (
        ( ( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 ) ),
        ( ( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 ) ),
        ( ( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 ) ),
        ( ( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 ) ),
        ( ( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 ) ),
        ( ( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ) )
    )

    clicked = QtCore.Signal()

    def __init__(self, parent, shareWidget):
        QtOpenGL.QGLWidget.__init__(self, parent, shareWidget)

        self.clearColor = QtCore.Qt.black
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.clearColor = QtGui.QColor()
        self.lastPos = QtCore.QPoint()

    def freeGLResources(self):
        GLWidget.refCount -= 1
        if GLWidget.refCount == 0:
            self.makeCurrent()
            glDeleteLists(self.__class__.sharedObject, 1)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def rotateBy(self, xAngle, yAngle, zAngle):
        self.xRot = (self.xRot + xAngle) % 5760
        self.yRot = (self.yRot + yAngle) % 5760
        self.zRot = (self.zRot + zAngle) % 5760
        self.updateGL()

    def setClearColor(self, color):
        self.clearColor = color
        self.updateGL()

    def initializeGL(self):
        if not GLWidget.sharedObject:
            self.textures = []
            for i in range(6):
                self.textures.append(self.bindTexture(QtGui.QPixmap(":/images/side%d.png" % (i + 1))))
            GLWidget.sharedObject = self.makeObject()
        GLWidget.refCount += 1

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

    def paintGL(self):
        self.qglClearColor(self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -10.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glCallList(GLWidget.sharedObject)

    def resizeGL(self, width, height):
        side = min(width, height)
        glViewport(int((width - side) / 2), int((height - side) / 2), side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.rotateBy(8 * dy, 8 * dx, 0)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.rotateBy(8 * dy, 0, 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def makeObject(self):
        dlist = glGenLists(1)
        glNewList(dlist, GL_COMPILE)

        for i in range(6):
            glBindTexture(GL_TEXTURE_2D, self.textures[i])

            glBegin(GL_QUADS)
            for j in range(4):
                tx = {False: 0, True: 1}[j == 0 or j == 3]
                ty = {False: 0, True: 1}[j == 0 or j == 1]
                glTexCoord2d(tx, ty)
                glVertex3d(0.2 * GLWidget.coords[i][j][0],
                           0.2 * GLWidget.coords[i][j][1],
                           0.2 * GLWidget.coords[i][j][2])

            glEnd()

        glEndList()
        return dlist


class Window(QtWidgets.QWidget):
    NumRows = 2
    NumColumns = 3

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        mainLayout = QtWidgets.QGridLayout()
        self.glWidgets = []

        for i in range(Window.NumRows):
            self.glWidgets.append([])
            for j in range(Window.NumColumns):
                self.glWidgets[i].append(None)

        for i in range(Window.NumRows):
            for j in range(Window.NumColumns):
                clearColor = QtGui.QColor()
                clearColor.setHsv(((i * Window.NumColumns) + j) * 255
                                  / (Window.NumRows * Window.NumColumns - 1),
                                  255, 63)

                self.glWidgets[i][j] = GLWidget(self, self.glWidgets[0][0])
                self.glWidgets[i][j].setClearColor(clearColor)
                self.glWidgets[i][j].rotateBy(+42 * 16, +42 * 16, -21 * 16)
                mainLayout.addWidget(self.glWidgets[i][j], i, j)

                self.glWidgets[i][j].clicked.connect(self.setCurrentGlWidget)
                QtWidgets.qApp.lastWindowClosed.connect(self.glWidgets[i][j].freeGLResources)

        self.setLayout(mainLayout)

        self.currentGlWidget = self.glWidgets[0][0]

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rotateOneStep)
        timer.start(20)

        self.setWindowTitle(self.tr("Textures"))

    def setCurrentGlWidget(self):
        self.currentGlWidget = self.sender()

    def rotateOneStep(self):
        if self.currentGlWidget:
            self.currentGlWidget.rotateBy(+2 * 16, +2 * 16, -1 * 16)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
