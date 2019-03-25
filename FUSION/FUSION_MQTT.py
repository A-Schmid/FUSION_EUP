from .core import *
import struct
import inspect
import paho.mqtt.client as mqtt

# main class for MQTT based nodes
# extend this one if you want to write your own nodes
# handles connection and communication, parses and stores data, calls callback functions
class FUSION_MQTT():
    def __init__(self, node_name, node_network=MQTT_DEFAULT_NETWORK, node_location=MQTT_DEFAULT_LOCATION):
        self.__last_update = 0

        # data is structured based on key/value pairs with an arbitrary "data entry" string as a key
        # each type of sensor data (like "temperature", "humidity", ...) can be used as a data entry key
        # sensor nodes know which type of data they publish (it's defined in the library)
        # so similar sensor nodes are exchangeable and you only have to make the model of your node listen to the correct data entry by adding the entry to the following list
        self.data_entries = []

        # keeps track of all registered callbacks - data entry specific callbacks are stored under the corresponding key
        self._callbacks = dict()
        self._callbacks["all"] = []

        # contains actual sensor data with data entry strings as keys. gets updated each time new data arrives
        self.data = dict()
        self._data_types = dict()

        # the MQTT topic to listen to is defined here
        self.mqtt_network = node_network
        self.mqtt_location = node_location
        self.mqtt_name = node_name

        # register MQTT callbacks
        self._mqtt = mqtt.Client()
        self._mqtt.on_connect = self.on_connect
        self._mqtt.on_message = self.on_message
        
        self._mqtt.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE)

        print("mqtt connected")

        self._mqtt.loop_start()

        print("loop started")

    # use this function to add new data entries to the object
    # data_entry (String) is a string representing the type of data the sensor measures (like "temperature")
    # data_type (Type) is the data type of the sensor data. it is sometimes necessary to specify it so the data can be deserialized correctly
    def add_data_entry(self, data_entry, data_type=None):
        print("data entry: " + data_entry)
        self.data_entries.append(data_entry)
        self.data[data_entry] = None
        self._data_types[data_entry] = data_type
        self._callbacks[data_entry] = []

    def on_connect(self, client, userdata, flags, result_code):
        #print("on_connect: " + result_code)
        #self._mqtt.subscribe("{}/{}/{}/#".format(self.mqtt_network, self.mqtt_location, self.mqtt_name))
        # we listen to the specified topic defined by NETWORK, LOCATION and NODE_NAME with a wildcard for the data entry
        self._mqtt.subscribe("{}/{}/{}/#".format(self.mqtt_network, self.mqtt_location, self.mqtt_name))

    # checks if the received message matches a data entry our object listens to
    # if this is the case, decode the message, store the data and call corresponding callbacks
    def on_message(self, client, userdata, msg):
        for entry in self.data_entries:
            if(msg.topic.split("/")[-1] == entry):
                self.data[entry] = self._decode_message(msg.payload, self._data_types[entry]) 
                for callback in self._callbacks[entry]:
                    cb_arg_num = len(inspect.getargspec(callback).args)
                    if cb_arg_num == 0:
                        callback()
                    elif cb_arg_num == 1: 
                        callback(self.data[entry])
                    else:
                        print("invalid number of arguments for callback") # TODO: print function name
        for callback in self._callbacks["all"]:
            callback()

    # send a message to the specified node
    def send_message(self, topic, payload=None, qos=0, retain=False):
        theTopic = "{}/{}/{}/{}".format(self.mqtt_network, self.mqtt_location, self.mqtt_name, topic)
        #print(theTopic, payload)
        self._mqtt.publish(theTopic, payload, qos, retain)

    # deserialize the binary data from a message to a matching data type
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

    # get the last received data for data_entry
    def get(self, data_entry):
        return self.data[data_entry]

    # registers a callback to a specific data entry
    # this callback is called whenever data for this entry is updated
    def OnUpdate(self, callback, data_entry=None):
        if(data_entry == None):
            self._callbacks["all"].append(callback)
        elif(data_entry in self.data_entries):
            self._callbacks[data_entry].append(callback)

    def info(self):
        print("FUSION MQTT wrapper")
