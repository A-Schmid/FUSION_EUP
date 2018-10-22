from .core import *

class GPIO:
    def __init__(self, node_id):
        self.node_id = node_id
        self.__path = '/dev/FUSION/node{}_out'.format(node_id)

    def writeToOutFile(self, data):
        with open(self.__path, "ab+") as f:
            f.write(bytes(data))
            f.write(b'\n')
            #for d in data:
            #    f.write(d)
            #f.write("\n")

    def setDirection(self, pin, value):
        self.writeToOutFile([0x00, pin, value])

    def setPinAsInput(self, pin):
        self.writeToOutFile([0x00, pin, 0x00])
        #TODO define INPUT and OUTPUT variables

    def setPinAsOutput(self, pin):
        self.writeToOutFile([0x00, pin, 0x01])

    def digitalWrite(self, pin, value):
        self.writeToOutFile([0x01, pin, value])

    def analogWrite(self, pin, value):
        self.writeToOutFile([0x02, pin, value])
        #TODO mapping of 0 to 1, two bytes for data

    def digitalRead(self, pin):
        self.writeToOutFile([0x03, pin, 0])
        #TODO: return value

    def analogRead(self, pin):
        self.writeToOutFile([0x04, pin, 0])
        #TODO: return value
