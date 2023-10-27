# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_scd4x`
================================================================================

Driver for Sensirion SCD4X CO2 sensor


* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

* `Adafruit SCD4X breakout board <https://www.adafruit.com/product/5187>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

"""
================================================================================
Librairie initiale : adafruit_scd4x
Driver for Sensirion SCD4X CO2 sensor
* Author(s): ladyada

Modification pour Raspberry Pi pico
* Author(s): PG
SCD41.py

**Hardware:**
* `Hardware : Sensirion Devkit SEK-SCD41 <https://sensirion.com/products/catalog/SEK-SCD41/>`_
* `Hardware : Microcontrôleur cible : Raspberry Pi pico`_

**Software and Dependencies:**
* `IDE de développement : Thonny`_
* `Micropython V1.18`_

"""

from machine import I2C
import time
import struct
from micropython import const

SCD4X_DEFAULT_ADDR = const(0x62) # Adresse I2C capteur scd41_capteur_co2
# Liste et codes des commandes
_SCD4X_REINIT = const(0x3646)
_SCD4X_FACTORYRESET = const(0x3632)
_SCD4X_FORCEDRECAL = const(0x362F)
_SCD4X_SELFTEST = const(0x3639)
_SCD4X_DATAREADY = const(0xE4B8)
_SCD4X_STOPPERIODICMEASUREMENT = const(0x3F86)
_SCD4X_STARTPERIODICMEASUREMENT = const(0x21B1)
_SCD4X_STARTLOWPOWERPERIODICMEASUREMENT = const(0x21AC)
_SCD4X_READMEASUREMENT = const(0xEC05)
_SCD4X_SERIALNUMBER = const(0x3682)
_SCD4X_GETTEMPOFFSET = const(0x2318)
_SCD4X_SETTEMPOFFSET = const(0x241D)
_SCD4X_GETALTITUDE = const(0x2322)
_SCD4X_SETALTITUDE = const(0x2427)
_SCD4X_SETPRESSURE = const(0xE000)
_SCD4X_PERSISTSETTINGS = const(0x3615)
_SCD4X_GETASCE = const(0x2313)
_SCD4X_SETASCE = const(0x2416)


class SCD4X:
    """
    Librairie initiale Adafruit et CircuitPython

    Librairie pour Raspberry Pi pico

    :param  i2c_bus: The I2C bus the SCD4X is connected to.
    :param int address: The I2C device address for the sensor. Default is :const:`0x62`

    **Quickstart: Importing and using the SCD4X**

        First import the libraries to use the sensor
            from machine import I2C
            from Adafruit_scd4x import *

        Define the i2c object :
            i2c = I2C(0, sda = SDA_pin, scl = SCL_pin, freq= Freq_i2c)
            # Init RP2040 en maitre; I2C par défaut : I2C0; SCL : GP9 (broche 12 PCB) ; SDA : GP8 (broche 11 PCB)

        Define the SCD41_sensor object :
            SCD41_sensor = SCD4X(i2c)
            SCD41_sensor.start_periodic_measurement()

        Acquisition des grandeurs du SCD41 : CO2, temperature, relative humidity
            if scd.data_ready:
                temperature_SCD41 = SCD41_sensor.temperature
                relative_humidity_SCD41 = SCD41_sensor.relative_humidity
                co2_ppm_level = SCD41_sensor.CO2
    """


    def __init__(self, i2c_bus, address=SCD4X_DEFAULT_ADDR):
        self.i2c_device = i2c_bus
        self._buffer = bytearray(18)
        self._cmd = bytearray(2)
        self._crc_buffer = bytearray(2)

        # cached readings
        self._temperature = None
        self._relative_humidity = None
        self._co2 = None

        self.stop_periodic_measurement()

    @property
    def CO2(self):  # pylint:disable=invalid-name
        """Returns the CO2 concentration in PPM (parts per million)

        .. note::
            Between measurements, the most recent reading will be cached and returned.

        """
        if self.data_ready:
            self._read_data()
        return self._co2

    @property
    def temperature(self):
        """Returns the current temperature in degrees Celsius

        .. note::
            Between measurements, the most recent reading will be cached and returned.

        """
        if self.data_ready:
            self._read_data()
        return self._temperature

    @property
    def relative_humidity(self):
        """Returns the current relative humidity in %rH.

        .. note::
            Between measurements, the most recent reading will be cached and returned.

        """
        if self.data_ready:
            self._read_data()
        return self._relative_humidity

    def reinit(self):
        """Reinitializes the sensor by reloading user settings from EEPROM."""
        self.stop_periodic_measurement()
        self._send_command(_SCD4X_REINIT, cmd_delay=0.02)

    def factory_reset(self):
        """Resets all configuration settings stored in the EEPROM and erases the
        FRC and ASC algorithm history."""
        self.stop_periodic_measurement()
        self._send_command(_SCD4X_FACTORYRESET, cmd_delay=1.2)

    def force_calibration(self, target_co2):
        """Forces the sensor to recalibrate with a given current CO2"""
        self.stop_periodic_measurement()
        self._set_command_value(_SCD4X_FORCEDRECAL, target_co2)
        time.sleep(0.5)
        self._read_reply(self._buffer, 3)
        correction = struct.unpack_from(">h", self._buffer[0:2])[0]
        if correction == 0xFFFF:
            raise RuntimeError(
                "Forced recalibration failed.\
            Make sure sensor is active for 3 minutes first"
            )

    @property
    def self_calibration_enabled(self):
        """Enables or disables automatic self calibration (ASC). To work correctly, the sensor must
        be on and active for 7 days after enabling ASC, and exposed to fresh air for at least 1 hour
        per day. Consult the manufacturer's documentation for more information.

        .. note::
            This value will NOT be saved and will be reset on boot unless
            saved with persist_settings().

        """
        self._send_command(_SCD4X_GETASCE, cmd_delay=0.001)
        self._read_reply(self._buffer, 3)
        return self._buffer[1] == 1

    @self_calibration_enabled.setter
    def self_calibration_enabled(self, enabled):
        self._set_command_value(_SCD4X_SETASCE, enabled)

    def self_test(self):
        """Performs a self test, takes up to 10 seconds"""
        self.stop_periodic_measurement()
        self._send_command(_SCD4X_SELFTEST, cmd_delay=10)
        self._read_reply(self._buffer, 3)
        if (self._buffer[0] != 0) or (self._buffer[1] != 0):
            raise RuntimeError("Self test failed")

    def _read_data(self):
        """Reads the temp/hum/co2 from the sensor and caches it"""
        self._send_command(_SCD4X_READMEASUREMENT, cmd_delay=0.001)
        self._read_reply(self._buffer, 9)
        self._co2 = (self._buffer[0] << 8) | self._buffer[1]
        temp = (self._buffer[3] << 8) | self._buffer[4]
        self._temperature = -45 + 175 * (temp / 2 ** 16)
        humi = (self._buffer[6] << 8) | self._buffer[7]
        self._relative_humidity = 100 * (humi / 2 ** 16)

    @property
    def data_ready(self):
        """Check the sensor to see if new data is available"""
        self._send_command(_SCD4X_DATAREADY, cmd_delay=0.001)
        self._read_reply(self._buffer, 3)
        return not ((self._buffer[0] & 0x07 == 0) and (self._buffer[1] == 0))

    @property
    def serial_number(self):
        """Request a 6-tuple containing the unique serial number for this sensor"""
        self._send_command(_SCD4X_SERIALNUMBER, cmd_delay=0.001)
        self._read_reply(self._buffer, 9)
        return (
            self._buffer[0],
            self._buffer[1],
            self._buffer[3],
            self._buffer[4],
            self._buffer[6],
            self._buffer[7],
        )

    def stop_periodic_measurement(self):
        """Stop measurement mode"""
        self._send_command(_SCD4X_STOPPERIODICMEASUREMENT, cmd_delay=0.5)

    def start_periodic_measurement(self):
        """Put sensor into working mode, about 5s per measurement"""
        self._send_command(_SCD4X_STARTPERIODICMEASUREMENT)

    def start_low_periodic_measurement(self):
        """Put sensor into low power working mode, about 30s per measurement"""
        self._send_command(_SCD4X_STARTLOWPOWERPERIODICMEASUREMENT)

    def persist_settings(self):
        """Save temperature offset, altitude offset, and selfcal enable settings to EEPROM"""
        self._send_command(_SCD4X_PERSISTSETTINGS, cmd_delay=0.8)

    def set_ambient_pressure(self, ambient_pressure):
        """Set the ambient pressure in hPa at any time to adjust CO2 calculations"""
        if ambient_pressure < 0 or ambient_pressure > 65535:
            raise AttributeError("`ambient_pressure` must be from 0~65535 hPascals")
        self._set_command_value(_SCD4X_SETPRESSURE, ambient_pressure)

    @property
    def temperature_offset(self):
        """Specifies the offset to be added to the reported measurements to account for a bias in
        the measured signal. Value is in degrees Celsius with a resolution of 0.01 degrees and a
        maximum value of 374 C

        .. note::
            This value will NOT be saved and will be reset on boot unless saved with
            persist_settings().

        """
        self._send_command(_SCD4X_GETTEMPOFFSET, cmd_delay=0.001)
        self._read_reply(self._buffer, 3)
        temp = (self._buffer[0] << 8) | self._buffer[1]
        return 175.0 * temp / 2 ** 16

    @temperature_offset.setter
    def temperature_offset(self, offset):
        if offset > 374:
            raise AttributeError(
                "Offset value must be less than or equal to 374 degrees Celsius"
            )
        temp = int(offset * 2 ** 16 / 175)
        self._set_command_value(_SCD4X_SETTEMPOFFSET, temp)

    @property
    def altitude(self):
        """Specifies the altitude at the measurement location in meters above sea level. Setting
        this value adjusts the CO2 measurement calculations to account for the air pressure's effect
        on readings.

        .. note::
            This value will NOT be saved and will be reset on boot unless saved with
            persist_settings().
        """
        self._send_command(_SCD4X_GETALTITUDE, cmd_delay=0.001)
        self._read_reply(self._buffer, 3)
        return (self._buffer[0] << 8) | self._buffer[1]

    @altitude.setter
    def altitude(self, height):
        if height > 65535:
            raise AttributeError("Height must be less than or equal to 65535 meters")
        self._set_command_value(_SCD4X_SETALTITUDE, height)

    def _check_buffer_crc(self, buf):
        for i in range(0, len(buf), 3):
            self._crc_buffer[0] = buf[i]
            self._crc_buffer[1] = buf[i + 1]
            if self._crc8(self._crc_buffer) != buf[i + 2]:
                raise RuntimeError("CRC check failed while reading data")
        return True

    def _send_command(self, cmd: int, cmd_delay: float = 0) -> None:
        self._cmd[0] = (cmd >> 8) & 0xFF
        self._cmd[1] = cmd & 0xFF

        '''
        Ne fonctionne pas sur RaspBerry Pi pico et IDE Thonny
        with self.i2c_device as i2c:
            i2c.write(self._cmd, end=2)
        '''
        #self.i2c_device.write(self._cmd, end=2) ne fonctionne pas
        #i2c.writeto(addr, buf, stop=True) Prototype méthode
        self.i2c_device.writeto(SCD4X_DEFAULT_ADDR, self._cmd, True)
        time.sleep(cmd_delay)

    def _set_command_value(self, cmd, value, cmd_delay=0):
        self._buffer[0] = (cmd >> 8) & 0xFF
        self._buffer[1] = cmd & 0xFF
        self._crc_buffer[0] = self._buffer[2] = (value >> 8) & 0xFF
        self._crc_buffer[1] = self._buffer[3] = value & 0xFF
        self._buffer[4] = self._crc8(self._crc_buffer)
        '''
        Ne fonctionne pas sur RaspBerry Pi pico et IDE Thonny
        with self.i2c_device as i2c:
            i2c.write(self._buffer, end=5)
        '''
        self.i2c_device.writeto(SCD4X_DEFAULT_ADDR, self._buffer, True)
        time.sleep(cmd_delay)

    def _read_reply(self, buff, num):
        '''
        Ne fonctionne pas sur RaspBerry Pi pico et IDE Thonny
        with self.i2c_device as i2c:
            i2c.readinto(buff, end=num)
        '''
        self.i2c_device.readfrom_into(SCD4X_DEFAULT_ADDR, buff, True)
        self._check_buffer_crc(self._buffer[0:num])

    @staticmethod
    def _crc8(buffer):
        crc = 0xFF
        for byte in buffer:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1
        return crc & 0xFF  # return the bottom 8 bits
