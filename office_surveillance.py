import time
import datetime
from FUSION import *

#hygro = GPIO(43)
dht_103 = DHT11(41)
dht_104 = DHT11(44)
dht_101 = DHT11(40)
#lumi = GPIO(40)

while True:
    h_103 = dht_103.getHumidity()
    t_103 = dht_103.getTemperature()
    h_104 = dht_104.getHumidity()
    t_104 = dht_104.getTemperature()
    h_101 = dht_101.getHumidity()
    t_101 = dht_101.getTemperature()
    #moisture = hygro.analogRead(0)
    #light = lumi.analogRead(0)
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    #log_append_line(filename = "office_21_11.txt", message = "{};{};{};{};{};{};{}".format(dt, t_101, h_101, t_103, h_103, t_104, h_104))
    print("{} - 1.101: {}°C, {}% - 1.103: {}°C, {}% - 1.104: {}°C, {}%".format(dt, t_101, h_101, t_103, h_103, t_104, h_104))
    time.sleep(5)

time.sleep(5)
