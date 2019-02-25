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

import json, os, warnings

from PySide2 import QtCore
from PySide2.QtCore import (QDir, QFileInfo, QModelIndex, QStandardPaths, Qt,
    QUrl)
from PySide2.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (QAction, QDockWidget, QMenu, QMessageBox,
    QToolBar, QTreeView, QWidget)

_url_role = Qt.UserRole + 1

# Default bookmarks as an array of arrays which is the form
# used to read from/write to a .json bookmarks file
_default_bookmarks = [
    ['Tool Bar'],
    ['http://qt.io', 'Qt', ':/qt-project.org/qmessagebox/images/qtlogo-64.png'],
    ['https://download.qt.io/snapshots/ci/pyside/', 'Downloads'],
    ['https://doc-snapshots.qt.io/qtforpython/', 'Documentation'],
    ['https://bugreports.qt.io/projects/PYSIDE/', 'Bug Reports'],
    ['https://www.python.org/', 'Python', None],
    ['https://wiki.qt.io/PySide2', 'Qt for Python', None],
    ['Other Bookmarks']
]

def _config_dir():
    return '{}/QtForPythonBrowser'.format(
        QStandardPaths.writableLocation(QStandardPaths.ConfigLocation))

_bookmark_file = 'bookmarks.json'

def _create_folder_item(title):
    result = QStandardItem(title)
    result.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    return result

def _create_item(url, title, icon):
    result = QStandardItem(title)
    result.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    result.setData(url, _url_role)
    if icon is not None:
        result.setIcon(icon)
    return result

# Create the model from an array of arrays
def _create_model(parent, serialized_bookmarks):
    result = QStandardItemModel(0, 1, parent)
    last_folder_item = None
    for entry in serialized_bookmarks:
        if len(entry) == 1:
            last_folder_item = _create_folder_item(entry[0])
            result.appendRow(last_folder_item)
        else:
            url = QUrl.fromUserInput(entry[0])
            title = entry[1]
            icon = QIcon(entry[2]) if len(entry) > 2 and entry[2] else None
            last_folder_item.appendRow(_create_item(url, title, icon))
    return result

# Serialize model into an array of arrays, writing out the icons
# into .png files under directory in the process
def _serialize_model(model, directory):
    result = []
    folder_count = model.rowCount()
    for f in range(0, folder_count):
        folder_item = model.item(f)
        result.append([folder_item.text()])
        item_count = folder_item.rowCount()
        for i in range(0, item_count):
            item = folder_item.child(i)
            entry = [item.data(_url_role).toString(), item.text()]
            icon = item.icon()
            if not icon.isNull():
                icon_sizes = icon.availableSizes()
                largest_size = icon_sizes[len(icon_sizes) - 1]
                icon_file_name = '{}/icon{:02}_{:02}_{}.png'.format(directory,
                               f, i, largest_size.width())
                icon.pixmap(largest_size).save(icon_file_name, 'PNG')
                entry.append(icon_file_name)
            result.append(entry)
    return result

# Bookmarks as a tree view to be used in a dock widget with
# functionality to persist and populate tool bars and menus.
class BookmarkWidget(QTreeView):
    """Provides a tree view to manage the bookmarks."""

    open_bookmark = QtCore.Signal(QUrl)
    open_bookmark_in_new_tab = QtCore.Signal(QUrl)
    changed = QtCore.Signal()

    def __init__(self):
        super(BookmarkWidget, self).__init__()
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self._model = _create_model(self, self._read_bookmarks())
        self.setModel(self._model)
        self.expandAll()
        self.activated.connect(self._activated)
        self._model.rowsInserted.connect(self._changed)
        self._model.rowsRemoved.connect(self._changed)
        self._model.dataChanged.connect(self._changed)
        self._modified = False

    def _changed(self):
        self._modified = True
        self.changed.emit()

    def _activated(self, index):
        item = self._model.itemFromIndex(index)
        self.open_bookmark.emit(item.data(_url_role))

    def _action_activated(self, index):
        action = self.sender()
        self.open_bookmark.emit(action.data())

    def _tool_bar_item(self):
        return self._model.item(0, 0)

    def _other_item(self):
        return self._model.item(1, 0)

    def add_bookmark(self, url, title, icon):
        self._other_item().appendRow(_create_item(url, title, icon))

    def add_tool_bar_bookmark(self, url, title, icon):
        self._tool_bar_item().appendRow(_create_item(url, title, icon))

    # Synchronize the bookmarks under parent_item to a target_object
    # like QMenu/QToolBar, which has a list of actions. Update
    # the existing actions, append new ones if needed or hide
    # superfluous ones
    def _populate_actions(self, parent_item, target_object, first_action):
        existing_actions = target_object.actions()
        existing_action_count = len(existing_actions)
        a = first_action
        row_count = parent_item.rowCount()
        for r in range(0, row_count):
            item = parent_item.child(r)
            title = item.text()
            icon = item.icon()
            url = item.data(_url_role)
            if a < existing_action_count:
                action = existing_actions[a]
                if (title != action.toolTip()):
                    action.setText(BookmarkWidget.short_title(title))
                    action.setIcon(icon)
                    action.setToolTip(title)
                    action.setData(url)
                    action.setVisible(True)
            else:
                action = target_object.addAction(icon, BookmarkWidget.short_title(title))
                action.setToolTip(title)
                action.setData(url)
                action.triggered.connect(self._action_activated)
            a = a + 1
        while a < existing_action_count:
            existing_actions[a].setVisible(False)
            a = a + 1

    def populate_tool_bar(self, tool_bar):
        self._populate_actions(self._tool_bar_item(), tool_bar, 0)

    def populate_other(self, menu, first_action):
        self._populate_actions(self._other_item(), menu, first_action)

    def _current_item(self):
        index = self.currentIndex()
        if index.isValid():
            item = self._model.itemFromIndex(index)
            if item.parent(): # exclude top level items
                return item
        return None

    def context_menu_event(self, event):
        context_menu = QMenu()
        open_in_new_tab_action = context_menu.addAction("Open in New Tab")
        remove_action = context_menu.addAction("Remove...")
        current_item = self._current_item()
        open_in_new_tab_action.setEnabled(current_item is not None)
        remove_action.setEnabled(current_item is not None)
        chosen_action = context_menu.exec_(event.globalPos())
        if chosen_action == open_in_new_tab_action:
            self.open_bookmarkInNewTab.emit(current_item.data(_url_role))
        elif chosen_action == remove_action:
            self._remove_item(current_item)

    def _remove_item(self, item):
        button = QMessageBox.question(self, "Remove",
            "Would you like to remove \"{}\"?".format(item.text()),
            QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            item.parent().removeRow(item.row())

    def write_bookmarks(self):
        if not self._modified:
            return
        dir_path = _config_dir()
        native_dir_path = QDir.toNativeSeparators(dir_path)
        dir = QFileInfo(dir_path)
        if not dir.isDir():
            print('Creating {}...'.format(native_dir_path))
            if not QDir(dir.absolutePath()).mkpath(dir.fileName()):
                warnings.warn('Cannot create {}.'.format(native_dir_path),
                              RuntimeWarning)
                return
        serialized_model = _serialize_model(self._model, dir_path)
        bookmark_file_name = os.path.join(native_dir_path, _bookmark_file)
        print('Writing {}...'.format(bookmark_file_name))
        with open(bookmark_file_name, 'w') as bookmark_file:
            json.dump(serialized_model, bookmark_file, indent = 4)

    def _read_bookmarks(self):
        bookmark_file_name = os.path.join(QDir.toNativeSeparators(_config_dir()),
                                        _bookmark_file)
        if os.path.exists(bookmark_file_name):
            print('Reading {}...'.format(bookmark_file_name))
            return json.load(open(bookmark_file_name))
        return _default_bookmarks

    # Return a short title for a bookmark action,
    # "Qt | Cross Platform.." -> "Qt"
    @staticmethod
    def short_title(t):
        i = t.find(' | ')
        if i == -1:
            i = t.find(' - ')
        return t[0:i] if i != -1 else t
