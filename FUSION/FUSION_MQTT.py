from .core import *
import paho.mqtt.client as mqtt

class FUSION_MQTT():
    def __init__(self, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION, node_name):
        self.__last_update = 0

        self.data_entries = []

        self._callbacks = dict()
        self._callbacks["all"] = []

        self.data = dict()
        self._data_types = dict()
        
        self.mqtt_network = node_network
        self.mqtt_location = node_location
        self.mqtt_name = node_name

        self._mqtt = mqtt.Client()
        self._mqtt.on_connect = self.on_connect
        self._mqtt.on_message = self.on_message

        self._mqtt.loop_start()

    def self.add_data_entry(data_entry, data_type=None):
        self.data_entries.append(data_entry)
        self.data[entry] = None
        self._data_types[entry] = data_type
        self._callbacks[entry] = []

    def self.on_connect(client, userdata, msg, result_code):
        self._mqtt.subscribe("{}/{}/{}/#".format(self.mqtt_network, self.mqtt_location, self.mqtt_name))

    def self.on_message(client, userdata, msg):
        for entry in self.data_entries:
            if(msg.topic.split("/")[-1] == entry):
                self.data[entry] = self._decode_message(msg.payload, self._data_types[entry])
                for callback in self._callbacks[entry]:
                    callback()
        for callback in self._callbacks["all"]:
            callback()

    def self._decode_message(data, data_type):
        if(data_type == bool):
            return struct.unpack("<?", data)[0]
        elif(data_type == int):
            if(len(data) == 1):
                return struct.unpack("<B", data)[0]
            elif(len(data) == 2):
                return struct.unpack("<h", data)[0]
            elif(len(data) == 4):
                return struct.unpack("<i", data)[0]
            elif(len(data) == 8):
                return struct.unpack("<q", data)[0]
        elif(data_type == float):
            if(len(data) == 4):
                return struct.unpack("<f", data)[0]
            elif(len(data) == 8):
                return struct.unpack("<d", data)[0]
        elif(data_type == str):
            return data.decode("UTF-8")

    def self.get(data_entry):
        return self.data[data_entry]

    def OnUpdate(self, data_entry=None, callback):
        if(data_entry == None):
            self._callbacks["all"].append(callback)
        elif(data_entry in self.data_entries):
            self._callbacks[data_entry].append(callback)

    def info(self):
        print("FUSION MQTT wrapper")
