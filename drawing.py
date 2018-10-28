drawing = {'num': 0}

with open('canvas.html', encoding='utf8') as template_file:
    template = template_file.read()

def start():
    drawing['num'] += 1
    canvas_id = 'state_canvas%d' % drawing['num']
    drawing['code'] = template.replace(r'%id', canvas_id) \
                              .replace(r'%width', '600')  \
                              .replace(r'%height', '600')

def end():
    return drawing['code'].replace(r'%drawing', '')

def add(code):
    drawing['code'] = drawing['code'].replace(r'%drawing', code + r'%drawing')

# User methods
def ink(r, g, b):
    add('''
    c$.fillStyle = 'rgb(%d, %d, %d)';
    c$.strokeStyle = 'rgb(%d, %d, %d)';''' % (r, g, b, r, g, b))

def line(x1, y1, x2, y2):
    add('''
    c$.beginPath();
    c$.moveTo(%d, %d);
    c$.lineTo(%d, %d);
    c$.closePath();
    c$.stroke();''' % (x1, y1, x2, y2))

def rect(x, y, w, h):
    add('''
    c$.fillRect(%d, %d, %d, %d);''' % (x, y, w, h)) 

def circ(x, y, r):
    add('''
    c$.beginPath();
    c$.arc(%d, %d, %d, 0, 2 * Math.PI);
    c$.fill();
    c$.stroke();''' % (x, y, r))

def font(size):
    add('''
    c$.font = '%dpx Arial';''' % size)

def text(s, x, y):
    add('''
    c$.fillText(%s, %d, %d);''' % (repr(s), x, y))
