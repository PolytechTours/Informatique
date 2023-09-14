# -*- coding: utf8 -*-
#===============================================================================
#Exercice 2 : Calculer la distance euclidienne entre deux points 
#             de coordonnées (x,y)
#===============================================================================
import math as m

#===============================================================================
#Fonction DistanceEuclidienne
# entrée : 2 points de coordonnées x,y
# sortie : la distance
#===============================================================================
def DistanceEuclidienne(A,B):
    distance = m.sqrt((B[0]-A[0])**2+(B[1]-A[1])**2)
    return distance

# --------------------------------------------------------------------------------------------

#   PROGRAMME PRINCIPAL

# --------------------------------------------------------------------------------------------

pointA=(0,0)
pointB=(1,1)
print(pointA)
print(pointB)

print(DistanceEuclidienne(pointA,pointB))