import threading
import time
from .core import *

digital_pins = [0, 2, 4, 5, 12, 13, 14, 15, 16]

class GPIO:
    def __init__(self, node_id):
        self.node_id = node_id
        self.__out_path = '/dev/FUSION/node{}_out'.format(node_id)
        self.__in_path = '/dev/FUSION/node{}_in'.format(node_id)
        self.__index = {"ni" : 0, "heart_beat" : 1, "data" : 2, "time" : 3}
        self.__last_update = 0
        self.__callbacks = {}
        for i in digital_pins:
            self.__callbacks[i] = {}
            self.__callbacks[i]["rise"] = []
            self.__callbacks[i]["fall"] = []
            self.__callbacks[i]["change"] = []
        self.__interval = 0.1
        self.node_id = node_id
        self.heart_beat = 0
        self.time = 0

        thread = threading.Thread(tartget=self.__update, args=())
        thread.daemon = True
        thread.start()

    def __get_gpio_data(self):
        pass

    def __update(self):
        while(True):
            self.__get_gpio_data()
            try:
                self.__update_gpio_data()
            except:
                continue
            time.sleep(self.__interval)

    def writeToOutFile(self, data):
        with open(self.__out_path, "ab+") as f:
            f.write(bytes(data))
            f.write(b'\n')
            #for d in data:
            #    f.write(d)
            #f.write("\n")

    def setDirection(self, pin, value):
        self.writeToOutFile([0x00, pin, value])

    def setPinAsInput(self, pin):
        self.writeToOutFile([0x00, pin, 0x00])
        #TODO define INPUT and OUTPUT variables

    def setPinAsOutput(self, pin):
        self.writeToOutFile([0x00, pin, 0x01])

    def digitalWrite(self, pin, value):
        self.writeToOutFile([0x01, pin, value])

    def analogWrite(self, pin, value):
        self.writeToOutFile([0x02, pin, value])
        #TODO mapping of 0 to 1, two bytes for data

    def digitalRead(self, pin):
        self.writeToOutFile([0x03, pin, 0])
        #TODO: return value

    def analogRead(self, pin):
        self.writeToOutFile([0x04, pin, 0])
        #TODO: return value
