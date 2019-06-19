import uuid
import drawing, gui, sketch, mock

class Control:
    def __init__(self, maincode='', recording=None):
        self.maincode = maincode
        self.globals = {}
        self.recording = recording
        self.state = 'ready'
        self.stdout = []

    def get(self, guid, key):
        # TODO: potential optimisations around when re-run is necessary
        return self.globals.get(key)

    def set(self, guid, key, value):
        self.globals[key] = value

    def get_stdout(self, step):
        stdout = ''
        for s, out in self.stdout:
            if s <= step:
                stdout += out
            else:
                break
        return stdout

class Proxy:
    def __init__(self, control, guid=uuid.uuid4()): #, mock_io=mock.MockIO()):
        self.control = control
        self.guid = guid
        self.io = mock.MockIO()
        self.canvas = drawing.Canvas()
        self.refresh_callback = None
        self.click_callback = None
        self.wheel_callback = None

    def __getitem__(self, key):
        return self.control.get(self.guid, key)

    def __setitem__(self, key, value):
        self.control.set(self.guid, key, value)

    def visits(self, line):
        return self.control.recording.visits(line)

    def line(self, step):
        return self.control.recording.line(step)

    def state(self, step):
        return self.control.recording.state(step)

    def spill(self, step, globs):
        state = self.control.recording.state(step)
        for k, v in state.items():
            if k not in globs:
                #print(k)
                globs[k] = v

    def num_steps(self):
        return self.control.recording.steps()

    def num_lines(self):
        return self.control.maincode.count('\n') + 1

    def mouse(self):
        screen_x, screen_y = gui.mouse_position()
        return (screen_x - self.canvas.x, screen_y - self.canvas.y)

    def key(self, k):
        return gui.key_state(k)

    def on_click(self, callback):
        self.click_callback = callback

        def mouse_up(screen_x, screen_y, d):
            callback(screen_x - self.canvas.x, screen_y - self.canvas.y, False)
        
        gui.add_callback(self.guid, 'mouse_up', mouse_up)

    def on_wheel(self, callback):
        self.wheel_callback = callback

    def on_refresh(self, callback):
        self.refresh_callback = callback
