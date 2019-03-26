import sys
sys.path.append("..")
import time
from FUSION import *
sensor = pir(43)

def onEnter():
    print("enter")

def onLeave():
    print("leave")

sensor.OnEnter(onEnter)
sensor.OnLeave(onLeave)

while(True):
    time.sleep(5)
