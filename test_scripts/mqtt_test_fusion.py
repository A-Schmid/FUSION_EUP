import time
import sys
sys.path.append("..")
from FUSION import DHT11_MQTT

sensor = DHT11_MQTT.DHT11_MQTT(node_name = "tempi", node_location="1104")

def on_temp():
    print("{} Grad Celsius".format(sensor.get("temperature")))

sensor.OnUpdate(on_temp, "temperature")

print("go!")

#for i in range(1, 100):
#    print("loop {}".format(sensor.get("temperature")))
#    time.sleep(1)

time.sleep(60)
