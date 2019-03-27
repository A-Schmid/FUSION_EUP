import time
import sys
sys.path.append("..")
from FUSION import Pir

sensor = Pir(node_name = "pir", node_location="1104")

# TODO move this to the Button class
def on_change(data):
    if(data == True):
        print("enter")
    else:
        print("leave")

sensor.OnUpdate(on_change, "action")

time.sleep(60)
