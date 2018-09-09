import threading
import time
from .core import *

class udp:
    def __init__(self, node_id):
        self.__path = '/dev/FUSION/node{}_in'.format(node_id)
        self.__index = {"ni" : 0, "heart_beat" : 1, "data" : 2}
        self.__callbacks = []
        self.__interval = 0.1

        self.node_id = node_id
        self.heart_beat = 0
        self.data = []

        thread = threading.Thread(target=self.__update, args=())
        thread.daemon = True
        thread.start()

    def __get_sensor_data(self):
        self.__sensor_data = []
        with open(self.__path) as data_file:
            for line in data_file:
                self.__sensor_data.append(line)

    def __update_sensor_data(self):
        self.node_id = int(self.__sensor_data[self.__index["ni"]])
        self.heart_beat = int(self.__sensor_data[self.__index["heart_beat"]])
        self.data = self.__sensor_data[self.__index["data"]]

    def __update(self):
        while(True):
            self.__get_sensor_data()
            try:
                self.__update_sensor_data()
            except:
                continue
            time.sleep(self.__interval)

    def info(self):
        print("todo")
"""
        print("bme280 Sensor:\n" \
              "node_id:     id of the sensor node\n" \
              "heart_beat:  number incrementing each update\n" \
              "temperature: ambient temperature in celsius\n" \
              "pressure:    ambient pressure in Pa\n" \
              "humidity:    ambient humidity in %RH\n" \
              "info():      shows this menu\n" \
              "running:     indicates if sensor is running\n")
"""
