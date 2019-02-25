#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet
from pyglet.gl import *

joysticks = pyglet.input.get_joysticks()
assert joysticks, 'No joystick device is connected'
joystick = joysticks[0]
joystick.open()

window = pyglet.window.Window()

@window.event
def on_draw():
    x = (0.8*joystick.x + 1) * window.width / 2
    y = (-0.8*joystick.y + 1) * window.height / 2
    z = joystick.z
    angle = joystick.rz * 180

    # Axes

    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 0, 0)
    glLoadIdentity()
    glTranslatef(x, y, 0)
    glScalef(1 + z, 1 + z, 1 + z)
    glRotatef(-angle, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-10, 0)
    glVertex2f(0, 13)
    glVertex2f(10, 0)
    glEnd()

    # Buttons

    glLoadIdentity()
    x = 10
    y = 10
    glPointSize(5)
    glBegin(GL_POINTS)
    for button in joystick.buttons:
        if button:
            glVertex2f(x, y)
        x += 20
    glEnd()

    # Hat

    glColor3f(0, 0, 1)
    x = window.width / 2
    y = window.height / 2
    glBegin(GL_POINTS)
    glVertex2f(x + joystick.hat_x * 50, y + joystick.hat_y * 50)
    glEnd()

pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
