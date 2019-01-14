from FUSION import *

t = Tone(40)

while(True):
    t.playTone(NOTE["A2"], 1000)
    time.sleep(1)
    t.playTone(NOTE["C#2"], 1000)
    time.sleep(1)
    t.playTone(NOTE["E2"], 1000)
    time.sleep(1)
    t.stopTone()
    time.sleep(1)
