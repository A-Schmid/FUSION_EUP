#from .core import *
import struct
from .module import *
from .packet import *

digital_pins = [0, 2, 4, 5, 12, 13, 14, 15, 16]
INDEX_DREAD_VALUE = INDEX_DATA
INDEX_AREAD_PIN = INDEX_DATA
INDEX_AREAD_VALUE_HIGH = INDEX_DATA + 1
INDEX_AREAD_VALUE_LOW = INDEX_DATA + 2

class GPIO(Module):
    def __init__(self, node_id):
        Module.__init__(self, node_id)

        for i in digital_pins:
            self._callbacks[i] = {}
            self._callbacks[i]["rise"] = []
            self._callbacks[i]["fall"] = []
            self._callbacks[i]["change"] = []
        
        self._uds_connect()
        self._wait_for_connection() # blocking!

    # TODO whats that?
    def __get_gpio_data(self):
        pass

    def buildPacket(self, data):
        length = len(data)
        FRAME_BEGIN = 0xAA
        MSG_TYPE = MSG_TYPE_PACKET
        MSG_ID = 0 #TODO
        NI = self.node_id
        NMB_DATA = length
        DATA = data 
        CHECKSUM = 0x0405 #TODO
        packet = struct.pack("<BBBBB{}BH".format(NMB_DATA), FRAME_BEGIN, MSG_TYPE, MSG_ID, NI, NMB_DATA, *DATA, CHECKSUM) # TODO
        return packet

    def requestAnswer(self, data):
        length = len(data)
        try:
            length_packet = Packet(1, 0, self.node_id, [length])
            packet = Packet(2, 0, self.node_id, data)
            self._uds_sock.sendall(length_packet.serialize()) #bytes([length]))
            self._uds_sock.setblocking(1)
            ack = self._uds_sock.recv(1024)
            self._uds_sock.setblocking(0)
            self._uds_sock.sendall(packet.serialize())
            #wait for answer
            self._uds_sock.setblocking(1)
            answer = self._uds_sock.recv(1024)
            self._uds_sock.setblocking(0)
            return answer
        except:
            print("requestAnswer error")

    def sendMessage(self, data):
        length = len(data)
        print(data)
        print(length)
        try:
            # idea: length not needed? just use large enough buffer on esp
            length_packet = Packet(1, 0, self.node_id, [length])
            packet = Packet(2, 0, self.node_id, data)
            self._uds_sock.sendall(length_packet.serialize()) #bytes([length]))
            #self._uds_sock.sendall(bytes([length]))
            self._uds_sock.setblocking(1)
            ack = self._uds_sock.recv(1024)
            self._uds_sock.setblocking(0)
            self._uds_sock.sendall(packet.serialize())
            #self._uds_sock.sendall(self.buildPacket(data))
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
        valueL = value & 0xFF
        valueH = (value >> 8) & 0xFF
        self.sendMessage([0x02, pin, valueH, valueL])
        #TODO mapping of 0 to 1, two bytes for data

    def digitalRead(self, pin):
        answer = self.requestAnswer([0x03, pin, 0])
        data = answer[INDEX_DREAD_VALUE]
        return data

    def analogRead(self, pin):
        answer = 0
        data = -1
        try:
            answer = self.requestAnswer([0x04, pin, 0])
            data = (answer[INDEX_AREAD_VALUE_HIGH] << 8) | answer[INDEX_AREAD_VALUE_LOW]
        except:
            print("analogRead - something went wrong... answer: ", answer)
        return data

    def info(self):
        print("GPIO")
