#!/usr/bin/env python

'''Graphically show all devices available via the pyglet.input interface.

Each device is shown in its own collapsed panel.  Click on a device panel
to expand it, revealing that device's controls.  The controls show the
current live values, and flash white when the value changes.
'''

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet
from pyglet import gl


class LineGroup(pyglet.graphics.OrderedGroup):
    def set_state(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def unset_state(self):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)


class Box(object):
    def __init__(self, batch, group=None,
                 stroke_color=(255, 255, 255, 255),
                 fill_color=(200, 200, 200, 255)):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.fill_vertices = batch.add(4, gl.GL_QUADS,
            pyglet.graphics.OrderedGroup(0, group),
            'v2f', ('c4B', fill_color * 4))
        self.stroke_vertices = batch.add(4, gl.GL_QUADS,
            LineGroup(1, group),
            'v2f', ('c4B', stroke_color * 4))

    def set_bounds(self, x1, y1, x2, y2):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.fill_vertices.vertices[:] = (x1, y1, x2, y1, x2, y2, x1, y2)
        self.stroke_vertices.vertices[:] = (x1, y1, x2, y1, x2, y2, x1-1, y2)

    def set_fill(self, r, g, b):
        self.fill_vertices.colors[:] = (r, g, b, 255) * 4

    def delete(self):
        self.fill_vertices.delete()
        self.stroke_vertices.delete()


class DevicePanel(object):
    BORDER_MARGIN = 5
    CONTENT_MARGIN = 8

    def __init__(self, device):
        self.device = device

        self.box = Box(batch, group=background_group,
           stroke_color=(0, 0, 200, 255),
           fill_color=(200, 200, 255, 255))
        self.name_label = pyglet.text.Label(device.name or 'Unknown device',
           font_size=10,
           color=(0, 0, 0, 255),
           anchor_y='top',
           batch=batch, group=text_group)
        self.manufacturer_label = pyglet.text.Label(device.manufacturer or '',
           font_size=10,
           color=(0, 0, 0, 255), anchor_x='right', anchor_y='top',
           batch=batch, group=text_group)

        self.is_open = False
        self.widgets = []

    def set_bounds(self, left, right, top):
        self.left = left
        self.right = right
        self.top = top
        self.layout()

    def layout_widgets(self):
        max_row_width = self.right - self.left - self.CONTENT_MARGIN * 2

        row = []
        row_width = 0
        row_height = 0

        def layout_row(row, x1, y1, x2, y2):
            x = x1
            for widget in row:
                widget.set_bounds(x,
                                  y1,
                                  x + widget.min_width,
                                  y1 + widget.min_height)
                x += widget.min_width

        y = self.bottom + self.CONTENT_MARGIN
        for widget in self.widgets:
            if widget is None or row_width + widget.min_width > max_row_width:
                layout_row(row,
                           self.left + self.CONTENT_MARGIN,
                           y - row_height,
                           self.right - self.CONTENT_MARGIN,
                           y)
                row = []
                y -= row_height
                row_width = 0

                if widget is None:
                    break

            row.append(widget)
            row_width += widget.min_width
            row_height = max(row_height, widget.min_height)

        self.bottom = y - self.CONTENT_MARGIN

    def layout(self):
        self.title_bottom = self.top - \
            self.name_label.content_height - self.CONTENT_MARGIN * 2
        self.bottom = self.title_bottom
        if self.is_open:
            self.layout_widgets()

        self.box.set_bounds(self.left + self.BORDER_MARGIN,
                            self.bottom + self.BORDER_MARGIN,
                            self.right - self.BORDER_MARGIN,
                            self.top - self.BORDER_MARGIN)

        self.name_label.x = self.left + self.CONTENT_MARGIN
        self.name_label.y = self.top - self.CONTENT_MARGIN
        self.manufacturer_label.x = self.right - self.CONTENT_MARGIN
        self.manufacturer_label.y = self.top - self.CONTENT_MARGIN

    def hit_test(self, x, y):
        return self.left < x < self.right and self.title_bottom < y < self.top

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    def open(self):
        if self.is_open:
            return

        try:
            self.device.open()
        except pyglet.input.DeviceException as e:
            try:
                self.device.open(window)
            except pyglet.input.DeviceException as e:
                print(e) # TODO show error
                return

        window.set_mouse_cursor(window.get_system_mouse_cursor('wait'))
        for control in self.device.get_controls():
            if isinstance(control, pyglet.input.Button):
                widget = ButtonWidget(control, batch, group=text_group)
            else:
                widget = ControlWidget(control, batch, group=text_group)
            self.widgets.append(widget)

        if not self.widgets:
            self.widgets.append(NoControlsWidget(batch, group=text_group))

        self.widgets.append(None)
        window.set_mouse_cursor(None)

        self.is_open = True

    def close(self):
        if not self.is_open:
            return

        for widget in self.widgets:
            if widget:
                widget.delete()
        del self.widgets[:]

        self.device.close()

        self.is_open = False


class ControlWidget(object):
    BORDER_MARGIN = 2
    CONTENT_MARGIN = 4

    def __init__(self, control, batch, group=None):
        self.control_name = control.name
        if not self.control_name:
            self.control_name = control.raw_name
        self.box = Box(batch, pyglet.graphics.OrderedGroup(0, group))
        self.name_label = pyglet.text.Label(self.control_name,
            font_size=10,
            anchor_x='left',
            anchor_y='bottom',
            color=(0, 0, 0, 255),
            batch=batch,
            group=pyglet.graphics.OrderedGroup(1, group))
        self.value_label = pyglet.text.Label('          ',
            font_size=8,
            anchor_x='right',
            anchor_y='bottom',
            color=(0, 0, 0, 255),
            batch=batch,
            group=pyglet.graphics.OrderedGroup(1, group))

        self.min_width = \
            self.name_label.content_width + \
            self.value_label.content_width + self.CONTENT_MARGIN * 2
        self.min_height = self.name_label.content_height + self.CONTENT_MARGIN * 2

        self.relative = isinstance(control, pyglet.input.RelativeAxis)
        self.fade = 200

        self.control = control
        control.push_handlers(self)

    def set_bounds(self, x1, y1, x2, y2):
        self.box.set_bounds(
            x1 + self.BORDER_MARGIN,
            y1 + self.BORDER_MARGIN,
            x2 - self.BORDER_MARGIN,
            y2 - self.BORDER_MARGIN)
        self.name_label.x = x1 + self.CONTENT_MARGIN
        self.name_label.y = y1 + self.CONTENT_MARGIN
        self.value_label.x = x2 - self.CONTENT_MARGIN
        self.value_label.y = y1 + self.CONTENT_MARGIN

    def delete(self):
        if self in changed_widgets:
            changed_widgets.remove(self)
        self.control.remove_handlers(self)
        self.name_label.delete()
        self.value_label.delete()
        self.box.delete()

    def on_change(self, value):
        self.value = value
        self.fade = 255
        changed_widgets.add(self)

    def update(self):
        self.value_label.text = str(self.value)
        if self.relative and self.value:
            self.value = 0
            changed_widgets.add(self)

        self.box.set_fill(self.fade, self.fade, self.fade)
        if self.fade > 200:
            self.fade = max(200, self.fade - 10)
            changed_widgets.add(self)


class ButtonWidget(ControlWidget):
    BORDER_MARGIN = 2
    CONTENT_MARGIN = 4

    def __init__(self, control, batch, group=None):
        self.control_name = control.name
        if not self.control_name:
            self.control_name = control.raw_name
        self.box = Box(batch, pyglet.graphics.OrderedGroup(0, group))
        self.name_label = pyglet.text.Label(self.control_name,
            font_size=10,
            anchor_x='center',
            anchor_y='bottom',
            color=(0, 0, 0, 255),
            batch=batch,
            group=pyglet.graphics.OrderedGroup(1, group))

        self.min_width = self.name_label.content_width + self.CONTENT_MARGIN * 2
        self.min_height = self.name_label.content_height + self.CONTENT_MARGIN * 2

        self.fade = 200

        self.control = control
        control.push_handlers(self)

    def set_bounds(self, x1, y1, x2, y2):
        self.box.set_bounds(
            x1 + self.BORDER_MARGIN,
            y1 + self.BORDER_MARGIN,
            x2 - self.BORDER_MARGIN,
            y2 - self.BORDER_MARGIN)
        self.name_label.x = (x1 + x2) // 2
        self.name_label.y = y1 + self.CONTENT_MARGIN

    def delete(self):
        if self in changed_widgets:
            changed_widgets.remove(self)
        self.control.remove_handlers(self)
        self.name_label.delete()
        self.box.delete()

    def on_change(self, value):
        self.value = value
        if value:
            self.fade = 255
        changed_widgets.add(self)

    def update(self):
        self.box.set_fill(self.fade, self.fade, self.fade)
        if not self.value and self.fade > 200:
            self.fade = max(200, self.fade - 10)
            changed_widgets.add(self)


class NoControlsWidget(object):
    CONTENT_MARGIN = 4

    def __init__(self, batch, group):
        self.label = pyglet.text.Label('No controls on this device.',
            font_size=10,
            color=(0, 0, 0, 255),
            anchor_y='bottom',
            batch=batch,
            group=group)

        self.min_width = self.label.content_width + self.CONTENT_MARGIN * 2
        self.min_height = self.label.content_height + self.CONTENT_MARGIN * 2

    def set_bounds(self, x1, y1, x2, y2):
        self.label.x = x1 + ControlWidget.CONTENT_MARGIN
        self.label.y = y1 + ControlWidget.CONTENT_MARGIN

    def delete(self):
        self.label.delete()


window = pyglet.window.Window(caption='Input Devices', resizable=True)
batch = pyglet.graphics.Batch()
background_group = pyglet.graphics.OrderedGroup(0)
text_group = pyglet.graphics.OrderedGroup(1)

panels = [DevicePanel(device) for device in pyglet.input.get_devices()]
help_label = pyglet.text.Label(
    'Click on a device name to show or hide its controls.',
    x=DevicePanel.CONTENT_MARGIN,
    anchor_y='top',
    font_size=10,
    color=(255, 255, 255, 255),
    batch=batch,
    group=background_group)


def layout_panels():
    y = window.height
    for panel in panels:
        panel.set_bounds(left=0, right=window.width, top=y)
        y = panel.bottom
    help_label.y = y

@window.event
def on_draw():
    gl.glClearColor(0.3, 0.3, 0.4, 1.0)
    window.clear()
    batch.draw()
    window.invalid = False

@window.event
def on_resize(width, height):
    layout_panels()
    window.invalid = True
    return pyglet.event.EVENT_UNHANDLED

@window.event
def on_mouse_press(x, y, button, modifiers):
    for panel in panels:
        if panel.hit_test(x, y):
            panel.toggle()
            layout_panels()
            window.invalid = True

changed_widgets = set()


def update(dt):
    pending = list(changed_widgets)
    changed_widgets.clear()
    for widget in pending:
        widget.update()
    window.invalid = True

pyglet.clock.schedule_interval(update, 0.05)
pyglet.app.run()
