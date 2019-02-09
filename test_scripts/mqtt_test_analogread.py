import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

sensor = FUSION_MQTT.FUSION_MQTT(node_name = "drehi", node_location="1104")
sensor.add_data_entry("analogReadResult", int)

def on_value():
    print("{} / 1024".format(sensor.get("analogReadResult")))

sensor.OnUpdate(on_value, "analogReadResult")

sensor.send_message("setDirection", 0)

while(True):
    sensor.send_message("analogRead");
    time.sleep(1)

time.sleep(60)
