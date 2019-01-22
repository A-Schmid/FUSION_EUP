import sys
sys.path.append("..")
import time
import datetime
from FUSION import *

dht = {}
dht["gang"] = DHT11(50)
dht["104"] = DHT11(51)
#dht["besprechungsraum"] = DHT11(52)
#dht["RW"] = DHT11(50)
#dht["florin"] = DHT11(51)
#dht["fischi"] = DHT11(52)

while True:
    t_gang = dht["gang"].getTemperature()
    t_104 = dht["104"].getTemperature()
    t_besprechungsraum = 0
    #t_klo = dht["klo"].getTemperature()
    #t_besprechungsraum = dht["besprechungsraum"].getTemperature()
    #t_RW = dht["RW"].getTemperature()
    #t_florin = dht["florin"].getTemperature()
    #t_fischi = dht["fischi"].getTemperature()
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    #log_append_line(filename = "office_22_11_night.txt", message = "{};{};{};{};{};{};{}".format(dt, t_gang, t_klo, t_besprechungsraum, t_RW, t_florin, t_fischi))
    print("{} - Gang: {}°C, 104: {}°C, Besprechungsraum: {}°C".format(dt, t_gang, t_104, t_besprechungsraum))
    time.sleep(5)

time.sleep(5)
