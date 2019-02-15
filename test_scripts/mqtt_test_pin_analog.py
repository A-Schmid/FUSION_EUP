import time
import sys
sys.path.append("..")
from FUSION import pin

axel = pin.pin(node_name="axel", pin_id=17, node_location="1104")

def on_value():
    print(axel.data["analogData"])

axel.OnUpdate(on_value, "analogData")

axel.setDirection(0)

while(True):
    axel.send_message("analogRead")
    time.sleep(1)
