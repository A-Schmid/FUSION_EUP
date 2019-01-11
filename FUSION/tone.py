#from .core import *
import struct
import select
import time
from .module import *
from .packet import *

INDEX_FREQUENCY = INDEX_DATA
INDEX_DURATION = INDEX_DATA + 2

class Tone(Module):
    def __init__(self, node_id):
        Module.__init__(self, node_id)
        
        self._uds_connect()
        self._wait_for_connection() # blocking!

    def sendMessage(self, data):
        length = len(data)
        packet = Packet(2, 0, self.node_id, data)
        try:
            self._sendToUDS(packet.serialize())
        except: 
            print("sendMessage error")

    def playTone(self, frequency, duration):
        # TODO
        self.sendMessage([0xF0, 0x00, 0x00, 0xFF, 0x00, 0x00])

    def stopTone(self):
        self.sendMessage([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def info(self):
        print("Tone")
