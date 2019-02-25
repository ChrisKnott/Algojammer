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

'''A simple demonstration of the HTMLLabel class, as it might be used on a
help or introductory screen.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import os
import pyglet

html = '''
<h1>HTML labels in pyglet</h1>

<p align="center"><img src="pyglet.png" /></p>

<p>HTML labels are a simple way to add formatted text to your application.
Different <font face="Helvetica,Arial" size=+2>fonts</font>, <em>styles</em>
and <font color=maroon>colours</font> are supported.

<p>This window has been made resizable; text will reflow to fit the new size.
'''

window = pyglet.window.Window(resizable=True)
location = pyglet.resource.FileLocation(os.path.dirname(__file__))
label = pyglet.text.HTMLLabel(html, location=location,
                              width=window.width,
                              multiline=True, anchor_y='center')

@window.event
def on_resize(width, height):
    # Wrap text to the width of the window
    label.width = window.width

    # Keep text vertically centered in the window
    label.y = 0 #window.height // 2
    label.text += '<div>lol</div>'

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.gl.glClearColor(1, 1, 1, 1)
pyglet.app.run()
