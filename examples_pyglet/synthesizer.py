import pyglet


class Keyboard:
    def __init__(self):
        """A VERY basic semi-realtime synthesizer."""
        self.window = pyglet.window.Window(720, 480)
        instructions = "Press keys on your keyboard to play notes."
        self.instructions = pyglet.text.Label(text=instructions, font_size=20, x=10, y=10)
        self.current_note = pyglet.text.Label(text="", font_size=33, x=50, y=200)

        self.c4_notes = {"C": 261.63, "C#": 277.183,
                         "D": 293.66, "D#": 311.127,
                         "E": 329.63,
                         "F": 349.23, "F#": 369.994,
                         "G": 392.00, "G#": 415.305,
                         "A": 440.00, "A#": 466.164,
                         "B": 493.88, "R": 0}

        self.key_map = {pyglet.window.key.S: "C#",
                        pyglet.window.key.D: "D#",
                        pyglet.window.key.G: "F#",
                        pyglet.window.key.H: "G#",
                        pyglet.window.key.J: "A#",
                        pyglet.window.key.L: "C#",
                        pyglet.window.key.SEMICOLON: "D#",
                        pyglet.window.key.Z: "C",
                        pyglet.window.key.X: "D",
                        pyglet.window.key.C: "E",
                        pyglet.window.key.V: "F",
                        pyglet.window.key.B: "G",
                        pyglet.window.key.N: "A",
                        pyglet.window.key.M: "B",
                        pyglet.window.key.COMMA: "C",
                        pyglet.window.key.PERIOD: "D",
                        pyglet.window.key.BACKSLASH: "E"}

        self.note_cache = {}

        @self.window.event
        def on_key_press(key, mod):
            try:
                self.play_note(self.c4_notes[self.key_map[key]])
                self.current_note.text = "Current note: {0}".format(self.key_map[key])
            except KeyError:
                pass

        @self.window.event
        def on_draw():
            self.window.clear()
            self.instructions.draw()
            self.current_note.draw()

    def play_note(self, frequency, length=0.6):
        if frequency in self.note_cache:
            note_wave = self.note_cache[frequency]
            note_wave.play()
        else:
            adsr = pyglet.media.procedural.ADSREnvelope(0.05, 0.2, 0.1)
            note_wave = pyglet.media.StaticSource(
                pyglet.media.procedural.Sawtooth(duration=length, frequency=frequency, envelope=adsr))
            self.note_cache[frequency] = note_wave
            note_wave.play()


if __name__ == "__main__":
    keyboard = Keyboard()
    pyglet.app.run()
