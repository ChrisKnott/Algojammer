import io, sys, copy as cpy, traceback as tbk, types as typ, time as tme
import hashlib as hsh, state as sta, algorecord as rec, pickle as pkl, io

def bounded_exec(code, limit, report):
    D = {'hash': hsh.md5(code.encode('utf-8')).hexdigest(),
         'line': [], 'steps': 0}

    def update(lines):
        D['steps'] += len(lines)
        D['line'] = lines
        report(D)

        if D['steps'] > limit:
            raise RuntimeError('Reached max execution steps')

        tme.sleep(0.001)    # Yield to other threads        

    try:
        code = compile(code, 'algojammer', 'exec')
        rec.clear_recordings()
        rec.start_trace(update)
        exec(code, {})
    except Exception as e:
        tbk.print_exc()

    rec.stop_trace()
