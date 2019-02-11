from .FUSION_MQTT import *

class pin(FUSION_MQTT):
    def __init__(self, node_name, pin_id, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
        self.pin = pin_id
        node_name = "{}/{}".format(pin, node_name)

        FUSION_MQTT.__init__(self, node_name, node_network, node_location)

        self.add_data_entry("change", int)
        self.add_data_entry("rise", int)
        self.add_data_entry("fall", int)
        self.add_data_entry("analogReadResult", int)
        self.add_data_entry("digitalReadResult", int)

    def digitalWrite(self, data):
        self.send_message("digitalWrite", data)

    def digitalRead(self):
        self.send_message("digitalRead")

    def analogWrite(self, data):
        self.send_message("analogWrite", data)

    def analogRead(self):
        self.send_message("analogRead")

    def setDirection(self, direction):
        self.send_message("setDirection", direction)

    def setInterrupt(self, edge):
        self.send_message("setInterrupt", edge)

    def removeInterrupt(self):
        self.send_message("removeInterrupt")

    def streamData(self, delay):
        self.send_message("streamData", delay)

    def info(self):
        print("GPIO Pin")
