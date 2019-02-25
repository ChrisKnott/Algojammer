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

'''Bounces balls around a window and plays noises.

This is a simple demonstration of how pyglet efficiently manages many sound
channels without intervention.
'''

import os
import random
import sys

from pyglet.gl import *
import pyglet
from pyglet.window import key

BALL_IMAGE = 'ball.png'
BALL_SOUND = 'ball.wav'

if len(sys.argv) > 1:
    BALL_SOUND = sys.argv[1]

sound = pyglet.resource.media(BALL_SOUND, streaming=False)

class Ball(pyglet.sprite.Sprite):
    ball_image = pyglet.resource.image(BALL_IMAGE)
    width = ball_image.width
    height = ball_image.height

    def __init__(self):
        x = random.random() * (window.width - self.width)
        y = random.random() * (window.height - self.height)

        super(Ball, self).__init__(self.ball_image, x, y, batch=balls_batch)

        self.dx = (random.random() - 0.5) * 1000
        self.dy = (random.random() - 0.5) * 1000

    def update(self, dt):
        if self.x <= 0 or self.x + self.width >= window.width:
            self.dx *= -1
            sound.play()
        if self.y <= 0 or self.y + self.height >= window.height:
            self.dy *= -1
            sound.play()
        self.x += self.dx * dt
        self.y += self.dy * dt

        self.x = min(max(self.x, 0), window.width - self.width)
        self.y = min(max(self.y, 0), window.height - self.height)

window = pyglet.window.Window(640, 480)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        balls.append(Ball())
    elif symbol == key.BACKSPACE:
        if balls:
            del balls[-1]
    elif symbol == key.ESCAPE:
        window.has_exit = True

@window.event
def on_draw():
    window.clear()
    balls_batch.draw()
    label.draw()

def update(dt):
    for ball in balls:
        ball.update(dt)
pyglet.clock.schedule_interval(update, 1/30.)

balls_batch = pyglet.graphics.Batch()
balls = []
label = pyglet.text.Label('Press space to add a ball, backspace to remove',
                          font_size=14,
                          x=window.width // 2, y=10, 
                          anchor_x='center')

if __name__ == '__main__':
    pyglet.app.run()
