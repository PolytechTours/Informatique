#import matplotlib.pyplot as plt
#import networkx as nx
#import graphviz as gv

from tkinter import *       # pour affichage de la carte

import math                 # focntion trigo pour conversion en coordonnées cartésienne
import sys
from random import *
import math     # fonction trigo pour conversion en coordonnées cartésienne
from collections import OrderedDict

# --------------------------------------------------------------------------------------------
#      VARIABLES GLOBALES
#       dimension fenetre et cercle
# --------------------------------------------------------------------------------------------

# fenetre
winWidth =1000     # largeur de la fenetre
winHeight = 720     # hauteur de la fenetre : recalculée en focntion de la taille du graphe
MaxHeight =720     # hauteur maximale de la fenetre
border = 20             # taille en px des bords

# decalration ratio mise a l'echelle
ratio= 1.0                  # rapport taille graphe / taille fenetre
ratioWidth = 1.0      #  rapport largeur graphe/ largeur de la fenetre
ratioHeight =1.0      #  rapport hauteur du graphe hauteur de la fenetre

#  cercle
rayon = 1                # rayon pour dessin des points
""" mettre 10 pour les graphes de tests
et mettre 1 pour les vrai graphes paris et berlin
"""


# defintion source et dest par defaut 
Source = 0
Destination = 0

# Permet de stocker mapper les noeud avec les cercles qui sont leur représentation graphie pour les retrouver suite à unclick de la souris
MappageNoeud = OrderedDict()

# --------------------------------------------------------------------------
#   Classe d'un arc
#   indice Sommet Source , indice sommet Dest , longueur, danger
# --------------------------------------------------------------------------
class Arc : 
     indSource = 0    # indice du noued Source de l'arc
     indDest = 0      # indice du noued destination de l'arc 
     longueur = 0       # longueur de l'arc en me
     danger = 0          # danger de l'arc 


    # constructzeur par defaut : indice du noued spource, indice du noeud destination de l'arc, diatnce de l'arc et danger de l'arc
     def __init__(self, indS, indD, long, dang) :
         self.indSource = indS 
         self.indDest =  indD 
         self.longueur = long
         self.danger = dang

    # affichage formaté en console d'un arc
     def affiche(self):
         print("--- Affiche Arc ---")
         print(" indiceSource = ", self.indSource)
         print(" indiceDest = ", self.indDest)
         print(" long = ", self.longueur)
         print(" lat =  ", self.danger)

    # ffichage graphique de l'arc : le graphe qui contient l'arc à afficher, le canvas d'affichage, la couleur 
     def dessinArc(self, graphe, can, color):
         noeudSource = graphe.listeNoeud[self.indSource]
         noeudDest = graphe.listeNoeud[self.indDest]

         xStart = noeudSource.pixelX
         yStart = noeudSource.pixelY

         xEnd = noeudDest.pixelX
         yEnd = noeudDest.pixelY
         arc = can.create_line(xStart, yStart, xEnd, yEnd, fill=color, width =1)
         MappageNoeud[arc] = self.indSource


# --------------------------------------------------------------------------
#   Classe d'un noeud
#   Long , Lat, X (coordonnée cartesienne), Y(coordonnée cartesienne)
#   données pour l'afficahe ( en pixel)
#   liste des arcs sortant du noeud
# --------------------------------------------------------------------------
class Noeud:
     
     indice = 0             # indice du noued
     longitude = 0.0        #longitude en radian 
     latitude  = 0.0        #latitude en radian 
     coordX = 0             # cordX dans la fenetre 
     coordY = 0             # cordY dans la fenetre

     pixelX = 0             # coord en pixel
     pixelY = 0            #coor en pixel 

     listeArcSucc = []     # liste des successeurs (arc sortant du noeud)

     # constructeur par defaut : indice, longitude te latitude en degré
     def __init__(self, ind, long, lat) :
         self.indice = ind
         self.longitude = long
         self.latitude = lat 
         self.listeArcSucc = []
         
    # affichage formaté en console d'un noeud
     def affiche(self):
         print(" ======== Affiche noeud =========")
         print(" indice = ", self.indice)
         print(" long = ", self.longitude)
         print(" lat =  ", self.latitude)
         print(" X =  ", self.coordX)
         print(" Y =  ", self.coordY)
         print("liste Arc Sortant ")
         for arc in self.listeArcSucc : 
            arc.affiche()
         print("-------------")

    # affichage graphique du noeud : le graphe qui contient le noeud à afficher, le canvas d'affichage, la couleur 
     def dessinNoeud(self, graphe, can, color):
        global rayon
        x = self.pixelX
        y = self.pixelY
        cercle  = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline = color, fill = color)
        MappageNoeud[cercle] = self.indice

    # affichage graphique du noeud en gros: le graphe qui contient le noeud à afficher, le canvas d'affichage, la couleur 
     def dessinNoeudHuge(self, graphe, can, color):
        global rayon
        x = self.pixelX
        y = self.pixelY
        can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline = color, fill = color)

     def dessinNoeudSmall(self, graphe, can):
         global rayon
         x = self.pixelX
         y = self.pixelY
         can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline = "grey50", fill = "grey50")

    # affichage graphique du noeud et de tous les arcs sortants du noeud : le graphe qui contient le noeud à afficher, le canvas d'affichage, la couleur 
     def dessinNoeudArc(self, graphe, can, color):
        self.dessinNoeud(graphe, can, color)
        for succ in self.listeArcSucc:
             succ.dessinArc(graphe, can, color)
      

# --------------------------------------------------------------------------
#   Classe d'un graphe 
#   Long , Lat, X, Y
# --------------------------------------------------------------------------
class Graphe:

     listeNoeud = []       #liste des noeuds

    # ajoute d'un noeud au graphe
     def addNoeud(self, noeud) : 
         self.listeNoeud.append(noeud)

    # affichage formaté en console d'un graphe
     def affiche(self) :
         print("--- Affiche graphe ---")
         for n in self.listeNoeud :
             n.affiche()

    
    # ---------------------------------------------------------------   
    # lecture du fichier des noeuds
    # ---------------------------------------------------------------   
     def lectureNoeud(self, chemin): 
         #ouverture du fichier
         fichier = open(chemin, 'r')
         listeNoeud  = fichier.readlines()

         # lecture ligne a ligne
         for line in listeNoeud:
            lineSplit = line.split("\t")                        # coupe la ligne selon separateur tabulation
        
            # recuperation (long ,lat)
            stringLong = lineSplit[1].strip('\n " ')     #permet de nettoyer ligne de caractères inutile (")
            long = float(stringLong)
            long = math.pi *long / 180                      # conversion en radian 
            stringLat= lineSplit[2].strip('\n " ')         #permet de nettoyer ligne de caractères inutile (")
            lat = float(stringLat)
            lat = math.pi*lat / 180                             # conversion en radian 

            #recuperation de l'indice
            stringInd = lineSplit[0].strip('\n " ')
            indNoeud = int (stringInd)
            # ajout au graphe
            noeud = Noeud(indNoeud, long, lat)

            self.addNoeud(noeud)
        
         #femeture du fichier 
         fichier.close()

    # ---------------------------------------------------------------   
    #       lecture du fichier des arcs
    # ---------------------------------------------------------------   
     def lectureArc(self, chemin): 
         #ouverture du fichier
         fichier = open(chemin, 'r')
         listeArc = fichier.readlines()

          # lecture ligne a ligne
         for line in listeArc:
             lineSplit = line.split("\t");
             # recuperation (source, dest, long ,lat)
             stringSource = lineSplit[0].strip('\n " ')       # permet de nettoyer ligne de caractères inutile (")
             source = int(stringSource)
             stringDest= lineSplit[1].strip('\n " ')            # permet de nettoyer ligne de caractères inutile (")
             dest = int(stringDest)
             stringDist= lineSplit[2].strip('\n " ')             #permet de nettoyer ligne de caractères inutile (")
             dist = int(stringDist)
             stringDang= lineSplit[3].strip('\n " ')          # permet de nettoyer ligne de caractères inutile (")
             dang = int(stringDang)
             # creation de l'arc
             arc = Arc(source, dest, dist, dang)

             # recuperation du noeud source
             #print("source =>", source )
             noeud = self.listeNoeud[source]
             noeud.listeArcSucc.append(arc)
             #noeud.affiche()
             #input()

         #femeture du fichier 
         fichier.close()

    # ---------------------------------------------------------------   
    # permet le calcul des cordonnées eX et Y de cahcun des noeud et une mise à l'echelle 
    # ---------------------------------------------------------------   
     def miseEchelle(self):

        # minimum lat, long
         minLat = sys.maxsize
         maxLat = 0
         minLong = sys.maxsize  
         maxLong = 0

        # calcul des min en long et lat
         for noeud in self.listeNoeud:
            long= noeud.longitude
            lat = noeud.latitude
            minLat = min(lat, minLat)
            minLong = min(long, minLong)
            maxLat = max(lat,maxLat)
            maxLong = max(long, maxLong)

        # calcule de l'absisse - distance a un point de coordonnees(min long , meme lat)
         for noeud in self.listeNoeud:
             long= noeud.longitude
             lat = noeud.latitude
             pointA = (long, lat)
             pointB=(minLong, lat)
             x = distanceLongLat(pointA, pointB)
             noeud.coordX = x

        # calcule de l'ordonnee - distance a un point de coordonnees (meme long , min lat)
         for noeud in self.listeNoeud:
             long= noeud.longitude
             lat = noeud.latitude
             pointA = (long, lat)
             pointB=(long, minLat)
             y = distanceLongLat(pointA, pointB)
             noeud.coordY = y

         # verification abscisse min max, ordonnee min max

         minX =  sys.maxsize
         minY = sys.maxsize
         maxX = 1
         maxY = 1

         for noeud in self.listeNoeud :
            x = noeud.coordX
            y = noeud.coordY
            minX= min(x, minX)
            minY = min(y, minY)
            maxX = max(x,maxX)
            maxY = max(y, maxY)

        # calcul des ratio
         global ratio 
         global winHeight
         ratio = (winWidth - 2*border) / (maxX )
         winHeight = int ( ratio *  (maxY)) + 2* border
         winHeight = min (winHeight, MaxHeight)
         ratio = min (ratio, (winHeight - 2*border) / (maxY))

         for noeud in self.listeNoeud :
            noeud.pixelX = int(noeud.coordX*ratio)+ border
            noeud.pixelY = winHeight - (int(noeud.coordY*ratio)+ border)

    # affichage graphique du noeud :
     def dessinGraphe(self, can, color) :
         for noeud in self.listeNoeud :
            noeud.dessinNoeudArc(self, can, color)
            
    # affichage graphique d'une liste d'arc :
     def dessinCheminArc(self, can, cheminArc, color):
         for arc in cheminArc :
             arc.dessinArc(self, can, color)

    # affichage graphique d'uneliste de noeud :
     def dessinCheminNoeud(self, can, cheminNoeud, color) :
         for indNoeud in cheminNoeud : 
             noeud= self.listeNoeud[indNoeud]
             noeud.dessinNoeud(self, can, color)

    # ---------------------------------------------------------------
    # Algorithme Dijkstra - V1
    #  algo avec une  gestion liste candidat : a chqaue fois qu'un noeud non atteint est atteint
    #       il est ajouté à la liste des sommets candidats
    #  pour trouver le prochain noeud on ne parcours que la liste des candidats
    #  le noeud exploré est retiré de la liste des candidats
    # ---------------------------------------------------------------
    # entrée : noeud source, noeud dest, graphe
    # sortie : (tableau des pred noeuds du chemin, liste des indices des noeuds explorés)
     def DijkstraV1(self, source, dest) :
         # Initialisation
        distance=[]
        explore=[]
        cheminTmp=[]
        listeCandidat=[]

        for noeud in self.listeNoeud:
            indNoeud = noeud.indice
            distance.append(sys.maxsize)
            cheminTmp.append(sys.maxsize)
        
        distance[source]=0
        cheminTmp[source]=source
        listeCandidat.append(source)
        explore.append(source)

        # Exploration
        while (listeCandidat != []): 
            min = sys.maxsize
            indiceMin = sys.maxsize
            for ind in listeCandidat:
                if (distance[ind]<min):
                    min = distance[ind]
                    indiceMin = ind
            xi = indiceMin
            #append xi à S
            explore.append(xi)
            #Retirer xi de Candidat
            listeCandidat.remove(xi)
            #Pour tout xj appartenant au candidat successeur de xi 	
            for arc in self.listeNoeud[xi].listeArcSucc:
                xj = arc.indDest
                #si dj = infini ajouter xj à Candidat
                if (distance[xj]==sys.maxsize):
                    listeCandidat.append(xj)
                #dj = min (dj, di+d(xi,xj))
                if (distance[xj]>distance[xi]+arc.longueur):
                    distance[xj]=distance[xi]+arc.longueur
                    cheminTmp[xj]=xi
            #chemin
            if (xi==dest):
                return (self.reconstruitChemin(cheminTmp, source, dest), explore)


     def DijkstraV2(self, source, dest) : #dijkstra utilisant le danger au lieu de la distance
         # Initialisation
            danger=[]
            explore=[]
            cheminTmp=[]
            listeCandidat=[]
            for noeud in self.listeNoeud:
                indNoeud = noeud.indice
                danger.append(sys.maxsize)
                cheminTmp.append(sys.maxsize)
            danger[source]=0
            cheminTmp[source]=source
            listeCandidat.append(source)
            explore.append(source)
            # Exploration
            while (listeCandidat != []): 
                min = sys.maxsize
                indiceMin = sys.maxsize
                for ind in listeCandidat:
                    if (danger[ind]<min):
                        min = danger[ind]
                        indiceMin = ind
                xi = indiceMin
                #append xi à S
                explore.append(xi)
                #Retirer xi de Candidat
                listeCandidat.remove(xi)
                #Pour tout xj appartenant au candidat successeur de xi 	
                for arc in self.listeNoeud[xi].listeArcSucc:
                    xj = arc.indDest
                    #si dj = infini ajouter xj à Candidat
                    if (danger[xj]==sys.maxsize):
                        listeCandidat.append(xj)
                    #dj = min (dj, di+d(xi,xj))
                    if (danger[xj]>danger[xi]+arc.danger):
                        danger[xj]=danger[xi]+arc.danger
                        cheminTmp[xj]=xi
                #chemin
                if (xi==dest):
                    return (self.reconstruitChemin(cheminTmp, source, dest), explore)
         
     

    # ---------------------------------------------------------------
    # Algorithme ASTAR
    #  algo avec une  gestion liste candidat : a chqaue fois qu'un noeud non atteint est atteint
    #       il est ajouté à la liste des sommets candidats
    #  pour trouver le prochain noeud on ne parcours que la liste des candidats
    #  le noeud exploré est retiré de la liste des candidats
    # on utilise la distance euclidienne entre deux noeud pour trouver le prochain noeud à explorer
    # ---------------------------------------------------------------
    # entrée : noeud source, noeud dest, graphe
    # sortie : (tableau des pred noeuds du chemin, liste des indices des noeuds explorés)
     def distanceEuclidienne(self, source, dest):
        noeudSource = self.listeNoeud[source]
        noeudDest = self.listeNoeud[dest]
        xSource = noeudSource.pixelX
        ySource = noeudSource.pixelY
        xDest = noeudDest.pixelX
        yDest = noeudDest.pixelY
        return math.sqrt((xDest-xSource)**2 + (yDest-ySource)**2)

     def AStar(self, source, dest) :
        # Initialisation
        distance=[]
        explore=[]
        cheminTmp=[]
        listeCandidat=[]

        for noeud in self.listeNoeud:
            indNoeud = noeud.indice
            distance.append(sys.maxsize)
            cheminTmp.append(sys.maxsize)
        
        distance[source]=0
        cheminTmp[source]=source
        listeCandidat.append(source)
        explore.append(source)

        # Exploration
        while (listeCandidat != []):
            #Choisir xi appartenant au candidat de (di + Deuclid(i, destination)) minimum 
            min = sys.maxsize
            indiceMin = sys.maxsize
            for ind in listeCandidat:
                if (distance[ind]+self.distanceEuclidienne(ind, dest)<min):
                    min = distance[ind]+self.distanceEuclidienne(ind, dest)
                    indiceMin = ind
            xi = indiceMin
            #append xi à S
            explore.append(xi)
            #Retirer xi de Candidat
            listeCandidat.remove(xi)
            #Pour tout xj appartenant au candidat successeur de xi 	
            for arc in self.listeNoeud[xi].listeArcSucc:
                xj = arc.indDest
                #si dj = infini ajouter xj à Candidat
                if (distance[xj]==sys.maxsize):
                    listeCandidat.append(xj)
                #dj = min (dj, di+d(xi,xj))
                if (distance[xj]>distance[xi]+self.distanceEuclidienne(xi, xj)):
                    distance[xj]=distance[xi]+self.distanceEuclidienne(xi, xj)
                    cheminTmp[xj]=xi
            #chemin
            if (xi==dest):
                return (self.reconstruitChemin(cheminTmp, source, dest), explore)

     #----------------------------------------------------------------   
     def reconstruitChemin(self, cheminTmp, source, dest):
        chemin =[]
        # reconstruit chemin
        chemin.append(dest)
        ind  = cheminTmp[dest]
        # on part de la destination, puis on cherche son pred, etc.
        while (ind != source):
            chemin.append(ind)
            ind = cheminTmp[ind]
        chemin.append(source)
        # renvoie le chemin
        return chemin

# --------------------------------------------------------------------------
#
# Fonction Globales : gestion de l'interface et différentes focntions de serrvice
#
# --------------------------------------------------------------------------

#   Calcul de la distance entre deux points : (Long, Lat)
#   entrée : point - coordonnée long et lat en radian
#   sortie : distance entre les deux points en metre
def distanceLongLat(pointA, pointB):
    longA = pointA[0]
    longB =pointB[0]
    latA = pointA[1]
    latB=pointB[1]
    deltaLong = longB - longA
    # distance angulaire en radian
    S_AB = math.acos(math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(deltaLong))
    # distance en metre= distance angulaire * rayon terre
    return (S_AB* 6378000)

# click droit : permet de marquer un noued source :
# le noeud le plus proche du click souris
def callback1(event,graphe):

    global Source

    if(Source != 0):
        (graphe.listeNoeud[Source]).dessinNoeudSmall(graphe, can)

    indNoeud = noeudPlusProche(event)

    noeudCible = graphe.listeNoeud[indNoeud]
    noeudCible.dessinNoeudHuge(graphe, can, "purple")
    Source = indNoeud
    return()

# click gauche : permet de marquer un noued destination : 
# le noeud le plus proche du click souris
def callback2(event,graphe):

    global Destination 

    min = sys.maxsize
    indice  = sys.maxsize

    if(Destination != 0):
        graphe.listeNoeud[Destination].dessinNoeudSmall(graphe, can)

    indNoeud = noeudPlusProche(event)

    noeudCible = graphe.listeNoeud[indNoeud]
    noeudCible.dessinNoeudHuge(graphe, can, "green")
    Destination = indNoeud
    return()
        

# permet de trouver le noeud le plus proche d'un click de soursi (event contient les coordonnées du click)        
def noeudPlusProche(event): 
    obj = can.find_closest(event.x, event.y)
    indObj = obj[0]
    return(MappageNoeud[indObj])

# recupere le noeud source et le noeud dest
# lance Dijkstra 
# dessine le chemin (rouge), et l'ensemble des noeuds explorés (jaune)
def applyDijkstra(graphe) :
    print("ok")

    global Source
    global Destination

    # calcul du chemin 
    result= graphe.DijkstraV1(Source, Destination)
    print("============ Calcul Chemin OK ================")
    chemin = result[0]    # chemin non formaté
    explore = result[1]    
    print('CHEMIN DISKSTRA', chemin)
    can.delete(ALL)
    graphe.dessinGraphe(can, "grey50")
    graphe.dessinCheminNoeud(can, explore, "yellow")
    graphe.dessinCheminNoeud(can, chemin, "red")
    noeudCible = graphe.listeNoeud[Destination]
    noeudCible.dessinNoeudHuge(graphe, can, "green")
    noeudCible = graphe.listeNoeud[Source]
    noeudCible.dessinNoeudHuge(graphe, can, "purple")


def applyDijkstraV2(graphe) : #trace le chemin deux fois, une fois pour le danger et une fois pour la distance
    print("ok")

    global Source
    global Destination

    # calcul du chemin
    result= graphe.DijkstraV2(Source, Destination)
    print("============ Calcul Chemin OK ================")
    chemin = result[0]    # chemin non formaté
    explore = result[1]
    print('CHEMIN DISKSTRA', chemin)
    can.delete(ALL)
    graphe.dessinGraphe(can, "grey50")
    graphe.dessinCheminNoeud(can, explore, "yellow")
    graphe.dessinCheminNoeud(can, chemin, "red")
    noeudCible = graphe.listeNoeud[Destination]
    noeudCible.dessinNoeudHuge(graphe, can, "green")
    noeudCible = graphe.listeNoeud[Source]
    noeudCible.dessinNoeudHuge(graphe, can, "purple")

    result1= graphe.DijkstraV1(Source, Destination)
    print("============ Calcul Chemin OK ================")
    chemin1 = result1[0]    # chemin non formaté
    print('CHEMIN DISKSTRA', chemin1)
    graphe.dessinCheminNoeud(can, chemin1, "blue")
    noeudCible = graphe.listeNoeud[Destination]
    noeudCible.dessinNoeudHuge(graphe, can, "green")
    noeudCible = graphe.listeNoeud[Source]
    noeudCible.dessinNoeudHuge(graphe, can, "purple")
    

# recupere le noeud source et le noeud dest
# lance A* 
# dessine le chemin (rouge), et l'ensemble des noeuds explorés (jaune)def applyAStar(graphe) :
def applyAStar(graphe) :
    print("ok")

    global Source
    global Destination

    # calcul du chemin 
    result= graphe.AStar(Source, Destination)
    print("============ Calcul Chemin OK ================")
    chemin = result[0]    # chemin non formaté
    explore = result[1]    
    print('CHEMIN ASTAR',chemin)
    can.delete(ALL)
    graphe.dessinGraphe(can, "grey50")
    graphe.dessinCheminNoeud(can, explore, "yellow")
    graphe.dessinCheminNoeud(can, chemin, "red")
    noeudCible = graphe.listeNoeud[Destination]
    noeudCible.dessinNoeudHuge(graphe, can, "green")
    noeudCible = graphe.listeNoeud[Source]
    noeudCible.dessinNoeudHuge(graphe, can, "purple")


# --------------------------------------------------------------------------------------------
#   PROGRAMME PRINCIPAL
# --------------------------------------------------------------------------------------------

# definition du graphe Paris
graphe = Graphe()
nomFichierNoeud ="./graphes/paris_noeuds.csv"
nomFichierArc ="./graphes/paris_arcs.csv"

# lecture noeud Paris
graphe.lectureNoeud(nomFichierNoeud)
graphe.lectureArc(nomFichierArc)
#graphe.affiche()

graphe.miseEchelle()

# ouverture de la fenetre pour affichage
fen = Tk()
can = Canvas(fen, width = winWidth, height = winHeight, bg ='white')
can.delete(ALL)
can.bind("<Button-1>", lambda event, g = graphe :callback1(event, g))
can.bind("<Button-3>", lambda event, g = graphe :callback2(event, g))
b = Button(fen , text = "Dijkstra", command = lambda   g= graphe :applyDijkstra(g))
c = Button(fen , text = "   A*   ", command = lambda   g= graphe :applyAStar(g))
d = Button(fen , text = "DijkstraV2", command = lambda   g= graphe :applyDijkstraV2(g))

 
# Placer le bouton sur la fenêtre
b.pack()
c.pack()
d.pack()

graphe.dessinGraphe(can, "grey50")

can.pack()
fen.mainloop()

#lectureArc(nomFichierArc, G)
