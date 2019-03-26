import time
import sys
sys.path.append("..")
from FUSION import pin

buttoni = pin.pin(node_name="buttoni", pin_id=0, node_location="1104")

def on_change():
    print("change!")

def on_rise():
    print("rise!")

def on_fall():
    print("fall!")

buttoni.OnUpdate(on_change, "change")
buttoni.OnUpdate(on_rise, "rise")
buttoni.OnUpdate(on_fall, "fall")

buttoni.setInterrupt(1)

#while(True):
#    drehi.send_message("digitalWrite", 1)
#    time.sleep(1)
#    drehi.send_message("digitalWrite", 0)
#    time.sleep(1)

time.sleep(60)
