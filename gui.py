import eel, collections

callbacks = collections.defaultdict(list)
gui = {'mouse': (0, 0)}

@eel.expose
def update_mouse_position(x, y):
    gui['mouse'] = (x, y)

@eel.expose
def key_down(guid, key):
    gui[key] = True
    for callback in callbacks[key]:
        callback(guid, key, True)

@eel.expose
def key_up(guid, key):
    gui[key] = False
    for callback in callbacks[key]:
        callback(guid, key, False)

@eel.expose
def mouse_down(guid, x, y):
    gui['click'] = True
    for callback in callbacks['click']:
        callback(guid, x, y, True)

@eel.expose
def mouse_up(guid, x, y):
    gui['click'] = False
    for callback in callbacks['click']:
        callback(guid, x, y, False)

## Public interface ###############

def mouse_position():
    return gui['mouse']

def key_state(key):
    return gui.get(key, False)

def add_callback(key, callback):
    callbacks[key].append(callback)
