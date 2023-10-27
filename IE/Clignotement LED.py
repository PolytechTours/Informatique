from machine import Pin, PWM
import time
from ConfigMateriel_pico import*

# -------------- Initialisation Clignotement LED --------------
# Led_25 = Pin(Led_Pin_25, Pin.OUT)
# Led_25.value(0)
# time.sleep(0.25)

pwm_Led_25 = PWM(Pin(Led_Pin_25))
pwm_Led_25.freq(1000)
pwm_Led_25.duty_u16(0)

while True :
#     Led_25.value(1)
#     time.sleep(1)
#     Led_25.value(0)
#     time.sleep(0.5)

    for i in range(0, 65536):
        pwm_Led_25.duty_u16(i)
        
    for k in range(65536, 0, -1):
        pwm_Led_25.duty_u16(k)
    
    time.sleep(0.25)
    