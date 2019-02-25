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

from functools import partial
import sys

from bookmarkwidget import BookmarkWidget
from webengineview import WebEngineView
from PySide2 import QtCore
from PySide2.QtCore import QPoint, Qt, QUrl
from PySide2.QtWidgets import (QAction, QMenu, QTabBar, QTabWidget)
from PySide2.QtWebEngineWidgets import (QWebEngineDownloadItem,
    QWebEnginePage, QWebEngineProfile)

class BrowserTabWidget(QTabWidget):
    """Enables having several tabs with QWebEngineView."""

    url_changed = QtCore.Signal(QUrl)
    enabled_changed = QtCore.Signal(QWebEnginePage.WebAction, bool)
    download_requested = QtCore.Signal(QWebEngineDownloadItem)

    def __init__(self, window_factory_function):
        super(BrowserTabWidget, self).__init__()
        self.setTabsClosable(True)
        self._window_factory_function = window_factory_function
        self._webengineviews = []
        self.currentChanged.connect(self._current_changed)
        self.tabCloseRequested.connect(self.handle_tab_close_request)
        self._actions_enabled = {}
        for web_action in WebEngineView.web_actions():
            self._actions_enabled[web_action] = False

        tab_bar = self.tabBar()
        tab_bar.setSelectionBehaviorOnRemove(QTabBar.SelectPreviousTab)
        tab_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        tab_bar.customContextMenuRequested.connect(self._handle_tab_context_menu)

    def add_browser_tab(self):
        factory_func = partial(BrowserTabWidget.add_browser_tab, self)
        web_engine_view = WebEngineView(factory_func, self._window_factory_function)
        index = self.count()
        self._webengineviews.append(web_engine_view)
        title = 'Tab {}'.format(index + 1)
        self.addTab(web_engine_view, title)
        page = web_engine_view.page()
        page.titleChanged.connect(self._title_changed)
        page.iconChanged.connect(self._icon_changed)
        page.profile().downloadRequested.connect(self._download_requested)
        web_engine_view.urlChanged.connect(self._url_changed)
        web_engine_view.enabled_changed.connect(self._enabled_changed)
        self.setCurrentIndex(index)
        return web_engine_view

    def load(self, url):
        index = self.currentIndex()
        if index >= 0 and url.isValid():
            self._webengineviews[index].setUrl(url)

    def find(self, needle, flags):
        index = self.currentIndex()
        if index >= 0:
            self._webengineviews[index].page().findText(needle, flags)

    def url(self):
        index = self.currentIndex()
        return self._webengineviews[index].url() if index >= 0 else QUrl()

    def _url_changed(self, url):
        index = self.currentIndex()
        if index >= 0 and self._webengineviews[index] == self.sender():
                self.url_changed.emit(url)

    def _title_changed(self, title):
        index = self._index_of_page(self.sender())
        if (index >= 0):
            self.setTabText(index, BookmarkWidget.short_title(title))

    def _icon_changed(self, icon):
        index = self._index_of_page(self.sender())
        if (index >= 0):
            self.setTabIcon(index, icon)

    def _enabled_changed(self, web_action, enabled):
        index = self.currentIndex()
        if index >= 0 and self._webengineviews[index] == self.sender():
            self._check_emit_enabled_changed(web_action, enabled)

    def _check_emit_enabled_changed(self, web_action, enabled):
        if enabled != self._actions_enabled[web_action]:
            self._actions_enabled[web_action] = enabled
            self.enabled_changed.emit(web_action, enabled)

    def _current_changed(self, index):
        self._update_actions(index)
        self.url_changed.emit(self.url())

    def _update_actions(self, index):
        if index >= 0 and index < len(self._webengineviews):
            view = self._webengineviews[index]
            for web_action in WebEngineView.web_actions():
                enabled = view.is_web_action_enabled(web_action)
                self._check_emit_enabled_changed(web_action, enabled)

    def back(self):
        self._trigger_action(QWebEnginePage.Back)

    def forward(self):
        self._trigger_action(QWebEnginePage.Forward)

    def reload(self):
        self._trigger_action(QWebEnginePage.Reload)

    def undo(self):
        self._trigger_action(QWebEnginePage.Undo)

    def redo(self):
        self._trigger_action(QWebEnginePage.Redo)

    def cut(self):
        self._trigger_action(QWebEnginePage.Cut)

    def copy(self):
        self._trigger_action(QWebEnginePage.Copy)

    def paste(self):
        self._trigger_action(QWebEnginePage.Paste)

    def select_all(self):
        self._trigger_action(QWebEnginePage.SelectAll)

    def zoom_factor(self):
        return self._webengineviews[0].zoomFactor() if self._webengineviews else 1.0

    def set_zoom_factor(self, z):
        for w in self._webengineviews:
            w.setZoomFactor(z)

    def _handle_tab_context_menu(self, point):
        index = self.tabBar().tabAt(point)
        if index < 0:
            return
        tab_count = len(self._webengineviews)
        context_menu = QMenu()
        duplicate_tab_action = context_menu.addAction("Duplicate Tab")
        close_other_tabs_action = context_menu.addAction("Close Other Tabs")
        close_other_tabs_action.setEnabled(tab_count > 1)
        close_tabs_to_the_right_action = context_menu.addAction("Close Tabs to the Right")
        close_tabs_to_the_right_action.setEnabled(index < tab_count - 1)
        close_tab_action = context_menu.addAction("&Close Tab")
        chosen_action = context_menu.exec_(self.tabBar().mapToGlobal(point))
        if chosen_action == duplicate_tab_action:
            current_url = self.url()
            self.add_browser_tab().load(current_url)
        elif chosen_action == close_other_tabs_action:
            for t in range(tab_count - 1, -1, -1):
                if t != index:
                     self.handle_tab_close_request(t)
        elif chosen_action == close_tabs_to_the_right_action:
            for t in range(tab_count - 1, index, -1):
                self.handle_tab_close_request(t)
        elif chosen_action == close_tab_action:
            self.handle_tab_close_request(index)

    def handle_tab_close_request(self, index):
        if (index >= 0 and self.count() > 1):
            self._webengineviews.remove(self._webengineviews[index])
            self.removeTab(index)

    def close_current_tab(self):
        self.handle_tab_close_request(self.currentIndex())

    def _trigger_action(self, action):
        index = self.currentIndex()
        if index >= 0:
            self._webengineviews[index].page().triggerAction(action)

    def _index_of_page(self, web_page):
        for p in range(0, len(self._webengineviews)):
            if (self._webengineviews[p].page() == web_page):
                return p
        return -1

    def _download_requested(self, item):
        self.downloadRequested.emit(item)
