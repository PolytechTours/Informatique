from machine import Pin, PWM, Timer
from ConfigMateriel_pico import*
from BME280 import *
from SCD41 import *
from adafruit_sgp40 import *
import machine
import time
from ILI9341 import ili9341
from ILI9341 import xglcd_font


# --------------- Connection I2C ---------------
i2c = I2C(0, sda = SDA_pin, scl = SCL_pin, freq= Freq_i2c)
adr = i2c.scan ()
print ('Adresse peripherique I2C :', adr)


# --------------- Liaison SPI ---------------
spi_tft = machine.SPI(0)
tft = ili9341.Display(spi_tft, dc = TFT_DC_pin, cs = SPI_CS_pin, rst = TFT_RESET_pin, rotation = 90)
tft.clear()

# --------------- BME280 ---------------
# Id du capteur BME280 : normalement 0x60 (soit 96 en décimal)
Id_BME280 = i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR, 1)
print ('Valeur Id_BME280 : ', hex (Id_BME280[0]))

capteur_BME280 = BME280 (BME280_I2C_ADR, i2c)
capteur_BME280.Calibration_Param_Load()

#initialisation variable BME280
capteur_BME280.read_temp()


# --------------- SCD41 ---------------
capteur_SCD41 = SCD4X (i2c, SCD4X_DEFAULT_ADDR)
capteur_SCD41.stop_periodic_measurement()

# Acquérir le numéro de série du capteur SCD41
print("Serial number :", [hex(i) for i in capteur_SCD41.serial_number])

# Compensation mesure taux CO2 en fonction de la pression atmosphérique
capteur_SCD41.set_ambient_pressure(int(capteur_BME280.read_pression()))

# Mode de mesure périodique
capteur_SCD41.start_periodic_measurement()
time.sleep(5)


# --------------- SGP40 ---------------
sgp40_capteur_cov = SGP40 (i2c)
print("SGP40 Serial number :", [hex(i) for i in sgp40_capteur_cov._serial_number])


# --------------- Police de caractères ---------------
# Importer police de caractères
print('Loading fonts...')
print('Loading unispace')
unispace = xglcd_font.XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Loading unispaceExt')
unispaceExt = xglcd_font.XglcdFont('fonts/UnispaceExt12x24.c', 12, 24, letter_count=224)
print('Fonts loaded.')


# --------------- Fonction ---------------
tft.draw_text(100, 100, "Hello world", unispace, const (0x8425), background_flag = True, background=0,
landscape = False, spacing = 1)

# --------------- Timer ---------------
Evenement1_flag = False
Evenement2_flag = False
Evenement3_flag = False

_1s = const(1000) # Correspond à 1000 ms, soit 1s
_5s = const(5000) # Correspond à 5000 ms, soit 5s

# Fonction callbak
def Evenement1_callback (self):
    global Evenement1_flag
    Evenement1_flag = True
def Evenement2_callback (self):
    global Evenement2_flag
    Evenement2_flag = True
def Evenement3_callback (self):
    global Evenement3_flag
    Evenement3_flag = True

# Init des timers
Evenement1_timer = Timer()
Evenement2_timer = Timer()
Evenement3_timer = Timer()
Evenement1_timer.init(period = _1s, mode = Timer.PERIODIC, callback = Evenement1_callback)
Evenement2_timer.init(period = _5s, mode = Timer.PERIODIC,  callback = Evenement2_callback)
Evenement3_timer.init(period = _1s, mode = Timer.PERIODIC, callback = Evenement3_callback)

Index_evenement_1 = 1
Index_evenement_2 = 1
Index_evenement_3 = 1


# --------------- Boucle infinie ---------------
while True :
    # Gestion de l'événement 1
    if Evenement1_flag == True :
        # Traitement de l'événement 1
        print ('------------------------')
        print ("  Index BME280 : ", Index_evenement_1)
        temp = "  Température : {température: .1f} °C"
        print (temp.format(température = capteur_BME280.read_temp()))
        pres = "  Pression : {pression: .1f} hPa"
        print (pres.format(pression = capteur_BME280.read_pression()))
        humi = "  Humidité : {humidité: .1f} %"
        print (humi.format(humidité = capteur_BME280.read_humidity()))
        Evenement1_flag = False
        Index_evenement_1 += 1

    # Gestion de l'événement 2
    if Evenement2_flag == True :
        if capteur_SCD41.data_ready:
            # Traitement de l'événement 2
            print ('------------------------')
            print ("  Index SCD41 : ", Index_evenement_2)
            co2 = "  CO2 : {co2: .1f} ppm"
            print (co2.format(co2 = capteur_SCD41.CO2))
            temperature_SCD41 = "  Température SCD41: {temperature_SCD41: .1f} °C"
            print (temperature_SCD41.format(temperature_SCD41 = capteur_SCD41.temperature))
            humidity_SCD41 = "  Humidité SCD41: {humidity_SCD41: .1f} %RH"
            print (humidity_SCD41.format(humidity_SCD41 = capteur_SCD41.relative_humidity))
            Evenement2_flag = False
            Index_evenement_2 += 1
            
    # Gestion de l'événement 3
    if Evenement3_flag == True :
        # Traitement de l'événement 3
        print ('------------------------')
        print ("  Index SGP40 : ", Index_evenement_3)
        voc_index = "  VOC Index {vocindex: .0f}"
        print(voc_index.format(vocindex = sgp40_capteur_cov.measure_index(capteur_BME280.read_temp(), capteur_BME280.read_humidity())))
        Evenement3_flag = False
        Index_evenement_3 += 1
    
