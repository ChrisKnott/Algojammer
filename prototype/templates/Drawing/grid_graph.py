Grid Graph
#draw

G = %expr
width, height = 250, 250
font(12)

x_max = max(x for x, y in G)
y_max = max(y for x, y in G)

def pos(n):
    x, y = n
    px = x * (width / x_max)
    py = y * (height / y_max)
    return px + 5, py + 5

for n in G:
    x, y = pos(n)
    ink(150, 150, 150)
    for m in G[n]:
        x2, y2 = pos(m)
        line(x, y, x2, y2)
    ink(0, 0, 0)
    circ(x, y, 3)
    text(repr(n), x + 5, y + 12)
