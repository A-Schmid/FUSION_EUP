import time
from FUSION import *

btn = GPIO(43)

btn.setDirection(0, 0)

while True:
    print(btn.digitalRead(0))
    time.sleep(1)

time.sleep(5)
