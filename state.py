import eel
import random as rnd, copy as cpy, pickle as pkl, io, algorecord as rec

execution = {}

class Jam:
    def state(self, n):
        state_at_step_n = State()
        state_dict, _ = get_state(n)
        for var, val in state_dict.items():
            setattr(state_at_step_n, var, val)
        return state_at_step_n

    def visits(self, n):
        if 0 <= n < len(execution['visits']):
            return execution['visits'][n]
        else:
            return []

    def line(self, s):
        return execution['lines'][s]

    def stack(self, n):
        return []   # TODO: This needs some refactoring in the C++ module to work...

class State:
    pass

def execution_start():
    execution['lines'] = []
    execution['visits'] = []

def execution_report(data):
    shift = len(execution['lines'])
    execution['lines'] += data['line']
    for i, l in enumerate(data['line']):
        if l > len(execution['visits']):
            for _ in range(len(execution['visits']), l):
                execution['visits'].append([])

        execution['visits'][l - 1].append(i + shift);

@eel.expose
def get_all_variables():
    var_names = [str(s) for s in rec.get_all_variables()] # weird bugs here...
    return sorted(var_names)

def get_state(step):
    # Could move this whole function into C++ ext for performance...
    milestone = rec.get_milestone(step)

    obj = {0: None}
    bytes_io = io.BytesIO(milestone['pickle_bytes'].getvalue())
    unpickler = pkl.Unpickler(bytes_io)
    for obj_id in milestone['pickle_order']:
        try:
            obj[obj_id] = unpickler.load()
        except:
            obj[obj_id] = '<pickle error>'

    state = {}
    for s, op, o, k, v in milestone['assignments']:
        # This is a sort of mini VM that re-executes all assignments
        if s <= step:
            if v in obj:
                if op == 0:     # o = v
                    state[obj[o]] = obj[v]
                elif op == 1:   # o[k] = v
                    obj[o][obj[k]] = obj[v]
                elif op == 2:   # o.k = v
                    setattr(obj[o], obj[k], obj[v])
        else:
            break

    return state, {}
