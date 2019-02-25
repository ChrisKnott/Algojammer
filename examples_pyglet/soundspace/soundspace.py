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
# $Id$

import math
import os

import pyglet
from pyglet.gl import *

import reader

pyglet.resource.path.append('res')
pyglet.resource.reindex()

# Check for AVbin
from pyglet.media import have_avbin

if not have_avbin():
    raise ImportError('AVbin is required for this example, see '
        'http://code.google.com/p/avbin')

def disc(r, x, y, slices=20, start=0, end=2*math.pi):
    d = (end - start) / (slices - 1)
    s = start
    points = [(x, y)] + [(x + r * math.cos(a*d+s), y + r * math.sin(a*d+s)) \
                         for a in range(slices)]
    points = ((GLfloat * 2) * len(points))(*points)
    glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, points)
    glDrawArrays(GL_TRIANGLE_FAN, 0, len(points))
    glPopClientAttrib()

def circle(r, x, y, slices=20):
    d = 2 * math.pi / slices
    points = [(x + r * math.cos(a*d), y + r * math.sin(a*d)) \
                         for a in range(slices)]
    points = ((GLfloat * 2) * len(points))(*points)
    glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, points)
    glDrawArrays(GL_LINE_LOOP, 0, len(points))
    glPopClientAttrib()


def orientation_angle(orientation):
    return math.atan2(orientation[2], orientation[0])

class Handle(object):
    tip = ''

    def __init__(self, player):
        self.player = player

    def hit_test(self, x, y, z):
        dx, dy, dz = [a - b for a, b in zip(self.pos(), (x, y, z))]
        if dx * dx + dy * dy + dz * dz < self.radius * self.radius:
            return -dx, -dy, -dz

    def draw(self):
        pass

    def begin_drag(self, window, offset):
        self.win = window
        self.offset = offset
        return self

    def on_mouse_press(self, x, y, button, modifiers):
        self.win.remove_handlers(self)

    def on_mouse_release(self, x, y, button, modifiers):
        self.win.remove_handlers(self)

class LabelHandle(Handle):
    def __init__(self, player):
        super(LabelHandle, self).__init__(player)
        self.text = pyglet.text.Label('', font_size=10, color=(0, 0, 0, 255),
                                      anchor_y='top', anchor_x='center')

    def hit_test(self, x, y, z):
        return None

    def draw(self):
        if hasattr(self.player, 'label'):
            x, _, y = self.player.position

            # ech. fudge scale back to 1
            mat = (GLfloat * 16)()
            glGetFloatv(GL_MODELVIEW_MATRIX, mat)

            glPushMatrix()
            glTranslatef(x, y, 0)
            glScalef(1/mat[0], 1/mat[5], 1/mat[10])
            glTranslatef(0, -5, 0)

            self.text.text = self.player.label
            self.text.draw()

            glPopMatrix()

class PositionHandle(Handle):
    tip = 'position'
    radius = .3

    def draw(self):
        glPushMatrix()
        glTranslatef(self.player.position[0], self.player.position[2], 0)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex2f(0, self.radius)
        glVertex2f(-self.radius * math.sqrt(3) / 2, -.5 * self.radius)
        glVertex2f(self.radius * math.sqrt(3) / 2, -.5 * self.radius)
        glEnd()
        glPopMatrix()

    def pos(self):
        return self.player.position

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pos = self.win.mouse_transform(x, y)
        self.player.position = \
            (pos[0] - self.offset[0],
             pos[1] - self.offset[1],
             pos[2] - self.offset[2])

class OrientationHandle(Handle):
    radius = .1
    length = 1.5

    def pos(self):
        x, _, z = self.player.position
        dir = self.get_orientation()
        sz = math.sqrt(dir[0] ** 2 + dir[1] ** 2 + dir[2] ** 2) or 1
        if sz != 0:
            x += dir[0] / sz * self.length
            z += dir[2] / sz * self.length
        return x, 0, z

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)

        px, _, py = self.player.position
        x, _, y = self.pos()

        # Dashed line
        glColor3f(.3, .3, .3)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0x7777)
        glBegin(GL_LINES)
        glVertex2f(px, py)
        glVertex2f(x, y)
        glEnd()

        # This handle (orientation)
        glColor3f(1, 1, 0)
        disc(self.radius, x, y)

        glPopAttrib()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        px, py, pz = self.player.position
        hx, hy, hz = self.win.mouse_transform(x, y)
        self.set_orientation(
            (hx - self.offset[0] - px,
             hy - self.offset[1] - py,
             hz - self.offset[2] - pz))

class ConeOrientationHandle(OrientationHandle):
    tip = 'cone_orientation'

    def get_orientation(self):
        return self.player.cone_orientation

    def set_orientation(self, orientation):
        self.player.cone_orientation = orientation

class ForwardOrientationHandle(OrientationHandle):
    tip = 'forward_orientation'

    def get_orientation(self):
        return self.player.forward_orientation

    def set_orientation(self, orientation):
        self.player.forward_orientation = orientation

class ConeAngleHandle(Handle):
    radius = .1

    def pos(self):
        px, py, pz = self.player.position
        angle = orientation_angle(self.player.cone_orientation)
        angle += self.get_angle() * math.pi / 180. / 2
        x = math.cos(angle) * self.length
        z = math.sin(angle) * self.length
        return px + x, py, pz + z

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)

        # Fill
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(*self.fill_color)
        px, _, py = self.player.position
        angle = orientation_angle(self.player.cone_orientation)
        a = self.get_angle() * math.pi / 180.
        disc(self.length, px, py,
             start=angle - a/2,
             end=angle + a/2)

        # Handle
        x, _, y = self.pos()
        glColor4f(*self.color)
        disc(self.radius, x, y)
        glPopAttrib()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        px, py, pz = self.player.position
        hx, hy, hz = self.win.mouse_transform(x, y)
        angle = orientation_angle(self.player.cone_orientation)
        hangle = orientation_angle((hx - px, hy - py, hz - pz))
        if hangle < angle:
            hangle += math.pi * 2
        res = min(max((hangle - angle) * 2, 0), math.pi * 2)
        self.set_angle(res * 180. / math.pi)

class ConeInnerAngleHandle(ConeAngleHandle):
    tip = 'cone_inner_angle'
    length = 1.
    color = (.2, .8, .2, 1)
    fill_color = (0, 1, 0, .1)

    def get_angle(self):
        return self.player.cone_inner_angle

    def set_angle(self, angle):
        self.player.cone_inner_angle = angle

class ConeOuterAngleHandle(ConeAngleHandle):
    tip = 'cone_outer_angle'
    length = 1.2
    color = (.2, .2, .8, 1)
    fill_color = (0, 0, 1, .1)

    def get_angle(self):
        return self.player.cone_outer_angle

    def set_angle(self, angle):
        self.player.cone_outer_angle = angle

class MoreHandle(Handle):
    tip = 'More...'
    radius = .2

    open = False
    open_width = 1.5
    open_height = 1.5

    def pos(self):
        x, y, z = self.player.position
        return x + 1, y, z + 1

    def draw(self):
        x, _, z = self.pos()

        if self.open:
            x -= .2
            z += .2
            glPushAttrib(GL_ENABLE_BIT)
            glEnable(GL_BLEND)

            glColor4f(1, 1, 1, .8)
            glBegin(GL_QUADS)
            glVertex2f(x, z)
            glVertex2f(x + self.open_width, z)
            glVertex2f(x + self.open_width, z - self.open_height)
            glVertex2f(x, z - self.open_height)
            glEnd()

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor4f(0, 0, 0, 1)
            glBegin(GL_QUADS)
            glVertex2f(x, z)
            glVertex2f(x + self.open_width, z)
            glVertex2f(x + self.open_width, z - self.open_height)
            glVertex2f(x, z - self.open_height)
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            glPopAttrib()
        else:
            glColor3f(1, 1, 1)
            disc(self.radius, x, z)

            glColor3f(0, 0, 0)
            circle(self.radius, x, z)

            r = self.radius - 0.1
            glBegin(GL_LINES)
            glVertex2f(x - r, z)
            glVertex2f(x + r, z)
            glVertex2f(x, z - r)
            glVertex2f(x, z + r)
            glEnd()

    def begin_drag(self, window, offset):
        self.open = True
        self.win = window
        self.win.set_more_player_handles(self.player)
        return self

    def on_mouse_press(self, x, y, button, modifiers):
        x, y, z = self.win.mouse_transform(x, y)
        for handle in self.win.more_handles:
            if handle.hit_test(x, y, z):
                return
        self.win.set_more_player_handles(None)
        self.win.remove_handlers(self)
        self.open = False

    def on_mouse_release(self, x, y, button, modifiers):
        pass

class SliderHandle(Handle):
    length = 1.
    width = .05
    radius = .1

    def __init__(self, player, x, z):
        super(SliderHandle, self).__init__(player)
        self.x = x
        self.z = z

    def pos(self):
        x, y, z = self.player.position
        x += self.x + self.get_value() * self.length
        z += self.z
        return x, y, z

    def draw(self):
        x = self.x + self.player.position[0]
        z = self.z + self.player.position[2]

        # Groove
        glColor3f(.5, .5, .5)
        glBegin(GL_QUADS)
        glVertex2f(x, z - self.width/2)
        glVertex2f(x + self.length, z - self.width/2)
        glVertex2f(x + self.length, z + self.width/2)
        glVertex2f(x, z + self.width/2)
        glEnd()

        # Thumb
        x, _, z = self.pos()
        glColor3f(.2, .2, .2)
        disc(self.radius, x, z)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        px, py, pz = self.player.position
        hx, hy, hz = self.win.mouse_transform(x, y)
        value = float(hx - px - self.x) / self.length
        value = min(max(value, 0), 1)
        self.set_value(value)

class VolumeHandle(SliderHandle):
    tip = 'volume'

    def __init__(self, player):
        super(VolumeHandle, self).__init__(player, 1, .9)

    def get_value(self):
        return self.player.volume

    def set_value(self, value):
        self.player.volume = value

class ListenerVolumeHandle(SliderHandle):
    tip = 'volume'

    def __init__(self, player):
        super(ListenerVolumeHandle, self).__init__(player, -.5, -1)

    def get_value(self):
        return self.player.volume

    def set_value(self, value):
        self.player.volume = value

class MinDistanceHandle(SliderHandle):
    tip = 'min_distance'

    def __init__(self, player):
        super(MinDistanceHandle, self).__init__(player, 1, .6)

    def get_value(self):
        return self.player.min_distance / 5.

    def set_value(self, value):
        self.player.min_distance = value * 5.

class MaxDistanceHandle(SliderHandle):
    tip = 'max_distance'

    def __init__(self, player):
        super(MaxDistanceHandle, self).__init__(player, 1, .3)

    def get_value(self):
        return min(self.player.max_distance / 5., 1.0)

    def set_value(self, value):
        self.player.max_distance = value * 5.

class ConeOuterGainHandle(SliderHandle):
    tip = 'cone_outer_gain'

    def __init__(self, player):
        super(ConeOuterGainHandle, self).__init__(player, 1, 0)

    def get_value(self):
        return self.player.cone_outer_gain

    def set_value(self, value):
        self.player.cone_outer_gain = value

class SoundSpaceWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        kwargs.update(dict(
            caption='Sound Space',
            resizable=True,
        ))
        super(SoundSpaceWindow, self).__init__(**kwargs)

        self.players = []
        self.handles = []
        self.more_handles = []

        listener = pyglet.media.get_audio_driver().get_listener()
        self.handles.append(PositionHandle(listener))
        self.handles.append(ForwardOrientationHandle(listener))
        self.handles.append(ListenerVolumeHandle(listener))
        self.handles.append(LabelHandle(listener))

        self.tip = pyglet.text.Label('', font_size=10, color=(0, 0, 0, 255),
                                     anchor_y='top', anchor_x='center')
        self.tip_player = None

        # pixels per unit
        self.zoom = 40
        self.tx = self.width/2
        self.ty = self.height/2

    def add_player(self, player):
        self.players.append(player)
        self.handles.append(PositionHandle(player))
        self.handles.append(ConeOrientationHandle(player))
        self.handles.append(ConeInnerAngleHandle(player))
        self.handles.append(ConeOuterAngleHandle(player))
        self.handles.append(LabelHandle(player))
        self.handles.append(MoreHandle(player))

    def set_more_player_handles(self, player):
        if player:
            self.more_handles = [
                VolumeHandle(player),
                MinDistanceHandle(player),
                MaxDistanceHandle(player),
                ConeOuterGainHandle(player),
            ]
        else:
            self.more_handles = []

    def draw_background(self):
        glLoadIdentity()
        glPushAttrib(GL_CURRENT_BIT)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for i in range(0, self.width, self.zoom):
            glVertex2f(i, 0)
            glVertex2f(i, self.height)
        for i in range(0, self.height, self.zoom):
            glVertex2f(0, i)
            glVertex2f(self.width, i)
        glEnd()
        glPopAttrib()

    def camera_transform(self):
        glLoadIdentity()
        glTranslatef(self.tx, self.ty, 0)
        glScalef(self.zoom, self.zoom, 1)

    def mouse_transform(self, x, y):
        return (float(x - self.tx) / self.zoom,
                0,
                float(y - self.ty) / self.zoom)

    def player_transform(self, player):
        return (player.position[0] * self.zoom + self.tx,
                player.position[2] * self.zoom + self.ty)

    def hit_test(self, mouse_x, mouse_y):
        x, y, z = self.mouse_transform(mouse_x, mouse_y)
        for handle in self.more_handles[::-1] + self.handles[::-1]:
            offset = handle.hit_test(x, y, z)
            if offset:
                return handle, offset
        return None, None

    def on_draw(self):
        glClearColor(.8, .8, .8, 1)
        self.clear()
        self.draw_background()

        glPushMatrix()
        self.camera_transform()
        for handle in self.handles + self.more_handles:
            handle.draw()
        glPopMatrix()

        if self.tip_player:
            player_pos = self.player_transform(self.tip_player)
            self.tip.x = player_pos[0]
            self.tip.y = player_pos[1] - 15
            self.tip.draw()

    def on_mouse_scroll(self, x, y, dx, dy):
        self.zoom += dy * 10
        self.zoom = min(max(self.zoom, 10), 100)

    def on_mouse_press(self, x, y, button, modifiers):
        handle, offset = self.hit_test(x, y)
        if handle:
            self.push_handlers(handle.begin_drag(self, offset))
        else:
            self.push_handlers(PanView(self))

    def on_mouse_motion(self, x, y, dx, dy):
        handle, offset = self.hit_test(x, y)
        if handle:
            self.tip.text = handle.tip
            pos = self.player_transform(handle.player)
            self.tip_player = handle.player
        else:
            self.tip.text = ''

class PanView(object):
    def __init__(self, window):
        self.win = window

    def on_mouse_release(self, x, y, button, modifiers):
        self.win.remove_handlers(self)

    def on_mouse_press(self, x, y, button, modifiers):
        self.win.remove_handlers(self)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.win.tx += dx
        self.win.ty += dy

if __name__ == '__main__':
    # We swap Y and Z, moving to left-handed system
    listener = pyglet.media.get_audio_driver().get_listener()
    listener.up_orientation = (0, -1, 0)

    # Start facing up (er, forwards)
    listener.forward_orientation = (0, 0, 1)

    listener.label = 'Listener'

    w = SoundSpaceWindow()
    r = reader.SpaceReader(w)
    r.read(pyglet.resource.file('space.txt'))
    player_group = pyglet.media.PlayerGroup(w.players)
    player_group.play()

    pyglet.app.run()
