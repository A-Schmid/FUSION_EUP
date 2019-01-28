import time
import sys
sys.path.append("..")
from FUSION import DHT11_MQTT

sensor = DHT11_MQTT.DHT11_MQTT(node_name = "tempi", node_location="1104")

def on_temp():
    print("{} Grad Celsius".format(sensor.get("temperature")))

def on_humi():
    print("{} Prozent Luftfeuchtigkeit".format(sensor.get("humidity")))

sensor.OnUpdate(on_temp, "temperature")
sensor.OnUpdate(on_humi, "humidity")

time.sleep(60)
