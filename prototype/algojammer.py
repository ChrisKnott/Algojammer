import eel, state_boxes as sbx, execution as exe, state as sta, time as tme

state = {
    'step': 0,
    'snapshots': [],
    'mode': 'stopped'
}
page_geom = {
    'algojammer.html': {'size': (1300, 800), 'position': (610, 200)},
    'sheet.html':      {'size': ( 500, 800), 'position': (100, 200)}
}

eel.init('web')

@eel.expose
def read_example():
    with open('files/example.py', encoding='utf8') as example_file:
        eel.set_code(example_file.read())

@eel.expose
def run(code, stdin=''):
    while state['mode'] != 'stopped':
        state['mode'] = 'interrupt'
        eel.sleep(0.01)

    state['mode'] = 'running'
    sta.execution_start()
    exe.bounded_exec(code, 10**7, report)
    state['mode'] = 'stopped'

def report(data):
    if state['mode'] == 'interrupt':
        raise InterruptedError('Code changed during execution')

    sta.execution_report(data)
    eel.execution_report(data)

@eel.expose
def update_state(n=state['step'], force=False):
    if n != state['step'] or force:
        state['step'] = n
        snapshot, modules = sta.get_state(n)
        sbx.update_state_boxes(snapshot, modules)

eel.start('algojammer.html', geometry=page_geom)
