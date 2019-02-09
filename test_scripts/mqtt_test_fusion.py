import time
import sys
sys.path.append("..")
from FUSION import DHT11_MQTT, BH1750_MQTT

sensor = DHT11_MQTT.DHT11_MQTT(node_name = "tempi", node_location="1104")
bh1750 = BH1750_MQTT.BH1750_MQTT(node_name = "lighty", node_location="1104")

def on_temp():
    print("{} Grad Celsius".format(sensor.get("temperature")))

def on_humi():
    print("{} Prozent Luftfeuchtigkeit".format(sensor.get("humidity")))

def on_light():
    print("{} Einheiten Lichtintesität".format(bh1750.get("light_intensity")))

sensor.OnUpdate(on_temp, "temperature")
sensor.OnUpdate(on_humi, "humidity")
bh1750.OnUpdate(on_light, "light_intensity")

time.sleep(60)
