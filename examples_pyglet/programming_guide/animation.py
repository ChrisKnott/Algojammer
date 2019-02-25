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

'''Load and display a GIF animation.

Usage::

    animation.py [<filename>]

If the filename is omitted, a sample animation is loaded
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

# The dinosaur.gif file packaged alongside this script is in the public
# domain, it was obtained from http://www.gifanimations.com/.

import sys

import pyglet

if len(sys.argv) > 1:
    # Load the animation from file path.
    animation = pyglet.image.load_animation(sys.argv[1])
    bin = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bin)
else:
    # Load animation from resource (this script's directory).
    animation = pyglet.resource.animation('dinosaur.gif')
sprite = pyglet.sprite.Sprite(animation)

window = pyglet.window.Window(width=sprite.width, height=sprite.height)

# Set window background color to white.
pyglet.gl.glClearColor(1, 1, 1, 1)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()
