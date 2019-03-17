import bisect

timeline = { 'mouse':        0, 'steps':     50,
             'dot_width':    8, 'grab':   False,
             'line_height': 19, 'margin':     5 }
camera = { 'scale':  15.0, 's_scale':   1.0,
           'x':     -20.0, 's_x':     -20.0 }

# Mouse controls
@jam.on_click
def timeline_click(x, y):
    timeline['grab'] = x

@jam.on_wheel
def timeline_zoom(direction):
    mouse_x = step_to_px(timeline['mouse'])
    anchor = round((mouse_x + camera['s_x']) / camera['s_scale'])
    
    if direction == 1:
        new_scale = clamp_scale(camera['scale'] * 1.25)
    elif direction == -1:
        new_scale = clamp_scale(camera['scale'] / 1.25)
    
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
    return max(min(15, scale), 500 / (timeline['steps'] + 1))

# Drawing functions
def draw_ruler(step):
    x, tag = step_to_px(step), '{:,}'.format(step)
    jam.stroke(x, 0, x, jam.canvas.height)
    jam.text(x + 3, jam.canvas.height - 3, tag, 14)

def draw_rulers():
    stride, s, scale = 10, 0, [2, 5]
    while stride < 80 / camera['scale']:
        stride *= scale[s]
        s = 1 - s

    ruler_step = stride * round(camera['x'] / (camera['scale'] * stride))

    jam.ink(80, 80, 80)
    while ruler_step <= px_to_step(jam.canvas.width):
        draw_ruler(ruler_step)
        ruler_step += stride

    jam.ink(150, 150, 120)
    draw_ruler(timeline['mouse'])

def get_visible_runs():
    '''Efficiently calculate a representation of the Timeline'''
    left_step  = max(0, px_to_step(0) - 1)
    right_step = min(timeline['steps'], px_to_step(jam.canvas.width) + 1)
    gap = timeline['dot_width'] / camera['s_scale']
    runs = []
    for line in range(1, jam.num_lines() + 1):
        V = jam.visits(line)
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
    runs = get_visible_runs()
    mouse_x = step_to_px(timeline['mouse'])
    mouse_line = jam.line(timeline['mouse'])

    jam.ink(150, 150, 150)
    jam.stroke(0, line_to_px(mouse_line), jam.canvas.width, line_to_px(mouse_line))

    for line, start, end, visits in runs:
        a = step_to_px(start) - 4
        b = step_to_px(end) + 4
        if end < timeline['mouse']:                     # Totally before
            jam.ink(220, 220, 200)
            jam.rect(a, line_to_px(line) - 4, b - a, 8)
        elif start > timeline['mouse']:                 # Totally after
            jam.ink(100, 100, 80)
            jam.rect(a, line_to_px(line) - 4, b - a, 8)
        else:                                           # Split in two
            jam.ink(220, 220, 200)
            jam.rect(a, line_to_px(line) - 4, mouse_x - a, 8)
            jam.ink(100, 100, 80)
            jam.rect(mouse_x, line_to_px(line) - 4, b - mouse_x, 8)
    
    jam.ink(220, 220, 200)
    jam.rect(mouse_x - 5, line_to_px(mouse_line) - 5, 10, 10)  # Current step


# Draw frame
camera['x'] = max(camera['x'], -15.0)
camera['scale'] = clamp_scale(camera['scale'])

if not jam.key('click'):
    timeline['grab'] = False
elif timeline['grab']:
    mouse_x, _ = jam.mouse_position()
    camera['x'] += (timeline['grab'] - mouse_x)
    timeline['grab'] = mouse_x

camera['s_x'] += (camera['x'] - camera['s_x']) * 0.4
camera['s_scale'] += (camera['scale'] - camera['s_scale']) * 0.4

mouse_step = round((canvas.mx + camera['x']) / camera['scale'])
timeline['mouse'] = max(0, min(mouse_step, timeline['steps'] - 1))

canvas.clear()
draw_rulers(canvas)

timeline['steps'] = jam.steps()
draw_dots(canvas, recording)




