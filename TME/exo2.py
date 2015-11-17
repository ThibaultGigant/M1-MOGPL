# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:09:51 2015

@author:  3363567
"""

from gurobipy import *



nbcont=2
nbvar=3

# on change le nombre de contraintes en nombre de variables et inversement pour récupérer le dual
nbvar, nbcont = nbcont, nbvar

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
#a = [[1,2,3],
#     [3,1,1]]

a = [[1,3],
     [2,1],
     [3,1]]

# Second membre
b = [8, 5]

# Coefficients de la fonction objectif
c = [7, 3, 4]

# on change le second membre en coeffs de la fonction objectif et inversement pour récupérer le dual
b, c = c, b

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
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print ""                
print 'Solution optimale:'
for j in colonnes:
    print 'x%d'%(j+1), '=', x[j].x
print ""
print 'Valeur de la fonction objectif :', m.objVal


#################################
## Commentaires sur l'exercice ##
#################################

# On obtient la même solution optimale pour D et P dans le cas des variables réelles (14,2),
# en revanche dans le cas de variables entières, on obtient une solution optimale de valeur 15 pour le primal et 13 pour le dual

   