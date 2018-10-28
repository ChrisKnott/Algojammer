Graph
#draw
import math

G = %expr
s = 120
font(12)

nodes = list(G)

def pos(n):
    i = nodes.index(n)
    theta = (2 * math.pi * i) / len(nodes)
    px = s + s * math.sin(theta)
    py = s - s * math.cos(theta)
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