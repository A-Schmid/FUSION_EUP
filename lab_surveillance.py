import time
import datetime
from FUSION import *

dht = {}
dht["lab_heizung"] = DHT11(40)
dht["lab_tisch"] = DHT11(41)
dht["lab_decke"] = DHT11(44)
dht["ws_werkbank"] = DHT11(50)
dht["studio_boden"] = DHT11(51)
dht["studio_decke"] = DHT11(52)

csv_header = "time;temp_lab_heizung;humi_lab_heizung;temp_lab_tisch;humi_lab_tisch;temp_lab_decke;humi_lab_decke;temp_ws_werkbank;humi_ws_werkbank;temp_studio_boden;humi_studio_boden;temp_studio_decke;humi_studio_decke"
log_append_line(filename = "lab_surveillance.txt", message = csv_header)

while True:
    temperature = {}
    humidity = {}

    dt = datetime.fromtimestamp(time.time()).strftime("%d.%m.%y, %H:%M:%S")
    message_log = "{}".format(dt)
    message_print = "{}".format(dt)

    for key, sensor in dht.items():
        temperature[key] = sensor.getTemperature()
        humidity[key] = sensor.getHumidity()
        message_log += ";{};{}".format(temperature[key], humidity[key])
        message_print += " - {}: {}°C / {}%".format(key, temperature[key], humidity[key])

    log_append_line(filename = "lab_surveillance.txt", message = message_log)
    print(message_print)
    time.sleep(60)

time.sleep(5)
