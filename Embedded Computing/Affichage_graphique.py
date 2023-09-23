def fond_ecran1():
    tft.drawtext(2, 10, "Temperature :", unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(2, 30, "Pression :", unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(2, 50, "Humidite :", unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(2, 70, "CO2 :", unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(2, 90, "COV_index :", unispace, ili9341.color565(255, 255, 255),  background=0,)


# Pour afficher la valeur des mesures de t, p, h, cov ou co2 sur écran1
def Affiche_mesure (self, x, y, mesure, mesure_prec, unite mesure, format str, couleur, police=None):
    #x, y : début position affichage
    # mesure = temp ou pression ou h ou cov ou co2. Valeur scalaire réelle ou entière 
    # mesure_prec = temp_prec ou pression prec ou n_prec ou cov_prec ou co2_prec. Valeur scalaire réelle ou entière
    # unité de mesure : string "°C" ou "%" ou "" ou "ppm"
    # format str: string
    # "{:+5.1f}" ; pour la température
    # "{:7.2f}" : pour la pression atmosphérique
    # "{:4.1f}": pour l'humidité
    # "{:4d}" : pour La concentration de co2
    # "{:3d}" : pour L'index cov
    if police == None :
        raise ValueError ('Une police de caractères est requise')


from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 
import board
import ili9341
import xpt2046

#Compléter le code du module Affichage_Graphique.py avec l’écriture des fonctions :
#- Tableau_ecran_2 : pour afficher le tableau des valeurs min et max de température, humidité, Index Cov et taux de CO2, ainsi que l’échelle du rétroéclairage avec le niveau courant, et un bouton Reset pour provoquer ultérieurement la mise à jour des valeurs du tableau ;
#- Bouton : pour afficher un bouton avec une légende et une couleur de fond ;
#- Echelle_choix_RetroEclairage : pour afficher sur l’écran TFT l’échelle des niveaux de luminosité du rétroéclairage et visualiser le niveau courant.



def tableau_ecran_2(temp, hum, cov, co2):
    min_temp = min(temp, min_temp)
    max_temp = max(temp, max_temp)
    min_hum = min(hum, min_hum)
    max_hum = max(hum, max_hum)
    min_cov = min(cov, min_cov)
    max_cov = max(cov, max_cov)
    min_co2 = min(co2, min_co2)
    max_co2 = max(co2, max_co2)
    #dessine un tableau de 3 colonnes et 5 lignes
    ImageDraw.rectangle((0, 0, 30, 100), fill=0, outline=255)
    ImageDraw.rectangle((30, 0, 60, 100), fill=0, outline=255)
    ImageDraw.rectangle((60, 0, 90, 100), fill=0, outline=255)

    ImageDraw.rectangle((0, 0, 90, 20), fill=0, outline=255)
    ImageDraw.rectangle((0, 20, 90, 40), fill=0, outline=255)
    ImageDraw.rectangle((0, 40, 90, 60), fill=0, outline=255)
    ImageDraw.rectangle((0, 60, 90, 80), fill=0, outline=255)
    ImageDraw.rectangle((0, 80, 90, 100), fill=0, outline=255)

    ImageDraw.text((2, 22), "Temp", font=unispace, fill=255)
    ImageDraw.text((2, 42), "Hum", font=unispace, fill=255)
    ImageDraw.text((2, 62), "COV", font=unispace, fill=255)
    ImageDraw.text((2, 82), "CO2", font=unispace, fill=255)

    ImageDraw.text((32, 2), "Min", font=unispace, fill=255)
    ImageDraw.text((62, 2), "Max", font=unispace, fill=255)

    ImageDraw.text((32, 22), "{:+5.1f} °C".format(min_temp), font=unispace, fill=255)
    ImageDraw.text((62, 22), "{:+5.1f} °C".format(max_temp), font=unispace, fill=255)
    ImageDraw.text((32, 42), "{:4.1f} %".format(min_hum), font=unispace, fill=255)
    ImageDraw.text((62, 42), "{:4.1f} %".format(max_hum), font=unispace, fill=255)
    ImageDraw.text((32, 62), "{:3d}".format(min_cov), font=unispace, fill=255)
    ImageDraw.text((62, 62), "{:3d}".format(max_cov), font=unispace, fill=255)
    ImageDraw.text((32, 82), "{:4d} ppm".format(min_co2), font=unispace, fill=255)
    ImageDraw.text((62, 82), "{:4d} ppm".format(max_co2), font=unispace, fill=255)


def Bouton():
    ImageDraw.rectangle((0, 102, 30, 124), fill=(255,0,0), outline=255)
    ImageDraw.text((2, 102), "Reset", font=unispace, fill=255)
    ts = xpt2046.get_touch()
    while True:
        p = ts.touch_point
        if p:
            x, y = p
            if 0 <= x < 30 and 102 <= y < 124:
                min_temp = temp
                max_temp = temp
                min_hum = hum
                max_hum = hum
                min_cov = cov
                max_cov = cov
                min_co2 = co2
                max_co2 = co2
            else:
                pass

def Echelle_choix_Retroeclairage():
    ImageDraw.rectangle((60, 102, 80, 124), fill=255, outline=255)
    ImageDraw.rectangle((80, 102, 100, 124), fill=200, outline=255)
    ImageDraw.rectangle((100, 102, 120, 124), fill=150, outline=255)
    ImageDraw.rectangle((120, 102, 140, 124), fill=100, outline=255)
    ImageDraw.rectangle((140, 102, 160, 124), fill=50, outline=255)

    # Turn on the Backlight
    backlight = adafruit_rgb_display.DigitalInOut(board.D26)
    backlight.switch_to_output()
    backlight.value = True

    ts = xpt2046.get_touch()

    while True:
        p = ts.touch_point
        if p:
            x, y = p
            if 60 <= x < 80 and 102 <= y < 124:
                tft.brightness = 0.5
                ImageDraw.circle((70, 113), 5, fill=(255,0,0), outline=255)
                ImageDraw.circle((90, 113), 5, fill=200, outline=255)
                ImageDraw.circle((110, 113), 5, fill=150, outline=255)
                ImageDraw.circle((130, 113), 5, fill=100, outline=255)
                ImageDraw.circle((150, 113), 5, fill=50, outline=255)
                backlight.value = 
            elif 80 <= x < 100 and 102 <= y < 124:
                tft.brightness = 0.4
                ImageDraw.circle((90, 113), 5, fill=(255,0,0), outline=255)
                ImageDraw.circle((70, 113), 5, fill=255, outline=255)
                ImageDraw.circle((110, 113), 5, fill=150, outline=255)
                ImageDraw.circle((130, 113), 5, fill=100, outline=255)
                ImageDraw.circle((150, 113), 5, fill=50, outline=255)
            elif 100 <= x < 120 and 102 <= y < 124:
                tft.brightness = 0.3
                ImageDraw.circle((110, 113), 5, fill=(255,0,0), outline=255)
                ImageDraw.circle((70, 113), 5, fill=255, outline=255)
                ImageDraw.circle((90, 113), 5, fill=200, outline=255)
                ImageDraw.circle((130, 113), 5, fill=100, outline=255)
                ImageDraw.circle((150, 113), 5, fill=50, outline=255)
            elif 120 <= x < 140 and 102 <= y < 124:
                tft.brightness = 0.2
                ImageDraw.circle((130, 113), 5, fill=(255,0,0), outline=255)
                ImageDraw.circle((70, 113), 5, fill=255, outline=255)
                ImageDraw.circle((90, 113), 5, fill=200, outline=255)
                ImageDraw.circle((110, 113), 5, fill=150, outline=255)
                ImageDraw.circle((150, 113), 5, fill=50, outline=255)
            elif 140 <= x < 160 and 102 <= y < 124:
                tft.brightness = 0.1
                ImageDraw.circle((150, 113), 5, fill=(255,0,0), outline=255)
                ImageDraw.circle((70, 113), 5, fill=255, outline=255)
                ImageDraw.circle((90, 113), 5, fill=200, outline=255)
                ImageDraw.circle((110, 113), 5, fill=150, outline=255)
                ImageDraw.circle((130, 113), 5, fill=100, outline=255)
            else:
                pass
