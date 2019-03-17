import uuid
import drawing, gui, sketch

class Control:
    def __init__(self, maincode='', recording=None):
        self.maincode = maincode
        self.globals = {}
        self.recording = recording
        self.state = 'ready'

    def get(self, guid, key):
        # TODO: potential optimisations around when re-run is necessary
        print('get', key, 'by', guid)
        return self.globals.get(key)

    def set(self, guid, key, value):
        print('set', key, 'by', guid)
        self.globals[key] = value


class Proxy:
    def __init__(self, control, canvas, guid=uuid.uuid4()):
        self.control = control
        self.guid = guid
        self.canvas = canvas

        for method in 'clear ink rect stroke circ text'.split():
            setattr(self, method, getattr(self.canvas, method))

    def __getitem__(self, key):
        return self.control.get(self.guid, key)

    def __setitem__(self, key, value):
        self.control.set(self.guid, key, value)

    def visits(self, line):
        return self.control.recording.visits(line)

    def line(self, step):
        return self.control.recording.line(step)

    def num_steps(self):
        return self.control.recording.steps()

    def num_lines(self):
        return self.control.maincode.count('\n') + 1

    def mouse(self):
        screen_x, screen_y = gui.mouse_position()
        return (screen_x - self.canvas.left, screen_y - self.canvas.top)

    def key(self, k):
        return gui.key_state(k)

    def on_click(self, callback):
        sketch.set_event_callback(self.guid, 'click', callback)

    def on_wheel(self, callback):
        sketch.set_event_callback(self.guid, 'wheel', callback)



