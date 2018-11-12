from .module import *

class button(Module):
    def __init__(self, node_id):
        Module.__init__(node_id)
        #self.__uds_path = FUSION_PATH + 'node{}'.format(node_id)
        self.__events = ["release", "press"]
        self.__last_update = 0
        self.__callbacks["all"] = []
        self.__callbacks["pressed"] = []
        self.__callbacks["released"] = []
        self.__interval = 0.1

        #self.node_id = node_id
        self.event = "release"

        # message queue for two-way??

        #self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #self.__uds_sock.setblocking(0)
        
        self.__uds_connect()
        self.__wait_for_connection() # blocking!
        self.__start_update_thread()

        #thread = threading.Thread(target=self.__update, args=())
        #thread.daemon = True
        #thread.start()

"""
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
"""

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
        print("button")
