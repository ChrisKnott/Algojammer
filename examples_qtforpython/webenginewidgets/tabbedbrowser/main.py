#!/usr/bin/env python

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

"""PySide2 WebEngineWidgets Example"""

import sys
from bookmarkwidget import BookmarkWidget
from browsertabwidget import BrowserTabWidget
from downloadwidget import DownloadWidget
from findtoolbar import FindToolBar
from webengineview import QWebEnginePage, WebEngineView
from PySide2 import QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QCloseEvent, QKeySequence, QIcon
from PySide2.QtWidgets import (qApp, QAction, QApplication, QDesktopWidget,
    QDockWidget, QLabel, QLineEdit, QMainWindow, QMenu, QMenuBar, QPushButton,
    QStatusBar, QToolBar)
from PySide2.QtWebEngineWidgets import (QWebEngineDownloadItem, QWebEnginePage,
    QWebEngineView)

main_windows = []

def create_main_window():
    """Creates a MainWindow using 75% of the available screen resolution."""
    main_win = MainWindow()
    main_windows.append(main_win)
    available_geometry = app.desktop().availableGeometry(main_win)
    main_win.resize(available_geometry.width() * 2 / 3, available_geometry.height() * 2 / 3)
    main_win.show()
    return main_win

def create_main_window_with_browser():
    """Creates a MainWindow with a BrowserTabWidget."""
    main_win = create_main_window()
    return main_win.add_browser_tab()

class MainWindow(QMainWindow):
    """Provides the parent window that includes the BookmarkWidget,
    BrowserTabWidget, and a DownloadWidget, to offer the complete
    web browsing experience."""
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('PySide2 tabbed browser Example')

        self._tab_widget = BrowserTabWidget(create_main_window_with_browser)
        self._tab_widget.enabled_changed.connect(self._enabled_changed)
        self._tab_widget.download_requested.connect(self._download_requested)
        self.setCentralWidget(self._tab_widget)
        self.connect(self._tab_widget, QtCore.SIGNAL("url_changed(QUrl)"),
                     self.url_changed)

        self._bookmark_dock = QDockWidget()
        self._bookmark_dock.setWindowTitle('Bookmarks')
        self._bookmark_widget = BookmarkWidget()
        self._bookmark_widget.open_bookmark.connect(self.load_url)
        self._bookmark_widget.open_bookmark_in_new_tab.connect(self.load_url_in_new_tab)
        self._bookmark_dock.setWidget(self._bookmark_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._bookmark_dock)

        self._find_tool_bar = None

        self._actions = {}
        self._create_menu()

        self._tool_bar = QToolBar()
        self.addToolBar(self._tool_bar)
        for action in self._actions.values():
            if not action.icon().isNull():
                self._tool_bar.addAction(action)

        self._addres_line_edit = QLineEdit()
        self._addres_line_edit.setClearButtonEnabled(True)
        self._addres_line_edit.returnPressed.connect(self.load)
        self._tool_bar.addWidget(self._addres_line_edit)
        self._zoom_label = QLabel()
        self.statusBar().addPermanentWidget(self._zoom_label)
        self._update_zoom_label()

        self._bookmarksToolBar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self._bookmarksToolBar)
        self.insertToolBarBreak(self._bookmarksToolBar)
        self._bookmark_widget.changed.connect(self._update_bookmarks)
        self._update_bookmarks()

    def _update_bookmarks(self):
        self._bookmark_widget.populate_tool_bar(self._bookmarksToolBar)
        self._bookmark_widget.populate_other(self._bookmark_menu, 3)

    def _create_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "E&xit",
                             self, shortcut = "Ctrl+Q", triggered=qApp.quit)
        file_menu.addAction(exit_action)

        navigation_menu = self.menuBar().addMenu("&Navigation")

        style_icons = ':/qt-project.org/styles/commonstyle/images/'
        back_action = QAction(QIcon.fromTheme("go-previous",
                                             QIcon(style_icons + 'left-32.png')),
                             "Back", self,
                             shortcut = QKeySequence(QKeySequence.Back),
                             triggered = self._tab_widget.back)
        self._actions[QWebEnginePage.Back] = back_action
        back_action.setEnabled(False)
        navigation_menu.addAction(back_action)
        forward_action = QAction(QIcon.fromTheme("go-next",
                                                QIcon(style_icons + 'right-32.png')),
                                "Forward", self,
                                shortcut = QKeySequence(QKeySequence.Forward),
                                triggered = self._tab_widget.forward)
        forward_action.setEnabled(False)
        self._actions[QWebEnginePage.Forward] = forward_action

        navigation_menu.addAction(forward_action)
        reload_action = QAction(QIcon(style_icons + 'refresh-32.png'),
                               "Reload", self,
                               shortcut = QKeySequence(QKeySequence.Refresh),
                               triggered = self._tab_widget.reload)
        self._actions[QWebEnginePage.Reload] = reload_action
        reload_action.setEnabled(False)
        navigation_menu.addAction(reload_action)

        navigation_menu.addSeparator()

        new_tab_action = QAction("New Tab", self,
                             shortcut = 'Ctrl+T',
                             triggered = self.add_browser_tab)
        navigation_menu.addAction(new_tab_action)

        close_tab_action = QAction("Close Current Tab", self,
                                 shortcut = "Ctrl+W",
                                 triggered = self._close_current_tab)
        navigation_menu.addAction(close_tab_action)

        edit_menu = self.menuBar().addMenu("&Edit")

        find_action = QAction("Find", self,
                             shortcut = QKeySequence(QKeySequence.Find),
                             triggered = self._show_find)
        edit_menu.addAction(find_action)

        edit_menu.addSeparator()
        undo_action = QAction("Undo", self,
                             shortcut = QKeySequence(QKeySequence.Undo),
                             triggered = self._tab_widget.undo)
        self._actions[QWebEnginePage.Undo] = undo_action
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self,
                             shortcut = QKeySequence(QKeySequence.Redo),
                             triggered = self._tab_widget.redo)
        self._actions[QWebEnginePage.Redo] = redo_action
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction("Cut", self,
                            shortcut = QKeySequence(QKeySequence.Cut),
                            triggered = self._tab_widget.cut)
        self._actions[QWebEnginePage.Cut] = cut_action
        cut_action.setEnabled(False)
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self,
                             shortcut = QKeySequence(QKeySequence.Copy),
                             triggered = self._tab_widget.copy)
        self._actions[QWebEnginePage.Copy] = copy_action
        copy_action.setEnabled(False)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self,
                             shortcut = QKeySequence(QKeySequence.Paste),
                             triggered = self._tab_widget.paste)
        self._actions[QWebEnginePage.Paste] = paste_action
        paste_action.setEnabled(False)
        edit_menu.addAction(paste_action)

        edit_menu.addSeparator()

        select_all_action = QAction("Select All", self,
                                  shortcut = QKeySequence(QKeySequence.SelectAll),
                                  triggered = self._tab_widget.select_all)
        self._actions[QWebEnginePage.SelectAll] = select_all_action
        select_all_action.setEnabled(False)
        edit_menu.addAction(select_all_action)

        self._bookmark_menu = self.menuBar().addMenu("&Bookmarks")
        add_bookmark_action = QAction("&Add Bookmark", self,
                                    triggered = self._add_bookmark)
        self._bookmark_menu.addAction(add_bookmark_action)
        add_tool_bar_bookmark_action = QAction("&Add Bookmark to Tool Bar", self,
                                           triggered = self._add_tool_bar_bookmark)
        self._bookmark_menu.addAction(add_tool_bar_bookmark_action)
        self._bookmark_menu.addSeparator()

        tools_menu = self.menuBar().addMenu("&Tools")
        download_action = QAction("Open Downloads", self,
                                 triggered = DownloadWidget.open_download_directory)
        tools_menu.addAction(download_action)

        window_menu = self.menuBar().addMenu("&Window")

        window_menu.addAction(self._bookmark_dock.toggleViewAction())

        window_menu.addSeparator()

        zoom_in_action = QAction(QIcon.fromTheme("zoom-in"),
                               "Zoom In", self,
                               shortcut = QKeySequence(QKeySequence.ZoomIn),
                               triggered = self._zoom_in)
        window_menu.addAction(zoom_in_action)
        zoom_out_action = QAction(QIcon.fromTheme("zoom-out"),
                                "Zoom Out", self,
                                shortcut = QKeySequence(QKeySequence.ZoomOut),
                                triggered = self._zoom_out)
        window_menu.addAction(zoom_out_action)

        reset_zoom_action = QAction(QIcon.fromTheme("zoom-original"),
                                  "Reset Zoom", self,
                                  shortcut = "Ctrl+0",
                                  triggered = self._reset_zoom)
        window_menu.addAction(reset_zoom_action)

        about_menu = self.menuBar().addMenu("&About")
        about_action = QAction("About Qt", self,
                              shortcut = QKeySequence(QKeySequence.HelpContents),
                              triggered=qApp.aboutQt)
        about_menu.addAction(about_action)

    def add_browser_tab(self):
        return self._tab_widget.add_browser_tab()

    def _close_current_tab(self):
        if self._tab_widget.count() > 1:
            self._tab_widget.close_current_tab()
        else:
            self.close()

    def close_event(self, event):
        main_windows.remove(self)
        event.accept()

    def load(self):
        url_string = self._addres_line_edit.text().strip()
        if url_string:
            self.load_url_string(url_string)

    def load_url_string(self, url_s):
        url = QUrl.fromUserInput(url_s)
        if (url.isValid()):
            self.load_url(url)

    def load_url(self, url):
        self._tab_widget.load(url)

    def load_url_in_new_tab(self, url):
        self.add_browser_tab().load(url)

    def url_changed(self, url):
        self._addres_line_edit.setText(url.toString())

    def _enabled_changed(self, web_action, enabled):
        action = self._actions[web_action]
        if action:
            action.setEnabled(enabled)

    def _add_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_bookmark(url, title, icon)

    def _add_tool_bar_bookmark(self):
        index = self._tab_widget.currentIndex()
        if index >= 0:
            url = self._tab_widget.url()
            title = self._tab_widget.tabText(index)
            icon = self._tab_widget.tabIcon(index)
            self._bookmark_widget.add_tool_bar_bookmark(url, title, icon)

    def _zoom_in(self):
        new_zoom = self._tab_widget.zoom_factor() * 1.5
        if (new_zoom <= WebEngineView.maximum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _zoom_out(self):
        new_zoom = self._tab_widget.zoom_factor() / 1.5
        if (new_zoom >= WebEngineView.minimum_zoom_factor()):
            self._tab_widget.set_zoom_factor(new_zoom)
            self._update_zoom_label()

    def _reset_zoom(self):
        self._tab_widget.set_zoom_factor(1)
        self._update_zoom_label()

    def _update_zoom_label(self):
        percent = int(self._tab_widget.zoom_factor() * 100)
        self._zoom_label.setText("{}%".format(percent))

    def _download_requested(self, item):
        # Remove old downloads before opening a new one
        for old_download in self.statusBar().children():
            if type(old_download).__name__ == 'download_widget' and \
                old_download.state() != QWebEngineDownloadItem.DownloadInProgress:
                self.statusBar().removeWidget(old_download)
                del old_download

        item.accept()
        download_widget = download_widget(item)
        download_widget.removeRequested.connect(self._remove_download_requested,
                                               Qt.QueuedConnection)
        self.statusBar().addWidget(download_widget)

    def _remove_download_requested(self):
            download_widget = self.sender()
            self.statusBar().removeWidget(download_widget)
            del download_widget

    def _show_find(self):
        if self._find_tool_bar is None:
            self._find_tool_bar = FindToolBar()
            self._find_tool_bar.find.connect(self._tab_widget.find)
            self.addToolBar(Qt.BottomToolBarArea, self._find_tool_bar)
        else:
            self._find_tool_bar.show()
        self._find_tool_bar.focus_find()

    def write_bookmarks(self):
        self._bookmark_widget.write_bookmarks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = create_main_window()
    initial_urls = sys.argv[1:]
    if not initial_urls:
        initial_urls.append('http://qt.io')
    for url in initial_urls:
        main_win.load_url_in_new_tab(QUrl.fromUserInput(url))
    exit_code = app.exec_()
    main_win.write_bookmarks()
    sys.exit(exit_code)
