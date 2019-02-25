#############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
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

from PySide2 import QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import (QAction, QCheckBox, QDockWidget, QHBoxLayout,
    QLabel, QLineEdit, QToolBar, QToolButton, QWidget)
from PySide2.QtWebEngineWidgets import QWebEnginePage

# A Find tool bar (bottom area)
class FindToolBar(QToolBar):

    find = QtCore.Signal(str, QWebEnginePage.FindFlags)

    def __init__(self):
        super(FindToolBar, self).__init__()
        self._line_edit = QLineEdit()
        self._line_edit.setClearButtonEnabled(True)
        self._line_edit.setPlaceholderText("Find...")
        self._line_edit.setMaximumWidth(300)
        self._line_edit.returnPressed.connect(self._find_next)
        self.addWidget(self._line_edit)

        self._previous_button = QToolButton()
        self._previous_button.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/up-32.png'))
        self._previous_button.clicked.connect(self._find_previous)
        self.addWidget(self._previous_button)

        self._next_button = QToolButton()
        self._next_button.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/down-32.png'))
        self._next_button.clicked.connect(self._find_next)
        self.addWidget(self._next_button)

        self._case_sensitive_checkbox = QCheckBox('Case Sensitive')
        self.addWidget(self._case_sensitive_checkbox)

        self._hideButton = QToolButton()
        self._hideButton.setShortcut(QKeySequence(Qt.Key_Escape))
        self._hideButton.setIcon(QIcon(':/qt-project.org/styles/macstyle/images/closedock-16.png'))
        self._hideButton.clicked.connect(self.hide)
        self.addWidget(self._hideButton)

    def focus_find(self):
        self._line_edit.setFocus()

    def _emit_find(self, backward):
        needle =  self._line_edit.text().strip()
        if needle:
            flags = QWebEnginePage.FindFlags()
            if self._case_sensitive_checkbox.isChecked():
                flags |= QWebEnginePage.FindCaseSensitively
            if backward:
                flags |= QWebEnginePage.FindBackward
            self.find.emit(needle, flags)

    def _find_next(self):
        self._emit_find(False)

    def _find_previous(self):
        self._emit_find(True)
