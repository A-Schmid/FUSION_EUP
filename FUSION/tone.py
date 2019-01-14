#from .core import *
import struct
import select
import time
from .module import *
from .packet import *

INDEX_FREQUENCY = INDEX_DATA
INDEX_DURATION = INDEX_DATA + 2

NOTE = dict()
NOTE_BASE = dict()
NOTES = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']
NOTE_BASE['C'] = 16.35
NOTE_BASE['C#'] = 17.32
NOTE_BASE['Db'] = 17.32
NOTE_BASE['D'] = 18.35
NOTE_BASE['D#'] = 19.45
NOTE_BASE['Eb'] = 19.45
NOTE_BASE['E'] = 20.60
NOTE_BASE['F'] = 21.83
NOTE_BASE['F#'] = 23.12
NOTE_BASE['Gb'] = 23.12
NOTE_BASE['G'] = 24.50
NOTE_BASE['G#'] = 25.96
NOTE_BASE['Ab'] = 25.96
NOTE_BASE['A'] = 27.50
NOTE_BASE['A#'] = 29.14
NOTE_BASE['Bb'] = 29.14
NOTE_BASE['B'] = 30.87

# calculate note frequencies
for i in range(0, 7):
    for c in NOTES:
        NOTE["{}{}".format(c, i)] = int(NOTE_BASE[c] * (i + 1))

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
        message = struct.pack(">HI", frequency, duration)
        self.sendMessage(list(message))

    def stopTone(self):
        self.sendMessage([0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def info(self):
        print("Tone")
