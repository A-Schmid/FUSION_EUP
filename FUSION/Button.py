from .FUSION_MQTT import *

class Button(FUSION_MQTT):
    def __init__(self, node_name, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
        FUSION_MQTT.__init__(self, node_name, node_network, node_location)
        self.add_data_entry("button_state", bool)

    def info(self):
        print("Button")
