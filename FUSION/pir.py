from .module import *

class pir(Module):
    def __init__(self, node_id):
        Module.__init__(self, node_id)
        #self.__path = '/dev/FUSION/node{}_in'.format(node_id)
        #self.__index = {"ni" : 0, "heart_beat" : 1, "event" : 2, "time" : 3}
        self.__events = ["leave", "enter"]
        self.__last_update = 0
        #self.__callbacks = []
        self._interval = 0.1
        #self.__last_heart_beats = [0, 0, 0]

        #self.node_id = node_id
        #self.heart_beat = 0
        self.event = "leave"
        #self.time = 0
        #self.running = False

        #thread = threading.Thread(target=self.__update, args=())
        #thread.daemon = True
        #thread.start()

        self._uds_connect()
        self._wait_for_connection() # blocking!
        self._start_update_thread()

    def __get_sensor_data(self):
        readable, writeable, exceptional = select.select([self._uds_sock], [], [], 0.1)
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            self.__parse_data(data)

    #def __get_sensor_data(self):
    #    self.__sensor_data = []
    #    with open(self.__path) as data_file:
    #        for line in data_file:
    #            self.__sensor_data.append(line)


    def __parse_data(self, data):
        state = data[5] #TODO constant for data index
        self.event = self.__events[state]
        self.time = time.time()

        if(self.time == self.__last_update):
            return

        self.__last_update = self.time

        for f in self._callbacks["all"]:
            f(self.event, self.time)
"""
        if(self.event == "enter"):
            for f in self._callbacks["enter"]:
                f()
        elif(self.event == "leave"):
            for f in self._callbacks["leave"]:
                f()
"""
"""
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
"""

    def _update(self):
        while(True):
            self.__get_sensor_data()
            time.sleep(self._interval)
"""
    def __update(self):
        while(True):
            self.__get_sensor_data()
            try:
                self.__update_sensor_data()
            except:
                continue
            time.sleep(self.__interval)
"""
    def OnEvent(self, callback):
        self._callbacks.append(callback)

    def info(self):
        print("pir")
