#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import cv2
import os
import numpy as np
import random
from random import shuffle
#import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split


DATA_PATH = "data/driving_log.csv"
DATA_IMG = "data/"
DIM_VEC_Image=67200#160*320*3

#
#La fonction à compléter par les étudiants
def DescenteGradient (X,Y,W,pas) :
    

    if np.random.random()>0.90:
        print('Erreur : ',erreur)
 
      
    return W,erreur


#Ne pas toucher normalement
def getBatch(log_content, index_list, batch_size,strict=True):
    images = np.zeros((batch_size,DIM_VEC_Image+1))
    #images = np.zeros((batch_size,160*320))
    rotations = np.zeros((batch_size,1))
    count=0
    while True:
        
        if not strict:
            shuffle(index_list)
        for index in index_list:
            # Futur angle correction
            angle_correction = [0., 0.25, -.25]
            # Randomly select one of of three images
            i = random.choice([0, 1, 2]) # [Center, Left, Right]
            img = cv2.imread(os.path.join(DATA_IMG, log_content[index][i]).replace(" ", ""))
            if img is None: continue
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            
            
            
            #on croppe l'image pour garder que ce qui interessant
            img=img[65:160-25,0:320-0]
            
            
            # Get the rotation
            rotation = float(log_content[index][3])

            #if not strict and random.random() > np.sqrt(rotation ** 2) + 0.1:
            #    continue

            # Apply correction
            rotation = rotation + angle_correction[i]
            # 1/2: random roation of the image
            if random.random() > 0.5:
                img = cv2.flip(img, 1)
                rotation = rotation * -1
            # Append the new image/rotation to the current batch
            img=(img/127.5)-1
            images[count,0]=1
            images[count,1:(DIM_VEC_Image+1)]=img.reshape(DIM_VEC_Image)
            rotations[count]=rotation
            count=count+1
            # Yield the new batch
            if count >= batch_size:
                #yield np.array(images), np.array(rotations)
                # Next batch
                #images, rotations = [], []
                return images, rotations


def main():
    """
        Main function to train the model
    """
    # Open log csv
    with open(DATA_PATH, "r") as f:
        content = [line for line in csv.reader(f)]
    # Split in train/validation set
    #On divise la base de données en une base d'apprentissage et une base de validation
    random_indexs = np.array(range(len(content)))
	#test_size=0.15 : 15 pour cent de la base sert pour la validation
    #test_size peut être diminué mais ça va rendre l'apprentissage plus long 
	train_index, valid_index = train_test_split(random_indexs, test_size=0.15)

    print("Train size = %s" % len(train_index))
	#si le temps le permet ou si les étudiants sont demandeurs
	#expliquer la notion de base de validation (et overfitting)
	#si pas le temps alors ce n'est grave pour faire le TP
    print("Valid size = %s" % len(valid_index))

    BATCH_SIZE = 64

    images, rotations = getBatch(content, train_index, BATCH_SIZE,True)
    
    print(images.shape)
    print(images[0].shape)
    
    
    nbdim = images.shape[1] 
    
    pas=0.00001
    nbiter=15
    print('Pas :',pas)
    print('Nombre itération : ',nbiter)
    W=np.zeros((nbdim,1))
	
	#####################################
	#Ici faire le code qui calcule les W
	# 2 : Récupérer un lot de données par la méthode get Batch
	# 3 : Trouver W (descente de gradient) pour un lot
	# 4 : Aller à l'étape 2 tant qu'on a pas traité toutes les données
	# 5 : Recommencer tant que le nombre d'itération n'est pas atteint
	####################################
    
	# to do
	
	
	
	
	# Après
	## Sauvegarde des W dans un fichier texte
	## Ne pas changer le nom de fichier
    np.savetxt("modelW.txt",W)
 

if __name__ == '__main__':
    main()
