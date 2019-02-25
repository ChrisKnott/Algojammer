#!/usr/bin/env python
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''Demonstrates how to handle a platform-specific event not defined in
pyglet by subclassing Window.  This is not for the faint-hearted!

A message will be printed to stdout when the following events are caught:

 - On Mac OS X, the window drag region is clicked.
 - On Windows, the display resolution is changed.
 - On Linux, the window properties are changed.

'''

from __future__ import print_function

import pyglet

# Check for Carbon (OS X)
try:
    from pyglet.window.carbon import *
    _have_carbon = True
except ImportError:
    _have_carbon = False

# Check for Win32
try:
    from pyglet.window.win32 import *
    from pyglet.window.win32.constants import *
    _have_win32 = True
except ImportError:
    _have_win32 = False

# Check for Xlib (Linux)
try:
    from pyglet.window.xlib import *
    _have_xlib = True
except ImportError:
    _have_xlib = False


# Subclass Window
class MyWindow(pyglet.window.Window):
    if _have_carbon:
        @CarbonEventHandler(kEventClassWindow, kEventWindowClickDragRgn)
        def _on_window_click_drag_rgn(self, next_handler, event, data):
            print('Clicked drag rgn.')
            carbon.CallNextEventHandler(next_handler, event)
            return noErr

    if _have_win32:
        @Win32EventHandler(WM_DISPLAYCHANGE)
        def _on_window_display_change(self, msg, lParam, wParam):
            print('Display resolution changed.')
            return 0

    if _have_xlib:
        @XlibEventHandler(xlib.PropertyNotify)
        def _on_window_property_notify(self, event):
            print('Property notify.')

if __name__ == '__main__':
    window = MyWindow()
    pyglet.app.run()
