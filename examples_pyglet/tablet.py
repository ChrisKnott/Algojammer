#!/usr/bin/python
# $Id:$

from __future__ import print_function

import pyglet

window = pyglet.window.Window()
tablets = pyglet.input.get_tablets()
canvases = []

if tablets:
    print('Tablets:')
    for i, tablet in enumerate(tablets):
        print('  (%d) %s' % (i + 1, tablet.name))
    print('Press number key to open corresponding tablet device.')
else:
    print('No tablets found.')


@window.event
def on_text(text):
    try:
        index = int(text) - 1
    except ValueError:
        return

    if not (0 <= index < len(tablets)):
        return

    name = tablets[i].name

    try:
        canvas = tablets[i].open(window)
    except pyglet.input.DeviceException:
        print('Failed to open tablet %d on window' % index)

    print('Opened %s' % name)

    @canvas.event
    def on_enter(cursor):
        print('%s: on_enter(%r)' % (name, cursor))

    @canvas.event
    def on_leave(cursor):
        print('%s: on_leave(%r)' % (name, cursor))

    @canvas.event
    def on_motion(cursor, x, y, pressure):
        print('%s: on_motion(%r, %r, %r, %r)' % (name, cursor, x, y, pressure))


@window.event
def on_mouse_press(x, y, button, modifiers):
    print('on_mouse_press(%r, %r, %r, %r' % (x, y, button, modifiers))


@window.event
def on_mouse_release(x, y, button, modifiers):
    print('on_mouse_release(%r, %r, %r, %r' % (x, y, button, modifiers))

pyglet.app.run()

