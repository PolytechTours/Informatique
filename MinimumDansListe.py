# -*- coding: utf8 -*-
#===============================================================================
#Exercice 1 : Trouver le nombre minimum dans une liste de nombres
#             et afficher le résultat
#===============================================================================



#===============================================================================
#Fonction RecherchMinimumDansListe
#Entrées : Une liste de nombres
#Sortie: le minimum
# 
#===============================================================================
def RecherchMinimumDansListe(uneliste):
    minimum=uneliste[0]
    for i in range(1,len(uneliste)):
        if uneliste[i]<minimum:
            minimum=uneliste[i]
    return minimum



# --------------------------------------------------------------------------------------------

#   PROGRAMME PRINCIPAL

# --------------------------------------------------------------------------------------------


#une list de nombres
maliste=[10,5,8,2,45,32]
print(maliste)
print(RecherchMinimumDansListe(maliste))

