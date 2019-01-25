import FUSION_MQTT

class DHT11_MQTT(FUSION_MQTT):
    def __init__(self, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION, node_name):
        FUSION_MQTT.__init__(self, node_network, node_location, node_name)
        self.add_data_entry("temperature", int)
        self.add_data_entry("humidity", int)


    def info(self):
        print("DHT11 Digital Humidity and Temperature Sensor")
