from .module import *

INDEX_HUMIDITY = INDEX_DATA
INDEX_TEMPERATURE = INDEX_DATA + 1

class DHT11(Module):
    def __init__(self, node_id):
        Module.__init__(self, node_id)
        self.__last_update = 0
        self._interval = 0.1
        
        self._callbacks["all"] = []

        self.temperature = 0
        self.humidity = 0

        self._uds_connect()
        self._wait_for_connection() # blocking!
        self._start_update_thread()

    def __get_sensor_data(self):
        readable, writeable, exceptional = select.select([self._uds_sock], [], [], 0.1)
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            self.__parse_data(data)

    def __parse_data(self, data):
        try:
            if(data[INDEX_NI] != self.node_id):
                print("{} wrong node id: {} (FD: {})".format(self.node_id, data[INDEX_NI], self._uds_sock.fileno()))
                return
            if(data[INDEX_MSG_TYPE] != MSG_TYPE_PACKET):
                print("{} wrong message type: {}".format(self.node_id, data[INDEX_MSG_TYPE]))
                return
            self.humidity = data[INDEX_HUMIDITY] #TODO constant for data index
            self.temperature = data[INDEX_TEMPERATURE]
        except:
            print("could not parse data")
            return
        self.time = time.time()
        self.__last_update = self.time
        for f in self._callbacks["all"]:
            f()

    def _update(self):
        while(True):
            self.__get_sensor_data()
            time.sleep(self._interval)

    def getTemperature(self):
        return self.temperature

    def getHumidity(self):
        return self.humidity

    def OnUpdate(self, callback):
        self._callbacks["all"].append(callback)

    def info(self):
        print("DHT11")
