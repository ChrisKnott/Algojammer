Grid
X = %expr
X = [[repr(x) for x in row] for row in X]
n = max(max(len(s) for s in row) for row in X)

for row in X:
	for s in row:
		print(s.rjust(n), end=' ')
	print('')
