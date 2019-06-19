import eel, collections

callbacks = collections.defaultdict(dict)
gui = {'mouse': (0, 0)}

@eel.expose
def update_mouse_position(x, y):
    gui['mouse'] = (x, y)

@eel.expose
def key_down(guid, key):
    gui[key] = True
    for callback in callbacks[key].values():
        try:
            callback(guid, key, True)
        except:
            ...

@eel.expose
def key_up(guid, key):
    gui[key] = False
    for callback in callbacks[key].values():
        try:
            callback(guid, key, False)
        except:
            ...

@eel.expose
def mouse_down(guid, x, y):
    gui['click'] = True
    for callback in callbacks['mouse_down'].values():
        try:
            callback(x, y, True)
        except:
            ...

@eel.expose
def mouse_up(guid, x, y):
    gui['click'] = False
    for callback in callbacks['mouse_up'].values():
        try:
            callback(x, y, True)
        except:
            ...

## Public interface ###############

def mouse_position():
    return gui['mouse']

def key_state(key):
    return gui.get(key, False)

def add_callback(guid, key, callback):
    callbacks[key][guid] = callback

