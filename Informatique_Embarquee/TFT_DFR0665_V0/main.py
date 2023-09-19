# Utilisation écran TFT DFRobot DFR0665
# Communication SPI

# Cible : Raspberry Pi pico

# Validé le 15.03.2022

from ConfigMateriel_pico import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font

# Init liaison spi
spi_tft = machine.SPI(0)
# Init ressource gestion écran
tft = ili9341.Display(spi_tft, dc = TFT_DC_pin, cs = SPI_CS_pin, rst = TFT_RESET_pin, rotation = 90)
tft.clear()

# Importer police de caractères
print('Loading fonts...')
print('Loading unispace')
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Loading unispaceExt')
unispaceExt = xglcd_font.XglcdFont('fonts/UnispaceExt12x24.c', 12, 24, letter_count=224)
print('Fonts loaded.')

# Fonction graphiques
# Cercles
tft.draw_circle(50, 192, 25, ili9341.color565(255, 0, 0))
tft.draw_circle(100, 128, 25, ili9341.color565(255, 128, 0))
tft.draw_circle(150, 192, 25, ili9341.color565(255, 255, 255))
# Octogone
tft.draw_polygon(8, 180, 120, 30, ili9341.color565(0, 255, 0), rotate=0)
tft.fill_polygon(8, 180, 120, 30, ili9341.color565(0, 255, 0), rotate=0)

# Texte
tft.draw_text(2, 10, "Hello unispace", unispace, ili9341.color565(255, 255, 255),  background=0,
                  landscape=False, spacing=10)

tft.draw_text(40, 40, 'Hello |{[Unispace Ext]}|', unispaceExt, ili9341.color565(255, 0, 0),
                      background=ili9341.color565(0, 128, 0), spacing = 1)

