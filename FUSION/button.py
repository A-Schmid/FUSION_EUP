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
        self.__events = ["release", "press"]
        self.__last_update = 0
        self.__callbacks = {}
        self.__callbacks["all"] = []
        self.__callbacks["pressed"] = []
        self.__callbacks["released"] = []
        self.__interval = 0.1
        self.__connected = False

        self.node_id = node_id
        self.event = "release"
        self.time = 0

        # message queue for two-way??

        self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__uds_sock.setblocking(0)
        
        self.__wait_for_connection() # blocking!

        thread = threading.Thread(target=self.__update, args=())
        thread.daemon = True
        thread.start()

    def __wait_for_connection(self):
        # loop?
        while self.__connected == False:
            try:
                self.__uds_sock.connect(self.__uds_path)
                self.__connected = True
            except socket.error as msg:
                print("could not connect to UDS: ", msg, self.__uds_path) # daemon not running?
                time.sleep(0.1)
                #sys.exit(1)

    def __get_sensor_data(self):
        readable, writeable, exceptional = select.select([self.__uds_sock], [], [], 0.1)
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            self.__parse_data(data)

    def __parse_data(self, data):
        state = data[5] #TODO constant for data index
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

    def __update(self):
        while(True):
            self.__get_sensor_data()
            time.sleep(self.__interval)

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
