import time
from FUSION import *

btn = GPIO(40)

btn.setDirection(A0, INPUT)

while True:
    print(btn.analogRead(A0))
    time.sleep(0.01)

time.sleep(5)
