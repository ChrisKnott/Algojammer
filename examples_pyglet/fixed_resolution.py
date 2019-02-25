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
# $Id:$

'''Demonstrates one way of fixing the display resolution to a certain
size, but rendering to the full screen.

The method used in this example is:

1. Set the OpenGL viewport to the fixed resolution
2. Render the scene using any OpenGL functions (here, just a polygon)
3. Copy the framebuffer into a texture
4. Reset the OpenGL viewport to the window (full screen) size
5. Blit the texture to the framebuffer

Recent video cards could also render the scene directly to the texture
using EXT_framebuffer_object.  (This is not demonstrated in this example).
'''

from pyglet.gl import *
import pyglet

# Create a fullscreen window using the user's desktop resolution.  You can
# also use this technique on ordinary resizable windows.
window = pyglet.window.Window(fullscreen=True)

# Use 320x200 fixed resolution to make the effect completely obvious.  You
# can change this to a more reasonable value such as 800x600 here.
target_resolution = 320, 200

class FixedResolutionViewport(object):
    def __init__(self, window, width, height, filtered=False):
        self.window = window
        self.width = width
        self.height = height
        self.texture = pyglet.image.Texture.create(width, height, 
            rectangle=True)

        if not filtered:
            # By default the texture will be bilinear filtered when scaled
            # up.  If requested, turn filtering off.  This makes the image
            # aliased, but is more suitable for pixel art.
            glTexParameteri(self.texture.target, 
                GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(self.texture.target, 
                GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    
    def begin(self):
        glViewport(0, 0, self.width, self.height)
        self.set_fixed_projection()

    def end(self):
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        self.texture.blit_into(buffer, 0, 0, 0)

        glViewport(0, 0, self.window.width, self.window.height)
        self.set_window_projection()

        aspect_width = self.window.width / float(self.width)
        aspect_height = self.window.height / float(self.height)
        if aspect_width > aspect_height:
            scale_width = aspect_height * self.width
            scale_height = aspect_height * self.height
        else:
            scale_width = aspect_width * self.width
            scale_height = aspect_width * self.height
        x = (self.window.width - scale_width) / 2
        y = (self.window.height - scale_height) / 2
        
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(1, 1, 1)
        self.texture.blit(x, y, width=scale_width, height=scale_height)
    
    def set_fixed_projection(self):
        # Override this method if you need to change the projection of the
        # fixed resolution viewport.
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def set_window_projection(self):
        # This is the same as the default window projection, reprinted here
        # for clarity.
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.window.width, 0, self.window.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

target_width, target_height = target_resolution
viewport = FixedResolutionViewport(window, 
    target_width, target_height, filtered=False)

def draw_scene():
    '''Draw the scene, assuming the fixed resolution viewport and projection
    have been set up.  This just draws the rotated polygon.'''
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    w, h = target_resolution
    glTranslatef(w//2, h//2, 0)
    glRotatef(rotate, 0, 0, 1)
    glColor3f(1, 0, 0)
    s = min(w, h) // 3
    glRectf(-s, -s, s, s)

rotate = 0
def update(dt):
    global rotate
    rotate += dt * 20
pyglet.clock.schedule_interval(update, 1/60.)

@window.event
def on_draw():
    viewport.begin()
    window.clear()
    draw_scene()
    viewport.end()

pyglet.app.run()

