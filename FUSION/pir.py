import threading
import time
from .core import *

class pir:
    def __init__(self, node_id):
        self.__path = '/dev/FUSION/node{}_in'.format(node_id)
        self.__index = {"ni" : 0, "heart_beat" : 1, "event" : 2, "time" : 3}
        self.__events = ["leave", "enter"]
        self.__last_update = 0
        self.__callbacks = []
        self.__interval = 0.1
        #self.__last_heart_beats = [0, 0, 0]

        self.node_id = node_id
        self.heart_beat = 0
        self.event = "leave"
        self.time = 0
        #self.running = False

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
        self.event = self.__events[int(self.__sensor_data[self.__index["event"]])]
        self.time = float(self.__sensor_data[self.__index["time"]])

        if(self.time == self.__last_update):
            return

        self.__last_update = self.time

        for f in self.__callbacks:
             f(self.event, self.time)

    def __update(self):
        while(True):
            self.__get_sensor_data()
            self.__update_sensor_data()
            time.sleep(self.__interval)

    def OnEvent(self, callback):
        self.__callbacks.append(callback)

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
