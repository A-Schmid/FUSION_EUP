import threading
import time
from .core import *

class bme280:
    def __init__(self, node_id):
        self.__path = '/dev/FUSION/FT232_Serial_UART_IC/node{}_in'.format(node_id)
        self.__index = {"ni" : 0, "heart_beat" : 1, "temperature" : 2, "pressure" : 3, "humidity" : 4}
        self.__interval = 1.0
        self.__last_heart_beats = [0, 0, 0]

        self.node_id = node_id
        self.heart_beat = 0
        self.temperature = 0
        self.pressure = 0
        self.humidity = 0
        self.running = False

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
        self.temperature = float(self.__sensor_data[self.__index["temperature"]])
        self.pressure = float(self.__sensor_data[self.__index["pressure"]])
        self.humidity = float(self.__sensor_data[self.__index["humidity"]])
        self.__last_heart_beats.pop(0)
        self.__last_heart_beats.append(self.heart_beat)
        if(all_elements_equal(self.__last_heart_beats)):
            self.running = False
        else:
            self.running = True

    def __update(self):
        while(True):
            self.__get_sensor_data()
            self.__update_sensor_data()
            time.sleep(self.__interval)

    def info(self):
        print("bme280 Sensor:\n" \
              "node_id:     id of the sensor node\n" \
              "heart_beat:  number incrementing each update\n" \
              "temperature: ambient temperature in celsius\n" \
              "pressure:    ambient pressure in Pa\n" \
              "humidity:    ambient humidity in %RH\n" \
              "info():      shows this menu\n" \
              "running:     indicates if sensor is running\n")

    

    #def temperature(self):
    #    __get_sensor_data()
    #    return self.__sensor_data["temperature"]
