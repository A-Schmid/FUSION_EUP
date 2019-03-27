import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

# example of the barebone MQTT module

sensor = FUSION_MQTT(node_name = "mqtt", node_location="1104")
sensor.add_data_entry("data", int)

def on_update(data):
    print(data)

sensor.OnUpdate(on_update, "data")

time.sleep(60)
