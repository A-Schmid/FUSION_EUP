from .core import *
import paho.mqtt.client as mqtt

class DHT11_MQTT():
    def __init__(self, node_name=MQTT_DEFAULT_NODENAME, node_location=MQTT_DEFAULT_LOCATION):
        self.__last_update = 0
        
        self._callbacks["all"] = []

        self.data_entries = ["temperature", "humidity"]
        self.data = dict()
        self.data["temperature"] = 0
        self.data["humidity"] = 0

        self.mqtt_network = "FUSION"
        self.mqtt_location = node_location
        self.mqtt_name = node_name

        self._mqtt = mqtt.Client()
        self._mqtt.on_connect = self.on_connect
        self._mqtt.on_message = self.on_message

    def self.on_connect(client, userdata, msg, result_code):
        self._mqtt.subscribe("{}/{}/{}/#".format(self.mqtt_network, self.mqtt_location, self.mqtt_name))

    def self.on_message(client, userdata, msg):
        for entry in self.data_entries:
            if(msg.topic.split("/")[-1] == entry):
                self.data[entry] = ord(msg.payload)

# TODO
#vvvvvv

    def __get_sensor_data(self):
        readable, writeable, exceptional = select.select([self._uds_sock], [], [], 0.1)
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            self.__parse_data(data)

    def __parse_data(self, data):
        try:
            if(data[INDEX_NI] != self.node_id):
                print("{} wrong node id: {} (FD: {})".format(self.node_id, data[INDEX_NI], self._uds_sock.fileno()))
                return
            if(data[INDEX_MSG_TYPE] != MSG_TYPE_PACKET):
                print("{} wrong message type: {}".format(self.node_id, data[INDEX_MSG_TYPE]))
                return
            self.humidity = data[INDEX_HUMIDITY] #TODO constant for data index
            self.temperature = data[INDEX_TEMPERATURE]
        except:
            print("could not parse data")
            return
        self.time = time.time()
        self.__last_update = self.time
        for f in self._callbacks["all"]:
            f()

    def _update(self):
        while(True):
            if(self._connected):
                self.__get_sensor_data()
                time.sleep(self._interval)

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def OnUpdate(self, callback):
        self._callbacks["all"].append(callback)

    def info(self):
        print("DHT11")
