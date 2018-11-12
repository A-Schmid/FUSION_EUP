#from .core import *
from .module import *

digital_pins = [0, 2, 4, 5, 12, 13, 14, 15, 16]

class GPIO(Module):
    def __init__(self, node_id):
        Module.__init__(node_id)
        #self.__uds_path = '/tmp/FUSION/node{}'.format(node_id)

        #self.node_id = node_id

        #self.__out_path = '/dev/FUSION/node{}_out'.format(node_id)
        #self.__in_path = '/dev/FUSION/node{}_in'.format(node_id)
        #self.__index = {"ni" : 0, "heart_beat" : 1, "data" : 2, "time" : 3}

        #self.__callbacks = {}
        #self.__connected = False
        for i in digital_pins:
            self.__callbacks[i] = {}
            self.__callbacks[i]["rise"] = []
            self.__callbacks[i]["fall"] = []
            self.__callbacks[i]["change"] = []
        #self.__interval = 0.1
        #self.node_id = node_id
        #self.heart_beat = 0
        #self.time = 0

        #self.__uds_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #self.__uds_sock.setblocking(0)
        
        self.__uds_connect()
        self.__wait_for_connection() # blocking!
        #self.__start_update_thread()

    # TODO whats that?
    def __get_gpio_data(self):
        pass

    def __get_data(self):
        readable, writeable, exceptional = select.select([self.__uds_sock], [], [], 0.1)
        if(len(readable) > 0):
            data = readable[0].recv(1024)
            self.__parse_data(data)

    def __parse_data(self, data):
        self.time = time.time()

        if(self.time == self.__last_update):
            return

        self.__last_update = self.time
        #TODO

    def __update(self):
        while(True):
            self.__get_data()
            try:
                self.__update_gpio_data()
            except:
                continue
            time.sleep(self.__interval)
            
    def buildPacket(self, data):
        length = len(data)
        FRAME_BEGIN = 0xAA
        FRAME_ID = 0
        MSG_ID = 0
        NI = 0
        NMB_DATA = length
        DATA = data 
        CHECKSUM = 0x0405 #TODO
        packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, FRAME_ID, MSG_ID, NI, NMB_DATA, *DATA, CHECKSUM) # TODO
        return packet

    def requestAnswer(self, data):
        length = len(data)
        try:
            self.__uds_sock.sendall(bytes([length]))
            self.__uds_sock.setblocking(1)
            ack = self.__uds_sock.recv(1024)
            self.__uds_sock.setblocking(0)
            #print(ack)
            self.__uds_sock.sendall(self.buildPacket(data))
            #wait for answer
            self.__uds_sock.setblocking(1)
            answer = self.__uds_sock.recv(1024)
            self.__uds_sock.setblocking(0)
            #print(answer)
            return answer
        except:
            print("sendMessage error")

    def sendMessage(self, data):
        length = len(data)
        try:
            # idea: length not needed? just use large enough buffer on esp
            self.__uds_sock.sendall(bytes([length]))
            self.__uds_sock.setblocking(1)
            ack = self.__uds_sock.recv(1024)
            self.__uds_sock.setblocking(0)
            #print(ack)
            self.__uds_sock.sendall(self.buildPacket(data))
        except OSError as msg:
            print("sendMessage error", msg)

    def receiveMessage(self):
        pass

    def setDirection(self, pin, value):
        self.sendMessage([0x00, pin, value])

    def setPinAsInput(self, pin):
        self.sendMessage([0x00, pin, 0x00])
        #TODO define INPUT and OUTPUT variables

    def setPinAsOutput(self, pin):
        self.sendMessage([0x00, pin, 0x01])

    def digitalWrite(self, pin, value):
        self.sendMessage([0x01, pin, value])

    def analogWrite(self, pin, value):
        self.sendMessage([0x02, pin, value])
        #TODO mapping of 0 to 1, two bytes for data

    def digitalRead(self, pin):
        answer = self.requestAnswer([0x03, pin, 0])
        return answer
        #TODO: return value

    def analogRead(self, pin):
        answer = self.requestAnswer([0x04, pin, 0])
        return answer
        #TODO: return value

    def info(self):
        print("GPIO")
