code = '''
import random
X = [[i] * 10 for i in range(10)]
random.shuffle(X)
print(X)
'''

code = '''
def f(x):
    a = x + 1
    print(a)

f(123)
'''

import dis
import sys
import io
import inspect

disses = {}

# frame
# 'f_back', 'f_builtins', 'f_code', 'f_globals', 'f_lasti', 'f_lineno', 'f_locals', 'f_trace'

# frame.f_code
# 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 
# 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize', 'co_varnames'

def tr(frame, what, args):
    if not hasattr(frame, 'jam'):
        frame.f_locals = None

    return tr

#sys.settrace(tr)
code = compile(code, 'test', 'exec')
#exec(code)
dis.dis(code)
#print(dir(code))
#print(code.co_names)
#print(code.co_varnames)

for c in []:#'<module> shuffle _randbelow'.split():
    code = disses[c]
    file = io.StringIO()
    dis.dis(code.co_code, file=file)

    print(c)
    print(file.getvalue())
    print('')
    for k in 'co_names co_varnames co_consts co_cellvars'.split():
        print(k)
        for i, v in enumerate(getattr(code, k)):
            print(i, v)
        print('')
    try:
        print(inspect.getsource(code))
    except:
        pass

import sys; sys.exit()

import pickle # way to convert a python object (list, dict, etc.) into a character stream.
import random
import io
import pickletools
import gc

def save_referents(obj):
    depth, _, _ = objects.get(id(obj), (0, None, None))
    if depth == 0:
        depth = 1
        for ref in gc.get_referents(obj):
            depth = max(depth, save_referents(ref) + 1)
        objects[id(obj)] = (depth, id(obj), obj)
    return depth

X = [[random.randint(0, 1000) for n in range(10)] for m in range(10)]

pickles = []

for state in 0, 1:
    random.shuffle(X)
    b = io.BytesIO()
    p = pickle.Pickler(b)

    objects = {}
    save_referents(X)
    for _, _, obj in sorted(objects.values()):
        p.dump(obj)

    p.dump({'X': X})
    pickles += [b.getvalue()]

A, B = pickles

# See how different A and b are
diffs = 0
for a, b in zip(A, B):
    if a != b:
        diffs += 1

print('A, B differ at', diffs, 'bytes\n')

for data in A, B:
    b = io.BytesIO(data)
    p = pickle.Unpickler(b)

    while True:
        try:
            globs = p.load()
        except EOFError:
            break

    X = globs['X']
    for row in X:
        print(row)
    print('\n')
