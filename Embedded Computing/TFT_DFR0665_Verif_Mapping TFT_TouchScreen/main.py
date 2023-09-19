# Utilisation écran TFT DFRobot DFR0665
# Communication SPI
# Test écran TFT et Test dalle tactile
# Vérification de la calibration

# Cible : Raspberry Pi pico

# Validé le 16.03.2022
#   Pour rotation = 0
#   Pour rotation = 90
#   Pour rotation = 180
#   Pour rotation = 270

# Validé le 21.03.2022

# Source : http://electroniqueamateur.blogspot.com/2021/06/utilisation-dun-ecran-tactile-tft-spi.html

from ConfigMateriel_pico import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font
from xpt2046 import *

#-------------------------------------------------------------------------------
def routine_touch(x, y):
    '''
    Routine d'interruption appelée lors d'un appui sur la dalle tactile
    Args : (x,y)
        Coordonnées écran TFT retournée après mapping avec
        les coordonnées du point d'appui sur la dalle tactile
    '''

    tft.fill_circle(x, y, 2, ili9341.color565(255, 255, 255))

#-------------------------------------------------------------------------------

# Init liaison spi
spi_tft = machine.SPI(0)
# Init ressource gestion écran TFT
tft = ili9341.Display(spi_tft, dc=TFT_DC_pin, cs=SPI_CS_pin, rst=TFT_RESET_pin, rotation = 0)

# Init des ressources pour gestion de la dalle tactile
'''
def __init__(self, spi, cs, int_pin=None, int_handler=None,
             width=240, height=320, rotation = 0,
             x_min=100, x_max=1962, y_min=100, y_max=1900):
        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            int_pin (Class Pin):  Touch controller interrupt pin
            int_handler (function): Handler for screen interrupt
            width (int): Width of LCD screen
            height (int): Height of LCD screen
            rotation (Optional int): Rotation must be 0 default, 90, 180 or 270
            x_min (int): Minimum x coordinate
            x_max (int): Maximum x coordinate
            y_min (int): Minimum Y coordinate
            y_max (int): Maximum Y coordinate

            Valeur de rotation :
                Doit être identique avec celle utilisée pour
                    initialiser l'écran TFT

            Valeurs de x_min, x_max, y_min, y_max :
                Dépendent de la calibration de la dalle tactile
                Doivent être instanciées selon résultat de la calibration

'''
Touchscreen = Touch (spi_tft, Touch_Screen_CS_pin, Touch_Interrupt_pin, int_handler = routine_touch,
                     width = 240, height = 320, rotation = 0,
                     x_min = 157, x_max = 1841, y_min = 200, y_max = 1947)

#-------------------------------------------------------------------------------


# Importer police de caractères
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)

tft.draw_text( 2, 10, "Hello", unispace, ili9341.color565(255, 255, 255),  background=0,
                  landscape=False, spacing=5)
time.sleep (2)
tft.clear()
tft.draw_text(30, 150, "Touchez l'ecran", unispace,
                  ili9341.color565(255, 255, 255))


while True :
    pass
