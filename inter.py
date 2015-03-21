#!/usr/bin/env python

import simp

# Generates two columns: x, f(x)  from input file

eng = []; den = [] #x; f(x)
with open('input.dat', 'r') as r:
    for line in r:
        if not (line.startswith("#")):
            col1, col2 = [float(x) for x in line.split()]
            eng.append(col1); den.append(col2)

# Asks user input 

si = raw_input("Enter the initial index: ")
si = int(si) - 1
fi = raw_input("Enter the final index: ")
fi = int(fi) - 1
print '[', eng[si], ':', eng[fi], ']'
ind = raw_input("Enter the index distance: ")
ind = int(ind)

# Loops over indicies

pivot = si
with open('output.dat', 'w') as w:
    while (si < fi):
        res = simp.quad(eng, den, pivot, ind)
        w.write('{0} {1}\n'.format(eng[si], res))
        si += ind; pivot = si
