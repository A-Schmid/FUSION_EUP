import time
import datetime
from FUSION import *

sensor = GPIO(43)

sensor.setDirection(0, 0)

while True:
    value = sensor.analogRead(0)
    dt = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
    log_append_line(filename = "hygro.txt", message = "{};{}".format(dt, value))
    print("{} - {}".format(dt, value))
    time.sleep(10)

time.sleep(5)
