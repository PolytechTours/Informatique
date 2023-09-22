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