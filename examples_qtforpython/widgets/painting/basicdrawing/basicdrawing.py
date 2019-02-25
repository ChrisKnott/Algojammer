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

"""PySide2 port of the widgets/painting/basicdrawing example from Qt v5.x, originating from PyQt"""

from PySide2.QtCore import QPoint, QRect, QSize, Qt, qVersion
from PySide2.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter,
        QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient)
from PySide2.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
        QLabel, QSpinBox, QWidget)

import basicdrawing_rc


class RenderArea(QWidget):
    points = QPolygon([
        QPoint(10, 80),
        QPoint(20, 10),
        QPoint(80, 30),
        QPoint(90, 70)
    ])

    Line, Points, Polyline, Polygon, Rect, RoundedRect, Ellipse, Arc, Chord, \
            Pie, Path, Text, Pixmap = range(13)

    def __init__(self, parent=None):
        super(RenderArea, self).__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()
        self.pixmap = QPixmap()

        self.shape = RenderArea.Polygon
        self.antialiased = False
        self.transformed = False
        self.pixmap.load(':/images/qt-logo.png')

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def minimumSizeHint(self):
        return QSize(100, 100)

    def sizeHint(self):
        return QSize(400, 200)

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def setPen(self, pen):
        self.pen = pen
        self.update()

    def setBrush(self, brush):
        self.brush = brush
        self.update()

    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def setTransformed(self, transformed):
        self.transformed = transformed
        self.update()

    def paintEvent(self, event):
        rect = QRect(10, 20, 80, 60)

        path = QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.cubicTo(80, 0, 50, 50, 80, 80)

        startAngle = 30 * 16
        arcLength = 120 * 16

        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        if self.antialiased:
            painter.setRenderHint(QPainter.Antialiasing)

        for x in range(0, self.width(), 100):
            for y in range(0, self.height(), 100):
                painter.save()
                painter.translate(x, y)
                if self.transformed:
                    painter.translate(50, 50)
                    painter.rotate(60.0)
                    painter.scale(0.6, 0.9)
                    painter.translate(-50, -50)

                if self.shape == RenderArea.Line:
                    painter.drawLine(rect.bottomLeft(), rect.topRight())
                elif self.shape == RenderArea.Points:
                    painter.drawPoints(RenderArea.points)
                elif self.shape == RenderArea.Polyline:
                    painter.drawPolyline(RenderArea.points)
                elif self.shape == RenderArea.Polygon:
                    painter.drawPolygon(RenderArea.points)
                elif self.shape == RenderArea.Rect:
                    painter.drawRect(rect)
                elif self.shape == RenderArea.RoundedRect:
                    painter.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)
                elif self.shape == RenderArea.Ellipse:
                    painter.drawEllipse(rect)
                elif self.shape == RenderArea.Arc:
                    painter.drawArc(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Chord:
                    painter.drawChord(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Pie:
                    painter.drawPie(rect, startAngle, arcLength)
                elif self.shape == RenderArea.Path:
                    painter.drawPath(path)
                elif self.shape == RenderArea.Text:
                    painter.drawText(rect, Qt.AlignCenter,
                                     "PySide 2\nQt %s" % qVersion())
                elif self.shape == RenderArea.Pixmap:
                    painter.drawPixmap(10, 10, self.pixmap)

                painter.restore()

        painter.setPen(self.palette().dark().color())
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))


IdRole = Qt.UserRole

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.renderArea = RenderArea()

        self.shapeComboBox = QComboBox()
        self.shapeComboBox.addItem("Polygon", RenderArea.Polygon)
        self.shapeComboBox.addItem("Rectangle", RenderArea.Rect)
        self.shapeComboBox.addItem("Rounded Rectangle", RenderArea.RoundedRect)
        self.shapeComboBox.addItem("Ellipse", RenderArea.Ellipse)
        self.shapeComboBox.addItem("Pie", RenderArea.Pie)
        self.shapeComboBox.addItem("Chord", RenderArea.Chord)
        self.shapeComboBox.addItem("Path", RenderArea.Path)
        self.shapeComboBox.addItem("Line", RenderArea.Line)
        self.shapeComboBox.addItem("Polyline", RenderArea.Polyline)
        self.shapeComboBox.addItem("Arc", RenderArea.Arc)
        self.shapeComboBox.addItem("Points", RenderArea.Points)
        self.shapeComboBox.addItem("Text", RenderArea.Text)
        self.shapeComboBox.addItem("Pixmap", RenderArea.Pixmap)

        shapeLabel = QLabel("&Shape:")
        shapeLabel.setBuddy(self.shapeComboBox)

        self.penWidthSpinBox = QSpinBox()
        self.penWidthSpinBox.setRange(0, 20)
        self.penWidthSpinBox.setSpecialValueText("0 (cosmetic pen)")

        penWidthLabel = QLabel("Pen &Width:")
        penWidthLabel.setBuddy(self.penWidthSpinBox)

        self.penStyleComboBox = QComboBox()
        self.penStyleComboBox.addItem("Solid", Qt.SolidLine)
        self.penStyleComboBox.addItem("Dash", Qt.DashLine)
        self.penStyleComboBox.addItem("Dot", Qt.DotLine)
        self.penStyleComboBox.addItem("Dash Dot", Qt.DashDotLine)
        self.penStyleComboBox.addItem("Dash Dot Dot", Qt.DashDotDotLine)
        self.penStyleComboBox.addItem("None", Qt.NoPen)

        penStyleLabel = QLabel("&Pen Style:")
        penStyleLabel.setBuddy(self.penStyleComboBox)

        self.penCapComboBox = QComboBox()
        self.penCapComboBox.addItem("Flat", Qt.FlatCap)
        self.penCapComboBox.addItem("Square", Qt.SquareCap)
        self.penCapComboBox.addItem("Round", Qt.RoundCap)

        penCapLabel = QLabel("Pen &Cap:")
        penCapLabel.setBuddy(self.penCapComboBox)

        self.penJoinComboBox = QComboBox()
        self.penJoinComboBox.addItem("Miter", Qt.MiterJoin)
        self.penJoinComboBox.addItem("Bevel", Qt.BevelJoin)
        self.penJoinComboBox.addItem("Round", Qt.RoundJoin)

        penJoinLabel = QLabel("Pen &Join:")
        penJoinLabel.setBuddy(self.penJoinComboBox)

        self.brushStyleComboBox = QComboBox()
        self.brushStyleComboBox.addItem("Linear Gradient",
                Qt.LinearGradientPattern)
        self.brushStyleComboBox.addItem("Radial Gradient",
                Qt.RadialGradientPattern)
        self.brushStyleComboBox.addItem("Conical Gradient",
                Qt.ConicalGradientPattern)
        self.brushStyleComboBox.addItem("Texture", Qt.TexturePattern)
        self.brushStyleComboBox.addItem("Solid", Qt.SolidPattern)
        self.brushStyleComboBox.addItem("Horizontal", Qt.HorPattern)
        self.brushStyleComboBox.addItem("Vertical", Qt.VerPattern)
        self.brushStyleComboBox.addItem("Cross", Qt.CrossPattern)
        self.brushStyleComboBox.addItem("Backward Diagonal", Qt.BDiagPattern)
        self.brushStyleComboBox.addItem("Forward Diagonal", Qt.FDiagPattern)
        self.brushStyleComboBox.addItem("Diagonal Cross", Qt.DiagCrossPattern)
        self.brushStyleComboBox.addItem("Dense 1", Qt.Dense1Pattern)
        self.brushStyleComboBox.addItem("Dense 2", Qt.Dense2Pattern)
        self.brushStyleComboBox.addItem("Dense 3", Qt.Dense3Pattern)
        self.brushStyleComboBox.addItem("Dense 4", Qt.Dense4Pattern)
        self.brushStyleComboBox.addItem("Dense 5", Qt.Dense5Pattern)
        self.brushStyleComboBox.addItem("Dense 6", Qt.Dense6Pattern)
        self.brushStyleComboBox.addItem("Dense 7", Qt.Dense7Pattern)
        self.brushStyleComboBox.addItem("None", Qt.NoBrush)

        brushStyleLabel = QLabel("&Brush Style:")
        brushStyleLabel.setBuddy(self.brushStyleComboBox)

        otherOptionsLabel = QLabel("Other Options:")
        self.antialiasingCheckBox = QCheckBox("&Antialiasing")
        self.transformationsCheckBox = QCheckBox("&Transformations")

        self.shapeComboBox.activated.connect(self.shapeChanged)
        self.penWidthSpinBox.valueChanged.connect(self.penChanged)
        self.penStyleComboBox.activated.connect(self.penChanged)
        self.penCapComboBox.activated.connect(self.penChanged)
        self.penJoinComboBox.activated.connect(self.penChanged)
        self.brushStyleComboBox.activated.connect(self.brushChanged)
        self.antialiasingCheckBox.toggled.connect(self.renderArea.setAntialiased)
        self.transformationsCheckBox.toggled.connect(self.renderArea.setTransformed)

        mainLayout = QGridLayout()
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(3, 1)
        mainLayout.addWidget(self.renderArea, 0, 0, 1, 4)
        mainLayout.setRowMinimumHeight(1, 6)
        mainLayout.addWidget(shapeLabel, 2, 1, Qt.AlignRight)
        mainLayout.addWidget(self.shapeComboBox, 2, 2)
        mainLayout.addWidget(penWidthLabel, 3, 1, Qt.AlignRight)
        mainLayout.addWidget(self.penWidthSpinBox, 3, 2)
        mainLayout.addWidget(penStyleLabel, 4, 1, Qt.AlignRight)
        mainLayout.addWidget(self.penStyleComboBox, 4, 2)
        mainLayout.addWidget(penCapLabel, 5, 1, Qt.AlignRight)
        mainLayout.addWidget(self.penCapComboBox, 5, 2)
        mainLayout.addWidget(penJoinLabel, 6, 1, Qt.AlignRight)
        mainLayout.addWidget(self.penJoinComboBox, 6, 2)
        mainLayout.addWidget(brushStyleLabel, 7, 1, Qt.AlignRight)
        mainLayout.addWidget(self.brushStyleComboBox, 7, 2)
        mainLayout.setRowMinimumHeight(8, 6)
        mainLayout.addWidget(otherOptionsLabel, 9, 1, Qt.AlignRight)
        mainLayout.addWidget(self.antialiasingCheckBox, 9, 2)
        mainLayout.addWidget(self.transformationsCheckBox, 10, 2)
        self.setLayout(mainLayout)

        self.shapeChanged()
        self.penChanged()
        self.brushChanged()
        self.antialiasingCheckBox.setChecked(True)

        self.setWindowTitle("Basic Drawing")

    def shapeChanged(self):
        shape = self.shapeComboBox.itemData(self.shapeComboBox.currentIndex(),
                IdRole)
        self.renderArea.setShape(shape)

    def penChanged(self):
        width = self.penWidthSpinBox.value()
        style = Qt.PenStyle(self.penStyleComboBox.itemData(
                self.penStyleComboBox.currentIndex(), IdRole))
        cap = Qt.PenCapStyle(self.penCapComboBox.itemData(
                self.penCapComboBox.currentIndex(), IdRole))
        join = Qt.PenJoinStyle(self.penJoinComboBox.itemData(
                self.penJoinComboBox.currentIndex(), IdRole))

        self.renderArea.setPen(QPen(Qt.blue, width, style, cap, join))

    def brushChanged(self):
        style = Qt.BrushStyle(self.brushStyleComboBox.itemData(
                self.brushStyleComboBox.currentIndex(), IdRole))

        if style == Qt.LinearGradientPattern:
            linearGradient = QLinearGradient(0, 0, 100, 100)
            linearGradient.setColorAt(0.0, Qt.white)
            linearGradient.setColorAt(0.2, Qt.green)
            linearGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(QBrush(linearGradient))
        elif style == Qt.RadialGradientPattern:
            radialGradient = QRadialGradient(50, 50, 50, 70, 70)
            radialGradient.setColorAt(0.0, Qt.white)
            radialGradient.setColorAt(0.2, Qt.green)
            radialGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(QBrush(radialGradient))
        elif style == Qt.ConicalGradientPattern:
            conicalGradient = QConicalGradient(50, 50, 150)
            conicalGradient.setColorAt(0.0, Qt.white)
            conicalGradient.setColorAt(0.2, Qt.green)
            conicalGradient.setColorAt(1.0, Qt.black)
            self.renderArea.setBrush(QBrush(conicalGradient))
        elif style == Qt.TexturePattern:
            self.renderArea.setBrush(QBrush(QPixmap(':/images/brick.png')))
        else:
            self.renderArea.setBrush(QBrush(Qt.green, style))


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
