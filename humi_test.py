import time
import datetime
from FUSION import *

sensor = DHT11(50)

while True:
    humidity = sensor.getHumidity()
    temperature = sensor.getTemperature()
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    #log_append_line(filename = "heizung_direkt.txt", message = "{};{};{}".format(dt, temperature, humidity))
    print("{} - {}°C, {}%".format(dt, temperature, humidity))
    time.sleep(5)

time.sleep(5)
