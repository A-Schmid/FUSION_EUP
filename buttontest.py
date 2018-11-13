import time
from FUSION import *
btn = button(43)

def onPress():
    print("press")

def onRelease():
    print("release")

btn.OnPress(onPress)
btn.OnRelease(onRelease)

while(True):
    time.sleep(5)
