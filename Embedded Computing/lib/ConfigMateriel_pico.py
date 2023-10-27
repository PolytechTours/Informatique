# Ressources GPIO du microcontrôleur Raspberry Pi pico

from machine import Pin

Led_Pin_25 = 25 # Variable Led_Pin_25 pour adresser la broche GP25 du µC RP2040

# Ressources pour communication I2C
#   - SCL : GP9 soit broche 12 PCB
#   - SDA : GP8 soit broche 11 PCB
#   - Fréquence : 400KHz
# Correspond à I2C0
SDA_pin = Pin(8)
SCL_pin = Pin(9)
Freq_i2c = 400000

# Ressources pour gestion écran TFT : SPI0
# GPIO par défaut : bus SPI
#   SPI_SCK_pin = 6 # GP6 soit broche 9 du PCB; CLK
#   SPI_TX_pin = 7 # GP7 soit broche 10 du PCB; MOSI
#   SPI_RX_pin = 4 # GP4 soit broche 6 du PCB; MISO

# Spécifique à l'écran TFT Touchscreen DFR0665
SPI_CS_pin = Pin(5) # GP5 soit broche 7 du PCB;
TFT_DC_pin = Pin(2) # GP2 soit broche 4 du PCB. Permet de gérer envoi data ou commande vers écran TFT
TFT_RESET_pin = Pin(13) # GP13 soit broche 17 du PCB
TFT_Backlite_pin = Pin(3) # GP3 soit broche 5 du PCB

# Dalle tactile écran TFT DFR0665
Touch_Screen_CS_pin = Pin(14) # GP14 soit broche 19 du PCB
Touch_Interrupt_pin = Pin(15) # GP15 soit broche 20 du PCB

# Utilisation des boutons poussoir
BP_RESET_min_max_pin = Pin(21, Pin.IN)      # SW1 sur le PCB
BP_ECRAN2_pin = Pin(20, Pin.IN)             # SW2 sur le PCB
BP_BACKLITE_GAUCHE_pin = Pin(19, Pin.IN)    # SW3 sur le PCB
BP_BACKLITE_VALIDE_pin = Pin(18, Pin.IN)    # SW4 sur le PCB
BP_BACKLITE_DROITE_pin = Pin(17, Pin.IN)    # SW5 sur le PCB
