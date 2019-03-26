import time
import sys
sys.path.append("..")
from FUSION import BH1750

bh1750 = BH1750(node_name = "bh", node_location="1104")

def on_light(data):
    print("{} Einheiten Lichtintesität".format(data))

bh1750.OnUpdate(on_light, "light_intensity")

time.sleep(60)
