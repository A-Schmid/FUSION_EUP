import sys
sys.path.append("..")
import time
import datetime
from FUSION import *

sensor = BH1750(42)

while True:
    light = sensor.getLightIntensity()
    #log_append_line(filename = "heizung_direkt.txt", message = "{};{};{}".format(dt, temperature, humidity))
    print(light)
    time.sleep(0.5)

time.sleep(5)
