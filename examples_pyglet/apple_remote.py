#!/usr/bin/env python

'''
'''

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet
import sys

window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()

remote = pyglet.input.get_apple_remote()
if not remote:
    print('Apple IR Remote not available.')
    sys.exit(0)

remote.open(window, exclusive=True)

@remote.select_control.event
def on_press():
    print('Press select')

@remote.menu_control.event
def on_press():
    print('Press menu')

@remote.up_control.event
def on_press():
    print('Press up')

@remote.down_control.event
def on_press():
    print('Press down')

@remote.left_control.event
def on_press():
    print('Press left')

@remote.right_control.event
def on_press():
    print('Press right')

@remote.select_control.event
def on_release():
    print('Release select')

@remote.menu_control.event
def on_release():
    print('Release menu')

@remote.up_control.event
def on_release():
    print('Release up')

@remote.down_control.event
def on_release():
    print('Release down')

@remote.left_control.event
def on_release():
    print('Release left')

@remote.right_control.event
def on_release():
    print('Release right')

pyglet.app.run()
