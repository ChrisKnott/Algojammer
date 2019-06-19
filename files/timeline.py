import eel, bisect
import gui

# TODO: once Sheets and Metacode are powerful enough, this should be
# done entirely as a standard Sheet. At the moment it's sort of halfway

timeline = { 'mouse':        0, 'steps':     50,
             'dot_width':    8, 'grab':   False,
             'line_height': 19, 'margin':     5 }
camera = { 'scale':  15.0, 's_scale':   1.0,
           'x':     -20.0, 's_x':     -20.0 ,
           'zoom_rate': 2.0}

# Mouse controls
@eel.expose
def timeline_click(x, y, down):
    if down:
        timeline['grab'] = x
    else:
        timeline['grab'] = False

@eel.expose
def timeline_zoom(direction):
    mouse_x = step_to_px(timeline['mouse'])
    anchor = round((mouse_x + camera['s_x']) / camera['s_scale'])
    
    if direction == 1:
        new_scale = clamp_scale(camera['scale'] * camera['zoom_rate'])
    elif direction == -1:
        new_scale = clamp_scale(camera['scale'] / camera['zoom_rate'])
    
    camera['x'] += anchor * (new_scale - camera['scale'])
    camera['scale'] = new_scale

# Utility functions
def line_to_px(line):
    return timeline['line_height'] * line - timeline['margin']

def step_to_px(step):
    return (step * camera['s_scale']) - camera['s_x']

def px_to_step(x):
    return round((x + camera['s_x']) / camera['s_scale'])

def clamp_scale(scale):
    return max(min(15, scale), 500 / timeline['steps'])

# Drawing functions
def draw_ruler(canvas, step):
    x, tag = step_to_px(step), '{:,}'.format(step)
    canvas.line(x, 0, x, canvas.height)
    canvas.text(x + 3, canvas.height - 3, tag, 14)

def draw_rulers(canvas):
    step, s, scale = 10, 0, [2, 5]
    while step < 80 / camera['scale']:
        step *= scale[s]
        s = 1 - s

    shift = step * round(camera['x'] / (camera['scale'] * step))
    
    canvas.ink(80, 80, 80)
    for i in range(10):
        draw_ruler(canvas, shift + (i * step))

    canvas.ink(150, 150, 120)
    draw_ruler(canvas, timeline['mouse'])

def get_visible_runs(recording, canvas_width):
    '''Efficiently calculate a representation of the Timeline'''
    left_step  = max(0, px_to_step(0) - 1)
    right_step = min(timeline['steps'], px_to_step(canvas_width) + 1)
    gap = timeline['dot_width'] / camera['s_scale']
    runs = []
    for line in range(50):      # TODO
        V = recording.visits(line)
        if len(V) > 0:
            s = e = bisect.bisect_left(V, left_step)
            while e < len(V) and V[e] <= right_step:
                jump = 1
                while jump >= 1 and V[e] < right_step:
                    if e + jump < len(V) and V[e + jump] - V[e] <= gap:
                        e += jump   # This visit overlaps, extend run
                        jump *= 2   # Also, next time, try a bigger jump
                    else:
                        jump //= 2  # Didn't overlap - try smaller jump

                num_visits = e - s + 1
                runs += [(line, V[s], V[e], num_visits)]
                s = e = e + 1
    return runs

def draw_dots(canvas, recording):
    runs = get_visible_runs(recording, canvas.width)
    mouse_x = step_to_px(timeline['mouse'])
    mouse_line = recording.line(timeline['mouse'])

    canvas.ink(150, 150, 150)
    canvas.line(0, line_to_px(mouse_line), canvas.width, line_to_px(mouse_line))

    for line, start, end, visits in runs:
        a = step_to_px(start) - 4
        b = step_to_px(end) + 4
        if end < timeline['mouse']:                     # Totally before
            canvas.ink(220, 220, 200)
            canvas.rect(a, line_to_px(line) - 4, b - a, 8)
        elif start > timeline['mouse']:                 # Totally after
            canvas.ink(100, 100, 80)
            canvas.rect(a, line_to_px(line) - 4, b - a, 8)
        else:                                           # Split in two
            canvas.ink(220, 220, 200)
            canvas.rect(a, line_to_px(line) - 4, mouse_x - a, 8)
            canvas.ink(100, 100, 80)
            canvas.rect(mouse_x, line_to_px(line) - 4, b - mouse_x, 8)
    
    canvas.ink(220, 220, 200)
    canvas.rect(mouse_x - 5, line_to_px(mouse_line) - 5, 10, 10)  # Current step

def draw_timeline(canvas, recording):
    camera['x'] = max(camera['x'], -15.0)
    camera['scale'] = clamp_scale(camera['scale'])

    if timeline['grab']:
        mouse_x, _ = gui.mouse_position()
        camera['x'] += (timeline['grab'] - mouse_x)
        timeline['grab'] = mouse_x

    camera['s_x'] += (camera['x'] - camera['s_x']) * 0.4
    camera['s_scale'] += (camera['scale'] - camera['s_scale']) * 0.4
    
    mouse_step = round((canvas.mx + camera['x']) / camera['scale'])
    timeline['mouse'] = max(0, min(mouse_step, timeline['steps'] - 1))

    canvas.clear()
    draw_rulers(canvas)
    if recording:
        timeline['steps'] = recording.steps()
        draw_dots(canvas, recording)
