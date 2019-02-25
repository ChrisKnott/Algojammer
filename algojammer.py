import eel, execorder, time
import windows, drawing, timeline, gui

execution = {'state': 'ready'}

def execution_callback(recording):
    execution['recording'] = recording
    eel.sleep(0.001)    # Yield to other threads

@eel.expose
def run(code):
    if execution['state'] == 'ready':
        execution['state'] = 'running'
        try:
            execution['recording'] = execorder.exec(code, 0, execution_callback)
        except Exception as e:
            # TODO: display somehow
            print(e)

        execution['state'] = 'ready'

@eel.expose
def draw_frame(guid, canvas_data):
    x, y, w, h = canvas_data
    canvas = drawing.Canvas(w, h)
    mx, my = gui.mouse_position()
    canvas.mx = mx - x
    canvas.my = my - y
    timeline.draw_timeline(canvas, execution.get('recording'))
    return canvas._commands


eel.init('web')
eel.start('editor/main_editor.html', 'sheet/timeline.html',
          mode = 'electron',
          port = 8888, 
          cmdline_args = ['--disable-http-cache'],
          geometry={'editor/main_editor.html': {'position': ( 450, 200),
                                                'size':     ( 600, 700)},
                    'sheet/timeline.html':     {'position': (1050, 200),
                                                'size':     ( 600, 700)}})
