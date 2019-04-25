import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

# example of the barebone MQTT module

sensor = FUSION_MQTT(node_name = "#", node_location="1104")
sensor.add_data_entry("#", int)

def on_update(data):
    print(data)

sensor.OnUpdate(on_update, "#")

time.sleep(60)
