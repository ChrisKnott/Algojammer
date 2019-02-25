import random

X = [random.random() for n in range(100)]

done = False
while not done:
	done = True
	for i, _ in enumerate(X):
		if i < len(X) - 1:
			a, b = X[i], X[i + 1]
			if a > b:
				done = False
				X[i], X[i + 1] = b, a
