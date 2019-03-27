import time
import sys
sys.path.append("..")
from FUSION import Button

btn = Button(node_name = "button", node_location="1104")

# TODO move this to the Button class
def on_change(data):
    if(data == True):
        print("press")
    else:
        print("release")

btn.OnUpdate(on_change, "button_state")

time.sleep(60)
