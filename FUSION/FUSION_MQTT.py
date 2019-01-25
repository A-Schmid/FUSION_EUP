from .core import *
import struct
import paho.mqtt.client as mqtt

class FUSION_MQTT():
    def __init__(self, node_name, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
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
        
        self._mqtt.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)

        print("mqtt connected")

        self._mqtt.loop_start()

        print("loop started")

    def add_data_entry(self, data_entry, data_type=None):
        print("data entry: " + data_entry)
        self.data_entries.append(data_entry)
        self.data[data_entry] = None
        self._data_types[data_entry] = data_type
        self._callbacks[data_entry] = []

    def on_connect(self, client, userdata, flags, result_code):
        #print("on_connect: " + result_code)
        self._mqtt.subscribe("{}/{}/{}/#".format(self.mqtt_network, self.mqtt_location, self.mqtt_name))

    def on_message(self, client, userdata, msg):
        for entry in self.data_entries:
            if(msg.topic.split("/")[-1] == entry):
                self.data[entry] = self._decode_message(msg.payload, self._data_types[entry]) 
                for callback in self._callbacks[entry]:
                    callback()
        for callback in self._callbacks["all"]:
            callback()

    def _decode_message(self, data, data_type):
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

    def get(self, data_entry):
        return self.data[data_entry]

    def OnUpdate(self, callback, data_entry=None):
        if(data_entry == None):
            self._callbacks["all"].append(callback)
        elif(data_entry in self.data_entries):
            self._callbacks[data_entry].append(callback)

    def info(self):
        print("FUSION MQTT wrapper")
