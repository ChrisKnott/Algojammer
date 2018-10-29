import eel, copy as cpy, html as htm, os, json as jsn
import tkinter as tkt, tkinter.filedialog as fdg
import drawing as drw, state as sta

box_code = {}
data = {'snapshot': {},
        'modules': {}}

@eel.expose
def get_state_box_templates():
    templates = {}
    for folder, _, files in os.walk('templates'):
        d = templates
        for p in folder.split(os.path.sep):
            if p not in d:
                d[p] = {}
            d = d[p]

        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(folder, file), encoding='utf8') as file:
                    lines = file.read().split('\n')
                    name, code = lines[0], '\n'.join(lines[1:])
                    d[name] = code
    return templates

@eel.expose
def set_state_box_code(uid, code):
    box_code[uid] = code.strip()
    update_state_boxes(None, None)

@eel.expose
def delete_state_box(uid):
    box_code.pop(uid)

@eel.expose
def get_state_box_code(uid):
    return box_code[uid]

def state_print(*args, **kwargs):
    sep, end = kwargs.get('sep', ' '), kwargs.get('end', '\n')
    output = sep.join(str(arg) for arg in args) + end
    data['print'] += output

@eel.expose
def update_state_boxes(snapshot, modules):
    snapshot = snapshot or data['snapshot']
    data['snapshot'] = snapshot

    modules = modules or data['modules']
    data['modules'] = modules

    for uid, code in box_code.items():
        snapshot_copy = cpy.deepcopy(snapshot)
        snapshot_copy.update(modules)
        snapshot_copy['jam'] = sta.Jam()
        snapshot_copy['print'] = state_print
        try:
            if code.startswith('#draw'):
                # Add drawing functions to snapshot scope
                for f in 'ink line circ rect font text'.split():
                    snapshot_copy[f] = ast.literal_eval('drw.' + f)
                drw.start()
                exec(code, snapshot_copy)
                value = drw.end()
            else:
                data['print'] = ''
                exec(code, snapshot_copy)
                value = htm.escape(data['print'])
        except Exception as e:
            value = htm.escape(repr(e))

        eel.set_state_box_value(uid, value)

root = tkt.Tk()
root.withdraw()
root.update()

@eel.expose
def save_state_boxes(box_info):
    for i, box in enumerate(box_info):
        box_info[i]['code'] = box_code[box['id']]
    
    root.update()
    save_path = fdg.asksaveasfilename()
    root.update()

    with open(save_path, 'w', encoding='utf8') as save_file:
        jsn.dump(box_info, save_file)

@eel.expose
def load_state_boxes():
    root.update()
    load_path = fdg.askopenfilename()
    root.update()

    with open(load_path, encoding='utf8') as load_file:
        box_info = jsn.load(load_file)
        return box_info

