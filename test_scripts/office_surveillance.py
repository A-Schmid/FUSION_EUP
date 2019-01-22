import sys
sys.path.append("..")
import time
import datetime
from FUSION import *

dht = {}
dht["gang"] = DHT11(40)
dht["klo"] = DHT11(41)
dht["besprechungsraum"] = DHT11(44)
dht["RW"] = DHT11(50)
dht["florin"] = DHT11(51)
dht["fischi"] = DHT11(52)

while True:
    t_gang = dht["gang"].getTemperature()
    t_klo = dht["klo"].getTemperature()
    t_besprechungsraum = dht["besprechungsraum"].getTemperature()
    t_RW = dht["RW"].getTemperature()
    t_florin = dht["florin"].getTemperature()
    t_fischi = dht["fischi"].getTemperature()
    #h_gang = dht_gang.getHumidity()
    #t_gang = dht_gang.getTemperature()
    #h_104 = dht_104.getHumidity()
    #t_104 = dht_104.getTemperature()
    #h_101 = dht_101.getHumidity()
    #t_101 = dht_101.getTemperature()
    #moisture = hygro.analogRead(0)
    #light = lumi.analogRead(0)
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    log_append_line(filename = "office_22_11_night.txt", message = "{};{};{};{};{};{};{}".format(dt, t_gang, t_klo, t_besprechungsraum, t_RW, t_florin, t_fischi))
    print("{} - Gang: {}°C, Klo: {}°C, Besprechungsraum: {}°C, Raphael: {}°C, Florin: {}°C, Fischi: {}°C".format(dt, t_gang, t_klo, t_besprechungsraum, t_RW, t_florin, t_fischi))
    time.sleep(60)

time.sleep(5)
