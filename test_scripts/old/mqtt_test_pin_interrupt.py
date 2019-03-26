import time
import sys
sys.path.append("..")
from FUSION import FUSION_MQTT

drehi = FUSION_MQTT.FUSION_MQTT(node_name="drehi", node_location="1104")
drehi.add_data_entry("change", int)
drehi.add_data_entry("rise", int)
drehi.add_data_entry("fall", int)

def on_change():
    print("change!")

def on_rise():
    print("rise!")

def on_fall():
    print("fall!")

drehi.OnUpdate(on_change, "change")
drehi.OnUpdate(on_rise, "rise")
drehi.OnUpdate(on_fall, "fall")

drehi.send_message("setInterrupt", 2)
time.sleep(3)

drehi.send_message("removeInterrupt", 2)
time.sleep(3)

drehi.send_message("setInterrupt", 3)
#while(True):
#    drehi.send_message("digitalWrite", 1)
#    time.sleep(1)
#    drehi.send_message("digitalWrite", 0)
#    time.sleep(1)

time.sleep(60)
