import time
from FUSION import *
led = GPIO(43)

led.setDirection(16, 1)

while True:
    led.analogWrite(16, 0)
    time.sleep(1)
    led.analogWrite(16, 256)
    time.sleep(1)
    led.analogWrite(16, 512)
    time.sleep(1)
    led.analogWrite(16, 1023)
    time.sleep(1)

time.sleep(5)
