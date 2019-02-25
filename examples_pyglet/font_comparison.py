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

'''A simple tool that may be used to explore font faces. (Windows only)

Only the fonts installed in the system are visible.

Use the left/right cursor keys to change font faces.

By default only the pyglet safe fonts are shown, toggle the safe flag
to see all.

Don't include tabs in the text sample (see
http://pyglet.org/doc-current/programming_guide/text.html#id9 )
'''

from __future__ import print_function, unicode_literals

import pyglet
import pyglet.font.win32query as wq


# support to generate a sample text good to spot monospace compliance.
# Chosen to do a table of fields_per_line columns, each column with field_size
# characters. Fields are filled with a rolling subset of ASCII characters.
class SampleTable(object):
    field_size = 7
    gap_size = 3
    fields_per_line = 7
    spaces = ' ' * field_size
    max_chars_per_line = (field_size + gap_size) * fields_per_line - gap_size

    def __init__(self):
        self.lines = []
        self.current_line = ''

    def newline(self):
        self.lines.append(self.current_line)
        self.current_line = ''

    def add_field(self, s):
        assert len(s) <= self.field_size
        to_add = self.spaces[len(s):] + s
        if self.current_line:
            to_add = ' ' * self.gap_size + to_add
        if len(self.current_line) + len(to_add) > self.max_chars_per_line:
            self.newline()
            self.add_field(s)
        else:
            self.current_line = self.current_line + to_add

    def text(self):
        return '\n'.join(self.lines)

def sample_text_monospaced_table():
    printables = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
    table = SampleTable()
    for i in range(6):
        s = printables[i:] + printables[:i]
        for k in range(0, len(printables), table.field_size):
            table.add_field(s[k:k + table.field_size])
        table.newline()
    return table.text()

# this worked right with all fonts in a win xp installation
def pyglet_safe(fontentry):
    """ this is heuristic and conservative. YMMV. """
    return fontentry.vector and fontentry.family != wq.FF_DONTCARE


class Window(pyglet.window.Window):
    font_num = 0
    def on_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_RIGHT:
            self.font_num += 1
            if self.font_num == len(font_names):
                self.font_num = 0
        elif motion == pyglet.window.key.MOTION_LEFT:
            self.font_num -= 1
            if self.font_num < 0:
                self.font_num = len(font_names) - 1

        face = font_names[self.font_num]
        self.head = pyglet.text.Label(face, font_size=16, y=0,
            anchor_y='bottom')
        self.text = pyglet.text.Label(sample_text, font_name=face, font_size=12,
            y=self.height, anchor_y='top', width=self.width, multiline=True)

    def on_draw(self):
        self.clear()
        self.head.draw()
        self.text.draw()


lorem_ipsum = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget
libero egestas mattis sit amet vitae augue.


"""

if __name__ == '__main__':
    print(__doc__)
    safe = True
    sample_text = lorem_ipsum + sample_text_monospaced_table()
    # all fonts known by the OS
    fontdb = wq.query()

    if safe:
        candidates = [ f for f in fontdb if pyglet_safe(f)]
    else:
        canditates = fontdb

    # theres one fontentry for each charset supported, so reduce names
    font_names = list(set([f.name for f in candidates]))

    font_names.sort()
    window = Window(1024, 600)
    window.on_text_motion(None)
    pyglet.app.run()

