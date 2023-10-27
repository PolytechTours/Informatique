from machine import Pin, PWM, Timer
from ConfigMateriel_pico import*
from BME280 import *
from SCD41 import *
from adafruit_sgp40 import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font

# --------------- Liaison SPI ---------------
spi_tft = machine.SPI(0)
tft = ili9341.Display(spi_tft, dc = TFT_DC_pin, cs = SPI_CS_pin, rst = TFT_RESET_pin, rotation = 90)
tft.clear()


# --------------- Police de caractères ---------------
# Importer police de caractères
print('Loading fonts...')
print('Loading unispace')
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Loading unispaceExt')
unispaceExt = xglcd_font.XglcdFont('fonts/UnispaceExt12x24.c', 12, 24, letter_count=224)
print('Fonts loaded.')


# --------------- Fonctions ---------------

tft.draw_circle(50, 50, 10, const (0x8410))
tft.draw_circle(50, 50, 11, const (0x8410))
tft.draw_circle(50, 50, 12, const (0x8410))

tft.draw_text(160, 120, "Hello world", unispace, const (0x8425), background_flag = True, background=0,
landscape = False, spacing = 1)
Affiche_Graphique.Affiche_mesure()

# --------------- Boucle infinie ---------------
    