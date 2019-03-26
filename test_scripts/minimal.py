import time
import sys
sys.path.append("..") # needed because test scripts are in a subdirectory
from FUSION import Minimal

# initialize the module
sensor = Minimal(node_name = "mini", node_location="1104")

# define a callback
def on_update(data):
    print(data)

# register the callback
sensor.OnUpdate(on_update, "value")

# make sure the script runs for a while
time.sleep(60)
