import time
import sys
sys.path.append("..")
from FUSION import DHT11

dht = DHT11(node_name = "dht", node_location="1104")

def on_temperature(data):
    print("{} Grad".format(data))

def on_humidity(data):
    print("{} Prozent".format(data))

dht.OnUpdate(on_temperature, "temperature")
dht.OnUpdate(on_humidity, "humidity")

time.sleep(60)
