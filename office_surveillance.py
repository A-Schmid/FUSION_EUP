import time
import datetime
from FUSION import *

hygro = GPIO(43)
dht = DHT11(41)
lumi = GPIO(40)

while True:
    humidity = dht.getHumidity()
    temperature = dht.getTemperature()
    moisture = hygro.analogRead(0)
    light = lumi.analogRead(0)
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    log_append_line(filename = "office_16_11.txt", message = "{};{};{};{};{}".format(dt, temperature, humidity, moisture, light))
    print("{} - {}°C, {}%, {}, {}".format(dt, temperature, humidity, moisture, light))
    time.sleep(60)

time.sleep(5)
