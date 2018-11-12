import time
from ../FUSION import *
led = GPIO(43)

led.setDirection(16, 1)

while True:
    led.digitalWrite(16, 1)
    time.sleep(1)
    led.digitalWrite(16, 0)
    time.sleep(1)

time.sleep(5)
