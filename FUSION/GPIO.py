#from .core import *
import struct
from .module import *
from .packet import *

digital_pins = [0, 2, 4, 5, 12, 13, 14, 15, 16]
INDEX_DREAD_VALUE = INDEX_DATA
INDEX_AREAD_PIN = INDEX_DATA
INDEX_AREAD_VALUE_HIGH = INDEX_DATA + 1
INDEX_AREAD_VALUE_LOW = INDEX_DATA + 2
INPUT = 0
OUTPUT = 1

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
            self._uds_sock.sendall(length_packet.serialize()) 
            self._uds_sock.setblocking(1)
            ack = self._uds_sock.recv(1024)
            self._uds_sock.setblocking(0)
            self._uds_sock.sendall(packet.serialize())
        except OSError as msg:
            print("sendMessage error", msg)

    def receiveMessage(self):
        pass

    def setDirection(self, pin, value):
        self.sendMessage([0x00, pin, value])

    def setPinAsInput(self, pin):
        self.sendMessage([0x00, pin, INPUT])

    def setPinAsOutput(self, pin):
        self.sendMessage([0x00, pin, OUTPUT])

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
        answer = self.requestAnswer([0x04, pin, 0])
        data = (answer[INDEX_AREAD_VALUE_HIGH] << 8) | answer[INDEX_AREAD_VALUE_LOW]
        return data

    def info(self):
        print("GPIO")
