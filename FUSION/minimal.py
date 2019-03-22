from .FUSION_MQTT import *

class Minimal(FUSION_MQTT):
    def __init__(self, node_name, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
        FUSION_MQTT.__init__(self, node_name, node_network, node_location)
        self.add_data_entry("value", int)

    def info(self):
        print("minimum working example")
