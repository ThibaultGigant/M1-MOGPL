# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:09:51 2015

@author:  3363567 et 3200818
"""

from gurobipy import *
from numpy import arange, array, ones, linalg
from pylab import plot, show

xi = array([4, 17, 37, 55, 88, 96])
A = array([xi, ones(6)])
# linearly generated sequence
y = [11, 25, 46, 48, 65, 71]
# obtaining the parameters
w = linalg.lstsq(A.T,y)[0]
# plotting the line
line = w[0]*xi+w[1] # regression line
plot(xi, line, 'r-', xi, y, 'o')
show()

xi = array([4, 17, 37, 55, 88, 14])
A = array([xi, ones(6)])
# linearly generated sequence
y = [11, 25, 46, 48, 65, 97]
# obtaining the parameters
w = linalg.lstsq(A.T,y)[0]
# plotting the line
line = w[0]*xi+w[1] # regression line
plot(xi, line, 'r-', xi, y, 'o')
show()


nbcont=12
nbvar=8


# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [0, 0, 0, 1, 0, 0],
     [0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 1, 0],
     [0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 1]]


# ajout des variables w0 et w1
for i in range(len(a)):
    if i%2 == 0:
        a[i] += [xi[i//2], 1]
    else:
        a[i] += [-xi[i//2], -1]


# Second membre
b = []
for i in y:
    b += [i,-i]

# Coefficients de la fonction objectif
c = [1]*(nbvar-2)+[0,0]

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print ""                
print 'Solution optimale:'
for j in colonnes:
    print 'x%d'%(j+1), '=', x[j].x
print ""
print 'Valeur de la fonction objectif :', m.objVal


xi = array([4, 17, 37, 55, 88, 14])
A = array([xi, ones(6)])
# linearly generated sequence
y = [11, 25, 46, 48, 65, 97]
# obtaining the parameters
w = linalg.lstsq(A.T,y)[0]
w[0] = x[-2].x
w[1] = x[-1].x
# plotting the line
line = w[0]*xi+w[1] # regression line
plot(xi, line, 'r-', xi, y, 'o')
show()
