import time
from FUSION import *
btn = GPIO(43)

btn.setDirection(16, 1)

while True:
    btn.digitalWrite(16, 1)
    time.sleep(1)
    btn.digitalWrite(16, 0)
    time.sleep(1)

time.sleep(5)
