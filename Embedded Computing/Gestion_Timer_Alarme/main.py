# Programme d'exemple de gestion temporelle d'événements
# Ce programme illustre l'utilisation des timers, associée à la notion d'alarme
# Notions complémentaires :
#   - Interuption timer;
#   - Routine d'interruption
#   - Gestion de flags
# Evénement 1 : périodicité de prise en compte : 1s
# Evénement 2 : périodicité de prise en compte : 5s

# Cible Raspberry Pi pico
# Micropython V1.18

from machine import Timer
from micropython import const

Evenement1_flag = False
Evenement2_flag = False

_1s = const(1000) # Correspond à 1000 ms, soit 1s
_5s = const(5000) # Correspond à 5000 ms, soit 5s

# Fonction callbak
def Evenement1_callback (self):
    global Evenement1_flag
    Evenement1_flag = True
def Evenement2_callback (self):
    global Evenement2_flag
    Evenement2_flag = True

# Init des timers
Evenement1_timer = Timer()
Evenement2_timer = Timer()
Evenement1_timer.init(period = _1s, mode = Timer.PERIODIC, callback = Evenement1_callback)
Evenement2_timer.init(period = _5s, mode = Timer.PERIODIC,  callback = Evenement2_callback)

Index_evenement_1 = 1
Index_evenement_2 = 1

while True :
    # Gestion de l'événement 1
    if Evenement1_flag == True :
        # Traitement de l'événement 1
        print ('------------------------')
        print ("  Index_evenement_1 : ", Index_evenement_1)
        print ("  Evenement 1 en cours de traitement")
        Evenement1_flag = False
        Index_evenement_1 += 1

    # Gestion de l'événement 2
    if Evenement2_flag == True :
        # Traitement de l'événement 2
        print ('------------------------')
        print ("  Index_evenement_2 : ", Index_evenement_2)
        print ("  Evenement 2 en cours de traitement")
        Evenement2_flag = False
        Index_evenement_2 += 1
