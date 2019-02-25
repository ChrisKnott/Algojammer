#!/usr/bin/env python

'''
'''

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet

window = pyglet.window.Window()
devices = pyglet.input.get_devices()


def watch_control(device, control):
    @control.event
    def on_change(value):
        print('%r: %r.on_change(%r)' % (device, control, value))

    if isinstance(control, pyglet.input.base.Button):
        @control.event
        def on_press():
            print('%r: %r.on_press()' % (device, control))

        @control.event
        def on_release():
            print('%r: %r.on_release()' % (device, control))

print('Devices:')
for device in devices:
    print('  ', device.name, end=' ')
    try:
        device.open(window=window)
        print('OK')

        for control in device.get_controls():
            print('    ', control.name)
            watch_control(device, control)

    except pyglet.input.DeviceException:
        print('Fail')

pyglet.app.run()
