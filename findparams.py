#!/usr/bin/env python

import fnmatch
from os import listdir
import numpy
from scipy.optimize import minimize, basinhopping


# Store z coordinates data

zcor = []
for file in listdir('.'):
    if fnmatch.fnmatch(file, '3p??.dat'):
        with open(file, 'r') as r:
          for line in r:
              if not (line.startswith("#")):
                col = line.split()
                zcor.append(float(col[2]))
        
# Write z planes

cz = 38.7; zplane = []; iter = 0;
while (iter < range(len(zcor))):
    if (iter == 25):
        zplane.append(cz * (zcor[iter] + zcor[iter + 1]) / 2)
        break
    zplane.append(cz * (zcor[iter] + zcor[iter + 4]) / 2)
    zplane.append(cz * (zcor[iter + 1] + zcor[iter + 2] + zcor[iter + 3]) / 3)
    iter += 5
zplane = zplane[3:(len(zplane)-3)]; xm = zplane[(len(zplane)/2)]

# Store E data

eng = []
for file in listdir('.'):
    if fnmatch.fnmatch(file, 'l1.dat'):
        with open(file, 'r') as r:
            for line in r:
              if not (line.startswith("#")):
                col = line.split()
                eng.append(float(col[0]))

# Store E, lnum, Q(E,z)

ezq = []; ltot = 0;
for file in listdir('.'):
    if fnmatch.fnmatch(file, 'l?.dat'):
        ltot += 1
        with open(file, 'r') as r:
          for line in r:
              if not (line.startswith("#")):
                col = line.split()
                ezq.append([float(col[0]), int(file[1]), float(col[1])])

# Loops over E in array to print z, Q(z)

def func_ch(x, *p): # Fitting function: Cosh
    a, dl, dr = p
    return a * (numpy.exp((x - xm) / dr) + numpy.exp(-(x - xm) / dl))
#def func_chgs(x, *p): # Fitting function: Cosh + Guassian
#    a, dl, dr, sd = p
#    return a * (numpy.exp((x - xm) / dr) + numpy.exp(-(x - xm) / dl) + numpy.exp((-(x - xm)**2.0) / sd))

def minbounds(**kwargs): # Bounds for Basin Hopping
    x = kwargs["x_new"]
    tmin = bool(numpy.all(x >= 0.0))
    return tmin


curves = open('curves.dat', 'w')
params = open('params.dat', 'w')
for evalue in eng: # E
#evalue = eng[0]
#if (evalue == eng[0]):
    xvar = []; yvar = []
    for iter in range(1, ltot + 1): # z
        for j in range(len(ezq)): # rows
            if ((evalue == ezq[j][0]) and (iter == ezq[j][1])):
                xvar.append(zplane[iter - 1]); yvar.append(ezq[j][2])
                curves.write('{0} {1}\n'.format(zplane[iter - 1],ezq[j][2]))
    curves.write('\n\n')

    xvar = numpy.asarray(xvar,dtype='int64'); yvar = numpy.asarray(yvar,dtype='int64')
    p0 = [0.1, 5.0, 5.0]; error = lambda p: numpy.mean((yvar - func_ch(xvar, *p))**2.0)
#    par = minimize(error, p0, bounds=[(0, None), (0, None), (0, None)], method="L-BFGS-B").x
    par = basinhopping(error, p0, T=0.5, minimizer_kwargs={"method":"L-BFGS-B"}, niter=1000, accept_test=minbounds).x

    params.write('{0} {1} {2} {3}\n'.format(evalue, par[0], par[1], par[2]))
#    params.write('{0} {1} {2} {3} {4}\n'.format(evalue, par[0], par[1], par[2], par[3]))

curves.close(); params.close()
