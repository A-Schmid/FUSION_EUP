import time
from FUSION import *

btn = GPIO(40)

btn.setDirection(0, 0)

while True:
    print(btn.analogRead(0))
    time.sleep(1)

time.sleep(5)
