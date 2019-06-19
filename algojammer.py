import execorder, time, eel, json, urllib
import windows, drawing, gui, sketch, jam, mock

control = jam.Control()

def print_callback(io):
    control.stdout += [(control.recording.steps(), io.get_new_output())]

def execution_callback(recording):
    control.recording = recording
    eel.sleep(0.0001)    # Yield to other threads

@eel.expose
def run_maincode(source):
    if control.state == 'ready':
        control.maincode = source
        control.state = 'running'
        try:
            io = mock.MockIO(gcj_input)
            io.print_callback = lambda: print_callback(io)
            control.stdout.clear()
            rec = execorder.exec(source, io.functions(), callback=execution_callback)
        except SyntaxError as e:
            print('compile error')
        except RuntimeError as e:
            print(e)    # TODO: display somehow

        control.state = 'ready'

@eel.expose
def set_metacode(sketch_guid, source):
    sketch.set_metacode(sketch_guid, source, control)
    sketch.run_metacode(sketch_guid)

@eel.expose
def save_to_file(object, path):
    try:
       with open(path, 'w', encoding='utf8') as file:
            json.dump(object, file, indent=2)
    except:
        pass

@eel.expose
def load_from_file(path):
    try:
        with open(path, encoding='utf8') as file:
            return json.load(file)
    except:
        pass

# TEMP TEMP TEMP ##########################################
with open('_input', encoding='utf8') as file:
    gcj_input = file.read()

with open('_code', encoding='utf8') as file:
    maincode = file.read()

@eel.expose
def get_code():
    return maincode
###########################################################

# Set up default Sketches
with open('files/Timeline.json', encoding='utf8') as timeline:
    timeline_url = 'sheet/sheet.html?' + urllib.parse.urlencode({'data': timeline.read()})

for guid, code in load_from_file('files/EditorSketches.json').items():
    set_metacode(guid, code)

eel.init('web')
eel.start('editor/main_editor.html', timeline_url,
          mode = 'electron',
          port = 8888, 
          geometry={'editor/main_editor.html': {'position': (480,  30),
                                                'size':     (600, 750)}})
