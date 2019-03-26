import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

led = FUSION_MQTT.FUSION_MQTT(node_name="pini", node_location="1104")

led.send_message("setDirection", 1)
time.sleep(1)

while(True):
    led.send_message("digitalWrite", 1)
    time.sleep(1)
    led.send_message("digitalWrite", 0)
    time.sleep(1)
