import time
from FUSION import *
led = GPIO(43)

leds = [D0, D6, D8]

for l in leds:
    led.setDirection(l, OUTPUT)
    time.sleep(1)

while True:
    for l in leds:
        led.digitalWrite(l, HIGH)
        time.sleep(1)
        led.digitalWrite(l, LOW)
        time.sleep(1)

time.sleep(5)
