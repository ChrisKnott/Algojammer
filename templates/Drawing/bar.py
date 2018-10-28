Bar Chart
#draw

X = %expr
width, height = 300, 100
max_height = max(X)
bar_width = width / len(X)

ink(50, 100, 200)
for i, x in enumerate(X):
    h = height * (x / max_height)
    rect(i * bar_width, height - h, bar_width, h)

ink(0, 0, 0)
rect(0, height - 1, width + 2, 2)