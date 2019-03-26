import sys
sys.path.append("..")
import time
from FUSION import *

btn = GPIO(42)

btn.setDirection(4, INPUT)

while True:
    print(btn.digitalRead(4))
    time.sleep(1)

time.sleep(5)
