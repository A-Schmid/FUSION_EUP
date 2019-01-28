import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

led = FUSION_MQTT.FUSION_MQTT(node_name="led", node_location="1104")

while(True):
    led.send_message("led2", bytes([0x00]))
    time.sleep(1)
    led.send_message("led2", bytes([0x01]))
    time.sleep(1)
