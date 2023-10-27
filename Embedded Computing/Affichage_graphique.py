# Module Affichage_Graphique.py
# Gestion des affichages graphique écran LCD

# fonts/UnispaceExt12x24
LARGEUR_CARACT = const (12)
HAUTEUR_CARACT = const (24)

from ILI9341 import *
import Colorimetrie

# Définition de couleur de base
BLANC = const (0xFFFF)
NOIR = const (0x0000)
ROUGE = const (0xF800)
VERT = const (0x07E0)
CYAN = const (0x07FF)
BLEU = const (0x001F)
LIGHTGREY =  const(0xAD75)
MEDIUMGREY = const (0x8410)
DARKGREY = const (0x4A49)

# Définition des niveaux de rétroéclairage en valeur de pwm sur 2 octets
BACKLITE_0 = const(65535) # Rétroéclairage Max
BACKLITE_1 = const(32768) # 2^15
BACKLITE_2 = const(16394) # 2^14
BACKLITE_3 = const(8192)  # 2^13
BACKLITE_4 = const(0) # Rétroéclairage éteint

COV_MIN = const(0)
CO2_MIN = const(400)
COV_MAX = const(500)
CO2_MAX = const(4000)

# Ecran 1
# Définition de constantes symboliques liées à la mise en forme de l'écran 1
Display1=Display(spi_tft, dc = TFT_DC_pin, cs = SPI_CS_pin, rst = TFT_RESET_pin, rotation = 90)
# A compléter selon besoins


# Ecran 2
# Définition de constantes symboliques liées à la mise en forme de l'écran 2
#   Tableau des valeurs min et max
#       A compléter selon besoins

#   Bouton Reset
#       A compléter selon besoins

#   Echelle de rétroéclairage
#       A compléter selon besoins

class TFT_affichage :

    def __init__ (self, tft = None) :

        """
        Args:
        TFT_affichage (Class ili9341) :  tft interface pour écran TFT
        """
        if tft is None:
            raise ValueError('An tft object is required.')
        self.tft = tft
#---------------------------------------------------------------------------------------------
# Afficher un bouton + légende centrée
    def bouton (self, x, y, w, h, couleur_fond, police, texte, couleur_texte) :
        self.tft.fill_hrect (x, y, w, h, couleur_fond)
        self.tft.draw_rectangle (x, y, w, h, BLANC)
        self.tft.draw_text (x + int ((w - len(texte) * LARGEUR_CARACT) // 2), y + (h - HAUTEUR_CARACT) // 2, texte, police, couleur_texte, False, background=couleur_fond,
                  landscape=False, spacing=2)
#---------------------------------------------------------------------------------------------
# Afficher le fond d'écran 1 d'affichage des valeurs de t, p, h, cov et co2
    def Fond_ecran_1 (self, police = None) :

        if police == None :
            raise ValueError ('Une police de caractères est requise')

        #Afficher les éléments de l'écran 1 : à compléter

        self.tft.draw_text(2, 10, "Temperature :", unispace, ili9341.color565(255, 255, 255),  background=0)
        self.tft.draw_text(2, 30, "Pression :", unispace, ili9341.color565(255, 255, 255),  background=0)
        self.tft.draw_text(2, 50, "Humidite :", unispace, ili9341.color565(255, 255, 255),  background=0)
        self.tft.draw_text(2, 70, "CO2 :", unispace, ili9341.color565(255, 255, 255),  background=0)
        self.tft.draw_text(2, 90, "COV_index :", unispace, ili9341.color565(255, 255, 255),  background=0)

#---------------------------------------------------------------------------------------------
# Pour afficher la valeur des mesures de t, p, h, cov ou co2 sur écran1

    def Affiche_mesure (self, x, y, mesure, mesure_prec, unite_mesure, format_str, couleur, police = None) :
        # x , y : début position affichage
        # mesure = temp ou pression ou h ou cov ou co2. Valeur scalaire réelle ou entière
        # mesure_prec = temp_prec ou pression_prec ou h_prec ou cov_prec ou co2_prec. Valeur scalaire réelle ou entière
        # unité de mesure : string "°C" ou "%" ou "" ou "ppm"
        # format_str : string
        #   "{:+5.1f}" : pour la température
        #   "{:7.2f}" : pour la pression atmosphérique
        #   "{:4.1f}" : pour l'humidité
        #   "{:4d}" : pour la concentration de co2
        #   "{:3d}" : pour l'index COV'

        if police == None :
            raise ValueError ('Une police de caractères est requise')

        # A compléter

#---------------------------------------------------------------------------------------------
# Afficher les valeurs des mesures de t_min, t_max, h_min, h_max, cov_min, cov_max, co2_min, co2_max
#   sur écran 2
# Les affichages sont centrés sur chaque cellule du tableau
    def Tableau_ecran_2 (self, mesures_min_max, Consigne_retroeclairage, police = None) :
        # mesures_min_max = (t_min, t_max, h_min, h_max, cov_min, cov_max, co2_min, co2_max)
        # Consigne_retroeclairage : indice du niveau de rétroéclairage dans {0, 1, 2, 3, 4, 5}
        if police == None :
            raise ValueError ('Une police de caractères est requise')
        if Consigne_retroeclairage < 0 or Consigne_retroeclairage > 5 :
            raise ValueError ('Consigne_retroeclairage doit être dans {0, 1, 2, 3, 4, 5}')

        # Légendes des cellules
        #   Affichage 'Min' et 'Max' : centré sur la cellule
        # A compléter

        #   Affichage 'T', 'H', 'COV', 'CO2' : centré sur la cellule
        # A compléter

        # Affichage des mesures min et max de T, H, COV, CO2
        # A compléter

        # Affichage bouton RESET
#       A compléter

        # Affichage Echelle niveaux rétroéclairage
        # A compléter

#---------------------------------------------------------------------------------------------
    def Spectre_couleurs (self, x, y, w, h, longueur_onde_deb, longueur_onde_fin, longueur_onde_pas) :
        # x : coordonnées écran début de la zone d'affichage du spectre des couleurs (pixels)
        # y : coordonnées écran début de la zone d'affichage du spectre des couleurs (pixels)
        # w : largeur de la zone d'affichage du spectre des couleurs (pixels)
        # h : hauteur de la zone d'affichage du spectre des couleurs (pixels)
        # longueur_onde_deb : longueur d'onde de la première couleur (nm)
        # longueur_onde_fin : longueur d'onde de la dernière couleur (nm)
        # longueur_onde_pas : incrément de longueur d'onde entre 2 couleurs (nm)

        # Table des composantes chromatiques CIE 1964: lambda_min = 380nm, lambda_max = 780nm, pas = 5nm
        pass
        # A compléter

#---------------------------------------------------------------------------------------------
    def Echelle_choix_RetroEclairage(self, x, y, w_cellule, h_cellule, choix_retroeclairage) :
        # x : coordonnées écran début de la zone d'affichage du choix du niveau de rétroéclairage (pixels)
        # y : coordonnées écran début de la zone d'affichage du choix du niveau de rétroéclairage (pixels)
        # w : largeur de la zone d'affichage du choix du niveau de rétroéclairage (pixels)
        # h : hauteur de la zone d'affichage du choix du niveau de rétroéclairage (pixels)
        # choix_retroeclairage : indice du niveau de rétroéclairage dans {0, 1, 2, 3, 4, 5}
        pass
        # A compléter
