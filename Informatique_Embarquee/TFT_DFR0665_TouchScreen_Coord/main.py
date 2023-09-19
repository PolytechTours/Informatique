# Utilisation écran TFT DFRobot DFR0665
# Communication SPI
# Test écran TFT et calibration de la dalle tactile
# Vérif des données dalle tactile telles que :
#   Mode portrait => rotation = 0
# Xe = 0 => Tx_min
# Xe = width = 240 => Tx_max
# Ye = 0 => Ty_min
# Ye = height = 320 => Ty_max

# Cible : Raspberry Pi pico
# Source : http://electroniqueamateur.blogspot.com/2021/06/utilisation-dun-ecran-tactile-tft-spi.html

# Validé le 16.03.2022

from ConfigMateriel_pico import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font
from xpt2046 import *

minX = maxX = minY = maxY = 500

#-------------------------------------------------------------------------------
def routine_touch(x, y):

    global minX, maxX, minY, maxY
    global etape

    if (etape < 6):

        # obtention des valeurs brutes
        rawX = Touchscreen.send_command(Touchscreen.GET_X)
        rawY = Touchscreen.send_command(Touchscreen.GET_Y)

        if rawX != 0:
            if rawX > maxX:
                maxX = rawX
            elif rawX < minX:
                minX = rawX
        if rawY != 0:
            if rawY > maxY:
                maxY = rawY
            elif rawY < minY:
                minY = rawY

        if etape < 5:
            print("Etape " + str(etape) + " : " + str(rawX) + "," + str(rawY))

        etape = etape + 1

        #effacage de toutes les fleches
        tft.fill_rectangle(0, 0, 41, 41, ili9341.color565(0, 0, 0))
        tft.fill_rectangle(199, 0, 41, 41, ili9341.color565(0, 0, 0))
        tft.fill_rectangle(0, 279, 41, 41, ili9341.color565(0, 0, 0))
        tft.fill_rectangle(199, 279, 41, 41, ili9341.color565(0, 0, 0))

        if etape < 5:
            dessine_fleche(etape)

        if etape == 5:
            print("x_min: " + str(minX) + " , " + "x_max: " + str(maxX) + " , " +
                  "y_min: " + str(minY) + " , " + "y_max: " + str(maxY))
            tft.fill_rectangle(0, 0, 240, 320, ili9341.color565(0, 0, 0))
            tft.draw_text(20, 100, "x_min: " + str(minX), unispace,
                  ili9341.color565(255, 255, 255))
            tft.draw_text(20, 130, "x_max: " + str(maxX), unispace,
                  ili9341.color565(255, 255, 255))
            tft.draw_text(20, 160, "y_min: " + str(minY), unispace,
                  ili9341.color565(255, 255, 255))
            tft.draw_text(20, 190, "y_max: " + str(maxY), unispace,
                  ili9341.color565(255, 255, 255))

#-------------------------------------------------------------------------------

# Init liaison spi
spi_tft = machine.SPI(0)
# Init ressource gestion écran : par défaut rotation = 0, width = 240 et height = 320
tft = ili9341.Display(spi_tft, dc=TFT_DC_pin, cs=SPI_CS_pin, rst=TFT_RESET_pin)

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
'''
Touchscreen = Touch (spi_tft, Touch_Screen_CS_pin, Touch_Interrupt_pin, int_handler = routine_touch)

#-------------------------------------------------------------------------------
def dessine_fleche(etape):
    if (etape == 1): # coin supérieur gauche
        tft.draw_line(0, 0, 40, 40, ili9341.color565(255, 255, 255))
        tft.draw_line(0, 0, 0, 20, ili9341.color565(255, 255, 255))
        tft.draw_line(0, 0, 20, 0, ili9341.color565(255, 255, 255))

    if (etape == 2): # coin supérieur droit
        tft.draw_line(239, 0, 199, 40, ili9341.color565(255, 255, 255))
        tft.draw_line(239, 0, 239, 20, ili9341.color565(255, 255, 255))
        tft.draw_line(239, 0, 219, 0, ili9341.color565(255, 255, 255))

    if (etape == 3): # coin inférieur gauche
        tft.draw_line(0, 319, 40, 279, ili9341.color565(255, 255, 255))
        tft.draw_line(0, 319, 0, 299, ili9341.color565(255, 255, 255))
        tft.draw_line(0, 319, 20, 319, ili9341.color565(255, 255, 255))

    if (etape == 4): # coin inférieur droit
        tft.draw_line(239, 319, 199, 279, ili9341.color565(255, 255, 255))
        tft.draw_line(239, 319, 239, 299, ili9341.color565(255, 255, 255))
        tft.draw_line(239, 319, 219, 319, ili9341.color565(255, 255, 255))
#-------------------------------------------------------------------------------

# Importer police de caractères
print('Loading fonts Unispace12x24 ...')
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Fonts loaded.')


tft.draw_text( 2, 10, "Hello", unispace, ili9341.color565(255, 255, 255),  background=0,
                  landscape=False, spacing=10)
time.sleep (3)
tft.clear()


# instructions à l'écran
tft.draw_text(30, 130, 'Touchez le bout', unispace,
                  ili9341.color565(255, 255, 255))
tft.draw_text(50, 160, 'de la fleche', unispace,
                  ili9341.color565(255, 255, 255))

etape = 1
dessine_fleche(etape)

while True :
    pass
