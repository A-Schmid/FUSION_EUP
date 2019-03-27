import time
import sys
sys.path.append("..")
from FUSION import Pin

pin = Pin(node_name="pin_analog", pin_id=17, node_location="1104")

def on_value(data):
    print(data)

pin.OnUpdate(on_value, "analogData")

pin.setDirection(0)

while(True):
    pin.send_message("analogRead")
    time.sleep(1)
