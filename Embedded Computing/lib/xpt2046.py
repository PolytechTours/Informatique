"""XPT2046 Touch module."""
from time import sleep


class Touch(object):
    """Serial interface for XPT2046 Touch Screen Controller."""

    # Command constants from ILI9341 datasheet
    GET_X = const(0b11010000)  # X position
    GET_Y = const(0b10010000)  # Y position
    GET_Z1 = const(0b10110000)  # Z1 position
    GET_Z2 = const(0b11000000)  # Z2 position
    GET_TEMP0 = const(0b10000000)  # Temperature 0
    GET_TEMP1 = const(0b11110000)  # Temperature 1
    GET_BATTERY = const(0b10100000)  # Battery monitor
    GET_AUX = const(0b11100000)  # Auxiliary input to ADC

    def __init__(self, spi, cs, int_pin=None, int_handler=None,
                 width=240, height=320, rotation = 0,
                 x_min=157, x_max=1841, y_min=200, y_max=1947):
        """Initialize touch screen controller.

        Args:
            spi (Class Spi):  SPI interface for OLED
            cs (Class Pin):  Chip select pin
            int_pin (Class Pin):  Touch controller interrupt pin
            int_handler (function): Handler for screen interrupt
            width (int): Width of LCD screen (default : 240)
            height (int): Height of LCD screen (default : 320)
            rotation (Optional int): Rotation must be 0 default, 90, 180 or 270
            x_min (int): Minimum Rawx coordinate
            x_max (int): Maximum Rawx coordinate
            y_min (int): Minimum RawY coordinate
            y_max (int): Maximum RawY coordinate
        """
        self.spi = spi
        self.cs = cs
        self.cs.init(self.cs.OUT, value=1)
        self.rx_buf = bytearray(3)  # Receive buffer
        self.tx_buf = bytearray(3)  # Transmit buffer
        
        self.width = width
        self.height = height
        self.rotation = rotation
        
        if rotation not in (0, 90, 180, 270):
            raise RuntimeError('Rotation must be 0, 90, 180 or 270.')
        
        # Set calibration
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        """
        On suppose ici que les repéres de l'écran et de la dalle tactile sont confondus soit :
            Même origine;
            Même orientation
        """
        self.x_multiplier = width / (x_max - x_min)
        self.x_add = x_min * -self.x_multiplier
        self.y_multiplier = height / (y_max - y_min)
        self.y_add = y_min * -self.y_multiplier

        if int_pin is not None:
            self.int_pin = int_pin
            self.int_pin.init(int_pin.IN)
            self.int_handler = int_handler
            self.int_locked = False
            int_pin.irq(trigger=int_pin.IRQ_FALLING | int_pin.IRQ_RISING,
                        handler=self.int_press)

    def get_touch(self):
        """Take multiple samples to get accurate touch reading."""
        timeout = 2  # set timeout to 2 seconds
        confidence = 5
        buff = [[0, 0] for x in range(confidence)]
        buf_length = confidence  # Require a confidence of 5 good samples
        buffptr = 0  # Track current buffer position
        nsamples = 0  # Count samples
        while timeout > 0:
            if nsamples == buf_length:
                meanx = sum([c[0] for c in buff]) // buf_length
                meany = sum([c[1] for c in buff]) // buf_length
                dev = sum([(c[0] - meanx)**2 +
                          (c[1] - meany)**2 for c in buff]) / buf_length
                if dev <= 50:  # Deviation should be under margin of 50
                    return self.normalize(meanx, meany)
            # get a new value
            sample = self.raw_touch()  # get a touch
            if sample is None:
                nsamples = 0    # Invalidate buff
            else:
                buff[buffptr] = sample  # put in buff
                buffptr = (buffptr + 1) % buf_length  # Incr, until rollover
                nsamples = min(nsamples + 1, buf_length)  # Incr. until max

            sleep(.05)
            timeout -= .05
        return None

    def int_press(self, pin):
        """Send X,Y values to passed interrupt handler."""
        if not pin.value() and not self.int_locked:
            self.int_locked = True  # Lock Interrupt
            buff = self.raw_touch()

            if buff is not None:
                x, y = self.normalize(*buff)
                self.int_handler(x, y)
            sleep(.1)  # Debounce falling edge
        elif pin.value() and self.int_locked:
            sleep(.1)  # Debounce rising edge
            self.int_locked = False  # Unlock interrupt

    def normalize(self, x, y):
        """
        Normalize mean X,Y values to match LCD screen.
        Pour écran DRF0665
            On suppose que pour l'écran LCD : rotation = 0
            On ramène le système de coordonnées de la dalle tactile avec la même position - orientation
                que celui de l'écran LCD lorsque rotation = 0
            Matrice de passage :
                -1   0  Raw_x_max
                0    1  -Raw_y_min
                0    0       1
            Puis on calcule les coordonnées pixel (Xe, Ye) avec les relations ci-dessous.
               x = int(self.x_multiplier * x)
               y = int(self.y_multiplier * y)
            Si rotation  != de 0 :
               On applique un changement de repère sur (x, y) pour avoir les coord finales (Xe, Ye)
               rotation = 90 :
                 Xe = y;
                 Ye = -x + self.width
               rotation = 180 :
                 Xe = -x + self.width
                 Ye = -y + self.height
               rotation = 270 :
                 Xe = -y + self.height
                 Ye = x

        """
        x = -x + self.x_max
        y = y - self.y_min
        x = int(self.x_multiplier * x)
        y = int(self.y_multiplier * y)
        
        if self.rotation == 90 :
            tmp = x
            x = y
            y = -tmp + self.width
        elif self.rotation == 180 :
            x = -x + self.width
            y = -y + self.height
        elif self.rotation == 270 :
            tmp = x
            x = -y + self.height
            y = tmp
        
        '''
        x = int(self.x_multiplier * x + self.x_add)
        y = int(self.y_multiplier * y + self.y_add)
        '''
        return x, y

    def raw_touch(self):
        """Read raw X,Y touch values.

        Returns:
            tuple(int, int): X, Y
        """
        x = self.send_command(self.GET_X)
        y = self.send_command(self.GET_Y)
        if self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max:
            return (x, y)
        else:
            return None

    def send_command(self, command):
        """Write command to XT2046 (MicroPython).

        Args:
            command (byte): XT2046 command code.
        Returns:
            int: 12 bit response
        """
        self.tx_buf[0] = command
        self.cs(0)
        self.spi.write_readinto(self.tx_buf, self.rx_buf)
        self.cs(1)

        return (self.rx_buf[1] << 4) | (self.rx_buf[2] >> 4)
