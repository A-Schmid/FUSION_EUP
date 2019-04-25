from .FUSION_MQTT import *

class Led(FUSION_MQTT):
    def __init__(self, node_name, pin_id, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
        self.pin = pin_id
        FUSION_MQTT.__init__(self, node_name, node_network, node_location)


    def turn_on(self):
        self.send_message("led_state", 1)

    def turn_off(self):
        self.send_message("led_state", 0)

    def info(self):
        print("LED")
