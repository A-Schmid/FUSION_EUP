from .module import *

class pir(Module):
    def __init__(self, node_id):
        Module.__init__(self, node_id)
        self.__events = ["leave", "enter"]
        self.__last_update = 0

        self._callbacks["all"] = []
        self._callbacks["enter"] = []
        self._callbacks["leave"] = []

        self._interval = 0.1
        self.event = "leave"

        self._uds_connect()
        self._wait_for_connection() # blocking!
        self._start_update_thread()

    def __get_sensor_data(self):
        readable, writeable, exceptional = select.select([self._uds_sock], [], [], 0.1)
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

        for f in self._callbacks["all"]:
            f(self.event, self.time)
        
        if(self.event == "enter"):
            for f in self._callbacks["enter"]:
                f()

        if(self.event == "leave"):
            for f in self._callbacks["leave"]:
                f()

    def _update(self):
        while(True):
            self.__get_sensor_data()
            time.sleep(self._interval)

    def OnEvent(self, callback):
        self._callbacks.append(callback)

    def OnEnter(self, callback):
        self._callbacks["enter"].append(callback)

    def OnLeave(self, callback):
        self._callbacks["leave"].append(callback)

    def info(self):
        print("pir")
