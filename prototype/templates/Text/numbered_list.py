Numbered List
X = %expr
fmt = '%%%dd) %%s' % len(str(len(X)))
for i, x in enumerate(X):
    print(fmt % (i, repr(x)))