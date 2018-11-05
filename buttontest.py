import time
from FUSION import *
btn = button(43)

def onPress():
    print("press")

btn.OnPress(onPress)

time.sleep(5)
