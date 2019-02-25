import pygments, pygments.lexers, pygments.formatter, pygments.token, pyglet, time, re

code = '''
import random

X = [random.random() for n in range(100)]

done = False
while not done:
    done = True
    for i, _ in enumerate(X):
        if i < len(X) - 1:
            a, b = X[i], X[i + 1]
            if a > b:
                done = False
                X[i], X[i + 1] = b, a

'''.strip()

colors = {
    pygments.token.Keyword:         '{color (  0,   0, 255, 255)}',
    pygments.token.Name.Function:   '{color (  0, 255, 255, 255)}',
    pygments.token.Comment.Single:  '{color (150, 120, 150, 255)}',
}

class NullFormatter(pygments.formatter.Formatter):
    def format(self, tokensource, outfile):
        outfile.write("{font_name 'Courier New'}\n")
        for ttype, value in tokensource:
            print(ttype)
            if value.strip():
                outfile.write(colors.get(ttype, '{color (0, 0, 0, 255)}'))
            outfile.write(value.replace('{', '{{')
                               .replace('}', '}}'))

start = time.perf_counter()
formatted = pygments.highlight( code, 
                                pygments.lexers.PythonLexer(), 
                                NullFormatter() )
formatted = re.sub(r'(\n+)', r'\1\n', formatted)
print(time.perf_counter() - start)

class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        start = time.perf_counter()
        self.document = pyglet.text.decode_attributed(formatted)
        print(time.perf_counter() - start)

        height = 400 - 20
        self.layout = pyglet.text.layout.IncrementalTextLayout(
                                            self.document,
                                            width, 
                                            height,
                                            multiline=True, 
                                            wrap_lines=False,
                                            batch=batch,
                                        )

        self.caret = pyglet.text.caret.Caret(self.layout)
        self.layout.x = x
        self.layout.y = y

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(600, 400, caption='Text entry')

        self.batch = pyglet.graphics.Batch()
        self.widget = TextWidget('', 10, 10, self.width - 20, self.batch)
        self.text_cursor = self.get_system_mouse_cursor('text')

    def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)
        self.widget.width = width - 20
        self.widget.height = height - 20

    def on_draw(self):
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.widget.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.widget.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        self.widget.caret.on_text(text)

    def on_text_motion(self, motion):
        self.widget.caret.on_text_motion(motion)
      
    def on_text_motion_select(self, motion):
        self.widget.caret.on_text_motion_select(motion)
        
window = Window(resizable=True)
pyglet.app.run()
