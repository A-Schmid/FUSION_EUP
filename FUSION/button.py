import threading
import time
import socket
import sys
import select
from .core import *

class button:
    def __init__(self, node_id):
        self.__uds_path = '/tmp/FUSION/node{}'.format(node_id)
        self.__path = '/tmp/FUSION/node{}_in'.format(node_id)
        #self.__index = {"ni" : 0, "heart_beat" : 1, "event" : 2, "time" : 3}
        self.__events = ["release", "press"]
        self.__last_update = 0
        self.__callbacks = {}
        self.__callbacks["all"] = []
        self.__callbacks["pressed"] = []
        self.__callbacks["released"] = []
        self.__interval = 0.1
        #self.__last_heart_beats = [0, 0, 0]

        self.node_id = node_id
        #self.heart_beat = 0
        self.event = "release"
        self.time = 0
        #self.running = False


        # message queue for two-way??

        self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__uds_sock.setblocking(0)
        
        self.__wait_for_connection() # blocking!

        thread = threading.Thread(target=self.__update, args=())
        thread.daemon = True
        thread.start()

    def __wait_for_connection(self):
        # loop?
        try:
            self.__uds_sock.connect(self.__uds_path)
        except socket.error as msg:
            print("could not connect to UDS: ", msg, self.__uds_path) # daemon not running?
            sys.exit(1)

    def __get_sensor_data(self):
        #print("gsd")
        readable, writeable, exceptional = select.select([self.__uds_sock], [], [], 0.1)
        #print(len(readable))
        #self.__sensor_data = []
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            print(data)
            self.__parse_data(data)

        #with open(self.__path) as data_file:
        #    for line in data_file:
        #        self.__sensor_data.append(line)

    def __parse_data(self, data):
        #print(data[0])
        state = data[4]
        self.event = self.__events[state]
        self.time = time.time()

        if(self.time == self.__last_update):
            return

        self.__last_update = self.time

        for f in self.__callbacks["all"]:
            f(self.event, self.time)

        if(self.event == "press"):
            for f in self.__callbacks["pressed"]:
                f()
        elif(self.event == "release"):
            for f in self.__callbacks["released"]:
                f()

    # deprecated
    def __update_sensor_data(self):
        self.node_id = int(self.__sensor_data[self.__index["ni"]])
        self.heart_beat = int(self.__sensor_data[self.__index["heart_beat"]])
        self.event = self.__events[int(self.__sensor_data[self.__index["event"]])]
        self.time = self.__sensor_data[self.__index["time"]]

        if(self.time == self.__last_update):
            return

        self.__last_update = self.time

        for f in self.__callbacks["all"]:
            f(self.event, self.time)

        if(self.event == "press"):
            for f in self.__callbacks["pressed"]:
                f()
        elif(self.event == "release"):
            for f in self.__callbacks["released"]:
                f()

    def __update(self):
        #print("update")
        while(True):
            self.__get_sensor_data()
            time.sleep(self.__interval)
            continue # TEMP
            # deprecated?
            try:
                self.__update_sensor_data()
            except:
                continue

    def OnPress(self, callback):
        self.__callbacks["pressed"].append(callback)
    
    def OnRelease(self, callback):
        self.__callbacks["released"].append(callback)

    def OnEvent(self, callback):
        self.__callbacks["all"].append(callback)
    
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
