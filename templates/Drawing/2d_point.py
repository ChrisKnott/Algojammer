2D Point
#draw
x, y = %expr
grid = 20
size = 500

ink(200, 200, 200)
for n in range(5, size, grid):
    line(5, n, size + 5, n)
    line(n, 5, n, size + 5)

ink(50, 100, 200)
circ(5 + x * grid, 5 + y * grid, 3)
