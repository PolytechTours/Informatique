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
        temperature_SCD41 = capteur_SCD41.temperature
        humidity_SCD41 = capteur_SCD41.relative_humidity
        # Affichage des mesures SCD41
        print("CO2 : %d ppm" % co2)
        print("Temperature : %.2f °C" % temperature_SCD41)
        print("Humidite : %.2f %%" % humidity_SCD41)
    else:
        print("No data available")
    
def callback_BME280 (timer):
    print ('Temperature : ', BM280.read_temp())
    print ('Pression : ', BM280.read_pressure())
    print ('Humidite : ', BM280.read_humidity())

def callback_SGP40 (timer):
    voc_index = sgp40_capteur_cov.measure_index(BME_280.read_temp(), BME_280.read_humidity())
    print("VOC index : %d" % voc_index)

timer_SCD41 = Timer(0)
timer_SCD41.init(period=5000, mode=Timer.PERIODIC, callback=callback_SCD41)
timer_BME280 = Timer(1)
timer_BME280.init(period=1000, mode=Timer.PERIODIC, callback=callback_BME280)
timer_SGP40 = Timer(2)
timer_SGP40.init(period=1000, mode=Timer.PERIODIC, callback=callback_SGP40)
timer_SCD41_2= Timer(3)
timer_SCD41_2.init(period=3600000, mode=Timer.PERIODIC, callback=capteur_SCD41.set_ambient_pressure(int(pression_BME280)))