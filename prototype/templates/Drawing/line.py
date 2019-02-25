Line Chart
#draw

X = %expr
width, height = 300, 100
max_height = max(X)
line_width = width / len(X)

ink(100, 200, 50)
for i, x in enumerate(X):
    if i > 0:
        h0 = height * (X[i - 1] / max_height)
        h1 = height * (X[i] / max_height)
        x0 = i * line_width
        x1 = x0 + line_width
        line(x0, height - h0, x1, height - h1)

ink(0, 0, 0)
rect(0, height - 1, width + 2, 2)