# -*- coding: utf8 -*-
#===============================================================================
#Exercice 3 : Calculer le périmétre d'un polygone dont les points sont contenus 
#             une liste 
#===============================================================================

import math as m

#===============================================================================
#Fonction : CalculPerimetrePolygone
#entrées : polygone sous forme d'une liste de points
#sortie  : la valeur du périmétre du polygone, la valeur est un float
#===============================================================================

def CalculPerimetrePolygone(polygone):
    perimetre=0
    for i in range(len(polygone)-1):
        perimetre+=m.sqrt((polygone[i+1][0]-polygone[i][0])**2+(polygone[i+1][1]-polygone[i][1])**2)
    perimetre+=m.sqrt((polygone[0][0]-polygone[len(polygone)-1][0])**2+(polygone[0][1]-polygone[len(polygone)-1][1])**2)
    return perimetre

# --------------------------------------------------------------------------------------------

#   PROGRAMME PRINCIPAL

# --------------------------------------------------------------------------------------------
A=(0,0)
B=(1,0)
C=(1,1)
D=(0,1)
polygone=[A,B,C,D]
print(polygone)
print(CalculPerimetrePolygone(polygone))