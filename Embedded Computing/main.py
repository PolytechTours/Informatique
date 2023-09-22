from machine import Pin, I2C
import time
from ConfigMateriel_pico import *
from micropython import const
from BM280 import *
from SCD41 import *
from adafruit_sgp40 import *

#Synthese 1 : 
#Led_25 = Pin (Led_Pin_25, Pin.OUT)
#Led_25.value(0)
#time.sleep(0.25)
#while True : 
#    for i in range (0, 65535, 1):
#        Led_25.value(i)
#        time.sleep(0.0001)
#    for i in range (65535, 0, -1):
#        Led_25.value(i)
#        time.sleep(0.0001)



#Synthese 2 :
#i2c = I2C(0, sda = SDA_pin, scl = SCL_pin, freq= Freq_i2c)
#adr = i2c.scan ()
#print ('Adresse peripherique I2C :', adr)
#
#Id_BME280 = i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
#print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
#capteur_BME280 = BME280 (BME280_I2C_ADR, i2c)
#capteur_BME280.Calibration_Param_Load()
#while True:
#    print ('Temperature : ', BM280.read_temp())
#    print ('Pression : ', BM280.read_pressure())
#    print ('Humidite : ', BM280.read_humidity())
#    time.sleep(1)



#Synthese 3 :
#capteur_SCD41 = SCD4X (i2c, SCD4X_DEFAULT_ADDR)
#capteur_SCD41.stop_periodic_measurement()
#print("Serial number :", [hex(i) for i in capteur_SCD41.serial_number])
#capteur_SCD41.set_ambient_pressure(int(pression_BME280))
#capteur_SCD41.start_periodic_measurement()
#time.sleep(5)
#if capteur_SCD41.data_ready: # attendre qu'une mesure soit disponible
#    co2 = capteur_SCD41.CO2
#    temperature_SCD41 = capteur_SCD41.temperature
#    humidity_SCD41 = capteur_SCD41.relative_humidity
#    # Affichage des mesures SCD41
#    print("CO2 : %d ppm" % co2)
#    print("Temperature : %.2f °C" % temperature_SCD41)
#    print("Humidite : %.2f %%" % humidity_SCD41)
#time.sleep(5000)



#Synthese 4 :
#i2c=I2C(0, sda=SDA_pin, scl=SCL_pin, freq=Freq_i2c)
#adr=i2c.scan()
#print('Adresse peripherique I2C :', adr)
#
#Id_BME280 = i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
#print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
#capteur_BME280 = BME280 (BME280_I2C_ADR, i2c)
#capteur_BME280.Calibration_Param_Load()
#
#capteur_SCD41 = SCD4X (i2c, SCD4X_DEFAULT_ADDR)
#capteur_SCD41.stop_periodic_measurement()
#print("Serial number :", [hex(i) for i in capteur_SCD41.serial_number])
#capteur_SCD41.set_ambient_pressure(int(pression_BME280))
#capteur_SCD41.start_periodic_measurement()
#
#def callback_SCD41 (timer):
#    if capteur_SCD41.data_ready: # attendre qu'une mesure soit disponible
#        co2 = capteur_SCD41.CO2
#        temperature_SCD41 = capteur_SCD41.temperature
#        humidity_SCD41 = capteur_SCD41.relative_humidity
#        # Affichage des mesures SCD41
#        print("CO2 : %d ppm" % co2)
#        print("Temperature : %.2f °C" % temperature_SCD41)
#        print("Humidite : %.2f %%" % humidity_SCD41)
#    else:
#        print("No data available")
#
#def callback_BME280 (timer):
#    print ('Temperature : ', BM280.read_temp())
#    print ('Pression : ', BM280.read_pressure())
#    print ('Humidite : ', BM280.read_humidity())
#
#timer_SCD41 = Timer(0)
#timer_SCD41.init(period=5000, mode=Timer.PERIODIC, callback=callback_SCD41)
#timer_BME280 = Timer(1)
#timer_BME280.init(period=1000, mode=Timer.PERIODIC, callback=callback_BME280)



#Synthese 5 :
#sgp40_capteur_cov = SGP40 (i2c)
#print("SGP40 Serial number :", [hex(i) for i in sgp40_capteur_cov._serial_number])
#voc_index = sgp40_capteur_cov.measure_index(temperature, relative_humidity)
#while True:
#    print("VOC index : %d" % voc_index)
#    time.sleep(1)



#Synthese 6 :
#- De récupérer les adresses I2C des périphérique I2C actifs et de les afficher sur la console ;
#- De lire les Id des capteurs BME280, SCD41 et SGP40, et d’afficher leur valeur sur la console ;
#- D’afficher sur la console (ou le terminal série) les mesures de température, pression et taux d’humidité du BME280, avec une périodicité d’acquisition de 1s.
#- D’afficher sur la console (ou le terminal série) les mesures de taux de CO2 du capteur SCD41, avec une périodicité d’acquisition de 5s.
#- D’afficher sur la console (ou le terminal série) la valeur des mesures de l’index COV, avec une périodicité de 1s.
#- La totalité des périodicités d’acquisition de chaque capteur sera géré en utilisant les timers ;
#- La compensation de la mesure du taux de CO2 par la pression atmosphérique sera aussi gérée par timer ;
#- La mesure de l’index COV sera systématiquement compensée par la dernière mesure de la température et du taux d’humidité du capteur BME280.

#i2c=I2C(0, sda=SDA_pin, scl=SCL_pin, freq=Freq_i2c)
#adr=i2c.scan()
#print('Adresse peripherique I2C :', adr)
#
#Id_BME280 = i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
#print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
#capteur_BME280 = BME280 (BME280_I2C_ADR, i2c)
#capteur_BME280.Calibration_Param_Load()
#
#capteur_SCD41 = SCD4X (i2c, SCD4X_DEFAULT_ADDR)
#capteur_SCD41.stop_periodic_measurement()
#print("Serial number :", [hex(i) for i in capteur_SCD41.serial_number])
#capteur_SCD41.set_ambient_pressure(int(pression_BME280))
#capteur_SCD41.start_periodic_measurement()
#
#sgp40_capteur_cov = SGP40 (i2c)
#print("SGP40 Serial number :", [hex(i) for i in sgp40_capteur_cov._serial_number])
#voc_index = sgp40_capteur_cov.measure_index(temperature, relative_humidity)
#
#def callback_SCD41 (timer):
#    if capteur_SCD41.data_ready: # attendre qu'une mesure soit disponible
#        co2 = capteur_SCD41.CO2
#        temperature_SCD41 = capteur_SCD41.temperature
#        humidity_SCD41 = capteur_SCD41.relative_humidity
#        # Affichage des mesures SCD41
#        print("CO2 : %d ppm" % co2)
#        print("Temperature : %.2f °C" % temperature_SCD41)
#        print("Humidite : %.2f %%" % humidity_SCD41)
#    else:
#        print("No data available")
#    
#def callback_BME280 (timer):
#    print ('Temperature : ', BM280.read_temp())
#    print ('Pression : ', BM280.read_pressure())
#    print ('Humidite : ', BM280.read_humidity())
#
#def callback_SGP40 (timer):
#    voc_index = sgp40_capteur_cov.measure_index(BME_280.read_temp(), BME_280.read_humidity())
#    print("VOC index : %d" % voc_index)
#
#timer_SCD41 = Timer(0)
#timer_SCD41.init(period=5000, mode=Timer.PERIODIC, callback=callback_SCD41)
#timer_BME280 = Timer(1)
#timer_BME280.init(period=1000, mode=Timer.PERIODIC, callback=callback_BME280)
#timer_SGP40 = Timer(2)
#timer_SGP40.init(period=1000, mode=Timer.PERIODIC, callback=callback_SGP40)
#timer_SCD41_2= Timer(3)
#timer_SCD41_2.init(period=3600000, mode=Timer.PERIODIC, callback=capteur_SCD41.set_ambient_pressure(int(pression_BME280)))



#Synthese 7 :
from ConfigMateriel_pico import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font


spi_tft = machine.SPI(0)
def __init__(self, spi, cs, dc, rst,
 width=240, height=320, rotation=0):
    """Initialize OLED.
     Args:
     spi (Class Spi): SPI interface for OLED
     cs (Class Pin): Chip select pin
     dc (Class Pin): Data/Command pin
     rst (Class Pin): Reset pin
     width (Optional int): Screen width (default 240)
     height (Optional int): Screen height (default 320)
     rotation (Optional int): Rotation must be 0 default, 90. 180 or 270
     """

tft = ili9341.Display(spi_tft, dc = TFT_DC_pin, cs = SPI_CS_pin, rst = TFT_RESET_pin, rotation = 90)
tft.clear()

print('Loading fonts...')
print('Loading unispace')
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Loading unispaceExt')
unispaceExt = xglcd_font.XglcdFont('fonts/UnispaceExt12x24.c', 12, 24, letter_count=224)
print('Fonts loaded.')

#: écrire le programme qui permet :
#- D’afficher les éléments du fond de l’écran 1 et de valider leur mise en forme ;
#- De vérifier que l’affichage des différentes mesures respecte les formats attendus ; 

i2c=I2C(0, sda=SDA_pin, scl=SCL_pin, freq=Freq_i2c)
adr=i2c.scan()
print('Adresse peripherique I2C :', adr)

Id_BME280 = i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))
capteur_BME280 = BME280 (BME280_I2C_ADR, i2c)
capteur_BME280.Calibration_Param_Load()

capteur_SCD41 = SCD4X (i2c, SCD4X_DEFAULT_ADDR)
capteur_SCD41.stop_periodic_measurement()
print("Serial number :", [hex(i) for i in capteur_SCD41.serial_number])
capteur_SCD41.set_ambient_pressure(int(pression_BME280))
capteur_SCD41.start_periodic_measurement()

sgp40_capteur_cov = SGP40 (i2c)
print("SGP40 Serial number :", [hex(i) for i in sgp40_capteur_cov._serial_number])
voc_index = sgp40_capteur_cov.measure_index(temperature, relative_humidity)

def callback_SCD41 (timer):
    if capteur_SCD41.data_ready: # attendre qu'une mesure soit disponible
        co2 = capteur_SCD41.CO2
        # Affichage des mesures SCD41
        tft.drawtext(50, 70, "CO2 : %d ppm" % co2, unispace, ili9341.color565(255, 255, 255),  background=0,)
    else:
        print("No data available")
    
def callback_BME280 (timer):
    tft.drawtext(50, 10, "Temperature : %.2f °C" % BM280.read_temp(), unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(50, 30, "Pression : %.2f hPa" % BM280.read_pressure(), unispace, ili9341.color565(255, 255, 255),  background=0,)
    tft.drawtext(50, 50, "Humidite : %.2f %%" % BM280.read_humidity(), unispace, ili9341.color565(255, 255, 255),  background=0,)

def callback_SGP40 (timer):
    voc_index = sgp40_capteur_cov.measure_index(BME_280.read_temp(), BME_280.read_humidity())
    tft.drawtext(50, 90, "COV_index : %d" % voc_index, unispace, ili9341.color565(255, 255, 255),  background=0,)

tft.drawtext(2, 10, "Temperature :", unispace, ili9341.color565(255, 255, 255),  background=0,)
tft.drawtext(2, 30, "Pression :", unispace, ili9341.color565(255, 255, 255),  background=0,)
tft.drawtext(2, 50, "Humidite :", unispace, ili9341.color565(255, 255, 255),  background=0,)
tft.drawtext(2, 70, "CO2 :", unispace, ili9341.color565(255, 255, 255),  background=0,)
tft.drawtext(2, 90, "COV_index :", unispace, ili9341.color565(255, 255, 255),  background=0,)

timer_SCD41 = Timer(0)
timer_SCD41.init(period=5000, mode=Timer.PERIODIC, callback=callback_SCD41)
timer_BME280 = Timer(1)
timer_BME280.init(period=1000, mode=Timer.PERIODIC, callback=callback_BME280)
timer_SGP40 = Timer(2)
timer_SGP40.init(period=1000, mode=Timer.PERIODIC, callback=callback_SGP40)
timer_SCD41_2= Timer(3)
timer_SCD41_2.init(period=3600000, mode=Timer.PERIODIC, callback=capteur_SCD41.set_ambient_pressure(int(pression_BME280)))