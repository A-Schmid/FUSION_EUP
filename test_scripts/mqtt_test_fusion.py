import sys
sys.path.append("..")
from FUSION import DHT11_MQTT

sensor = DHT11_MQTT("tempi")

def on_temp():
    print(sensor.get("temperature"))

sensor.OnUpdate("temperature", on_temp)

time.sleep(60)
