import eel
import jam, drawing, mock

metacode = {}                               # Meta source code for each Sketch
compiled = {}                               # Compiled metacode for each Sketch
proxies = {}                                # Control proxies passed to each Sketch

def set_metacode(guid, source, control):
    if source != metacode.get(guid):  # If source has changed...
        try:
            metacode[guid] = source
            compiled[guid] = None
            compiled[guid] = compile(source, '<metacode>', 'exec')
            proxies[guid] = jam.Proxy(control, guid)
        except Exception as e:
            pass;print('Exception set_metacode:', e)

@eel.expose
def get_metacode(guid):
    return metacode.get(guid, '')

def run_metacode(guid):
    try:
        code = compiled.get(guid)
        if code != None:
            proxy = proxies[guid]
            proxy.io = mock.MockIO()

            exec_vars = proxy.io.functions()
            exec_vars['jam'] = proxy

            # TODO: make execorder w/ max steps set + callback
            exec(code, exec_vars)
        else:
            pass;print("Can't run uncompilable code")
    except Exception as e:
        pass;print('Exception run_metacode:', e)

@eel.expose
def sketch_refresh(guid, geometry):
    proxy = proxies.get(guid)
    if proxy:
        proxy.io = mock.MockIO()
        proxy.canvas = drawing.Canvas(*geometry)
        try:
            if proxy.refresh_callback != None:
                proxy.refresh_callback()
            else:
                run_metacode(guid)      # No refresh callback defined - re-run all code
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('-'*50)
            #pass;print('Exception sketch_refresh:', e)

        return {'output': proxy.io.get_output(),
                'canvas': proxy.canvas.commands()}

    return {'output': 'ERROR', 'canvas': []}

@eel.expose
def sketch_click(guid, x, y):
    try:
        proxy = proxies.get(guid)
        if proxy and proxy.click_callback != None:
            proxy.click_callback(x, y, True)
    except Exception as e:
        print(e)

@eel.expose
def sketch_wheel(guid, direction):
    proxy = proxies.get(guid)
    if proxy and proxy.wheel_callback != None:
        proxy.wheel_callback(direction)

