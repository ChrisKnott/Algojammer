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

"""PySide2 port of the opengl/contextinfo example from Qt v5.x"""

import numpy
import sys

from PySide2.QtCore import QLibraryInfo, QSize, QTimer, Qt
from PySide2.QtGui import (QMatrix4x4, QOpenGLBuffer, QOpenGLContext, QOpenGLShader,
    QOpenGLShaderProgram, QOpenGLVertexArrayObject, QSurfaceFormat, QWindow)
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QMessageBox, QPlainTextEdit,
    QWidget)
from PySide2.support import VoidPtr
try:
    from OpenGL import GL
except ImportError:
    app = QApplication(sys.argv)
    messageBox = QMessageBox(QMessageBox.Critical, "ContextInfo",
                             "PyOpenGL must be installed to run this example.",
                             QMessageBox.Close)
    messageBox.setDetailedText("Run:\npip install PyOpenGL PyOpenGL_accelerate")
    messageBox.exec_()
    sys.exit(1)

vertexShaderSource110 = """
#version 110
attribute highp vec4 posAttr;
attribute lowp vec4 colAttr;
varying lowp vec4 col;
uniform highp mat4 matrix;
void main() {
   col = colAttr;
   gl_Position = matrix * posAttr;
}
"""

fragmentShaderSource110 = """
#version 110
varying lowp vec4 col;
void main() {
   gl_FragColor = col;
}
"""

vertexShaderSource = """
#version 150
in vec4 posAttr;
in vec4 colAttr;
out vec4 col;
uniform mat4 matrix;
void main() {
   col = colAttr;
   gl_Position = matrix * posAttr;
}
"""

fragmentShaderSource = """
#version 150
in vec4 col;
out vec4 fragColor;
void main() {
   fragColor = col;
}
"""

vertices = numpy.array([0, 0.707, -0.5, -0.5, 0.5, -0.5], dtype = numpy.float32)
colors = numpy.array([1, 0, 0, 0, 1, 0, 0, 0, 1], dtype = numpy.float32)

class RenderWindow(QWindow):
    def __init__(self, format):
        super(RenderWindow, self).__init__()
        self.setSurfaceType(QWindow.OpenGLSurface)
        self.setFormat(format)
        self.context = QOpenGLContext(self)
        self.context.setFormat(self.requestedFormat())
        if not self.context.create():
            raise Exception("Unable to create GL context")
        self.program = None
        self.timer = None
        self.angle = 0

    def initGl(self):
        self.program = QOpenGLShaderProgram(self)
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer()

        format = self.context.format()
        useNewStyleShader = format.profile() == QSurfaceFormat.CoreProfile
        # Try to handle 3.0 & 3.1 that do not have the core/compatibility profile
        # concept 3.2+ has. This may still fail since version 150 (3.2) is
        # specified in the sources but it's worth a try.
        if (format.renderableType() == QSurfaceFormat.OpenGL and format.majorVersion() == 3
            and format.minorVersion() <= 1):
            useNewStyleShader = not format.testOption(QSurfaceFormat.DeprecatedFunctions)

        vertexShader = vertexShaderSource if useNewStyleShader else vertexShaderSource110
        fragmentShader = fragmentShaderSource if useNewStyleShader else fragmentShaderSource110
        if not self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertexShader):
            raise Exception("Vertex shader could not be added: {} ({})".format(self.program.log(), vertexShader))
        if not self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragmentShader):
            raise Exception("Fragment shader could not be added: {} ({})".format(self.program.log(), fragmentShader))
        if not self.program.link():
            raise Exception("Could not link shaders: {}".format(self.program.log()))

        self.posAttr = self.program.attributeLocation("posAttr")
        self.colAttr = self.program.attributeLocation("colAttr")
        self.matrixUniform = self.program.uniformLocation("matrix")

        self.vbo.create()
        self.vbo.bind()
        self.verticesData = vertices.tobytes()
        self.colorsData = colors.tobytes()
        verticesSize = 4 * vertices.size
        colorsSize = 4 * colors.size
        self.vbo.allocate(VoidPtr(self.verticesData), verticesSize + colorsSize)
        self.vbo.write(verticesSize, VoidPtr(self.colorsData), colorsSize)
        self.vbo.release()

        vaoBinder = QOpenGLVertexArrayObject.Binder(self.vao)
        if self.vao.isCreated(): # have VAO support, use it
            self.setupVertexAttribs()

    def setupVertexAttribs(self):
        self.vbo.bind()
        self.program.setAttributeBuffer(self.posAttr, GL.GL_FLOAT, 0, 2)
        self.program.setAttributeBuffer(self.colAttr, GL.GL_FLOAT, 4 * vertices.size, 3)
        self.program.enableAttributeArray(self.posAttr)
        self.program.enableAttributeArray(self.colAttr)
        self.vbo.release()

    def exposeEvent(self, event):
        if self.isExposed():
            self.render()
            if self.timer is None:
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.slotTimer)
                self.timer.start(10)

    def render(self):
        if not self.context.makeCurrent(self):
            raise Exception("makeCurrent() failed")
        functions = self.context.functions()
        if self.program is None:
            functions.glEnable(GL.GL_DEPTH_TEST)
            functions.glClearColor(0, 0, 0, 1)
            self.initGl()

        functions.glViewport(0, 0, self.width(), self.height())
        functions.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.program.bind()
        matrix = QMatrix4x4()
        matrix.perspective(60, 4 / 3, 0.1, 100)
        matrix.translate(0, 0, -2)
        matrix.rotate(self.angle, 0, 1, 0)
        self.program.setUniformValue(self.matrixUniform, matrix)

        if self.vao.isCreated():
            self.vao.bind()
        else: # no VAO support, set the vertex attribute arrays now
            self.setupVertexAttribs()

        functions.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        self.vao.release()
        self.program.release()

        # swapInterval is 1 by default which means that swapBuffers() will (hopefully) block
        # and wait for vsync.
        self.context.swapBuffers(self)
        self.context.doneCurrent()

    def slotTimer(self):
        self.render()
        self.angle += 1

    def glInfo(self):
        if not self.context.makeCurrent(self):
            raise Exception("makeCurrent() failed")
        functions = self.context.functions()
        text = "Vendor: {}\nRenderer: {}\nVersion: {}\nShading language: {}".format(
               functions.glGetString(GL.GL_VENDOR), functions.glGetString(GL.GL_RENDERER),
               functions.glGetString(GL.GL_VERSION),
               functions.glGetString(GL.GL_SHADING_LANGUAGE_VERSION))
        self.context.doneCurrent()
        return text

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        hBoxLayout = QHBoxLayout(self)
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setMinimumWidth(400)
        self.plainTextEdit.setReadOnly(True)
        hBoxLayout.addWidget(self.plainTextEdit)
        self.renderWindow = RenderWindow(QSurfaceFormat())
        container = QWidget.createWindowContainer(self.renderWindow)
        container.setMinimumSize(QSize(400, 400))
        hBoxLayout.addWidget(container)

    def updateDescription(self):
        text = "{}\n\nPython {}\n\n{}".format(QLibraryInfo.build(), sys.version,
                                              self.renderWindow.glInfo())
        self.plainTextEdit.setPlainText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    mainWindow.updateDescription()
    sys.exit(app.exec_())
