import time
import sys
sys.path.append("..")
from FUSION import Pin

led = Pin(node_name="led", pin_id=16, node_location="1104")

while(True):
    led.digitalWrite(1)
    time.sleep(1)
    led.digitalWrite(0)
    time.sleep(1)

time.sleep(60)
