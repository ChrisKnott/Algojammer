import eel, collections

metacode = {}                               # Source code for each Sketch
compiled = {}                               # Compiled source code for each Sketch
variables = {}                              # Persistent globals between frames
callbacks = collections.defaultdict(dict)   # GUI events for the sketch
callback_code = {}

def run_sketch(guid, jam):
    try:
        variables[guid]['jam'] = jam
        exec(compiled[guid], variables[guid])
    except Exception as e:
        print('Sketch:', e)

@eel.expose
def set_code(guid, source):
    if source != metacode.get(guid):
        try:
            variables[guid] = {}
            compiled[guid] = compile(source, guid, 'exec')
            print('Compiled', guid)
        except:
            ...
        finally:
            metacode[guid] = source

def set_event_callback(guid, kind, method):
    callbacks[guid][kind] = method
    callback_code[guid] = compile('__jam_event__(*__jam_event_args__)', guid, 'exec')

def sketch_callback(guid, kind, args):
    try:
        callback_variables = {'__jam_event__':      callbacks[guid][kind],
                              '__jam_event_args__': args}
        exec(callback_code[guid], variables[guid], callback_variables)
    except Exception as e:
        print('Sketch GUI:', e)

@eel.expose
def sketch_click(guid, x, y):
    sketch_callback(guid, 'click', (x, y))

@eel.expose
def sketch_wheel(guid, direction):
    sketch_callback(guid, 'wheel', (direction,))

